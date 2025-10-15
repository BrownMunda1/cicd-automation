import argparse
from pathlib import Path

def process_files_changed(git_diff: str, modified_files: str) -> list:

    monorepos_to_build = set()
    modified_files = []

    files_diff = git_diff.split("\n")

    for file_diff in files_diff:
        file_diff_arr = file_diff.split("\t")

        status = file_diff_arr[0] # "M", "A", "D", "R"

        if status.find("R") != -1:
            old_file_path = file_diff_arr[1]
            new_file_path = file_diff_arr[2]
            is_old_path_monorepo, old_monorepo_name = monorepo_helper(file_path=old_file_path)
            is_new_path_monorepo, new_monorepo_name = monorepo_helper(file_path=new_file_path)
            if is_old_path_monorepo:
                monorepos_to_build.add(old_monorepo_name)
            if is_new_path_monorepo:
                monorepos_to_build.add(new_monorepo_name)
        else:
            file_path = file_diff_arr[1]
            if len(file_path.split("src")) > 1:
                is_monorepo, monorepo_name = monorepo_helper(file_path=file_path)
            if is_monorepo:
                if status != "M":
                    monorepos_to_build.add(monorepo_name)
                else:
                    modified_files.append(monorepo_name)

    return monorepos_to_build, modified_files

def monorepo_helper(file_path: str):
    temp = file_path.split("src")
    monorepo_name = temp[1].split("/")[0]
    repo_path = temp[0] + monorepo_name
    if Path.is_dir(repo_path):
        return True, monorepo_name
    return False, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--files-changed", help="The List of files changed obtained from a git diff command")
    parser.add_argument("--modified-files", help="The List of files which were modified.")

    args = parser.parse_args()

    # if args.files_changed:
    process_files_changed("M\t.github/workflows/build-workflow.yml\nM\tsrc/__init__.py\nM\tsrc/main.py\nD\ttemp.txt\nR100\tgithubActionsAPIResponse.json\ttest/resources/githubActionsAPIResponse.json\nA\ttest/resources/nameStatusResponse.txt")
# ['M\t.github/workflows/build-workflow.yml', 'M\tsrc/__init__.py', 'M\tsrc/main.py', 'D\ttemp.txt', 'R100\tgithubActionsAPIResponse.json\ttest/resources/githubActionsAPIResponse.json', 'A\ttest/resources/nameStatusResponse.txt']