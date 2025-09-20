import os
import sys
from rich.console import Console

console = Console()

def main(pkgname):
    console.log(f"[cyan]Uninstalling [bold]{pkgname}[/bold]...")
    try:
        exit_code = os.system(f"sudo rm -f /usr/bin/{pkgname}")
        if exit_code != 0:
            console.log(f"[red]Failed to uninstall [bold]{pkgname}[/bold]")
            sys.exit(1)
        console.log(f"[green]Successfully uninstalled [bold]{pkgname}[/bold]")
    except Exception:
        console.print_exception()
        sys.exit(1)

