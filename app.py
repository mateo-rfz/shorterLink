from flask import Flask , render_template

#import socket for find local ip
import socket


app = Flask(__name__)


@app.route("/" , methods = ["GET" , "POST"])
def mainPage() : 
    pass


@app.route("/home" , methods = ["GET" , "POST"])
def home() : 
    pass


@app.route("/createLink" , methods = ["GET" , "POST"])
def createLink() : 
    pass


@app.route("/login" , methods = ["GET" , "POST"])
def login() : 
    pass


@app.route("/signUp" , methods = ["GET" , "POST"])
def signUp():
    pass




if (__name__) == ("__main__") : 
    app.run(host=socket.gethostbyname(socket.gethostname()) , port=80)