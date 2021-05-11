from flask import Flask, render_template, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json

app = Flask(__name__,
            template_folder = 'HTML',
            static_folder = 'HTML/assets')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sendmessage', methods = ['POST'])
def process_contact_message():
    with open('config.json', 'r') as file:
        config = json.loads(file.read())
        file.close()

    form_data = request.form

    sender_email = 'administrator@thecodingdev.tech'
    receiver_email = 'administrator@thecodingdev.tech'

    message = MIMEMultipart('alternative')
    message['Subject'] = 'New Customer Message'
    message['From'] = sender_email
    message['To'] = receiver_email

    body = f'<html><body><p>You received a new message from a potential customer!</p><br /><hr /><br /><p>Name: {form_data["name"]}</p><br /><p>Email: {form_data["email"]}</p><br /><p>Telephone: {form_data["telephone"]}</p><br /><p>Message: {form_data["message"]}</p><br /><hr /></body></html>'

    body_mime = MIMEText(body, 'html')
    message.attach(body_mime)

    with smtplib.SMTP(config['smtp'], 587) as server:
        server.starttls()
        server.login(receiver_email, config['password'])
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()

    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True) # ssl_context = ('SSL/certificate.crt', 'SSL/private.key'))
