import argparse

def process_files_changed(git_diff: str):
    files_diff = git_diff.split("\\n")
    print(files_diff)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--files-changed", help="The List of files changed obtained from a git diff command")

    args = parser.parse_args()

    if args.files_changed:
        process_files_changed(args.files_changed)
