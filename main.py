import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()  # recoginises our voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')


# engine.setProperty('voice',voices[1].id) #0 th index for male voice and 1 for female voice

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_commad():
    try:
        with sr.Microphone() as source:
            print('listening.....')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                # print(command)
    except:
        pass
    return command


def run_jarvis():
    command = take_commad()
    # print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I %M %p')
        talk('current time is' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'Are you single' in command:
        talk('I am in a relationship with internet')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk('Please say the command again')


run_jarvis()