import smtplib

from email.mime.text import MIMEText


def send_email(

    recipient,

    subject,

    message

):

    sender_email = "your_email@gmail.com"

    app_password = "your_app_password"

    msg = MIMEText(message)

    msg["Subject"] = subject

    msg["From"] = sender_email

    msg["To"] = recipient

    with smtplib.SMTP_SSL(

        "smtp.gmail.com",

        465

    ) as smtp:

        smtp.login(

            sender_email,

            app_password

        )

        smtp.sendmail(

            sender_email,

            recipient,

            msg.as_string()

        )
