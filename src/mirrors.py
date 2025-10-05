from status import status
import os

try:
    with open("/home/" + os.getlogin() + "/.config/mirrors.car", "r") as f:
        mirrors = f.read()
except Exception:
    with open("/home/" + os.getlogin() + "/.config/mirrors.car", "w") as f:
        f.write(""":base:
install_script = https://raw.githubusercontent.com/crust-project/car-binary-storage/main/
packagelist = https://raw.githubusercontent.com/crust-project/car/main/existing-packages.txt
:end:
                """)

install_script_places = []
packagelist_places = []

current_repo = None
current_data = {}

for line in mirrors.strip().splitlines():
    line = line.strip()
    if line.startswith(":") and line.endswith(":") and line != ":end:":
        current_repo = line.strip(":")
        current_data = {}
    elif line == ":end:":
        if "install_script" in current_data:
            install_script_places.append(current_data["install_script"])
        if "packagelist" in current_data:
            packagelist_places.append(current_data["packagelist"])
        current_repo = None
        current_data = {}
    elif current_repo and "=" in line:
        key, value = line.split("=", 1)
        current_data[key.strip()] = value.strip()
