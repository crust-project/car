import os
import sys
from rich.console import Console
from rich.progress import Progress

console = Console()

def download(pkgname):
    try:
        console.log(f"[cyan]Fetching platform info for [bold]{pkgname}[/bold]...")
        exit_code = os.system(f"curl -s -L -o platform https://cpkg-mirrors.w3spaces.com/{pkgname}/carpkg-platform.html")
        if exit_code != 0:
            console.log("[red]Failed to fetch platform info")
            sys.exit(1)
    except Exception as e:
        console.print_exception()
        sys.exit(1)

    try:
        with open("platform") as f:
            platform = f.read().strip()

        if sys.platform.startswith("linux") and platform == "linux":
            console.log("[green]Package is installable on Linux")
        elif sys.platform == "darwin" and platform == "mac":
            console.log("[green]Package is installable on macOS")
        elif sys.platform in ("win32", "cygwin"):
            console.log("[red]Windows not supported")
            sys.exit(1)
        else:
            console.log("[yellow]System not detected or unsupported")
            sys.exit(1)

    except Exception:
        console.print_exception()
        sys.exit(1)
    
    console.log(f"[cyan]Downloading binary for [bold]{pkgname}[/bold]...")
    try:
        with Progress() as progress:
            task = progress.add_task("Downloading", total=100)
            exit_code = os.system(f"curl -# -L -o {pkgname} https://raw.githubusercontent.com/crust-project/car-binary-storage/main/{pkgname}")
            progress.update(task, completed=100)
        if exit_code != 0:
            console.log("[red]Download failed")
            sys.exit(1)
    except Exception:
        console.print_exception()
        sys.exit(1)

def install(pkgname):
    console.log("[cyan]Installing. Root password may be required.")
    try:
        os.system(f"sudo mv {pkgname} /usr/bin/{pkgname}")
        os.system(f"sudo chmod +x /usr/bin/{pkgname}")
        console.log(f"[green]Installed [bold]{pkgname}[/bold] successfully")
        sys.exit(0)
    except Exception:
        console.print_exception()
        sys.exit(1)

def main(pkgname):
    download(pkgname)
    install(pkgname)
