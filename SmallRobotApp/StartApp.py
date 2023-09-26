import tkinter as tk
import os
import pyaudio
from google.cloud import texttospeech
import pygame
import glob
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import pvporcupine
import time
import speech_recognition as sr
import wave
from mutagen.mp3 import MP3
import botConnecter

class VoiceAssistant:
    def __init__(self):
        self.msg = ""
        self.screen_width = None
        self.screen_height = None
        self.counter = 1
        self.label = None
        self.wake_label = None
        self.generate_button = None
        self.executor = ThreadPoolExecutor()
        self.is_closed = False
        self.root = None
        self.response_message = ""
        self.speech_label = None
        self.lang_code = "en-US"
        self.lang_change = False

    #To reopen microphone
    def open_mic(self):
        if self.detection:
            self.generate_button.invoke()
        else:
            print("Machine is idle")
    
    #Properly close application        
    def on_close(self):
        print("Closing...")
        self.is_closed = True
        self.executor.shutdown(wait=False)
        self.root.destroy()
        print("Application closed")
        exit(0)

    
    #Check For language
    def selectLangauge(self, msg):
        x = botConnecter.checkForSwitch(msg)
        print("Language code is", x)
        #language logic to change the speech to text
        if x is not None:
            self.lang_code = x
            if self.lang_code == "en-US":
                self.response_message = "Okay I will speak in english from now on."
                #self.speech_label.config(text="Okay I will speak in english from now on.")
                
              
            elif self.lang_code == "ar-LB":
                self.response_message = " ماشي حاءحْكي معكْ بالعربي  هَلّْاأْ"
               # self.speech_label.config(text=" ماشي حاءحْكي معكْ بالعربي  هَلّْاأْ")
               
            self.lang_change = True
            self.tts()


    def wake_check(self):
        access_key = 'PbCv1dGc7/WHiJQTyfqVBeLi6OBf5w99/gQg4Fjk0zbx2zUe0VWgEQ=='
        keyword_path_arab= '/home/wot/Desktop/SmallRobotApp/مرحبا-جوني_ar_raspberry-pi_v2_2_0.ppn'
        keyword_path_eng = '/home/wot/Desktop/SmallRobotApp/hey-johnny_en_raspberry-pi_v2_2_0.ppn'
        # Spécifiez le chemin vers le modèle Porcupine en arabe (.pv)
        model_path = '/home/wot/Desktop/SmallRobotApp/porcupine_params_ar.pv'
        print("Entered wake check")
        self.detection= False
        def audio_callback(in_data, frame_count, time_info, status):
            pcm = np.frombuffer(in_data, dtype=np.int16)
            keyword_index = handle.process(pcm)
            if keyword_index >= 0:
                self.detection = True
                print("Keyword Detected!")
            
            return None, pyaudio.paContinue
        if self.lang_code == "en-US":
            print("language is english")


            handle = pvporcupine.create(keyword_paths=[keyword_path_eng], access_key=access_key)
      
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=handle.frame_length,
                stream_callback=audio_callback
            )

            audio_stream.start_stream()

            while not self.detection:
                pass

            audio_stream.stop_stream()
            audio_stream.close()

            pa.terminate()

            print("All CLEAR")
            print(self.detection)

            self.response_message = "Hey, "
            print( "Hey, " )
            self.speech_label.config(text=self.response_message)
            print("after hey")
            self.tts() 

        if self.lang_code == "ar-LB":
            print("language is arabic")
            handle = pvporcupine.create(keyword_paths=[keyword_path_arab], access_key=access_key,model_path=model_path)
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=handle.frame_length,
                stream_callback=audio_callback
            )

            audio_stream.start_stream()

            while not self.detection:
                pass
            print("after detect keyword")

            audio_stream.stop_stream()
            audio_stream.close()

            pa.terminate()

            print("All CLEAR")
            print(self.detection)

            self.lang_change = False
         
            self.response_message = "مرحبا"
            print( "مرحبا")
            self.speech_label.config(text=self.response_message)
            self.tts()
            
    
    #its simple job is to only read the words that are results
    def tts(self):
   
        print("TTS")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'text.json'
        try:        
            
            client = texttospeech.TextToSpeechClient()
            print("Client created successfully.")
        except Exception as e:
            print("Error:", str(e))
        print("TTS")
        if self.response_message is not None:

            text = '<speak>'+""+self.response_message+""+'</speak>'
            synthesis_input = texttospeech.SynthesisInput(ssml=text)
            try:
                voice = texttospeech.VoiceSelectionParams(
                    language_code=self.lang_code ,
                    ssml_gender=texttospeech.SsmlVoiceGender.MALE,
                )
                audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3,
                        )
                response = client.synthesize_speech(
                            input=synthesis_input, voice=voice, audio_config=audio_config,
                        )


                filename = 'audio.mp3'
                with open(filename, 'wb') as out:
                    out.write(response.audio_content)
                pygame.mixer.init()
                pygame.mixer.music.load('dummy.mp3')
                files = glob.glob('audio*.mp3')
                for f in files:
                    try:
                        os.remove(f)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                filename = 'audio' + str(pygame.time.get_ticks()) + '.mp3'
                with open(filename, 'wb') as out:
                    out.write(response.audio_content)
                audio = MP3(filename)
                
                print("MP3 audio length is ",audio.info.length)
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.2)  # Wait a second before checking again
            except Exception as e:
                print("Error occured ", e)
            if self.lang_change:
                self.wake_check()
            else:
                self.stt(self.speech_label)
        else:
            print('no response message availbale')
    
    def stt(self, speech_label):

        r = sr.Recognizer()
        # Open the microphone for capturing the speech
        with sr.Microphone() as source:
            print("Listening...")   
            
            # Adjust the energy threshold for silence detection
            r.energy_threshold = 4000

            # Listen for speech and convert it to text
            audio = r.listen(source)

            try:

                text = r.recognize_google(audio, language=self.lang_code)
                print("You said:", text)
                self.selectLangauge(text)
                self.response_message = botConnecter.main(text) 
                print(self.response_message)


            except sr.UnknownValueError:
                #TODO here in future time is where will we implement the sleep function that turns microphoneoff
                # when there is no one talking to him
                x = "could not understand audio please repeat and be clear"
                print(x)

                if self.counter == 1:
                     
                     if self.lang_code == "en-US":
                        self.response_message = "could not understand audio please repeat and be clear"
                     else:
                         self.response_message = "مش عم بِفْهَمْ عَلَيْك عيد"
                     self.speech_label.config(text=self.response_message) 
                     print("loop- number 1")   
                     self.counter += 1 
                     self.tts()
                     
                elif self.counter == 2:
                    print("loop number 2")
                    self.counter += 1
                    self.stt(self.speech_label)
                
                else:
                    print("loop number 3")
                    self.counter = 1
                    self.wake_check()

                



            except sr.RequestError as e:
                x="Could not request results from Google Speech Recognition service; {0}".format(e)
                print(x)
                self.open_mic()

        self.speech_label.config(text=self.response_message)
        self.tts()
    
    
    
    def run(self):
        print("start execution")
        future2=self.executor.submit(self.wake_check)

#this starts the application
    
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

