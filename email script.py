import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "projectminor705@gmail.com"
APP_PASSWORD = "minorproject@123"
recipient_email = "div.awasthi01@gmail.com"
content = "henlo"
subject = "Attendance List"
excel_file = r'C:\Users\apollo\PycharmProjects\Attendance using face recognition\Attendance.csv'
def send_mail_with_excel():
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(content)

    with open(excel_file, 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=excel_file)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        #smtp.login(SENDER_EMAIL, APP_PASSWORD)
        #smtp.send_message(msg)
        smtp.ehlo()
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.ehlo()
        smtp.send_message(msg)
        smtp.ehlo()
        smtp.quit()

send_mail_with_excel()