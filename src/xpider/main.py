import argparse

from xpider.runner import runner
from xpider.cli.create_project import generate_project

def main():
    parser = argparse.ArgumentParser(description="test")
    subparsers = parser.add_subparsers(dest='operation', help='Available operations.')
    run_parser = subparsers.add_parser("run",help="Run a xpider project.")
    run_parser.add_argument("--path", action="store",help="Path to xpider project dir.")
    run_parser.add_argument("--mongo-url", action="store", help="Mongodb url to write data.")
    run_parser.add_argument("--redis-url", action="store", help="Redis url for queuing.")
    new_parser = subparsers.add_parser("new", help="Create new xpider project.")
    new_parser.add_argument("name", help="Name of the project in snake case.")
    args = parser.parse_args()
    if args.operation == 'run':
        print(args.__dict__)
        runner(args.__dict__)
    elif args.operation == 'new':
        generate_project(args.name)
