import speech_recognition as sr  # recognise speech

import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

import playsound  # to play an audio file
from gtts import gTTS  # google text to speech
import random
from time import ctime  # get time details
import webbrowser  # open browser
import yfinance as yf  # to fetch financial data
import ssl
import certifi
import time
import os  # to remove created audio files


class person:
    name = ''

    def setName(self, name):
        self.name = name


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer()  # initialise a recogniser
engine = pyttsx3.init()


# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:  # microphone as source
        if ask:
            talk(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            talk('I did not get that')
        except sr.RequestError:
            talk('Sorry, the service is down')  # error: recognizer is not connected
        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()


# get string and make a audio file to be played
def talk(text):
    engine.say(text)
    engine.runAndWait()


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                     f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}",
                     f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        talk(greet)

    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            talk("my name is Alexis")
        else:
            talk("my name is Alexis. what's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        talk(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)  # remember name in person object

    # 3: greeting
    if there_exists(["how are you", "how are you doing"]):
        talk(f"I'm very well, thanks for asking {person_obj.name}")

    # 4: time
    if there_exists(["what's the time", "tell me the time", "what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        talk(time)

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        talk(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        talk(f'Here is what I found for {search_term} on youtube')

    # 7: get stock price
    if there_exists(["price of"]):
        search_term = voice_data.lower().split(" of ")[
            -1].strip()  # strip removes whitespace after/before a term in string
        stocks = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "facebook": "FB",
            "tesla": "TSLA",
            "bitcoin": "BTC-USD"
        }
        try:
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]

            talk(f'price of {search_term} is {price} {stock.info["currency"]} {person_obj.name}')
        except:
            talk('oops, something went wrong')
    if there_exists(["exit", "quit", "goodbye"]):
        talk("going offline")
        exit()


time.sleep(1)

person_obj = person()
while (1):
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond

