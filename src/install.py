import os
import importlib.util
from rich.console import Console
import sys
from status import status
import mirrors
import hooks

console = Console()

def main(package, noconfirm=False):
    try:
        repro_path = "/home/" + os.getlogin() + "/.config/repro.car"

        def read_installed_versions(path):
            versions = {}
            if not os.path.isfile(path):
                return versions
            with open(path, "r") as f:
                for line in f.read().splitlines():
                    if not line.strip():
                        continue
                    if "=" in line:
                        name, ver = line.split("=", 1)
                        versions[name.strip()] = ver.strip()
                    else:
                        versions[line.strip()] = ""
            return versions

        def write_installed_versions(path, versions):
            lines = []
            for name, ver in versions.items():
                if ver:
                    lines.append(f"{name}={ver}")
                else:
                    lines.append(name)
            with open(path, "w") as f:
                f.write("\n".join(lines) + "\n")

        status("Going to /tmp", "info")
        os.chdir("/tmp/")
    
        found = False

        for mirror in mirrors.install_script_places:
            url = f"{mirror.rstrip('/')}/{package}/install_script"
            status(f"Trying {url}", "info")

            result = os.system(f"curl -s -L -o install_script.py {url}")
            
            with open("install_script.py", "r") as f:
                script = f.read()                

            if script != "404: Not Found":
                status(f"Successfully fetched install script from: {url}", "success")
                found = True
                break
            else:
                status(f"Failed to fetch from: {url}", "warning")

        if not found:
            status("Failed to fetch install script from all mirrors", "error")
            exit()

        status("Reading install_script.py", "info")

        spec = importlib.util.spec_from_file_location("install_script", "/tmp/install_script.py")
        install_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(install_script)

        script_version = None
        if hasattr(install_script, "VERSION"):
            script_version = getattr(install_script, "VERSION")
        elif hasattr(install_script, "version"):
            script_version = getattr(install_script, "version")
        if script_version is None:
            script_version = ""
        else:
            script_version = script_version

        installed_versions = read_installed_versions(repro_path)
        installed_version = installed_versions.get(package)
        if installed_version is not None and installed_version == script_version:
            status(f"{package} is up to date ({script_version}). Exiting.", "ok")
            return
        elif installed_version is not None and installed_version != script_version:
            status(f"New version available for {package}: {installed_version} -> {script_version}. Reinstalling.", "warn")
        elif installed_version is None:
            if not os.path.isfile(repro_path):
                status("No repro.car file. Creating", "warn")
                with open(repro_path, "w") as f:
                    f.write("")

        if hasattr(install_script, "beforeinst"):
            install_script.beforeinst()

        if not noconfirm:
            console.print("::", style="blue bold", end=" ")
            sure = input("Install dependencies and build? (Y/n) ")
            if sure not in ("", "y", "Y"):
                return

        status("Installing dependencies", "ok")
        install_script.deps()

        status("Building", "ok")
        install_script.build()

        if not noconfirm:
            console.print("::", style="blue bold", end=" ")
            sure = input("Install? (Y/n) ")
            if sure not in ("", "y", "Y"):
                return

        status("Installing", "ok")
        install_script.install()

        installed_versions[package] = script_version
        write_installed_versions(repro_path, installed_versions)

        hooks.post_inst(package)

        if hasattr(install_script, "postinst"):
            install_script.postinst()
    except Exception:
        console.print("::", style="red", end=" ")
        console.print("Unhandled exception")
        console.print_exception()
        sys.exit(1)
    except KeyboardInterrupt:
        status("Installation interrupted", "error")
        status("There might be some files that were installed, but not removed. You can remove them manually.", "warn")
        status("If you want to remove them, run the following command:", "warn")
        status("sudo car delete " + package, "warn")
        sys.exit(1)
