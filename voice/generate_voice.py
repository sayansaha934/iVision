from gtts import gTTS
from googletrans import Translator
import os
import playsound

def generate_voice(text, to_lang='en', filename='voice.mp3'):
    translator = Translator()
    text = translator.translate(text, src='en', dest=to_lang).text
    speak = gTTS(text=text, lang=to_lang, slow=True)
    speak.save(filename)
    playsound.playsound(filename)
    os.remove(filename)