import speech_recognition as sr
import pyttsx3
import pywhatkit

name = "yarvis"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Digame mi señor")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')    
    except:
        pass
    return rec

def run_yarvis():
    rec = listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        print("Reproduciendo" +music)
        talk("Reproduciendo" +music)
        pywhatkit.playonyt(music)

if __name__ == '__main__':
    run_yarvis()