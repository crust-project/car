import mirrors
import status
import os

def main(package):
    packages = mirrors.fetch_all_packages(mirrors.packagelist_places)
    for i in packages:
        if package in i:
            status.status("Found: " + i, "ok")
