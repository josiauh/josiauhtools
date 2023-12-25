try: 
    from pip._internal.operations import freeze
except ImportError: # pip < 10.0
    from pip.operations import freeze

import venv
import os
import platform
import yachalk

def convertToVenv(path = "."):
    if (os.path.isfile(os.path.join(path, "pyvenv.cfg"))):
        print(yachalk.chalk.yellow_bright("Venv already exists. Nothing will happen."))
        return
    print("""
    ╭── Status────────────────────╮
    ┃ 🕐 Freezing Packages...     ┃
    ╰─────────────────────────────╯ 
    """)
    pkgs = freeze.freeze()
    print("""
    ╭── Status────────────────────╮
    ┃ 📦 Packages frozen!         ┃
    ┃ 📝 Writing to file...       ┃
    ╰─────────────────────────────╯ 
    """)
    with open(path + "/pkgs.txt", "w") as f:
        f.write(pkgs)
        print("""
    ╭── Status────────────────────╮
    ┃ 📦 Packages frozen!         ┃
    ┃ 🗞️ File wrote!              ┃
    ┃ 🆕 Creating Venv...         ┃
    ╰─────────────────────────────╯ 
    """)
    venv.create(path)
    print("""
    ╭── Status────────────────────╮
    ┃ 📦 Packages frozen!         ┃
    ┃ 🗞️ File wrote!              ┃
    ┃ 💻 Venv created!            ┃
    ┃ 📲 Installing packages...   ┃
    ╰─────────────────────────────╯ 
    """)
    if platform.system() == "Windows":
        os.system(path + "\\Scripts\\activate && pip install -r " + path + "\\pkgs.txt")
    else:
        # assuming bash and zsh
        os.system("source " + path + "/bin/activate")
    print("""
    ╭── Status────────────────────╮
    ┃ 📦 Packages frozen!         ┃
    ┃ 🗞️ File wrote!              ┃
    ┃ 💻 Venv created!            ┃
    ┃ 🔄️ Packages installed!      ┃
    ┃ Converted to venv!          ┃
    ╰─────────────────────────────╯ 
    """)
    print("If not already activated, run the activate file.\n\nFind out how at https://docs.python.org/3.9/library/venv.html")