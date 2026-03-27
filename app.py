from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Optional
import os

# -------------------------
# APP SETUP
# -------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

# -------------------------
# CONTACT FORM
# -------------------------
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    thea_email = EmailField("Thea's Email (optional)", validators=[Optional(), Email()])
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

# ---------- CONTACT ----------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        thea_email = form.thea_email.data
        phone = form.phone.data
        message_body = form.message.data

        # Log submission instead of sending email
        print("\n===== NEW CONTACT FORM SUBMISSION =====")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Thea's Email: {thea_email if thea_email else 'N/A'}")
        print(f"Phone: {phone}")
        print(f"Message: {message_body}")
        print("======================================\n")

        flash("✅ Your request has been received!", "success")
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

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)