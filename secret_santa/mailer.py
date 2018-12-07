import smtplib
from time import sleep
from email.mime.text import MIMEText as emailtext


def send_mails(assignment, emails, private_data, for_real=False):
    gmail_user = private_data['gmail_user']
    google_app_code = private_data['google_app_code']
    wishlist_link = private_data['wishlist_link']

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, google_app_code)
    except:
        print('email fail')
        return

    for giver, receiver in assignment:
        send_from = gmail_user
        send_to = emails[giver]
        body = f'''Ho, ho, ho, {giver}! Your Secret Santa assignment is {receiver}.

Please list your wishes for your assigned giver here:
{wishlist_link}

Merry Christmas!
Santa

P.S. Don't respond to this email - Peter will see your assignment if you do. 
'''
        msg = emailtext(body)
        msg['Subject'] = 'Secret Santa assignment'
        msg['From'] = send_from
        msg['To'] = send_to
        if for_real:
            print('sending!')
            server.sendmail(send_from, send_to, msg.as_string())
        else:
            print(msg.as_string())
        sleep(1)

    server.close()
