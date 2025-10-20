import os
from status import status
import mirrors

def main():
    os.chdir("/tmp")
    status("Updating lists...")
    allpkgs = []

    for i in mirrors.packagelist_places:
        print("Fetching "+i)
        os.system("curl -s -L -o list "+i)

        with open("list", "r") as f:
            list = f.read().splitlines()

        for i in list:
            print("found "+i)

        allpkgs.extend(list)

    with open("/home/"+os.getlogin()+"/.config/car/packagelist", "w") as f:
        f.write("")
        
    for i in allpkgs:
        with open("/home/"+os.getlogin()+"/.config/car/packagelist", "a") as f:
            f.write(i+"\n")
