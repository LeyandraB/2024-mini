# Fall 2024 Mini Project Assignment by Astrid Mihalopoulos and Leyandra Burke
## Exercise 1
1.  what are the "max_bright" and "min_bright" values you found?
   min_bright = 46000
   max_bright = 2000

## Exercise 2
We started with the code in exercise_sound.py as a starting point. We decided to play the Wii Theme music or the "Mii Song". We first found the frequency for the notes. That was done by finding the sheet music and using the frequency website. 

Here are the frequencies for the notes 
##
Then we added the following code to play the song. We used the already existing playtone function. 
```python
playtone(370,.4)
playtone(440,.4)
playtone(554,.5)
playtone(440,.6)
playtone(370,.4)
playtone(294,.3)
playtone(15,.05)
playtone(294,.3)
playtone(15,.05)
playtone(294,.3)


playtone(554,.5)
playtone(294,.3)
playtone(370,.4)
playtone(440,.4)
playtone(554,.5)
playtone(440,.4)
playtone(370,.4)
playtone(330,.4)
playtone(311,.4)
playtone(294,.3)
```
The first part of the function is the frequency and the other is the duration the note will play. 

## Exercise 3
We edited the exercise_game.py code to calculate minimum, maximum and average response times. The following code was added 
The following code was added 
##
Since we need 10 flashes the variavle N was changed from 3 to 10 

# Upload to the cloud 
We created a Firebase project. Then we took the following steps Project Settings -> Service Accounts -> Python -> Generate New Private Key
This JSON file contains the key that the Rasberry Pi Pico can use. 

To extract the key we used the following code. 
```python
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

#Load the service account credentials from JSON file
SERVICE_ACCOUNT_FILE = (r"C:\Users\leyan\Downloads\miniprojKey.json")

#Specify the correct scope for Firestore
SCOPES = ['https://www.googleapis.com/auth/datastore']

#Create credentials object with the Firestore scope
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#Refresh the token to get a new OAuth 2.0 access token
credentials.refresh(Request())

#Get the OAuth 2.0 token
token = credentials.token

print("OAuth 2.0 Token:", token)
```

After extracting the key we put it in the exercise_game.py
Then we connected our Pi Pico to the internet using the following code. 

```python
import time
import network

ssid="Ley"
password="Password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 100
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >=3:
        print(str(wlan.status()))
        break
    max_wait -= 1
    print('waiting for connection')
    time.sleep(1)

 #Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
```

After that we ran exercise_game.py and the results showed up on the firestore database 
