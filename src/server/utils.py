import subprocess

# Get the latest git commit hash
git_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()[0:7]
