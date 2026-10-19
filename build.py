"""Push to GitHub, pull on the Pi and sync the venv there.

Usage: python build.py                                    # update the Pi only
       python build.py --run 9Lab/collision_Avoidance.py  # update, then run
"""
import argparse
import os
import subprocess
import sys

PI_HOST = os.environ.get("PI_HOST", "fridaypi")     # Host from ~/.ssh/config
PI_REPO = os.environ.get("PI_REPO", "~/raunkerfi")  # Where the repo lives on the Pi
# Homebrew's ssh: macOS's /usr/bin/ssh can't use the security-key (_sk) login
SSH = "/opt/homebrew/bin/ssh" if os.path.exists("/opt/homebrew/bin/ssh") else "ssh"

parser = argparse.ArgumentParser()
parser.add_argument("--run", metavar="SCRIPT", help="path relative to the repo root")
args = parser.parse_args()

if subprocess.run(["git", "diff", "--quiet", "HEAD"]).returncode != 0:
    print("Warning: uncommitted changes stay on the Mac — the Pi runs the last pushed commit.")

# Only push (Touch ID for GitHub) when there are local commits GitHub doesn't have
unpushed = subprocess.run(["git", "rev-list", "--count", "@{u}..HEAD"],
                          capture_output=True, text=True).stdout.strip()
if unpushed != "0":
    print("Approve Touch ID to push to GitHub…", flush=True)
    subprocess.run(["git", "push"], check=True)

repo_url = subprocess.run(["git", "remote", "get-url", "origin"],
                          capture_output=True, text=True, check=True).stdout.strip()
remote = [
    "set -e",
    'export PATH="$HOME/.local/bin:$PATH"',  # uv lives here; non-interactive ssh skips .bashrc
    f"[ -d {PI_REPO} ] || git clone {repo_url} {PI_REPO}",
    f"cd {PI_REPO}",
    "git pull --ff-only",
    "uv sync",
]
if args.run:
    remote.append(f"uv run python {args.run}")

print(f"Touch your security key to connect to {PI_HOST}…", flush=True)
# -tt forces a terminal even from PyCharm, so Stop kills the script on the Pi
sys.exit(subprocess.run([SSH, "-tt", PI_HOST, "\n".join(remote)]).returncode)
