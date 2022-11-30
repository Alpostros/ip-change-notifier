# Reference: https://realpython.com/python-send-email/

import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def prep_mail(ip_address, profile_name, profile_password):
  smtp_server = "smtp.gmail.com"
  port = 587
  sender_email = "sender-mail@example.com"
  receiver_email = "receiver-mail@example.com"
  password = "enter your app password here"
  subject = "Your Public IP Address Has Been Changed!"
  
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject
  html = """\
  <html>
    <body>
      <p>Dear Master,<br>
        As your slave, I would like to notify to you that your public IP address has been changed by your ISP.<br>
        You can find your freshly configured OpenVPN profile in attachments. <br>
      </p>
    </body>
  </html>
  """
  text = "Your new IP address is: "+ str(ip_address) + ". Your profile password is: " +profile_password

  filename = "/home/pi/ovpns/"+profile_name+".ovpn"
  with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
  
  encoders.encode_base64(part)
  part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)
  part1 = MIMEText(html, "html")
  part2 = MIMEText(text, "plain")

  message.attach(part1)
  message.attach(part2)
  message.attach(part)

  send_mail(smtp_server,port, sender_email, password, receiver_email, message)

def send_mail(smtp_server,port, sender_email, password, receiver_email, message):
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        print("Mail sent")
    except Exception as e:
        print("Connection not established.")
    finally:
        server.quit()

