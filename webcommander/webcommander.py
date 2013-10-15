#!flask/bin/python

from flask import Flask
from flask import render_template, request
import subprocess
import string
#import pygame.mixer

app = Flask(__name__)

print("Here")

#@app.route("/index")
#def showit():
#    return render_template('say.html')

@app.route("/say/", methods=['GET','POST'])
#@app.route("/say/<someWords>", methods=['GET','POST'])
def sayit():
    sfile = None
    print("say IT!")
    if request.method == 'POST':
        print(request.form)
        sayText = request.form['words']
        lang = "-v" + request.form['language'] + request.form['variation']
        print("Language " + lang)
        gap = "-g" + request.form['wordgap']
        spd = "-s" + request.form['speed']
        # Get the value from the submitted form
        print "---Message is", sayText
        subprocess.Popen(['espeak', lang, gap, spd, sayText], stdout=subprocess.PIPE)
        if request.form['saveaswav']:
            strippedName = "".join([c for c in sayText if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            print("save as wav")
#            sfile = "-w 'audio/ttsout/" + strippedName + lang + gap + spd + ".wav'"
            sfile = "-w audio//something.wav"
            print sfile
            subprocess.Popen(['espeak', lang, gap, spd, sfile, sayText]).stdout
            stdOut = subprocess.Popen(['pwd'], shell=True).stdout
#            print(stdOut)
    else:
        sayText = None
        sfile = None
    return render_template('say.html', value=sayText, wavFile=sfile)

@app.route("/play/", methods=['GET','POST'])
def playit():
    fileList = None
    if request.method == 'POST':
        #initialise the mixer to 44.1khz, 16bit, 2channel with 4096 buffer
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        
        #load the sound
#        snd = pygame.mixer.Sound(request.form['audiofile'])
#        snd.set_volume(request.form['audiovolume'])
        snd = pygame.mixer.Sound('bell.wav')
        snd.set_volume(0.8)
        
        #play it
        snd.play()
        
        while pygame.mixer.get_busy():
            #wait till the sound has finished
            pass
    else:
        fileChoice = None
    return render_template('play.html', files=fileList, value=fileChoice)


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',80)

