import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from rich.live import Live
from rich.prompt import Confirm
import typer
import sys

console = Console()

def restart_subprocess(script_path, fame):
    if fame:
        fame.kill()
    fame = subprocess.Popen(["python", script_path], stdout=sys.stdout, text=True)
    return fame

templateFile = """# This is your Blast app. You can change it as needed!
# You can add pages, post methods, and more.
from josiauhtools import blast
name = "%s"

# You can change parameters here,
app = blast.BlastApp()

@app.page("/")
def index():
    return f\"\"\"
You're a few steps away from making your Blast app, "{name}"!
Here's a few changes:
<ul>
    <li>Change your port</li>
    <li>Add a new page</li>
    <li>Add a script and/or a stylesheet</li>
</ul>
Up to the challenge? Good luck!\"\"\"

if __name__ == "__main__":
    app.run()
"""

def watch_and_run(name="main"):
    script_path = os.path.join(os.getcwd(), name + ".py")

    class MyHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path == script_path:
                console.print(f"File {script_path} has been modified. Restarting subprocess...")
                global fame
                fame = restart_subprocess(script_path, fame)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(script_path), recursive=False)
    observer.start()

    fame = subprocess.Popen(["python", script_path], stdout=sys.stdout, text=True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

app = typer.Typer()

@app.command("run", help="Runs a Blast app with hot reloading.")
def run_app(name: str = "main"):
    watch_and_run(name)

@app.command("new", help="Create a new Blast app.")
def create(name: str = "main"):
    console = Console()
    with open(name + ".py", "w") as f:
        with console.status("Writing file...", spinner="point"):
            f.write(templateFile % name)
    choice = Confirm.ask("🚀 Created! Do you want to run it? ")
    if choice:
        watch_and_run(name)
    messages = ["Launch the site on another device", "Add a new page", "Change the index file", "Add a favicon"]
    if (name == "main"):
        messages.append("Change the name")
    cmsgs = []
    console.rule("What to do:")
    with Live(refresh_per_second=4) as l:
        for a in range(len(messages)):
            a = a - 1
            time.sleep(0.4)
            cmsgs.append(messages[a])
            l.update("\n".join(cmsgs))
    





if __name__ == "__main__":
    app()
