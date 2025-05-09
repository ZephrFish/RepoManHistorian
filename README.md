# RepoManHistorian

## Overview

RepoManHistorian is a tool for modifying Git repository histories without altering file contents. It builds on the logic already writen into [RepoMan](https://github.com/ZephrFish/RepoMan). It allows users to rewrite commit messages, backdate commits, and simulate an organic repository timeline for research, security testing, and CTF challenges.

## Usage

### Rewrite Commit History
Modify commit messages while preserving file integrity:
```bash
python repohistorian.py
```

### Backdate Commits
Adjust commit timestamps to simulate historical activity:
```bash
python repohistorian.py --backdate
```

### Review Modified History
Check the updated commit log:
```bash
git log --oneline --date=iso
```

### Push Changes (If Required)
If modifications need to be reflected in a remote repository:
```bash
git push --force
```

## Help
For available options and flags:
```bash
python repohistorian.py --help
```


