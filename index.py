from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests



def talkToMe(audio):
    print(audio)
    tts = gTTS(text=audio,lang='en')
    tts.save('audio.mp3')
    os.system('mpg123 audio.mp3')



     #replace the mpg123 in say

def myCommand():
    "listen for command"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('you said:' + command + '\n')

        # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command

def assistance( command):
    "if statement for executing command"

    if 'open redit' in command:
        reg_ex = re.search('open reddit(.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')


    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass
    elif 'hello' in command:
        talkToMe('hi')
    elif 'how are you ' in command:
        talkToMe('good')

    elif 'what\s' in command:
        talkToMe('just doing my thing')
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"}
        )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'John' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

        #init gmail Smtp
        mail =smtplib.SMTP('smtp.gmail.com', 587)

        #identify to server
        mail.ehlo()

        #encrypt session
        mail.starttls()

        #login
        mail.login('username', 'password')

        #send message
        mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

        #end mail connection
        mail.close()

        talkToMe('Email sent.')

    else:
        talkToMe('I don\'t know what you mean!')
talkToMe('i am ready for you  command')
while True:
    assistance(myCommand())
