from flask import Flask , render_template , request , abort , redirect , url_for , send_file , make_response 

#import socket for find local ip addr
import socket

# Import the io module to create an in-memory byte buffer for sending the QR code
import io

#import metricManager module for manage metrix like link views
from modules import metricManager 

#import urlManager module for add shortLink and fetch original link using shortLink
from modules import urlManager 

#import registerKeyManager for manage login cookies register keys and key validation
from modules import registerKeyManager 

#import mainPageMetric for show metrix in main page like as users , links , views counter
from modules import mainPageMetric

#import userManager for add user and check user validation
from modules import userManager

#import qrcodeManager for create qrcode , push them to redis and fetch them from memory
from modules import qrcodeManager

#import logger for write logs
from modules import logger


app = Flask(__name__)





@app.before_request
def before_request():
    # Increment the view counter for all pages based on the visitor's IP address
    mainPageMetric.Views(request.remote_addr).addToViewsCounter()
 
 




@app.route("/", methods=["GET", "POST"])
def main():
    """
    main.html -> home page for all users before login
    cmain.html -> dashboard page for all users after login
    """
    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    if registerKeyManager.KeyValidation(email , registerKey).checkValidation() is True : 
        logger.Logger("request to home page(logged user)" , request.remote_addr , email).logWriter()
        links = []
        """
        this section: 
        find all short links and origin links with email
          on urlManager and find the view on metricManager
        """
        o = urlManager.ShortUrlWithEmail(email).show()
        
        try : 
            for i in o : 
                view = metricManager.LinkView(i[3]).view()
                links.append([i[3] , i[2] , view[2]])
        except Exception : 
            pass
        
        return render_template("cmain.html" , email = email , links = links)

    else :      
        logger.Logger("request to home page(guest user)" , request.remote_addr , email).logWriter()
        """
        This is the public home page for users
          who have not signed in to ShorterLink
        """
        links_created = mainPageMetric.LinksCounter().showLinksCounter()
        views = mainPageMetric.Views().showViewsCounter()
        users = mainPageMetric.Users().showUsersCounter()

        return render_template("main.html", linksCreated=links_created, view=views, users=users)








@app.route("/<string:shortLink>" , methods = ["GET"])
def redirectPage(shortLink) : 
    email = request.cookies.get("email")

    origin = urlManager.ShowUrlWithShortLink(shortLink).show()
    logger.Logger("request to short link redirector page" , request.remote_addr , email).logWriter()

    if origin : 
        # add view for wanted link if exists
        metricManager.AddView(shortLink).addView()
        logger.Logger(f"redirect to {origin} with {shortLink}" , request.remote_addr , email).logWriter()

        return redirect(origin)
    else : 
        return render_template("notice.html" ,title = "Wrong page" , text = "we cant find this page on database") 
        

        





@app.route("/createlink" , methods = ["GET" , "POST"])
def createLink() : 

    email = request.cookies.get("email")
    logger.Logger("request to create shortLink" , request.remote_addr , email).logWriter()

    if request.method == "POST" : 
        email = request.cookies.get("email")
        registerKey = request.cookies.get("key")

        if not registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
            return render_template("login.html", title = "Need to login" , text = "For create link you need to login first")
        
        originLink = request.form.get("originLink")
        shortLink = request.form.get("shortLink") or None   


        if not originLink:
            return render_template("createLink.html", title="Error", text="Origin link is required.")

        if shortLink == None : 
            shortURL = urlManager.AddUrl(email , originLink).add()
            logger.Logger(f"create shortLink for {originLink}" , request.remote_addr , email).logWriter()

            return render_template("showLink.html" , title = "Your link created" , link = shortURL)
        else : 

            shortURL = urlManager.AddUrl(email , originLink , shortLink).add()
            logger.Logger(f"create shortLink for {originLink} with {shortLink}" , request.remote_addr , email).logWriter()

            if not shortURL : 
                return render_template("createLink.html" , title = "URL USED" , text = "url used by another user")
            else : 
                return render_template("showLink.html" , title = "Your link created" , link = shortURL)


    else : 
        return render_template("createLink.html")











