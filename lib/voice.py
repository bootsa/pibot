import subprocess

class voice(object):
    """Make pibot speak and play audio."""
                
    def __init__(self):
        """Initialise text-to-speech elements."""
        self._voices = {"en":"British", "en-us":"American", "en-sc":"Scottish", "rp":"en-rp", "en-n":"Northern", "en-wm":"West Midlands", "en-wi":"West Indies"}
        self._variations = {"m1":"Male1", "m2":"Male2", "m3":"Male3", "m4":"Male4", "m5":"Male5", "m6":"Male6", "m7":"Male7", "f1":"Female1", "f2":"Female2", "f3":"Female3", "f4":"Female4", "croak":"Croak", "whisper":"Whisper"}
        self._params_volume = {"default":100, "min":0, "max":200, "units":""}
        self._params_speed = {"default":175, "min":80, "max":450, "units":"words per minute"}
        self._params_pitch = {"default":50, "min":0, "max":99, "units":""}
        self._params_wordGap = {"default":50, "min":0, "max":99, "units":""}
        self._params_capStress = {"default":0, "min":0, "max":9999, "units":""}
        
        
    def say(self,phrase="Hi, I'm PieBot!",volume=self._params_volume["default"],voice=0,variation=0,speed=self._params_speed["default"],pitch=self._params_pitch["default"],capStress=self._params_capStress["default"],wordGap=self._params_wordGap["default"],saveFile=NONE):
        """Use a text-to-speech engine to say phrases."""
        pLang = "-v" + self._voices[voice].key + "+" + self._variations[variation].key
        pGap = "-g" + str(wordGap)
        pSpeed = "-s" + str(speed)
        pPitch = "-p" + str(pitch)
        pCapStress = "-k" + str(capStress)
        subprocess.Popen(['espeak', pLang, pGap, pSpeed, pPitch, pCapStress, phrase], stdout=subprocess.PIPE)
        if saveFile:
            pFile = "-w" + saveFile
            subprocess.Popen(['espeak', pLang, pGap, pSpeed, pPitch, pCapStress, pFile, phrase], stdout=subprocess.PIPE)
            # strippedName = "".join([c for c in saveFile if c.isalpha() or c.isdigit()]).rstrip()
            # sFile = strippedName + lang + gap + spd + ".wav"
            # pFile = "-w" + sFile
            # print("---Saving file as: " + sFile)
            # subprocess.Popen(['espeak', lang, gap, spd, pFile, sText]).stdout
    
    
    def play(self, audioFile=NONE):
        """Play an audio file."""
        print audioFile
        subprocess.Popen(['aplay', audioFile], stdout=subprocess.PIPE)
