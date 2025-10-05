from rich.console import Console

console = Console()

def status(msg, level="info"):
    colors = {
        "info": "blue",
        "warn": "orange3",
        "ok": "green",
        "error": "red",
    }
    color = colors.get(level, "blue") + " bold"
    console.print("::", style=color, end=" ")
    console.print(msg)
