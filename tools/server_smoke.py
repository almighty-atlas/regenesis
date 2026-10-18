#!/usr/bin/env python3
"""Isolated Forge diagnostic. No EULA consent is implied by running this tool.

Network: official Forge installer/checksum plus installer-managed libraries.
Exit codes: 0 = Done + clean stop; 2 = expected EULA blocker; 1 = failure.
Existing .work/server-smoke is NEVER reused, removed, or overwritten.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".work" / "server-smoke"
VERSION = "1.20.1-47.4.10"
INSTALLER = f"forge-{VERSION}-installer.jar"
URL = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{VERSION}/{INSTALLER}"
START_TIMEOUT = 240
INSTALL_TIMEOUT = 600
STOP_TIMEOUT = 60


def digest(path, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def download(url, destination, limit):
    deadline = time.monotonic() + 120
    size = 0
    request = urllib.request.Request(url, headers={"User-Agent": "ReGenesis-Server-Smoke/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        if not response.url.startswith("https://"):
            raise RuntimeError("Refusing non-HTTPS download redirect")
        with destination.open("xb") as output:
            while True:
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"Download exceeded 120 seconds: {url}")
                block = response.read(64 * 1024)
                if not block:
                    break
                size += len(block)
                if size > limit:
                    raise RuntimeError(f"Download size limit exceeded: {url}")
                output.write(block)


def terminate(process):
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)


def run_installer(command, report):
    report["installer_command"] = shlex.join(command)
    with (WORK / "installer-console.log").open("xb") as output:
        process = subprocess.Popen(command, cwd=WORK, stdin=subprocess.DEVNULL,
                                   stdout=output, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            report["installer_exit"] = process.wait(timeout=INSTALL_TIMEOUT)
        finally:
            terminate(process)
    if report["installer_exit"] != 0:
        raise RuntimeError("Forge installer failed; see installer-console.log")


def run_server(command, consent, report):
    report["server_command"] = shlex.join(command)
    started = time.monotonic()
    done = False
    stop_sent = False
    timed_out = False
    deadline = started + START_TIMEOUT
    console = WORK / "server-console.log"
    with console.open("xb") as output, console.open("rb") as reader:
        process = subprocess.Popen(command, cwd=WORK, stdin=subprocess.PIPE,
                                   stdout=output, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        pending = b""
        try:
            while True:
                pending += reader.read()
                lines = pending.split(b"\n")
                pending = lines.pop()
                for line in lines:
                    if re.search(rb'\]: Done \([^)]+\)! For help, type "help"', line):
                        done = True
                if done and not stop_sent:
                    if not consent:
                        raise RuntimeError("Unexpected Done without explicit EULA consent")
                    process.stdin.write(b"stop\n")
                    process.stdin.flush()
                    stop_sent = True
                    deadline = time.monotonic() + STOP_TIMEOUT
                if process.poll() is not None:
                    break
                if time.monotonic() >= deadline:
                    timed_out = True
                    break
                time.sleep(0.1)
        finally:
            terminate(process)
            process.stdin.close()
        report.update(server_exit=process.returncode, done=done,
                      stop_sent=stop_sent, timed_out=timed_out,
                      server_elapsed_seconds=round(time.monotonic() - started, 2))
    text = console.read_text(errors="replace")
    if timed_out:
        raise RuntimeError("Server deadline exceeded (240s startup / 60s shutdown)")
    if not consent:
        eula = WORK / "eula.txt"
        if (not done and process.returncode == 0 and eula.is_file()
                and re.search(r"(?m)^eula=false\s*$", eula.read_text())
                and "You need to agree to the EULA" in text):
            report["result"] = "blocked_eula"
            return 2
        raise RuntimeError("Pre-EULA start did not reach the expected EULA refusal")
    if not done or not stop_sent or process.returncode != 0:
        raise RuntimeError("Server did not reach Done and stop with exit code 0")
    report["result"] = "passed"
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", required=True, type=Path,
                        help="Explicit path to a Java 17 executable")
    parser.add_argument("--accept-eula", action="store_true",
                        help="Explicitly agree to https://aka.ms/MinecraftEULA")
    args = parser.parse_args()
    report = {"result": "failed", "accept_eula": args.accept_eula,
              "minecraft": "1.20.1", "forge": "47.4.10",
              "diagnostic_exception": "Independent of unverified client boot",
              "startup_timeout_seconds": START_TIMEOUT,
              "installer_timeout_seconds": INSTALL_TIMEOUT,
              "stop_timeout_seconds": STOP_TIMEOUT}
    created = False
    try:
        if not args.java.is_absolute() or not args.java.is_file():
            raise RuntimeError("--java must name an existing absolute executable path")
        java = str(args.java.resolve(strict=True))
        version = subprocess.run([java, "-version"], capture_output=True, text=True,
                                 timeout=10, check=True)
        report["java_version"] = version.stdout + version.stderr
        if not re.search(r'version "17(?:\.|\")', report["java_version"]):
            raise RuntimeError("Java major version must be 17")
        if (ROOT / ".work").is_symlink():
            raise RuntimeError("Refusing symlink .work")
        (ROOT / ".work").mkdir(exist_ok=True)
        WORK.mkdir()  # Exclusive creation, including refusal of existing symlinks.
        created = True
        lock_path = ROOT / "pack" / "mods.lock.json"
        lock_bytes = lock_path.read_bytes()
        lock = json.loads(lock_bytes)
        report["mods_lock_sha256"] = hashlib.sha256(lock_bytes).hexdigest()
        if (lock["minecraft"], lock["forge"], lock["java"]) != ("1.20.1", "47.4.10", 17):
            raise RuntimeError("Unexpected modlock platform")
        (WORK / "mods.lock.snapshot.json").write_bytes(lock_bytes)
        mods_dir = WORK / "mods"
        mods_dir.mkdir()
        report["mods"] = []
        cache = ROOT / ".work" / "artifacts"
        if cache.is_symlink():
            raise RuntimeError("Refusing symlink artifact cache")
        for mod in lock["mods"]:
            if mod["side"] not in ("both", "server", "client"):
                raise RuntimeError(f"Unknown mod side: {mod['side']}")
            if mod["side"] == "client":
                continue
            name = mod["filename"]
            if not name or Path(name).name != name or not name.endswith(".jar"):
                raise RuntimeError(f"Unsafe artifact filename: {name}")
            source = cache / name
            if source.is_symlink() or not source.is_file():
                raise RuntimeError(f"Missing/non-regular cached artifact: {name}")
            target = mods_dir / name
            with source.open("rb") as src, target.open("xb") as dst:
                for block in iter(lambda: src.read(1024 * 1024), b""):
                    dst.write(block)
            if digest(target) != mod["sha256"]:
                raise RuntimeError(f"SHA256 mismatch: {name}")
            report["mods"].append({k: mod[k] for k in
                                   ("name", "version", "filename", "side", "sha256")})
        installer = WORK / INSTALLER
        checksum = WORK / (INSTALLER + ".sha1")
        download(URL + ".sha1", checksum, 1024)
        expected_sha1 = checksum.read_text().strip().lower()
        if not re.fullmatch(r"[0-9a-f]{40}", expected_sha1):
            raise RuntimeError("Malformed official SHA1")
        download(URL, installer, 32 * 1024 * 1024)
        sha1 = digest(installer, "sha1")
        if sha1 != expected_sha1:
            raise RuntimeError("Official installer SHA1 mismatch")
        platform = {"schema_version": 1, "minecraft": "1.20.1", "forge": "47.4.10",
                    "java": 17, "installer": {"filename": INSTALLER, "url": URL,
                    "sha256": digest(installer), "sha1": sha1,
                    "sha1_url": URL + ".sha1"}}
        pin_path = ROOT / "pack" / "platform.lock.json"
        if pin_path.is_symlink():
            raise RuntimeError("Refusing symlink platform lock")
        if pin_path.exists():
            if json.loads(pin_path.read_text()) != platform:
                raise RuntimeError("Existing platform lock differs; refusing overwrite")
        else:
            with pin_path.open("x") as output:
                output.write(json.dumps(platform, indent=2) + "\n")
        report["platform"] = platform
        run_installer([java, "-jar", INSTALLER, "--installServer"], report)
        user_args = WORK / "user_jvm_args.txt"
        unix_args = WORK / "libraries/net/minecraftforge/forge" / VERSION / "unix_args.txt"
        for path in (user_args, unix_args):
            if path.is_symlink() or not path.is_file() or not path.stat().st_size:
                raise RuntimeError(f"Missing/unsafe Forge argument file: {path}")
            if not path.resolve().is_relative_to(WORK):
                raise RuntimeError("Forge argument file escapes isolated directory")
        # The installed file initially contains only comments; do not execute arbitrary options.
        if any(line.strip() and not line.lstrip().startswith("#")
               for line in user_args.read_text().splitlines()):
            raise RuntimeError("Unexpected active installer user JVM arguments")
        with (WORK / "server.properties").open("x") as output:
            output.write("level-name=smoke-world\nserver-ip=127.0.0.1\nserver-port=25585\n"
                         "view-distance=2\nsimulation-distance=2\nonline-mode=true\n"
                         "spawn-protection=0\n")
        if args.accept_eula:
            with (WORK / "eula.txt").open("x") as output:
                output.write("# Explicit --accept-eula supplied by operator\neula=true\n")
        command = [java, "-Xmx3G", "@user_jvm_args.txt",
                   f"@{unix_args.relative_to(WORK)}", "nogui"]
        return run_server(command, args.accept_eula, report)
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        print(report["error"], file=sys.stderr)
        return 1
    finally:
        if created:
            (WORK / "result.json").write_text(json.dumps(report, indent=2) + "\n")
            print(json.dumps({k: v for k, v in report.items() if k != "mods"}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
