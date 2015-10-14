import smtplib,datetime,json
from flask import Flask,request
from flask.ext.bcrypt import Bcrypt
from flask.ext.pymongo import PyMongo
from flask import jsonify
from bson.objectid import ObjectId
import requests
app = Flask("FREEMAIL")
mongo=PyMongo(app)
bcrypt=Bcrypt(app)

@app.route('/registerapp',methods=["GET","POST"])
def register():
    try:
        appdetail={}
        # import pdb
        # pdb.set_trace()
        data=request.get_json(force=True)
        appdetail['email']=data['email']
        appdetail['password']=data['password']
        res=mongo.db.registeredapp.insert({"appemail":appdetail['email'],"password":appdetail['password'],
        "pwhash":bcrypt.generate_password_hash(appdetail['password'])})
        gmail_user =data['email']
        gmail_pwd = data['password']
        FROM = data['email']
        TO = data['email']
        SUBJECT = "FREEMAIL Registration"
        TEXT = "hi your app has been registered and your token is %s\n and your appid is %s" %(bcrypt.generate_password_hash(data['email']+str(datetime.datetime.now())),str(res))
        message = "FROM:%s\nTO:%s\nSUBJECT:%s\n%s" % (FROM,TO,SUBJECT,TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
        except Exception as e:
            print e
            return jsonify(error="You supplied wrong credentials"),500
        return jsonify(success="App registered successfully! Authtoken will be emailed to you.",)
    except Exception as e:
        print e
        return jsonify(error="something went wrong maybe you supplied wrong details"),500


@app.route('/mailer/<appid>',methods=["GET","POST"])
def send_mail(appid):
    try:
        res=mongo.db.registeredapp.find_one({"_id": ObjectId(appid)})
        if res is not None:
            data=request.get_json(force=True)
            if data['token']==res['pwhash']:
                gmail_user =res['appemail']
                gmail_pwd = res['password']
                FROM = res["appemail"]
                TO = data['to']
                SUBJECT = data['subject']
                TEXT = data['message']
                credits = "Email sent from FREEMAIL :developed by GAURAV SHUKLA (github handle deathping1994)" \
                        "\nDisclaimer: Developer does not hold any responsibility as to how this service may be used"
                message = "FROM:%s\nTO:%s\nSUBJECT:%s\n%s\n \n%s" % (FROM,TO,SUBJECT,TEXT,credits)
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                server.close()
                return jsonify(success='successfully sent the e-mail'),200
            else:
                return jsonify(error="You supplied wrong token."),403
        else:
            return jsonify(error="Your app is not registered to use this service"),500
    except Exception as e:
        print e
        return jsonify(error="failed to send mail"),500



if __name__ == '__main__':
    app.run()
