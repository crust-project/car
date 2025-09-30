import os
import importlib.util

def main(package):
    print(":: Going to /tmp")
    os.chdir("/tmp/")

    print(":: Fetching packagelist")
    os.system("curl -s -L -o packagelist https://raw.githubusercontent.com/crust-project/car/main/existing-packages.txt")

    print(f":: Fetching {package}%install_script")
    url = f"https://raw.githubusercontent.com/crust-project/car-binary-storage/main/{package}/install_script"
    os.system(f"curl -s -L -o install_script.py {url}")

    print(":: Reading install_script.py")
    os.system("ls")

    # dynamic import
    spec = importlib.util.spec_from_file_location("install_script", "/tmp/install_script.py")
    install_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(install_script)

    try:
        install_script.beforeinst()
    except Exception:
        pass

    print(":: Installing dependencies")
    install_script.deps()

    print(":: Building")
    install_script.build()

    print(":: Installing")
    install_script.install()

    try:
        install_script.postinst()
    except Exception:
        pass
