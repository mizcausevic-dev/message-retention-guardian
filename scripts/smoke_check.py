from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORT = "4541"

# Resolve bundle/ruby from PATH on POSIX (CI uses ruby/setup-ruby);
# fall back to the Windows installer location for local dev on Windows.
_BUNDLE_FROM_PATH = shutil.which("bundle")
_RUBY_FROM_PATH = shutil.which("ruby")

if _BUNDLE_FROM_PATH:
    BUNDLE = Path(_BUNDLE_FROM_PATH)
else:
    BUNDLE = Path(r"C:\Ruby33-x64\bin\bundle.bat")

if _RUBY_FROM_PATH:
    RUBY = Path(_RUBY_FROM_PATH)
else:
    RUBY = Path(r"C:\Ruby33-x64\bin\ruby.exe")


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    env = os.environ.copy()
    env["PORT"] = PORT
    # Only prepend the Windows Ruby install dir to PATH on Windows where
    # we are falling back to it.
    if os.name == "nt" and BUNDLE.parent.drive:
        env["PATH"] = str(BUNDLE.parent) + os.pathsep + env.get("PATH", "")
    process = subprocess.Popen(
        [str(BUNDLE), "exec", "ruby", "server.rb"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        time.sleep(2.5)
        if process.poll() is not None:
            stdout, stderr = process.communicate(timeout=2)
            raise RuntimeError(
                "ruby service exited before startup\n"
                f"stdout:\n{stdout}\n"
                f"stderr:\n{stderr}"
            )
        root = get_json(f"http://127.0.0.1:{PORT}/")
        docs = get_json(f"http://127.0.0.1:{PORT}/docs")
        summary = get_json(f"http://127.0.0.1:{PORT}/api/dashboard/summary")
        sample = get_json(f"http://127.0.0.1:{PORT}/api/sample")

        analyze_req = urllib.request.Request(
          f"http://127.0.0.1:{PORT}/api/analyze/request",
          data=json.dumps(sample).encode("utf-8"),
          headers={"Content-Type": "application/json"},
          method="POST",
        )
        with urllib.request.urlopen(analyze_req, timeout=10) as response:
            analysis = json.loads(response.read().decode("utf-8"))

        assert root["service"] == "message-retention-guardian"
        assert docs["routes"][0]["path"] == "/"
        assert summary["active_policies"] == 5
        assert analysis["status"] == "freeze"
        print("smoke_check: ok")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == "__main__":
    main()
