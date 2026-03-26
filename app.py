from flask import Flask, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email
import os

# -------------------------
# APP SETUP
# -------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")  # Replace with a strong key in production

# -------------------------
# MAIL CONFIGURATION
# -------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    raise RuntimeError("MAIL_USERNAME and MAIL_PASSWORD must be set as environment variables!")

mail = Mail(app)

# -------------------------
# FLASK-WTF CONTACT FORM
# -------------------------
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    thea_email = EmailField("Thea's Email (optional)")
    phone = StringField("Phone", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])

# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/workdone")
def workdone():
    return render_template("workdone.html")

# ---------- CONTACT FORM ----------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Form data
        name = form.name.data
        email = form.email.data
        thea_email = form.thea_email.data
        phone = form.phone.data
        message_body = form.message.data

        # Recipients
        recipients = [app.config['MAIL_USERNAME']]
        if thea_email:
            recipients.append(thea_email)

        # Message
        msg = Message(
            subject=f"🖨️ New Order from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=recipients,
            body=f"""
New Printing Order

Name: {name}
Email: {email}
Thea's Email: {thea_email or 'N/A'}
Phone: {phone}

Message:
{message_body}
""",
            html=f"""
<h2>New Printing Order</h2>
<table>
<tr><td><b>Name:</b></td><td>{name}</td></tr>
<tr><td><b>Email:</b></td><td>{email}</td></tr>
<tr><td><b>Thea's Email:</b></td><td>{thea_email or 'N/A'}</td></tr>
<tr><td><b>Phone:</b></td><td>{phone}</td></tr>
</table>
<p><b>Message:</b><br>{message_body}</p>
"""
        )

        try:
            mail.send(msg)
            flash("✅ Your request has been sent successfully!", "success")
        except Exception as e:
            print("❌ Email sending failed:", e)
            flash("❌ Failed to send request. Check console for details.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html", form=form)

# ---------- SERVICE PAGES ----------
@app.route('/services/document-printing')
def document_printing():
    return render_template('services/document.html')

@app.route('/services/branding')
def branding():
    return render_template('services/branding.html')

@app.route('/services/large-format')
def large_format():
    return render_template('services/large-format.html')

@app.route('/services/invitations')
def invitations():
    return render_template('services/invitations.html')

@app.route('/services/promotional')
def promotional():
    return render_template('services/promotional.html')

@app.route('/services/books')
def books():
    return render_template('services/books.html')

@app.route('/services/photo-printing')
def photo_printing():
    return render_template('services/photo.html')

@app.route('/services/packaging')
def packaging():
    return render_template('services/packaging.html')

# ---------- TEST EMAIL ----------
@app.route("/test-email")
def test_email():
    sender_email = app.config['MAIL_USERNAME']
    try:
        msg = Message(
            "Test Email from Flask",
            sender=sender_email,
            recipients=[sender_email],
            body="This is a test email to verify your Gmail app password."
        )
        mail.send(msg)
        return "✅ Test email sent successfully! Check your inbox."
    except Exception as e:
        print("❌ Test email failed:", e)
        return f"❌ Test email failed. See console for details."

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)