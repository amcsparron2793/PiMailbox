#! python3
"""
MailMonitorSMTP.py

Connects to AWDGISPlans using SMTP.
The script then waits for a new message to come in.
When that happens, the script  prints a message to the screen.

based on https://stackoverflow.com/questions/49086465/python-keep-checking-new-email-and-alert-of-further-new-emails

"""

# imports
import imaplib
# best cross platform way to check OS
from platform import system as p_system
import sys
import time
from socket import error
from sys import stderr

# if this is running on a windows system, use questionary, otherwise use getpass.
# this was changed from an environ["OS"] check for better compatibility with Linux.
if "windows" in p_system().lower():
    import questionary
else:
    try:
        import getpass
    except ImportError:
        print("getpass could not be imported, defaulting to basic text prompt.")
        pass

from MechClassesPi import Mechanics
# globals
# make a var so that the stdout can be set back to its normal state
org_stdout = sys.stdout

# instance of the Mechanics class to control servos etc
Mech = Mechanics(servo_pin=22,
                 pwr_led_pin=16,
                 mail_led_pin=20,
                 reset_button_pin=12,
                 fault_LED_pin=6)


# TODO: needs to be turned into a class
def mail_login(email_user):
    """ logs into an IMAP4 email server."""
    try:
        if "questionary" in sys.modules:
            email_pass = questionary.password('Password: ').ask()
        elif ("questionary" not in sys.modules
              and "getpass" in sys.modules):
            # noinspection PyUnresolvedReferences
            email_pass = getpass.unix_getpass()
        else:
            email_pass = input("password: ")
    except KeyboardInterrupt as e:
        Mech.FullErrHandle(e)
        print("\nGoodbye!!")
        exit()
    except Exception as e:
        Mech.FullErrHandle(e)

    try:
        mail.login(email_user, email_pass)
    except ConnectionResetError as e:
        Mech.FullErrHandle(e)
        exit(1)


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
    except error as e:  # socket.error
        Mech.FullErrHandle(e)
        print('Connection could not be made due to \'' + str(sys.exc_info()[1]) + '\', please try again later')
        sys.stderr.write(str(sys.exc_info()))
        return e

    # set email, ask for password, login and select inbox
    email_user = 'amcsparron@albanyny.gov\\AWDGISPlans'  # raw_input('Email: ')
    print('Account: ' + email_user)

    # mail_login is my function
    mail_login(email_user)

    mail.list()
    log_file_path = "./MailMonitorLog.log"
    latest_email_uid = None
    # used a random string to declare olddata
    # and assure that it doesn't initially match any uid
    olddata = "olddata"

    print("Monitoring email for new messages...")
    firstrun = True

    while True:
        #sys.stdout = open(log_file_path, "w")
        mail.select("Inbox", readonly=True)

        # this is set to no filter so that all UIDs will be returned, they're parsed out from there.
        result, data = mail.uid("Search", None, "ALL")  # search and return uids

        print("Running Email Check on {}.\nMost up to date UID before check is {}".format(time.strftime("%x at %X"),
                                                                                          latest_email_uid))
        # TODO: add in param for from field
        if latest_email_uid is not None:
            print(mail.fetch(latest_email_uid, "(BODY[HEADER.FIELDS (FROM)])"))
        # this isn't used so that an index error cant be thrown if data comes back blank.
        # latest_email_uid = data[0].split()[-1].decode("utf-8")

        # only print the result and raw data if it has changed.
        if (data[0].decode("utf-8") != ""
                and data[0].split()[-1].decode("utf-8") != latest_email_uid
                and not firstrun):
            print("possible new email detected...")
            print(result, data, type(data))

        try:
            if (data[0].split()[-1].decode("utf-8") == latest_email_uid
                    or data[0].split()[-1].decode("utf-8") == olddata[0]):
                print("no new email")

                firstrun = False
                time.sleep(120)  # time to sleep between checks 120 secs is the soft minimum
            else:
                latest_email_uid = data[0].split()[-1].decode("utf-8")
                if latest_email_uid != olddata[0] and not firstrun:
                    # TODO: add in param for from field
                    print(mail.fetch(latest_email_uid, "(BODY[HEADER.FIELDS (FROM)])"))
                    # Mech.YouGotMail() turns on the mail led and raises the servo to max.
                    Mech.YouGotMail()

                    print("New Email Received!! - uid is {}".format(latest_email_uid))
                    olddata = [bytes(latest_email_uid, "utf-8")]
                else:
                    print("no new email")
                    pass

                firstrun = False
                time.sleep(120)  # time to sleep between checks 120 secs is the soft minimum

        except IndexError as e:
            firstrun = False
            print("no new email")
            time.sleep(120)  # time to sleep between checks 120 secs is the soft minimum
            pass
        except UnboundLocalError as e:
            print("unbound local error")
            firstrun = False
            time.sleep(120)  # time to sleep between checks 120 secs is the soft minimum
