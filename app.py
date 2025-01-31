from flask import Flask , render_template , request , redirect , url_for

#import socket for find local ip
import socket

from modules import dbController

from modules import shortLinkCreator


app = Flask(__name__)


#constants
DOMAIN = request.url
 
 

@app.route("/", methods=["GET", "POST"])
def main():
    links_created = 123 
    views = 4567 
    users = 89 

    return render_template("main.html", linksCreated=links_created, view=views, users=users)








@app.route("/<string:shortLink>" , methods = ["GET" , "POST"])
def redirectPage(shortLink) : 
    origin = dbController.urlFinder(shortLink)

    if origin :
        return redirect(list(origin)[2])
    else : 
        return render_template("notice.html" ,title = "Wrong page" , text = "we cant find this page on database") 
        









@app.route("/createLink" , methods = ["GET" , "POST"])
def createLink() : 
    if request.method == "GET" : 
        return render_template("createLink.html")
    else : 
        username = request.form.get("username")
        originLink = request.form.get("originLink")
        shortLink =  shortLinkCreator.createShortLink()

        dbController.createShortUrl(username , originLink , shortLink)

        return render_template("link.html" , title = "Success" , domain = DOMAIN , shortLink = shortLink)







@app.route("/login" , methods = ["GET" , "POST"])
def login() : 
    return render_template("notice.html" , title = "Wrong" , text = "This feature is not available")








@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("notice.html" , title = "Wrong" , text = "This feature is not available")





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