#!flask/bin/python

from flask import Flask
from flask import render_template, request, send_file
import subprocess
import string
#import pygame.mixer

app = Flask(__name__.split('.')[0])

print("Server started...")

@app.route("/say/", methods=['GET','POST'])
#@app.route("/say/<string:someWords>", methods=['GET','POST'])
def sayit():
    sText = None
    sFile = None
    if request.method == 'POST':
        sText = request.form['words']
        lang = "-v" + request.form['language'] + request.form['variation']
        gap = "-g" + request.form['wordgap']
        spd = "-s" + request.form['speed']
        # Get the value from the submitted form
        print "---Message is: ", sText
        subprocess.Popen(['espeak', lang, gap, spd, sText], stdout=subprocess.PIPE)
        if request.form['saveaswav']:
            strippedName = "".join([c for c in sText if c.isalpha() or c.isdigit()]).rstrip()
            sFile = strippedName + lang + gap + spd + ".wav"
            pFile = "-w" + sFile
            print("---Saving file as: " + sFile)
            subprocess.Popen(['espeak', lang, gap, spd, pFile, sText]).stdout
    return render_template('say.html', sayText=sText, wavFile=sFile)

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
    
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0',80)

