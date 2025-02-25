from flask import Flask , render_template , request , redirect , url_for , send_file , make_response

#import socket for find local ip
import socket

from modules import metricManager ,urlManager ,registerKeyManager ,mainPageMetric, userManager


app = Flask(__name__)


# Constants
DOMAIN = None

@app.before_request
def before_request():
    global DOMAIN
    DOMAIN = request.url_root 
 
 

@app.route("/", methods=["GET", "POST"])
def main():
    mainPageMetric.Views().addToViewsCounter()

    links_created = mainPageMetric.LinksCounter().showLinksCounter()
    views = mainPageMetric.Views().showViewsCounter()
    users = mainPageMetric.Users().showUsersCounter()

    return render_template("main.html", linksCreated=links_created, view=views, users=users)








@app.route("/<string:shortLink>" , methods = ["GET" , "POST"])
def redirectPage(shortLink) : 
    origin = urlManager.ShowUrlWithShortLink(shortLink).show()

    if origin : 
        return redirect(origin)
    else : 
        return render_template("notice.html" ,title = "Wrong page" , text = "we cant find this page on database") 
        





@app.route("/createlink" , methods = ["GET" , "POST"])
def createLink() : 
    if request.method == "POST" : 
        email = request.cookies.get("email")
        registerKey = request.cookies.get("key")

        if not registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
            return render_template("notice.html" , title = "Need to login" , text = "for create link you need to login first")
        
        originLink = request.form.get("originLink")
        shortLink = request.form.get("shortLink") or None   


        if not originLink:
            return render_template("notice.html", title="Error", text="Origin link is required.")

        if shortLink == None : 
            shortURL = urlManager.AddUrl(email , originLink).add()
            return render_template("notice.html" , title = "Your link created" , text = f"YOUR Create Link is {shortURL}")
        else : 
            shortURL = urlManager.AddUrl(email , originLink , shortLink).add()
            
            if not shortURL : 
                return render_template("notice.html" , title = "URL USED" , text = "url used by another user")
            else : 
                return render_template("notice.html" , title = "Your link created" , text = f"YOUR Create Link is {shortURL}")


    else : 
        return render_template("createLink.html")











@app.route("/login" , methods = ["GET" , "POST"])
def login() : 
    if request.method == "POST" : 
       email = request.form.get("email")
       password = request.form.get("password")

       o = userManager.CheckUserValidation(email , password).validationChecker()
       if not o : 
            return render_template("login.html", title = "WRONG" , text = "your username or password is wrong")
       else : 
            registerKey = registerKeyManager.AddRegisterKey(email).registerKey()
            resp = make_response(redirect(url_for('main')))
            resp.set_cookie('email', email , max_age=60*60*24*7)  
            resp.set_cookie('key', registerKey , max_age=60*60*24*7)  
            return resp
    
    else :
       return render_template("login.html")








@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST" : 
        email = request.form.get("email")
        password = request.form.get("password")

        o = userManager.AddUser(email , password).adduser()
        if o is True: 
            return render_template("notice.html" , title = "CREATED" , text = "your account created")
        else : 
            return render_template("notice.html" , title = "Wrong" , text = o[1])
        
    else : 
        return render_template("signup.html")




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