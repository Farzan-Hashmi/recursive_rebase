import argparse
from collections import defaultdict
import subprocess

# branch name format: 'stack_tag/branch_info/number'


def rebase_onto(branch_to_rebase_on, branch_to_rebase):
    print(f"Rebasing {branch_to_rebase} onto {branch_to_rebase_on}")
    output = subprocess.check_output(
        f"git rebase {branch_to_rebase_on} {branch_to_rebase}", shell=True
    ).decode("utf-8")


def force_push(branch):
    print(f"Force pushing {branch}")
    output = subprocess.check_output(f"git push -f origin {branch}", shell=True).decode(
        "utf-8"
    )


def get_sorted_branches_in_stack(stack_tag):
    output = (
        subprocess.check_output(f"git branch --list {stack_tag}/*", shell=True)
        .decode("utf-8")
        .split("\n")
    )
    branches = [branch.split()[0] for branch in output if branch]
    branches.sort(key=lambda x: int(x.split("/")[-1]))
    return branches


def sync(stack_tag):
    branches = get_sorted_branches_in_stack(stack_tag)
    for i in range(1, len(branches)):
        rebase_onto(branches[i - 1], branches[i])
        force_push(branches[i])


def main():
    parser = argparse.ArgumentParser(
        description="Recursively rebase a series of common branches to create a stack of branches."
    )
    parser.add_argument("stack_tag", help="The common tag for the stack of branches.")
    args = parser.parse_args()
    sync(args.stack_tag)


if __name__ == "__main__":
    main()
