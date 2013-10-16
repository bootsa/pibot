#import the library to control the GPIO pins
import RPIO
from RPIO import PWM
RPIO.setwarnings(False)
import sys

PWM.setup()

#get rid of debug output
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

#import the time library
import time

class pibot(object):
    """Pibot Control Library."""
    
    class move(object):
        """Use the motors to move the pibot."""
        
        def __init__(self):
            """Initialise movement."""
            #pins
            #i2c pins can be enabled high at boot - see http://www.raspberrypi.org/phpBB3/viewtopic.php?f=44&t=35321
            self._l_enable_pin = 4
            self._l_forward_pin = 3
            self._l_backward_pin = 2
            self._r_enable_pin = 17
            self._r_forward_pin = 27
            self._r_backward_pin = 22

            #constants
            self._LEFT = 1
            self._RIGHT = 2

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
            if wheel == LEFT:
                print "left",
                dma = self._dma_l
                enable_pin = self._l_enable_pin
                forward_pin = self._l_forward_pin
                backward_pin = self._l_backward_pin
            elif wheel == RIGHT:
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
