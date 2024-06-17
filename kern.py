#!/usr/bin/env python3
import subprocess
import os
import pandas as pd


# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    if result.returncode != 0:
        raise Exception(f"Error running command {' '.join(command)}: {result.stderr}")
    return result.stdout.strip()


# Function to clone a Git repository if the directory does not exist
def git_clone(repo_url, directory):
    if not os.path.exists(directory):
        run_command(['git', 'clone', repo_url, directory])
        print(f"Repository cloned into {directory}")
    else:
        print(f"Directory {directory} already exists, skipping clone.")


# Function to get git log with one line commits by author, including the date
def git_log_oneline_by_author(directory, author):
    # Define a custom format for the log output: <short hash> <date> <message>
    log_format = "--pretty=format:%h %ad %s"
    command = ['git', '-C', directory, 'log', log_format, '--date=short', f'--author={author}']
    log = run_command(command)
    return log


# Function to parse commit data and save it to a DataFrame
def parse_commit_data(commit_data, user_email):
    commits_data = []
    for line in commit_data.split('\n'):
        parts = line.split(maxsplit=2)
        if len(parts) == 3:
            commit_hash, date, message = parts
            commits_data.append({
                "subject": message,
                "project": "",  # Update if project data is available
                "branch": "",  # Update if branch data is available
                "status": "MERGED",  # Default status
                "updated": date,
                "User": user_email,
                "Owner": user_email.split("@")[0],
                "Repo": "Linux_Kernel"
            })
    return pd.DataFrame(commits_data)


def get_kernel_github(user_email):
    repo_url = 'https://github.com/torvalds/linux.git'  # Replace with your repository URL
    directory = 'linux'  # Replace with your desired local directory name
    author = user_email# Replace with the author's name you're interested in

    try:
        git_clone(repo_url, directory)
        log = git_log_oneline_by_author(directory, author)
        df = parse_commit_data(log, author)
        return df

        # Display the DataFrame

       #print(df)

        # Save the DataFrame to a CSV file
        #df.to_csv('git_log.csv', index=False)
        #print("DataFrame saved to 'git_log.csv'")
    except Exception as e:
        print(e)
