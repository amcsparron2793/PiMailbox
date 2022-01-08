#! python3
"""
MailMonitor.py

Classes/functions to do the heavy lifting of waiting for new mail in AWDGISPlans.
"""

# imports
import ctypes  # for the VM_QUIT to stop PumpMessage()
import pythoncom
import win32com.client
import sys


# outlook config
SHARED_MAILBOX = "Your Mailbox Name"

# get the outlook instance and inbox folder
session = win32com.client.Dispatch("Outlook.Application").Session
user = session.CreateRecipient(SHARED_MAILBOX)
shared_inbox = session.GetSharedDefaultFolder(user, 6).Items  # 6 is Inbox


class HandlerClass(object):

    def OnItemAdd(self, item):
        print("New item added in shared mailbox")
        if item.Class == 43:
            print("The item is an email!")


outlook = win32com.client.DispatchWithEvents(shared_inbox, HandlerClass)


def main():
    print("Starting up Outlook watcher")
    pythoncom.PumpMessages()


if __name__ == "__main__":
    try:
        status = main()
        sys.exit(status)
    except KeyboardInterrupt:
        print("Terminating program..")
        ctypes.windll.user32.PostQuitMessage(0)
        sys.exit()
