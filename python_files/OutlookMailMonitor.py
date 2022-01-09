#! python3
"""
OutlookMailMonitor.py

**** this isn't needed for this project anymore but it might be useful for other projects ***

Classes/functions to do the heavy lifting of waiting for new mail in AWDGISPlans.

**** this isn't needed for this project anymore but it might be useful for other projects ***
"""

# imports
import ctypes  # for the VM_QUIT to stop PumpMessage()
import threading
import time

import pythoncom
import win32com.client
import sys

# outlook config
SHARED_MAILBOX = "AWDGISPlans"

# get the outlook instance and inbox folder
session = win32com.client.Dispatch("Outlook.Application").Session
user = session.CreateRecipient(SHARED_MAILBOX)
shared_inbox = session.GetSharedDefaultFolder(user, 6).Items  # 6 is Inbox


class HandlerClass(object):
    def OnItemAdd(self, item):
        print("New item added in shared mailbox")
        if item.Class == 43:
            print("The item is an email!")


class WatcherThread(threading.Thread):
    def run(self):
        print("Starting up Outlook watcher\n"
              "To terminate the program, press 'Ctrl + C'")
        # sends all messages from the waiting thread?
        pythoncom.PumpMessages()


def MailMonMain():
    win32com.client.DispatchWithEvents(shared_inbox, HandlerClass)
    WatcherThread(daemon=True).start()


def RunMailMon():
    status = MailMonMain()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Terminating program..")
            ctypes.windll.user32.PostQuitMessage(0)
            sys.exit(status)


if __name__ == "__main__":
    RunMailMon()
