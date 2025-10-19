import argparse
import install
import delete
import update
import search

parser = argparse.ArgumentParser(description="A simple package manager")
subparsers = parser.add_subparsers(dest="command", required=True)

# install
p_install = subparsers.add_parser("get", help="Install a package")
p_install.add_argument("package", help="Package to install")

# delete
p_delete = subparsers.add_parser("delete", help="Uninstall a package")
p_delete.add_argument("package", help="Package to delete")

# update
p_update = subparsers.add_parser("update", help="Update a package")
p_update.add_argument("package", help="Package to update")

# search
p_search = subparsers.add_parser("search", help="Search for a package")
p_search.add_argument("package", help="Package to search for") 

args = parser.parse_args()

if args.command == "get":
    install.main(args.package)
elif args.command == "delete":
    delete.main(args.package)
elif args.command == "update":
    update.main(args.package)
elif args.command == "search":
    search.main(args.package)

