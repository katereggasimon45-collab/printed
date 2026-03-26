from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "elisabathsim@gmail.com"
app.config['MAIL_PASSWORD'] = "ovuqhxgkmvoorwyu"

mail = Mail(app)

with app.app_context():
    msg = Message(
        "Test Email",
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']],
        body="This is a test email!"
    )
    mail.send(msg)
    print("Email sent!")