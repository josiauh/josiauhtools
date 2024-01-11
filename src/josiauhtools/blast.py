"""
Blast
A web server tool for Josiauhtools
"""
from __future__ import annotations
import ast
import inspect
import os
import enum
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import json
mimetypes.init()

class BlastException(Exception):
    class BlastExceptionCode(enum.Enum):
        HTTPInternalError = "500: Something may have been gone wrong in HTTP."
        PortNonInt = "Non-HTTP Error: Your port is a non-int string."
        BlastInternalError = "Non-HTTP Error: Something may have gone wrong with Blast."
    def __init__(self, code: BlastExceptionCode) -> None:
        super().__init__(f"{code}")

class BlastApp:
    def __init__(
            self,
            port: str | int = 5000,
            hostname: str = "localhost",
            closeOnError: bool = False,
            openOnCreate: bool = True
        ) -> None:
        """
        Creates a Blast app.
        Port is a string or an int, which defaults to 5000.
        Hostname is a string, which defaults to localhost.
        CloseOnError is a bool, which indicates if it should close the webserver on an error.
        OpenOnCreate is also a bool, which indicates if you want to open your browser on the webserver's creation.
        """
        if type(port) == type("") and not port.isnumeric():
            raise BlastException()
        self.port = int(port)
        self.host = hostname
        self.pages = []
        self.postMethods = []
        self.assets = []
        self.errClose = closeOnError
        self.openCreate = openOnCreate
        
    def page(
        self,
        path: str
    ):
        """
        Identifies a function as a page. Example:
        ```python
        app = blast.BlastApp()
        @app.page('/')
        def index():
            return 'this is the content of my index page. do you like it?'

        @app.page('404')
        def notFound():
            return '<a href="/">Not found. Click to go home!</a>'
        ```
        The page decorator supports HTML content, as seen in the "notFound" decorator.
        """
        def decorate(function):
            result = function()
            if result == None:
                print("Function did not return a result.")
            else:
                self.pages.append({"page": path, "content": result})
                print("Saved page " + path)
        return decorate
    def post(
        self,
        path: str
    ):
        """
        Identifies a function as a POST method. Example:
        ```python
        app = blast.BlastApp()
        @app.post('/postTest')
        def testPost():
            return 'allow me.'

        @app.post('404')
        def weezer():
            return 'bro just got weezer\\'d'
        ```
        You can't have a parameter POST method, which will be added in the future.
        """
        def decorate(function):
            result = function()
            if result == None:
                print("Function did not return a result.")
            else:
                self.postMethods.append({"path": path, "function": inspect.getsource(function)})
                print("Added post method " + path)
        return decorate
    def addAsset(self, assetPath: os.PathLike, webPath: str | None = None):
        """
        Adds an asset. This is not the same as adding a page, because every page stored in your app is automatically identified as an HTML file.
        This can be:
        * your favicon
        * CSS stylesheets
        * JS scripts
        """
        with open(assetPath, "r") as f:
            self.assets.append({"path": webPath, "content": f.read()})
    def addPageFromFile(self, filePath: os.PathLike, webPath: str | None = None):
        """
        Adds a page from a file. Like addAsset, but adds as a page.
        """
        with open(filePath, "r") as f:
            self.pages.append({"path": webPath, "content": f.read()})

    def run(self):
        """
        Starts your Blast app. This:
        * saves the pages and assets to a directory
        * launches the server under your specified hostname and port (default localhost:5000)
        """
        print("Running Blast app...")
        print(self.pages)
        print(self.assets)
        os.makedirs(".blast",exist_ok=True)
        os.makedirs(".privateBlast",exist_ok=True)
        for i in self.pages:
            page = "index" if i["page"] == "/" else i["page"]
            with open(f".blast/{page}.html", "w") as f:
                f.write(i["content"])
        for i in self.assets:
            with open(f".blast/{i['path']}", "w") as f:
                f.write(i['content'])
        with open(f".privateBlast/postMethods.txt", "w") as f:
            f.write(str(self.postMethods))
        print("Dumped all pages and assets to blast directory.")
        class Server(BaseHTTPRequestHandler):
            def do_GET(self):
                pth = self.path.split("?")[0]
                try:
                    alska = self.path.split("?")[1].split("&")
                except:
                    alska = []
                args = {}
                for i in alska:
                    asd = i.split("=")
                    args[asd[0]] = asd[1]
                isAsset = len(pth.split(".")) > 1
                print("Loading page %s..." % pth)
                sentResp = False
                try:
                    with open(".blast/index.html" if pth == "/" else '.blast' + pth if isAsset else '.blast' + pth + ".html", "r") as f:
                        file = f.read()
                    print("Loaded!")
                except FileNotFoundError:
                    print("Could not find the file. Loading 404 file...")
                    try:
                        with open(".blast/404.html","r") as f:
                            file = f.read()
                    except:
                        file = """
                            <h1>404</h1>
                            This is Blast's default 404 page.<br>
                            No worries! You can change it by adding a page as 404.<br>
                            Example 1:<br>
                            <code>
                                @app.page('404')
                                def iForgot():
                                    return 'insert your content here'
                            </code><br>
                            Example 2:<br>
                            <code>
                                app.addPageFromFile("path/to/404.html", "404")
                            </code><br>
                        """
                    self.send_response(404)
                    sentResp = True
                except Exception as e:
                    print(e)
                    self.send_error(500)
                    return
                if sentResp != True:
                    self.send_response(200)
                self.send_header("Content-type", mimetypes.guess_type(".blast/index.html" if pth == "/" else '.blast' + pth if isAsset else '.blast' + pth + ".html")[0])
                self.end_headers()
                self.wfile.write(bytes(file, "utf-8"))
            def do_POST(self):
                with open(".privateBlast/postMethods.txt", "r") as f:
                    self.postMethods = ast.literal_eval(f.read())
                try:
                    for i in self.postMethods:
                        if i["path"] == self.path:
                            self.send_response(200)
                            self.send_header('Content-type','text/html')
                            self.end_headers()
                            self.wfile.write(bytes(eval(i["function"]), "utf8"))
                            return
                    self.send_response(404)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    for i in self.postMethods:
                        if i["path"] == "404":
                            self.wfile.write(bytes(eval(i["function"]), "utf8"))
                            return
                    self.wfile.write(bytes("This is Blast's default 404 message for POST methods.\nNo worries! You can change it by adding a POST method as '404'.", "utf-8"))
                except:
                    self.send_response(500)
                    self.send_header('Content-type','text/plain')
                    self.end_headers()
                    self.wfile.write(bytes("Something went wrong.", "utf-8"))
        web = HTTPServer((self.host, self.port), Server)
        print("Blast app started! You can launch it at http://%s:%s." % (self.host, self.port))
        if self.openCreate:
            webbrowser.open("http://%s:%s" % (self.host, self.port), new=2)
        try:
            web.serve_forever()
        except KeyboardInterrupt:
            print("Closing server...")
            web.server_close()
        except Exception as e:
            print("Error occured:")
            print(e)
            if (self.errClose):
                print("Closing server...")
                web.server_close()
                
                