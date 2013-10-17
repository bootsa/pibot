#import the library to control the GPIO pins
import RPi.GPIO as RPIO
from RPIO import PWM
RPIO.setwarnings(False)
import sys
#import the time library
import time

class pibot(object):
    """Pibot Control Library."""
    
    class move(object):
        """Use the motors to move the pibot."""
        
        def __init__(self):
            """Initialise movement."""
            PWM.setup()
            
            #get rid of debug output
            PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
            
            #pins
            #i2c pins can be enabled high at boot - see http://www.raspberrypi.org/phpBB3/viewtopic.php?f=44&t=35321
            self._l_enable_pin = 4
            self._l_forward_pin = 3
            self._l_backward_pin = 2
            self._r_enable_pin = 17
            self._r_forward_pin = 27
            self._r_backward_pin = 22

            #constants
            self.LEFT = 1
            self.RIGHT = 2

            #setup the pins
            RPIO.setup(self._l_forward_pin, RPIO.OUT)
            RPIO.setup(self._r_forward_pin, RPIO.OUT)
            RPIO.setup(self._l_backward_pin, RPIO.OUT)
            RPIO.setup(self._r_backward_pin, RPIO.OUT)
            
            #pwm setup
            self._dma_l = 0
            self._dma_r = 1
            PWM.init_channel(self._dma_l)
            PWM.init_channel(self._dma_r)
            #this is silly, but otherwise pwm will complain if we try and clear a channel that hasn't been already used
            PWM.add_channel_pulse(self._dma_l,self._l_enable_pin,0,0)
            PWM.add_channel_pulse(self._dma_r,self._r_enable_pin,0,0)

        def stop_all(self):
            """Stop all movement."""
            print "stop"
            PWM.clear_channel_gpio(self._dma_l, self._l_enable_pin)
            PWM.clear_channel_gpio(self._dma_r, self._r_enable_pin)

        #direction, how long to drive for, how fast to drive
        def drive(self,wheel,speed):
            """Drive each wheel separately."""
            if wheel == self.LEFT:
                print "left",
                dma = self._dma_l
                enable_pin = self._l_enable_pin
                forward_pin = self._l_forward_pin
                backward_pin = self._l_backward_pin
            elif wheel == self.RIGHT:
                print "right",
                dma = self._dma_r
                enable_pin = self._r_enable_pin
                forward_pin = self._r_forward_pin
                backward_pin = self._r_backward_pin
            else:
                error_msg( "unknown wheel")
            return

            if speed > 100 or speed < -100:
                error_msg("speed should be > -100 and < 100")
                return

            if speed > 0:
                RPIO.output(forward_pin, True)
                RPIO.output(backward_pin, False)
                print "forward",
            elif speed < 0:
                RPIO.output(forward_pin, False)
                RPIO.output(backward_pin, True)
                print "backward",
            else:
                print "stop",

            pwm_amount = int(abs(speed * (1999/100)))

            print "pwm:", pwm_amount
            PWM.add_channel_pulse(dma,enable_pin,0,pwm_amount)

        def end(self):
            """Cleanup after usage."""
            PWM.cleanup()

        def error_msg(self,msg):
            """Deal with error messages."""
            sys.stderr.write(msg + "\n")

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
#                strippedName = "".join([c for c in saveFile if c.isalpha() or c.isdigit()]).rstrip()
#                sFile = strippedName + lang + gap + spd + ".wav"
#                pFile = "-w" + sFile
#                print("---Saving file as: " + sFile)
#                subprocess.Popen(['espeak', lang, gap, spd, pFile, sText]).stdout
        
        
        def play(self, audioFile=NONE):
            """Play an audio file."""
            print audioFile
            subprocess.Popen(['aplay', audioFile], stdout=subprocess.PIPE)
        
    class lights(object):
        """Illuminate PiBot's LEDs."""
                
        def __init__(self):
            """Initialise LED parameters."""

    class vision(object):
        """Control PiBot's camera."""
                
        def __init__(self):
            """Initialise camera parameters."""

    class distance(object):
        """Use PiBot's Ultrasound to track distance."""
                
        def __init__(self):
            """Initialise ultrasound parameters."""
            self._GPIO_TRIGGER = 18
            self._GPIO_ECHO    = 23
            # Set pins as output and input
            GPIO.setup(self._GPIO_TRIGGER,GPIO.OUT)  # Trigger
            GPIO.setup(self._GPIO_ECHO,GPIO.IN)      # Echo

        def measure(self):
            """Get a measurement."""
            
            # Set trigger to False (Low)
            GPIO.output(self._GPIO_TRIGGER, False)
            
            # Allow module to settle
            time.sleep(0.5)
            
            # Send 10us pulse to trigger
            GPIO.output(self._GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(self._GPIO_TRIGGER, False)
            start = time.time()
            
            while GPIO.input(self._GPIO_ECHO)==0:
                start = time.time()
            
            while GPIO.input(self._GPIO_ECHO)==1:
                stop = time.time()
            
            # Calculate pulse length
            elapsed = stop-start
            
            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            distance = elapsed * 34300
            
            # That was the distance there and back so halve the value
            return distance = distance / 2
