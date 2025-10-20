from status import status
import os

def main(package):
    status("Looking for packages...")
    
    print("(1/3) Reading packagelist")
    with open("/home/"+os.getlogin()+"/.config/car/packagelist", "r") as f:
        packages = f.read()

    print("(2/3) Loading packagelist...")
    packagelist = packages.splitlines()
    print(packagelist)

    print("(3/3) Checking for package...")
    if package in packagelist:
        return True
    else:
        status("Package not found.", "error")
        print("Maybe you forgot to update your packagelist?")
        print("     car updatelist")
    
