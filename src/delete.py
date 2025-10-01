import os
import sys
from rich.console import Console

console = Console()

def status(msg, level="info"):
    colors = {
        "info": "blue",
        "ok": "green",
        "error": "red",
    }
    color = colors.get(level, "blue") + " bold"
    console.print("::", style=color, end=" ")
    console.print(msg)

def main(pkgname):
    if not os.path.isfile("/home/" + os.getlogin() + "/.config/repro.car"):
        status("No repro.car file. Creating", "warn")
        with open("/home/" + os.getlogin() + "/.config/repro.car", "w") as f:
            f.write()
    else:
        with open("/home/" + os.getlogin() + "/.config/repro.car", "r") as f:
            pkgs_installed = f.read()
            pkgs_installed = pkgs_installed.replace(pkgname, "")
        with open("/home/" + os.getlogin() + "/.config/repro.car", "w") as f:
            f.write(pkgs_installed)

    status(f"Uninstalling {pkgname}...", "info")
    try:
        exit_code = os.system(f"sudo rm /usr/bin/{pkgname}")
        if exit_code != 0:
            status(f"Failed to uninstall {pkgname}", "error")
            sys.exit(1)
        status(f"Successfully uninstalled {pkgname}", "ok")
    except Exception:
        console.print("::", style="red", end=" ")
        console.print("Unhandled exception")
        console.print_exception()
        sys.exit(1)
