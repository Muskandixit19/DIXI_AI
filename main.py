import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
from config import apikey
import random
import numpy as np


chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = "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"
    chatStr += f"User: {query}\n Dixi: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    os.system(f'PowerShell -Command "Add-Type -TypeDefinition $type -Language CSharp; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Dixi"


if __name__ == '__main__':
    print('Welcome to Dixi A.I')
    say("Dixi A.I")
    say("Welcome to Dixi A.I. How can I assist you today?")
    while True:
        print("Listening...")
        query = takeCommand()

        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["whatsapp", "https://web.whatsapp.com"],
                 ["instagram", "https://www.instagram.com"],
                 ["facebook", "https://www.facebook.com"],
                 ["twitter", "https://www.twitter.com"],
                 ["linkedin", "https://www.linkedin.com"],
                 ["snapchat", "https://www.snapchat.com"]
                 ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            musicPath = "C:/Users/dixit/Downloads/DIXI/music.mp3"
            os.startfile(musicPath)

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} o'clock {min} minutes")

        elif "open video".lower() in query.lower():
            videoPath = "C:/Users/dixit/Downloads/DIXI/video.mp4"
            os.startfile(videoPath)

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Dixi Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
