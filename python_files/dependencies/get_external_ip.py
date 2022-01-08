""" makes a get request to ipinfo.io for the external ip of the current system and returns it to stdout"""
import requests
from os import system


r = requests.get(url='http://ipinfo.io/ip')
print('Current External IP is:\n' + r.text)

system('pause')