@app.route("/login" , methods = ["GET" , "POST"])
def login() : 
    if request.method == "POST" : 
       email = request.cookies.get("email")
       registerKey = request.cookies.get("key")

       if registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
            return render_template("login.html", title = f"You are already logged in" , text = f"You are already logged in as {email}" , color = "green")
    

       email = request.form.get("email")
       password = request.form.get("password")

       o = userManager.CheckUserValidation(email , password).validationChecker()
       if not o : 
            return render_template("login.html", title = "WRONG" , text = "your username or password is wrong")
       else : 
            logger.Logger(f"user logged in" , request.remote_addr , email).logWriter()

            registerKey = registerKeyManager.AddRegisterKey(email).registerKey()
            #redirect to home page after set cookies
            resp = make_response(redirect(url_for('main')))
            """
            The expiration for cookies is 7 days or 168h

            other times for expire time : 
            24h(1 day) -> 60 * 60 * 24
            48h(2 day) -> 60 * 60 * 24 * 2
            72h(3 day) -> 60 * 60 * 24 * 3
            96(4 day) -> 60 * 60 * 24 * 4
            """
            resp.set_cookie('email', email , max_age=60*60*24*7)  
            resp.set_cookie('key', registerKey , max_age=60*60*24*7)  
            return resp
    
    else :
       email = request.cookies.get("email")
       registerKey = request.cookies.get("key")

       logger.Logger(f"request for login page" , request.remote_addr , email).logWriter()


       if registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
            return render_template("login.html", title = f"You are already logged in" , 
                                   text = f"You are already logged in as {email}" ,
                                     color = "green"  , logout = True
                                   )
    
       return render_template("login.html")










@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST" : 

        email = request.cookies.get("email")
        registerKey = request.cookies.get("key")

        if registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
                return render_template("login.html", title = f"You are already logged in" , 
                                    text = f"You are already logged in as {email}" ,
                                        color = "green"  , logout = True
                                    )



        email = request.form.get("email")
        password = request.form.get("password")

        o = userManager.AddUser(email , password).adduser()
        if o == 300: 
            logger.Logger(f"user sginup" , request.remote_addr , email).logWriter()

            registerKey = registerKeyManager.AddRegisterKey(email).registerKey()
            #redirect to create link page after set cookies
            resp = make_response(redirect(url_for('createLink')))
            #the expiration for cookies is 7 days
            resp.set_cookie('email', email , max_age=60*60*24*7)  
            resp.set_cookie('key', registerKey , max_age=60*60*24*7) 
            return resp
    

        elif o == "WEAKPASS" : 
            return render_template("signup.html" , title = "Weak password" , text = "Your password is weak use Number and Letters")


        elif not o :
            return render_template("signup.html" , title = "Error" , text = "An account with this email already exists.")
        
        

    else : 
        email = request.cookies.get("email")
        registerKey = request.cookies.get("key")

        logger.Logger(f"request for signup page" , request.remote_addr , email).logWriter()


        if registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
            return render_template("signup.html", title = f"You are already logged in" , 
                                   text = f"You are already logged in as {email}" ,
                                     color = "green"  , logout = True
                                   )
        
        return render_template("signup.html")
    








@app.route("/resetpass" , methods = ["GET" , "POST"])
def resetPass() :
    if request.method == "POST" : 
        email = request.cookies.get("email")
        registerKey = request.cookies.get("key")

        if registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
            oldPassword = request.form.get("oldPassword")
            newPassword = request.form.get("newPassword")
            
            o = userManager.ChangeUserPassword(email , oldPassword , newPassword).changePass()
            if o == "WEAKPASS" : 
                return render_template("resetpass.html" , title = "Weak password" , text = "Your password is weak use Number and Letters")


            #set new register key for new login
            registerKeyManager.AddRegisterKey(email).registerKey()
            logger.Logger(f"user change password" , request.remote_addr , email).logWriter()


            return render_template("login.html" , title = "Success" , text = "your password was changed" , color = "green")

        else : 
            return render_template("login.html", title = "Need to login" , text = "For change password you need to login first")
        
    else :
        email = request.cookies.get("email")
        logger.Logger(f"request for reset pass page" , request.remote_addr , email).logWriter()

        return render_template("resetpass.html")









