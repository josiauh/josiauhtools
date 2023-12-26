"""
Blast
A web API for Josiauhtools
"""
from __future__ import annotations
import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
mimetypes.init()

class BlastApp:
    def __init__(
            self,
            port: str | int = 5000,
            hostname: str = "localhost",
            closeOnError: bool = False
        ) -> None:
        """
        Creates a Blast app.
        """
        self.port = int(port)
        self.host = hostname
        self.pages = []
        self.postMethods = []
        self.assets = []
        self.errClose = closeOnError
        
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
        ```
        The page decorator also supports HTML content.
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
        Identifies a POST method. You cannot have a parameter POST function, although it will be added later in the future.
        """
        def decorate(function):
            result = function()
            if result == None:
                print("Function did not return a result.")
            else:
                self.postMethods.append({"path": path, "function": function})
                print("Added post method " + path)
        return decorate
    def addAsset(self, assetPath: os.PathLike, webPath: str | None = None):
        """
        Adds an asset. This is not the same as adding a page, because every page stored in your app is automatically identified as an HTML file.
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
        os.makedirs(".blast",exist_ok=True)
        for i in self.pages:
            page = "index" if i["page"] == "/" else i["page"]
            with open(f".blast/{page}.html", "w") as f:
                f.write(i["content"])
        for i in self.assets:
            with open(f".blast/{i['path']}", "w") as f:
                f.write(i['content'])
        print("Dumped all pages and assets to blast directory.")
        class Server(BaseHTTPRequestHandler):
            def setVars(postReqs):
                self.posts = postReqs
            def do_GET(self):
                print("Loading page %s..." % self.path)
                sentResp = False
                try:
                    with open(".blast/index.html" if self.path == "/" else '.blast' + self.path, "r") as f:
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
                            No worries! You can change it by adding the page decorator as 404.
                        """
                    self.send_response(404)
                    sentResp = True
                except Exception as e:
                    print(e)
                    self.send_error(500)
                    return
                if sentResp != True:
                    self.send_response(200)
                self.send_header("Content-type", mimetypes.guess_type(".blast/index.html" if self.path == "/" else '.blast' + self.path)[0])
                self.end_headers()
                self.wfile.write(bytes(file, "utf-8"))
            def do_POST(self):
                for i in self.posts:
                    if i["path"] == self.path:
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()
                        self.wfile.write(bytes(i["function"](), "utf8"))
                        return
        web = HTTPServer((self.host, self.port), Server)
        print("Blast app started! You can launch it at http://%s:%s." % (self.host, self.port))
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
                
                