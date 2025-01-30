from flask import Flask , render_template , request , redirect , url_for

#import socket for find local ip
import socket


app = Flask(__name__)
 
 


@app.route("/" , methods = ["GET" , "POST"])
def mainPage() : 
    return render_template("main.html")








@app.route("/<string:shortLink>" , methods = ["GET" , "POST"])
def redirectPage(shortLink) : 
        pass #return the original link










@app.route("/home" , methods = ["GET" , "POST"])
def home() : 
    return "hello from home route"









@app.route("/createLink" , methods = ["GET" , "POST"])
def createLink() : 
    return "hello from createLink route"








@app.route("/login" , methods = ["GET" , "POST"])
def login() : 
    if request.method == "GET" : 
        return render_template("login.html")
    else : 
        username = request.form.get("username")
        password = request.form.get("password")
        

        if username and password : #check login validation
            return redirect(url_for("home"))
        else : 
            return render_template("login.html")








@app.route("/signUp" , methods = ["GET" , "POST"])
def signUp():
    if request.method == "POST" : 
        return render_template("signup.html")
    else : 
        email = request.form.get("email")
        password = request.form.get("password")

        #check exists for email 
        if email != True : 
            pass #create account on db
            return "your account is created" 
        else : 
            return "the email is already used"








if (__name__) == ("__main__") : 
    app.run(host=socket.gethostbyname(socket.gethostname()) , port=80)