import subprocess

#_voices = {"en":"British", "en-us":"American", "en-sc":"Scottish", "rp":"en-rp", "en-n":"Northern", "en-wm":"West Midlands", "en-wi":"West Indies"}
#_variations = {"m1":"Male1", "m2":"Male2", "m3":"Male3", "m4":"Male4", "m5":"Male5", "m6":"Male6", "m7":"Male7", "f1":"Female1", "f2":"Female2", "f3":"Female3", "f4":"Female4", "croak":"Croak", "whisper":"Whisper"}
_voices = ("en", "en-us", "en-sc", "rp", "en-n", "en-wm", "en-wi")
_variations = ("m1", "m2", "m3", "m4", "m5", "m6", "m7", "f1", "f2", "f3", "f4", "croak", "whisper")
_params_volume = {"default":150, "min":0, "max":200, "units":""}
_params_speed = {"default":175, "min":80, "max":450, "units":"words per minute"}
_params_pitch = {"default":50, "min":0, "max":99, "units":""}
_params_wordGap = {"default":0, "min":0, "max":99, "units":""}
_params_capStress = {"default":0, "min":0, "max":9999, "units":""}

devnull = open('/dev/null', 'w')

def say(phrase="Hi, I'm PieBot!",volume=_params_volume["default"],voice=0,variation=0,speed=_params_speed["default"],pitch=_params_pitch["default"],capStress=_params_capStress["default"],wordGap=_params_wordGap["default"],saveFile=None):
    """Use a text-to-speech engine to say phrases."""
    pLang = "-v" + _voices[voice] + "+" + _variations[variation]
    pGap = "-g" + str(wordGap)
    pSpeed = "-s" + str(speed)
    pPitch = "-p" + str(pitch)
    pCapStress = "-k" + str(capStress)
    subprocess.Popen(['espeak', pLang, pGap, pSpeed, pPitch, pCapStress, phrase], stdout=devnull, stderr=devnull)
    if saveFile:
        pFile = "-w" + saveFile
        subprocess.Popen(['espeak', pLang, pGap, pSpeed, pPitch, pCapStress, pFile, phrase], stdout=devnull, stderr=devnull)
        # strippedName = "".join([c for c in saveFile if c.isalpha() or c.isdigit()]).rstrip()
        # sFile = strippedName + lang + gap + spd + ".wav"
        # pFile = "-w" + sFile
        # print("---Saving file as: " + sFile)
        # subprocess.Popen(['espeak', lang, gap, spd, pFile, sText]).stdout

def play(audioFile=None):
    """Play an audio file."""
    print audioFile
    subprocess.Popen(['aplay', audioFile], stdout=subprocess.PIPE)
