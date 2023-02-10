import random

import kivy
from kivy.app import App
from kivy.properties import ( StringProperty, ObjectProperty )
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread

import speech_recognition as sr
from words import WORDS

class SpeechRecognitionControlPopUp(Popup):

    yesBtnText = StringProperty()
    tryAgainBtnText = StringProperty()
    labelText = StringProperty()

    def __init__(self, **kwargs):
        super(SpeechRecognitionControlPopUp, self).__init__(**kwargs)

        self.yesBtnText = "DA"
        self.tryAgainBtnText = "MAI INCEARCA O DATA"

    def fire_popup(self):
        self.open()

    def hidePopUpButtons(self):
        self.ids.yesBtn.opacity = 0
        self.ids.tryAgainBtn.opacity = 0

    def showPopUpButtons(self):
        self.ids.yesBtn.opacity = 1
        self.ids.tryAgainBtn.opacity = 1

    def showTryAgainBtnButton(self):
        self.ids.tryAgainBtn.opacity = 1

    def change_text(self, text):
        self.labelText = text

class MyRoot(BoxLayout):

    ERRORS = StringProperty()
    HANGMAN_IMG = StringProperty()
    GAME_MSG = StringProperty()
    WORD_DISPLAY = StringProperty()
    pickedLetter = StringProperty()
    popUp = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)

        self.popUp = SpeechRecognitionControlPopUp()
        self.popUp.ids.yesBtn.bind(on_release=self.checkChosenLetter)
        self.popUp.ids.tryAgainBtn.bind(on_release=self.listen)

        self.RANDOM_WORD = ""
        self.GUESSES = []

        self.start_game()
 
    def getAudio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        self.audio = audio
        
        try:
            letter = r.recognize_google(audio, language = 'en-US') 
            return letter.upper()
        except sr.UnknownValueError:
            print("Eroare Google Speech Recognition")
        except sr.RequestError as e:
            print("Erori serviciu Google Speech Recognition; {0}".format(e))

    def getLetter(self):
            letter = self.getAudio()
            if letter != None:
                if len(letter) > 1:
                    self.popUp.change_text("Am auzit mai multe litere")
                    self.popUp.showTryAgainBtnButton()
                else:
                    self.popUp.change_text("Ai rostit litera " + letter + " ?")
                    self.pickedLetter = letter
                    self.validatePlayerChoice()

    def listen(self, instance=0):
        
        if( not self.popUp._is_open ):
            self.popUp.fire_popup()

        self.popUp.hidePopUpButtons()
        self.popUp.change_text("Rosteste o litera")
        Clock.schedule_once(lambda d: self.getLetter(), 0)

    def validatePlayerChoice(self):
        self.popUp.showPopUpButtons()

    def checkChosenLetter(self, instance):
        self.popUp.dismiss()

        letter =  self.pickedLetter
        self.GUESSES.append(letter)

        if letter in self.RANDOM_WORD :

            self.update_word_display()

            if self.won:
                self.ids.speechBtn.opacity = 0
                self.GAME_MSG = "Ai castigat!!"
        else:

            self.ERRORS = str(int(self.ERRORS) + 1)

            self.HANGMAN_IMG = "images/hangman" + self.ERRORS + ".png"

            if int(self.ERRORS) == 1:
                self.GAME_MSG = "Ai pierdut!!"
                self.ids.speechBtn.opacity = 0
                self.WORD_DISPLAY = self.RANDOM_WORD

    def update_word_display(self):
        WORD_DISPLAY = []
        for alphabet in self.RANDOM_WORD:
            if alphabet in self.GUESSES:
                WORD_DISPLAY.append(alphabet)
            else:
                WORD_DISPLAY.append("_")

        self.WORD_DISPLAY = " ".join(WORD_DISPLAY)

    @property
    def won(self):
        return all(alphabet in self.GUESSES for alphabet in self.RANDOM_WORD)

    def start_game(self):

        self.RANDOM_WORD = random.choice(WORDS)

        print(self.RANDOM_WORD)

        self.GUESSES.clear()

        self.ERRORS = "0"

        self.HANGMAN_IMG = "images/hangman0.png"

        self.GAME_MSG = "Ghiceste cuvantul"

        self.WORD_DISPLAY = " ".join(["_" for _ in self.RANDOM_WORD])
        self.ids.speechBtn.opacity = 1


class Hangman(App):

    def build(self):
        return MyRoot()

hangman = Hangman()
hangman.run()
