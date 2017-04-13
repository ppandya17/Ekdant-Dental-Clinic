from flask import Flask, render_template, request, jsonify
import pymongo
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/appointment')
def appointmentBook():
    Name = request.args.get('appointmentName')
    phone = request.args.get('appointmentPhone')
    message = request.args.get('messageValue')
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

    TEXT = "Appointment booked by "+ Name +" on Date: "+ date +" at time: "+ str(time) +" and message from patient: "+ message +""
    send_data_to_gmail("Appointment Booked for "+ Name +"", "pspandya2009@gmail.com", TEXT)
    return jsonify("done")

@app.route('/sendmail')
def sendMail():

    name = request.args.get('nameValue')
    email = request.args.get('emailValue')
    message = request.args.get('messageValue')
    subject = request.args.get('subjectValue')

    #For inserting into database
    insertDatainDatabase(name, email, message, subject)

    subject_for_mail = "Information about " + subject + ""
    send_data_to_gmail(subject_for_mail, email, message)

    #gmail_user = "PSPandya2009@gmail.com"
    #gmail_pwd = "espire2Stevens#"
    #FROM = gmail_user
    #TO = email

    #TEXT = message


    # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # try:
    #     server = smtplib.SMTP("smtp.gmail.com", 587)
    #     server.ehlo()
    #     server.starttls()
    #     server.login(gmail_user, gmail_pwd)
    #     server.sendmail(FROM, TO, message)
    #     server.close()
    #     print
    #     'successfully sent the mail'
    # except Exception as e:
    #     print
    #     str(e)
    return jsonify("done")

def send_data_to_gmail(subject_for_mail, email, message):
    import smtplib
    gmail_user = "PSPandya2009@gmail.com"
    gmail_pwd = "espire2Stevens#"
    FROM = gmail_user
    TO = email
    SUBJECT = subject_for_mail
    TEXT = message

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

def insertDatainDatabase(name, email, message, subject):
    client = pymongo.MongoClient()
    db = client.ContactEnquiry
    db.sites.insert({
        "Name":name,
        "email":email,
        "message":message,
        "subject":subject
    })
    return True


def appointment_report():
    client = pymongo.MongoClient()
    db = client.Appointment
    db.sites.insert({
        "Name": Name,
        "phone": phone,
        "message": message,
        "date": date,
        "time": time
    })
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=appointment_report,
    trigger=IntervalTrigger(hours=24),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)

