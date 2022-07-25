from urllib import request
import numpy as np
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import re
# import fitz
import selenium.webdriver as webdriver


from tkinter import *

from tika import parser

import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer

import streamlit as st

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

def error_recognize():
    text = ("I did not understand you!, Please try again")
    text_speech(Tokenizer(text))


def text_speech(txt):
    speaker = tts.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[0].id)
    speaker.setProperty('rate', 180)
    speaker.say(txt)
    speaker.runAndWait()


def text_speech_pdf(doc):
    speaker = tts.init()
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[0].id)
    speaker.setProperty('rate', 180)
    raw = parser.from_file(doc)
    speaker.say(raw['content'])
    speaker.runAndWait()

def removeDuplicateWords(tok):
    i = 0
    # parser = GingerIt()
    tok2 = tok
    tok3 = tok2
    for i in range(len(tok)-1):
        if tok[i] != tok2[i+1]:
            tok3[i] = tok[i]
            tok3[i+1] = tok2[i+1]
        elif tok[i] == tok2[i+1]:
            tok3[i] = tok[i]
            tok3[i+1] = " "
    fixedd = tok3
    return fixedd


def removeDuplicatePhrase(txt):
    text = re.sub(r'((\b\w+\b.{1,2}\w+\b)+).+\1', r'\1', txt, flags=re.I)
    return text


def Tokenizer(txt):

    tokens = nltk.word_tokenize(txt)
    i = 0
    for i, val in enumerate(tokens):
        if tokens[i] == "You":
            if tokens[i + 1] == "ve":
                tokens[i] = "You"
                tokens[i + 1] = "have"
        if tokens[i] == "I":
            if tokens[i + 1] == "ve":
                tokens[i] = "I"
                tokens[i + 1] = "have"
        if tokens[i] == "wasn":
            if tokens[i + 1] == "t":
                tokens[i] = "was"
                tokens[i + 1] = "not"
        if tokens[i] == "they":
            if tokens[i + 1] == "re":
                tokens[i] = "they"
                tokens[i + 1] = "are"
        if tokens[i] == "I":
            if tokens[i + 1] == "m":
                tokens[i] = "I"
                tokens[i + 1] = "am"
        if tokens[i] == "wil":
            tokens[i] = "will"
        if tokens[i] == "bby":
            tokens[i] = "baby"
        if tokens[i] == "ar":
            tokens[i] = "are"
        if tokens[i] == "cn":
            tokens[i] = "can"
        if tokens[i] == "grl":
            tokens[i] = "girl"
        if tokens[i] == "rd":
            tokens[i] = "road"
        if tokens[i] == "st":
            tokens[i] = "street"
        if tokens[i] == "ty":
            tokens[i] = "thank you"
        if tokens[i] == "minuets":
            tokens[i] = "minutes"
        if tokens[i] == "thi":
            tokens[i] = "this"
        if tokens[i] == "yu":
            tokens[i] = "you"
        if tokens[i] == "ws":
            tokens[i] = "was"
        if tokens[i] == "t":
            tokens[i] = "to"
        if tokens[i] == "th":
            tokens[i] = "the"
        if tokens[i] == "yte":
            tokens[i] = "yet"
        if tokens[i] == "nce":
            tokens[i] = "nice"
        if tokens[i] == "corect":
            tokens[i] = "correct"
        if tokens[i] == "atm":
            tokens[i] = "at the moment"
        if tokens[i] == "aka":
            tokens[i] = "also known as"
        if tokens[i] == "btw":
            tokens[i] = "by the way"
        if tokens[i] == "asap":
            tokens[i] = "as soon as possible"

    tokfix = removeDuplicateWords(tokens)
    output = TreebankWordDetokenizer().detokenize(tokfix)
    result = removeDuplicatePhrase(output)
    
    return result;

def quit():

    text = ("Alright, thank you for using the chatbot service. Have a nice day!")
    text_speech(Tokenizer(text))
    sys.exit(0)


mappings = {
    "exit": quit
}

bot_assist = GenericAssistant('intents.json', mappings)
bot_assist.train_model()

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    def chat(self):

        text = "Hello how may i help you today?"
        text_speech(Tokenizer(text))

        recognizer = speech_recognition.Recognizer()

        while True:

            try:

                with speech_recognition.Microphone() as mic:

                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    message = recognizer.recognize_google(audio)

                text_speech(Tokenizer(bot_assist.request(message)))

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                error_recognize()

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [MainWindow(name="mm"), SecondWindow(name="sw")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "mm"

class botChatbot(App):
    def build(self):
        return sm

if __name__ == "__main__":
    botChatbot().run()