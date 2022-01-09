"""
MailMonitorSMTP.py

Connects to AWDGISPlans using SMTP.
The script then waits for a new message to come in.
When that happens, the script  prints a message to the screen.

based on https://stackoverflow.com/questions/49086465/python-keep-checking-new-email-and-alert-of-further-new-emails

"""

# imports
import imaplib
import sys
import time
from socket import error
from sys import stderr

# globals
# make a var so that the stdout can be set back to its normal state
org_stdout = sys.stdout


# TODO: needs to be turned into a class, and have its error handling updated
def mail_login(email_user):
    """ logs into an IMAP4 email server."""
    email_pass = input('Password: ')
    try:
        mail.login(email_user, email_pass)
    except ConnectionResetError:
        stderr.write(str(sys.exc_info()[1]))
        print(sys.exc_info()[1])


def NewEmailWatcher():
    """ Watches an email inbox for new messages. """
    global mail
    global data
    global id_list

    # connect to outlook's imap server on port 993 and print its welcome screen
    try:
        """Server name: outlook.office365.com Port: 993 Encryption method: SSL"""
        mail = imaplib.IMAP4_SSL(host='outlook.office365.com', port=993)  # ("imap.gmail.com", 993)
        print(mail.welcome)
    except error:  # socket.error
        print('Connection could not be made due to \'' + str(sys.exc_info()[1]) + '\', please try again later')
        sys.stderr.write(str(sys.exc_info()))
        e = True
        return e

    # set email, ask for password, login and select inbox
    email_user = 'amcsparron@albanyny.gov\\AWDGISPlans'  # raw_input('Email: ')
    print('Account: ' + email_user)

    # mail_login is my function
    mail_login(email_user)

    mail.list()

    latest_email_uid = None

    print("Monitoring email for new messages...")

    while True:
        mail.select("Inbox", readonly=True)

        result, data = mail.uid("Search", latest_email_uid, "ALL")  # search and return uids

        """ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string"""

        if data[0].split()[-1].decode("utf-8") == latest_email_uid:
            print(latest_email_uid)
            time.sleep(120)  # put your value here, be sure that this value is sufficient ( see @tripleee comment below)
        else:
            print(latest_email_uid)
            result, data = mail.uid('Search', latest_email_uid, "ALL")
            """
            "ALL" can be replaced with '(RFC822)')  
            in order to fetch the email headers and body (RFC822) for the given ID
            """

            #raw_email = data[0][1]

            latest_email_uid = data[0].split()[-1].decode("utf-8")
            print("New Email Received!! - uid is {} type is {}".format(latest_email_uid, type(latest_email_uid)))

            time.sleep(120)  # put your value here, be sure that this value is sufficient ( see @tripleee comment below)

NewEmailWatcher()
