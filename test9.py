# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

SENDGRID_API_KEY = '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'
sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
from_email = Email("test@example.com")
to_email = Email("seddon-software@keme.co.uk")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
