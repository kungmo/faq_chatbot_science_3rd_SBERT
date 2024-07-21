import subprocess
import json
from datetime import datetime

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True, encoding='utf-8')
    return result.stdout.strip()

def get_commit_info(repo_path):
    # Change to the repository directory
    subprocess.run(f"cd {repo_path}", shell=True, check=True)
    
    # Get all commit SHAs
    shas = run_command("git log --format=%H --reverse").split('\n')
    
    all_commits = []
    for sha in shas:
        # Get commit date and message
        date = run_command(f"git show -s --format=%cI {sha}")
        message = run_command(f"git show -s --format=%B {sha}")
        
        # Get full diff
        diff = run_command(f"git show -p {sha}")
        
        all_commits.append({
            'sha': sha,
            'date': date,
            'message': message,
            'diff': diff
        })
        print(f"Processed commit: {sha[:7]}")
    
    return all_commits

# Repository path
repo_path = '/home/ubuntu/faq_chatbot_science_3rd'

try:
    # Get all commit information
    commits = get_commit_info(repo_path)
    
    # Generate filename with current datetime
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"commit_history_{current_time}.json"
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(commits, f, indent=2, ensure_ascii=False)
    
    print(f"Commit history saved to {filename}")

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

# Print summary
print(f"Total commits processed: {len(commits)}")
print("First commit:")
print(json.dumps(commits[0], indent=2, ensure_ascii=False))
print("Last commit:")
print(json.dumps(commits[-1], indent=2, ensure_ascii=False))