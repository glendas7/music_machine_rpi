from ADCDevice import *
import firebase_setup
from firebase_admin import firestore
from gpiozero import TonalBuzzer, LED
from gpiozero.tones import Tone
from signal import pause
from time import sleep
import constant

potA = ADCDevice()
potA = ADS7830()    
notes = ["G4", "G#4", "A4","A#4","C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5"]
frequencies = [392, 415, 440, 466, 523, 554, 587, 622, 659, 698, 740, 783, 831, 880]
powerLed = LED(21)
t = TonalBuzzer(13)
power = True
valueA = 0
button = "off"

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_freq_data_ref = collection.document(constant.FREQ_DATA)
doc_note_data_ref = collection.document(constant.NOTE_DATA)
doc_led_data_ref = collection.document(constant.LED_DATA)
doc_button_data_ref = collection.document(constant.BUTTON_DATA)

doc_note_data_ref.update({u'note':"off"})
doc_freq_data_ref.update({u'frequency': "off"})
doc_led_data_ref.update({u'potOff': True})
doc_button_data_ref.update({u'powerButton': "off"})

powerLed.on()

def end():
    potA.close()

def checkNote(myNote):
    for note, freq in zip(notes, frequencies):
        if myNote == note:
            doc_freq_data_ref.update({u'frequency': freq})
            t.play(myNote)

def on_notedoc_snapshot(doc_snapshot):
    for doc in doc_snapshot:
        note_name = doc.to_dict()["note"]
        if note_name != "off":
            checkNote(note_name)
            
def on_leddoc_snapshot(doc_snapshot):
    for doc in doc_snapshot:
        led = doc.to_dict()["potOff"]
        global power
        if led == True:
            power = False
            powerLed.off()
        else:
            power = True
            powerLed.on()

def on_buttondoc_snapshot(doc_snapshot):
    for doc in doc_snapshot:
        global button
        button = doc.to_dict()["powerButton"]
            
doc_note_ref = collection.document(constant.NOTE_DATA)
doc_note_watch = doc_note_ref.on_snapshot(on_notedoc_snapshot)
doc_led_ref = collection.document(constant.LED_DATA)
doc_led_watch = doc_led_ref.on_snapshot(on_leddoc_snapshot)
doc_button_ref = collection.document(constant.BUTTON_DATA)
doc_button_watch = doc_button_ref.on_snapshot(on_buttondoc_snapshot)

print ('Program is starting ... ')
while True:
    valueA = potA.analogRead(0) + 500
    voltageA = valueA / 255.0 * 3.3 
    if button == "on":
        try:
            if power == True:
                t.play(Tone(valueA))
                doc_freq_data_ref.update({u'frequency': valueA})
                potFreq = valueA
        except KeyboardInterrupt:
            t.stop
            powerLed.off()
            end()
            pause()
        except:
            print("None")
    else:
        t.stop()
