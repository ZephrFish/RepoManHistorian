import os
import subprocess
import ollama
import toml
import random
from datetime import datetime, timedelta

# Load configuration from master.toml
config = toml.load("master.toml")
REPO_PATH = config["REPO_PATH"]  # Local Git repository path
git_user_name = config["GIT_USER_NAME"]
git_user_email = config["GIT_USER_EMAIL"]

# Ollama Model
OLLAMA_MODEL = config.get("OLLAMA_MODEL", "mistral")

# Modify the timestamps here to align your date ranges to something meaningful
def random_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 4, 1)
    random_days = (end_date - start_date).days
    random_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

    # Generate valid Git timestamp format
    date_obj = start_date + timedelta(days=random.randint(0, random_days)) + random_time
    return date_obj.strftime("%Y-%m-%dT%H:%M:%S %z")

# Function to generate an unhinged commit message using Ollama
def generate_commit_message(verbose=False):
    """Ask Ollama to generate a commit message without modifying file contents."""
    if verbose:
        print("🔹 Generating commit message using Ollama...")

    response = ollama.chat(model=OLLAMA_MODEL, messages=[
        {"role": "system", "content": "Generate a short, professional, programming-related commit message. No explanations, no prefixes, just the commit message."},
        {"role": "user", "content": "Generate a short commit message."}
    ])

    commit_msg = response["message"]["content"].strip()

    # Remove AI-generated prefixes
    unwanted_phrases = [
        "Sure! ", "Here's a commit message:", "Example:", "Generated commit message:", 
        "Here is a commit message:", "A possible commit message:"
    ]
    for phrase in unwanted_phrases:
        if commit_msg.startswith(phrase):
            commit_msg = commit_msg[len(phrase):].strip()

    if verbose:
        print(f"✅ Generated commit message: {commit_msg}")

    return commit_msg

# Ensure repo exists
if not os.path.exists(os.path.join(REPO_PATH, ".git")):
    print(f"❌ Error: No Git repository found at {REPO_PATH}")
    exit(1)

# Move into repo directory
os.chdir(REPO_PATH)

# Function to rewrite commit history without modifying files
def rewrite_commit_history(verbose=False):
    print("🔄 Rewriting commit history without modifying file contents...")

    # Get list of commits (oldest first)
    commit_hashes = subprocess.run(
        ["git", "rev-list", "--reverse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    ).stdout.strip().split("\n")

    if not commit_hashes or commit_hashes == [""]:
        print("⚠️ No commits found to rewrite.")
        return

    # Start interactive rebase
    for i, commit_hash in enumerate(commit_hashes):
        commit_msg = generate_commit_message(verbose)
        commit_date = random_date()

        print(f"📌 Rewriting commit {i+1}/{len(commit_hashes)}: {commit_msg} on {commit_date}")

        # Reset to commit
        subprocess.run(["git", "checkout", commit_hash], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=REPO_PATH)

        # Amend commit with new message and timestamp
        subprocess.run(["git", "commit", "--amend", "-m", commit_msg], env={
            **os.environ,
            "GIT_AUTHOR_DATE": commit_date,
            "GIT_COMMITTER_DATE": commit_date,
            "GIT_AUTHOR_NAME": git_user_name,
            "GIT_AUTHOR_EMAIL": git_user_email,
            "GIT_COMMITTER_NAME": git_user_name,
            "GIT_COMMITTER_EMAIL": git_user_email
        }, cwd=REPO_PATH)

    print("✅ Successfully rewrote commit history.")
    reattach_head()

# Function to reattach HEAD after commit rewriting
def reattach_head():
    print("🔄 Reattaching HEAD to the latest commit...")
    subprocess.run(["git", "checkout", "master"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=REPO_PATH)
    print("✅ HEAD successfully reattached to master branch.")

# Run the commit modification process
rewrite_commit_history(verbose=True)
