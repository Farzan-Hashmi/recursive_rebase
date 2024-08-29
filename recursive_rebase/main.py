import argparse



def main():
    parser = argparse.ArgumentParser(description='Recursively rebase a series of common branches to create a stack of branches.')
    parser.add_argument('branch', help='The branch to rebase from')
    args = parser.parse_args()

    #TODO: Implement the rebase logic
    print(f"Rebasing {args.branch}")


if __name__ == '__main__':