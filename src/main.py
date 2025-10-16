import json
import argparse
from pathlib import Path

def process_files_changed(git_diff: str) -> list:

    monorepos_to_build = set()

    ##### HANDLE OTHERS #####
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

    return monorepos_to_build

def process_modified_files(modified_files: dict) -> list:
    ##### HANDLE MODIFIED FILES #####

    monorepos_to_build = set()

    for file, diff in modified_files.items():
        is_monorepo, monorepo_name = monorepo_helper(file)
        if not is_monorepo:
            continue
        else:
            ## Pass diff to LLM and determine if the change is eligible to be built or not
            monorepos_to_build.add(monorepo_name)
            pass

    return monorepos_to_build

def monorepo_helper(file_path: str):
    temp = file_path.split("src")
    if len(temp) > 1:
        monorepo_name = temp[1].split("/")[1]
        repo_path = temp[0] + "src/" + monorepo_name
        if Path.is_dir(Path(repo_path)):
            return True, monorepo_name
    return False, None

def testing_func(a):
    return (type(a), a)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--files-changed", help="The List of files changed obtained from a git diff command")
    # parser.add_argument("--modified-files", help="The List of files which were modified.")
    parser.add_argument("--modified-files-json", help="JSON File where keys are the file paths which were modified, and the values are the git diffs of respective files")

    args = parser.parse_args()
    # print(testing_func(args.modified_files))

    if args.files_changed:
        files_changed = args.files_changed

    if args.modified_files_json:
        with open(args.modified_files_json, 'r', encoding='utf-8') as fh:
            modified_files = json.load(fh)
            # print("Modified Files:", modified_files)
    
    result1: set = process_files_changed(git_diff=files_changed)
    result2: set = process_modified_files(modified_files=modified_files)

    result = result1.union(result2)

    monorepos = ' '.join(res for res in list(result))

    print(monorepos)

    # if args.files_changed:
        # process_files_changed("M\t.github/workflows/build-workflow.yml\nM\tsrc/__init__.py\nM\tsrc/main.py\nD\ttemp.txt\nR100\tgithubActionsAPIResponse.json\ttest/resources/githubActionsAPIResponse.json\nA\ttest/resources/nameStatusResponse.txt", ".github/workflows/build-workflow.yml\nsrc/main.py")
# ['M\t.github/workflows/build-workflow.yml', 'M\tsrc/__init__.py', 'M\tsrc/main.py', 'D\ttemp.txt', 'R100\tgithubActionsAPIResponse.json\ttest/resources/githubActionsAPIResponse.json', 'A\ttest/resources/nameStatusResponse.txt']