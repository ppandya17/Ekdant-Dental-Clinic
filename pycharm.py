from flask import Flask, render_template, request, jsonify
import pymongo

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/appointment')
def appointmentBook():
    Name = request.args.get('appointmentName')
    phone = request.args.get('appointmentPhone')
    message = request.args.get('appointmentMessage')
    date = request.args.get('appointmentDate')
    time = request.args.get('timeValue')


    client = pymongo.MongoClient()
    db = client.Appointment
    db.sites.insert({
        "Name": Name,
        "phone": phone,
        "message": message,
        "date": date,
        "time": time
    })
    return jsonify("done")

@app.route('/sendmail')
def sendMail():
    import smtplib
    name = request.args.get('nameValue')
    email = request.args.get('emailValue')
    message = request.args.get('messageValue')
    subject = request.args.get('subjectValue')

    #For inserting into database
    insertDatainDatabase(name, email, message, subject)

    gmail_user = "PSPandya2009@gmail.com"
    gmail_pwd = "espire2Stevens#"
    FROM = gmail_user
    TO = email
    SUBJECT = "Information about "+ subject+""
    TEXT = message

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
       """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print
        'successfully sent the mail'
    except Exception as e:
        print
        str(e)
    return jsonify("done")

def insertDatainDatabase(name, email, message, subject):
    client = pymongo.MongoClient()
    db = client.ContactEnquiry
    db.sites.insert({
        "Name":name,
        "email":email,
        "message":message,
        "subject":subject
    })

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)

