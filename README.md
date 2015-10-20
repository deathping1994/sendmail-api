# gmail-sendmail-api

Note: Do not forget to enable `allow less secure apps` under sttings option in your apps email
Email sending api for gmail
**The server mentioned below is down but you can always set up your own using flask+ mongodb**
# Use Case
  1. Send Verification emails to user while signup
  2. Implement forgot password using OTP on email
  3. Ceate an email client for IOT or anything that can connect to internet
  
# How to use

#### Step 1:
  Register your app or website by sending an HTTP request to `http://128.199.169.129:8080/registerapp`
  with payload
    
    {
      "email":"yourappsemail@gmail.com", ** // As of now this api only supports app which have there emails on gmail **
      "password": "password"  // password for yourappsemail@gamil.com			
    }

**Note: yourappsemail is the email id from which you want to send emails to your users. As of now it supports gmail only but emails can be sent to all users (gmail,live,yahoo... etc)**


#### Step 2:
  If registration is successfull you would receive an auth token on yourappsemail@gmail.com. use that token to send emails to users.
  
To send email make an https request to `http://128.199.169.129:8080/mailer/appid`
with payload containing


    {
        "to":"deathping1994@gmail.com",
        "subject":"hey",
        "message":"you have tried it too many times",
        "token":"your auth token"
    }


You would get a response notifying you if email was sent successfully or not.
