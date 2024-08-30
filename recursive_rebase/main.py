import argparse
from collections import defaultdict
import subprocess
import json

# branch name format: 'stack_tag/branch_info/number'


def rebase_onto(branch_to_rebase_on, branch_to_rebase):
    print(f"Rebasing {branch_to_rebase} onto {branch_to_rebase_on}")
    subprocess.check_output(
        f"git rebase {branch_to_rebase_on} {branch_to_rebase}", shell=True
    ).decode("utf-8")


def force_push(branch):
    print(f"Force pushing {branch}")
    subprocess.check_output(f"git push -f origin {branch}", shell=True).decode("utf-8")


def get_sorted_branches_in_stack(stack_tag):
    output = (
        subprocess.check_output(f"git branch | grep {stack_tag}", shell=True)
        .decode("utf-8")
        .split("\n")
    )
    branches = [branch.strip() for branch in output if branch]
    branches = [branch[1:] if branch[0] == "*" else branch for branch in branches]
    branches = [branch.strip() for branch in branches]
    branches.sort(key=lambda x: int(x.split("/")[-1]))
    return branches


def print_pr_stack(current_branch):
    branches = get_sorted_branches_in_stack(current_branch.split("/")[0])
    stack = []
    for i in range(len(branches)):
        branch = branches[i]
        pr_title = subprocess.check_output(
            f"gh pr view {branch} --json title", shell=True
        ).decode("utf-8")
        pr_title_dict = json.loads(pr_title)
        pr_link = subprocess.check_output(
            f"gh pr view {branch} --json url", shell=True
        ).decode("utf-8")
        pr_link_dict = json.loads(pr_link)
        title = pr_title_dict["title"]
        link = pr_link_dict["url"]
        append_str = f"[{title}]({link})"
        if branch == current_branch:
            append_str += " <- here"
        append_str += "\n"
        stack.append(append_str)

    stack.reverse()

    stack_str = "".join(stack)

    print("Stack:")
    print(stack_str)


def sync(stack_tag, start_number):
    print("Syncing branches")
    branches = get_sorted_branches_in_stack(stack_tag)
    print(f"Branches: {branches}")

    for i in range(start_number + 1, len(branches)):
        base_branch = "main" if i == 0 else branches[i - 1]
        rebase_onto(base_branch, branches[i])
        force_push(branches[i])
        print(f"PR base for {branches[i]} to {base_branch}")
        subprocess.check_output(
            f"gh pr edit {branches[i]} --base {base_branch}", shell=True
        ).decode("utf-8")
        print(f"Printing PR body for {branches[i]}")
        print_pr_stack(branches[i])


def main():
    parser = argparse.ArgumentParser(
        description="Recursively rebase a series of common branches to create a stack of branches."
    )
    parser.add_argument("stack_tag", help="The common tag for the stack of branches.")
    parser.add_argument(
        "start_number", type=int, help="The starting number of the branches."
    )
    args = parser.parse_args()
    sync(args.stack_tag, args.start_number)


if __name__ == "__main__":
    main()
