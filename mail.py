import smtplib
from email.mime.text import MIMEText
from email.utils import make_msgid
from configs import SMTP_USER, ALERT_RECIPIENTS, SMTP_PASS, SMTP_SERVER, SMTP_PORT, DEFAULT_SUBJECT

def send_mail(body, subject=DEFAULT_SUBJECT, debug_level=True):
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) #port 465 or 587
    server.set_debuglevel(debug_level)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASS)
    
    for to_addr in ALERT_RECIPIENTS:
    
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = to_addr
        msg['Message-ID'] = make_msgid()
        server.sendmail(SMTP_USER,[to_addr],msg.as_string())
    
    server.close()

send_mail('testing')
