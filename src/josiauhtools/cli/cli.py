import random
import sys
from typing import Optional
from rich.panel import Panel
from rich import print
import typer
from josiauhtools.cli.exvenvded import app as exv
from josiauhtools.cli.cliblast import app as cbl
from typing_extensions import Annotated
app = typer.Typer()

@app.command("fortnite")
def fortnite():
    if (random.randrange(0, 100) == 0):
        print("Fortnite launched.")
    deleted = Panel("You are now in a smaller version of Windows.",title="Deleted System32")
    print(deleted)

@app.command("cheese")
def cheese(steal: Annotated[Optional[str], typer.Option(help="The user to steal from.")] = ""):
    if not steal is "":
        print(Panel(f"You stole {random.randrange(0, 1000)} cheese from {steal}.",title="Stole cheese"))
    else:
        print(Panel(f"You gained {random.randrange(0, 1000)} cheese.",title="Gained cheese"))
    

def cli():
    args = sys.argv[1:]
    try:
        if args[0] == "exvenvded":
            sys.argv = sys.argv[1:]
            exv()
        elif args[0] == "blast":
            sys.argv = sys.argv[1:]
            cbl()
        else:
            app()
    except IndexError:
        app()
    except Exception as e:
        print(Panel(f"An error occured.\n{e}",title="Error"))

cli()