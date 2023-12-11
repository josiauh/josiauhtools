try: 
    from pip._internal.operations import freeze
except ImportError: # pip < 10.0
    from pip.operations import freeze

import venv
import os

def convertToVenv(path = "."):
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
    os.system((path + "\\Scripts\\activate" if os.name == "nt" else path + "/Scripts/activate") + "&&" + "python -m pip install -r "+path+"/pkgs.txt")
    print("""
    ╭── Status────────────────────╮
    ┃ 📦 Packages frozen!         ┃
    ┃ 🗞️ File wrote!              ┃
    ┃ 💻 Venv created!            ┃
    ┃ 🔄️ Packages installed!      ┃
    ┃ Converted to venv!          ┃
    ╰─────────────────────────────╯ 
    """)
    print("If not already activated, run the activate file.")