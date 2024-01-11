# This is your Blast app. You can change it as needed!
# You can add pages, post methods, and more.
from josiauhtools import blast
name = "post"

# You can change parameters here,
app = blast.BlastApp()

@app.page("/")
def index():
    return f"""
You're a few steps away from making your Blast app, "{name}"!
Here's a few changes:
<ul>
    <li>Change your port</li>
    <li>Add a new page</li>
    <li>Add a script and/or a stylesheet</li>
</ul>
Up to the challenge? Good luck!"""

if __name__ == "__main__":
    app.run()
