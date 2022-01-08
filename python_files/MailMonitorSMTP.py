"""
MailMonitorSMTP.py

Connects to AWDGISPlans using SMTP.
The script then waits for a new message to come in.
When that happens, the script  prints a message to the screen
"""

# imports
import imaplib
import sys
import time
from socket import error
from sys import stderr

# make a var so that the stdout can be set back to its normal state
org_stdout = sys.stdout


def mail_login(email_user):
    email_pass = input('Password: ')
    try:
        mail.login(email_user, email_pass)
    except ConnectionResetError:
        stderr.write(str(sys.exc_info()[1]))
        print(sys.exc_info()[1])


def NewEmailWatcher():
    global mail
    global data
    global id_list

    # connect to outlook's imap server on port 993 and print its welcome screen
    try:
        """Server name: outlook.office365.com Port: 993 Encryption method: SSL"""
        mail = imaplib.IMAP4_SSL(host='outlook.office365.com', port=993)  # ("imap.gmail.com", 993)
        print(mail.welcome)
    except error:  # socket.error
        # FIXME: make this log to stderr fileoutput correctly - moving all logging to its own .py file might work best?
        #  Moving the logging to a new file should just be a matter of repointing stderr to logging.whateverfunction()
        #  and moving functions to a new .py file?
        print('Connection could not be made due to \'' + str(sys.exc_info()[1]) + '\', please try again later')
        sys.stderr.write(str(sys.exc_info()))
        e = True
        return e

    # set email, ask for password, login and select inbox
    email_user = 'amcsparron@albanyny.gov\\AWDGISPlans'  # raw_input('Email: ')
    print('Account: ' + email_user)
    # mail_login is my function
    mail_login(email_user)
    # these are two attributes of the imported mail module
    mail.list()
    # mail.select(mailbox='inbox')

    latest_email_uid = ''

    while True:
        mail.select("Inbox", readonly=True)
        result, data = mail.uid("Search", None, "ALL")  # search and return uids instead
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        print("Monitoring email for new messages...")
        if data[0].split()[-1] == latest_email_uid:
            time.sleep(120)  # put your value here, be sure that this value is sufficient ( see @tripleee comment below)
        else:
            result, data = mail.uid('search', latest_email_uid, "ALL")
                                    #'(RFC822)')  # fetch the email headers and body (RFC822) for the given ID
            raw_email = data[0][1]
            latest_email_uid == data[0].split()[-1]
            print("New Email Received!! ")
            time.sleep(120)  # put your value here, be sure that this value is sufficient ( see @tripleee comment below)

