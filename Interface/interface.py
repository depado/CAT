from pygame.locals import *
import speech_recognition as sr
import pyttsx as tts
import random
import urllib
import pygame
import pickle
import time
import re
import os


class SpeechRecognition:
    def __init__(self, language="en-US", name=""):
        self.engine = tts.init()
        self.language = language
        self.recognizer = sr.Recognizer(language)
        self.recognizer.pause_threshold = 0.5
        self.recognizer.energy_threshold = 2500
        self.name = name

    def you_talk_to_me(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            work = self.recognizer.recognize(audio)
            if work == self.name:
                return self.recognize()
            return ""
        except LookupError:
            return ""

    def recognize(self):
        self.engine.say('Yes Sir ?')
        self.engine.runAndWait()
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, timeout=5)
        try:
            work = self.recognizer.recognize(audio)
            return work
        except LookupError:
            return "Error"


class ThinkingArray:
    def __init__(self):
        self.array = {}
        self.polite_words = ['please', 'could you', 'can you']
        self.polite_answers = ['Sur I can Sir', 'Yes of course Sir']
        self.salutations_words = ['hello', 'hi', 'good morning']
        self.salutations_answers = ['Hi Sir', 'Hello Sir', 'Good morning Sir']
        self.emotion = "."
        self.engine = tts.init()

    def recognize_commands(self, texte):
        work = ""
        texte = texte.lower()
        no_salutation = True
        for i in self.salutations_words:
            if i in texte:
                no_salutation = False
        if not no_salutation:
            work += random.choice(self.salutations_answers) + self.emotion + " "
        no_politess = True
        for j in self.polite_words:
            if j in texte:
                no_politess = False
        if not no_politess:
            work += random.choice(self.polite_answers) + self.emotion
        return work

    def execute(self, texte):
        analysis_txt = self.recognize_commands(texte)
        if not analysis_txt:
            self.engine.say("Error")
            self.engine.runAndWait()
            return "Error"
        self.engine.say(analysis_txt)
        self.engine.runAndWait()
        return analysis_txt

    def load(self, datas):
        self.array = datas

    def save(self):
        return self.array


class Interface:
    def __init__(self):
        self.name = "name"
        self.version = "0.0.1-a"
        self.thinking_array = ThinkingArray()
        self.recognizer = SpeechRecognition(name=self.name)
        self.save_file = "test."
        self.location = os.path.dirname(os.path.abspath(__file__)) + "\\"
        self.i = "IN  : "
        self.o = "OUT : "
        self.continuer = 1
        self.load()

    def start(self):
        print("Starting " + self.name + " v" + self.version + " ...")
        while self.continuer:
            print(self.i, end=' ', flush=True)
            inputusr = self.recognizer.you_talk_to_me()
            print(inputusr, flush=True)
            if inputusr != "":
                print(self.o, end=' ', flush=True)
                print(self.thinking_array.execute(inputusr), flush=True)
        self.save()

    def visualise_core(self):
        screen = pygame.display.set_mode((640, 480))
        continuer = 1
        while continuer:
            for e in pygame.event.get():
                if e.type == QUIT:
                    continuer = 0
            pygame.display.flip()

    def load(self):
        if os.path.exists(self.location + self.save_file):
            with open(self.location + self.save_file, "rb") as saved_rb:
                self.thinking_array.load(pickle.Unpickler(saved_rb).load())

    def save(self):
        with open(self.location + self.save_file, "wb") as saved_wb:
            pickle.Pickler(saved_wb).dump(self.thinking_array.save())