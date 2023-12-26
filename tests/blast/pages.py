from josiauhtools_josiauh import blast

app = blast.BlastApp()

@app.page("/")
def index():
    return """
        hi :D
    """

@app.page("404")
def notfound():
    return """
    404. womp.
    """

app.run()