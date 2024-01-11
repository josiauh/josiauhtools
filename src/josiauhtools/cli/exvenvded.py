try: 
    from pip._internal.operations import freeze #type: ignore
except ImportError: # pip < 10.0
    from pip.operations import freeze #type: ignore

import venv
import os
import platform
from typer import Typer
import yachalk
from rich import print as rprint
from josiauhtools.cli.display import LivePanelDisplay
app = Typer(help="Venv tools.")
def convertFromVenv(path = "."):
    if os.path.isfile(os.path.join(path, "pyvenv.cfg")) == False:
        print(yachalk.chalk.yellow_bright("Venv does not exist."))
        return
    with LivePanelDisplay(title="Status") as l:
        pkgs = freeze.freeze()
        l.update(":ice_cube: Freezing packages...")
        with open(path + "/pkgs.txt", "w") as f:
            f.write(pkgs)
        l.changeLastLine(":package: Packages frozen!")
        l.update(":computer: Deleting venv...")
        os.rmdir("Lib")
        os.rmdir("Scripts")
        os.rmdir("Include")
        l.changeLastLine(":desktop: Venv deleted!")
app.command("convertFrom", help="Convert your current Python environment to a venv.")(convertFromVenv)
@app.command("convertTo",help="Same as convertFrom, but swap the envs.")
def convertToVenv(path="."):
    if (os.path.isfile(os.path.join(path, "pyvenv.cfg"))):
        print(yachalk.chalk.yellow_bright("Venv already exists."))
        return
    with LivePanelDisplay(title="Status") as l:
        pkgs = freeze.freeze()
        l.update(":ice_cube: Freezing packages...")
        with open(path + "/pkgs.txt", "w") as f:
            f.write(pkgs)
        l.changeLastLine(":package: Packages frozen!")
        l.update(":desktop: Creating venv...")
        venv.create(path)
        l.changeLastLine(":computer: Venv created!")
        l.update(":x: Activating venv...")
        if platform.system() == "Windows":
            os.system(path + "\\Scripts\\activate && pip install -r " + path + "\\pkgs.txt")
        else:
            # assuming bash and zsh
            os.system("source " + path + "/bin/activate")
        l.changeLastLine("Venv activated!\nAll done.")
    print("If not already activated, run the activate file.\n\nFind out how at https://docs.python.org/3.9/library/venv.html")