@app.route("/deletelink/<string:shortLink>", methods=["POST"])
def deleteLink(shortLink):
    if not shortLink:
        return render_template("notice.html", title="Error", text="Invalid link."), 400
    
    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    logger.Logger(f"request for delete {shortLink}" , request.remote_addr , email).logWriter()


    if not registerKeyManager.KeyValidation(email, registerKey).checkValidation():
        return render_template("login.html", title="Need to login", text="You need to login to remove a link."), 401

    if urlManager.DelUrl(email, shortLink).delete():
        return redirect(url_for("main"))
    else:
        return render_template("notice.html", title="Error", text="Permission denied or link does not exist."), 403








@app.route("/qrcode/<string:shortUrl>")
def qrcode(shortUrl):

    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    logger.Logger(f"request qrcode for {shortUrl}" , request.remote_addr , email).logWriter()


    if not registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
        return render_template("login.html", title="Need to login", text="You need to login"), 401

    # url =      host_url      + shortUrl
    # url = https://example.com/ + example
    url = f"{request.host_url}{shortUrl}"
    print(url)

    cr = qrcodeManager.CreateQrCode(url).create()

    qr_data = qrcodeManager.FetchQrCode(url).fetch()
    
    if not qr_data:
        return abort(404, description="WE CANT FIND THIS QRCODE")

    return send_file(
        io.BytesIO(qr_data),
        mimetype='image/png',
        as_attachment=False,
        download_name=f'{url}.png'
    )








@app.route("/dqrcode/<string:shortUrl>")
def downloadQrCode(shortUrl): 
    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    logger.Logger(f"download qrcode shortLink {shortUrl}" , request.remote_addr , email).logWriter()

    if not registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
        return render_template("login.html", title="Need to login", text="You need to login"), 401

    # url =      host_url      + shortUrl
    # url = https://example.com/ + example
    url = f"{request.host_url}{shortUrl}"

    qrcodeManager.CreateQrCode(url).create()

    qr_data = qrcodeManager.FetchQrCode(url).fetch()
    
    if not qr_data:
        return abort(404, description="WE CANT FIND THIS QRCODE")

    return send_file(
        io.BytesIO(qr_data),
        mimetype='image/png',
        as_attachment=True,
        download_name=f'{url}.png'
    )







@app.route("/profile")
def profile() : 
    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    logger.Logger(f"request to profile page" , request.remote_addr , email).logWriter()

    if not registerKeyManager.KeyValidation(email , registerKey).checkValidation() :
        return render_template("login.html", title="Need to login", text="You need to login to access to profile"), 401

    else : 
        return render_template("profile.html" , email = email)






@app.route("/logout")
def logout() : 
    email = request.cookies.get("email")
    logger.Logger(f"logout" , request.remote_addr , email).logWriter()

    response = make_response(redirect(url_for("login")))
    response.delete_cookie('key')
    return response






#main page api for policy and about and contactus
@app.route("/policy" , methods = ["GET"])
def policy() : 
    email = request.cookies.get("email")
    logger.Logger(f"request to policy page" , request.remote_addr , email).logWriter()

    return render_template("policy.html")


@app.route("/about" , methods = ["GET"])
def about() : 
    email = request.cookies.get("email")
    logger.Logger(f"request to about page" , request.remote_addr , email).logWriter()

    return render_template("about.html")


@app.route("/contactus" , methods = ["GET"])
def contactus() : 
    email = request.cookies.get("email")
    logger.Logger(f"request to contactus page" , request.remote_addr , email).logWriter()

    return render_template("contactus.html")









if (__name__) == ("__main__") : 
    app.run(host=socket.gethostbyname(socket.gethostname()) ,
             port=80 ,
               debug=False)