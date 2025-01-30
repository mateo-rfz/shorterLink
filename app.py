from flask import Flask , render_template , request , redirect , url_for

#import socket for find local ip
import socket


app = Flask(__name__)
 
 

@app.route("/", methods=["GET", "POST"])
def mainPage():
    links_created = 123 
    views = 4567 
    users = 89 

    return render_template("main.html", linksCreated=links_created, view=views, users=users)









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








@app.route("/signup", methods=["GET", "POST"])
def signup():
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





#main page api
@app.route("/policy" , methods = ["GET"])
def policy() : 
    return render_template("policy.html")


@app.route("/about" , methods = ["GET"])
def about() : 
    return render_template("about.html")


@app.route("/contactus" , methods = ["GET"])
def contactus() : 
    return render_template("contactus.html")











if (__name__) == ("__main__") : 
    app.run(host=socket.gethostbyname(socket.gethostname()) , port=80 , debug=True)