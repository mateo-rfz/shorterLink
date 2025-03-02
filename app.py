from flask import Flask , render_template , request , abort , redirect , url_for , send_file , make_response 

#import socket for find local ip    
import socket
import io
from modules import metricManager ,urlManager ,registerKeyManager ,mainPageMetric, userManager
from modules import qrcodeManager

app = Flask(__name__)



@app.before_request
def before_request():
    mainPageMetric.Views(request.remote_addr).addToViewsCounter()
 
 

@app.route("/", methods=["GET", "POST"])
def main():
    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    if registerKeyManager.KeyValidation(email , registerKey).checkValidation() is True : 
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
    origin = urlManager.ShowUrlWithShortLink(shortLink).show()

    if origin : 
        metricManager.AddView(shortLink).addView()
        return redirect(origin)
    else : 
        return render_template("notice.html" ,title = "Wrong page" , text = "we cant find this page on database") 
        





@app.route("/createlink" , methods = ["GET" , "POST"])
def createLink() : 
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
            return render_template("showLink.html" , title = "Your link created" , link = shortURL)
        else : 

            shortURL = urlManager.AddUrl(email , originLink , shortLink).add()
            
            if not shortURL : 
                return render_template("createLink.html" , title = "URL USED" , text = "url used by another user")
            else : 
                return render_template("showLink.html" , title = "Your link created" , link = shortURL)


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
            #redirect to home page after set cookies
            resp = make_response(redirect(url_for('main')))
            #the expiration for cookies is 7 days
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
            registerKey = registerKeyManager.AddRegisterKey(email).registerKey()
            #redirect to create link page after set cookies
            resp = make_response(redirect(url_for('createLink')))
            #the expiration for cookies is 7 days
            resp.set_cookie('email', email , max_age=60*60*24*7)  
            resp.set_cookie('key', registerKey , max_age=60*60*24*7) 
            return resp
    
        elif not o :
            return render_template("signup.html" , title = "Error" , text = "An account with this email already exists.")
        
        elif o == "WEAKPASS" : 
            return render_template("signup.html" , title = "Weak password" , text = "Your password is weak use Number and Letters")


    else : 
        return render_template("signup.html")
    






@app.route("/deletelink/<string:shortLink>", methods=["POST"])
def deleteLink(shortLink):
    if not shortLink:
        return render_template("notice.html", title="Error", text="Invalid link."), 400
    
    email = request.cookies.get("email")
    registerKey = request.cookies.get("key")

    if not registerKeyManager.KeyValidation(email, registerKey).checkValidation():
        return render_template("login.html", title="Need to login", text="You need to login to remove a link."), 401

    if urlManager.DelUrl(email, shortLink).delete():
        return redirect(url_for("main"))
    else:
        return render_template("notice.html", title="Error", text="Permission denied or link does not exist."), 403






@app.route("/qrcode/<string:shortUrl>")
def qrcode(shortUrl):
    url = f"{request.host_url}{shortUrl}"
    print(url)

    cr = qrcodeManager.CreateQrCode(url).create()
    print(cr)

    qr_data = qrcodeManager.fetchQrCode(url).fetch()
    
    if not qr_data:
        return abort(404, description="WE CANT FIND THIS QRCODE")

    return send_file(
        io.BytesIO(qr_data),
        mimetype='image/png',
        as_attachment=False,
        download_name=f'{shortUrl}.png'
    )

@app.route("/dqrcode/<string:shortUrl>")
def downloadQrCode(shortUrl): 
    url = f"{request.host_url}{shortUrl}"

    qrcodeManager.CreateQrCode(url).create()

    qr_data = qrcodeManager.fetchQrCode(url).fetch()
    
    if not qr_data:
        return abort(404, description="WE CANT FIND THIS QRCODE")

    return send_file(
        io.BytesIO(qr_data),
        mimetype='image/png',
        as_attachment=True,
        download_name=f'{shortUrl}.png'
    )





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