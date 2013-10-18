import RPIO
from RPIO import PWM
RPIO.setwarnings(False)
import sys

PWM.setup()

#get rid of debug output
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
            
#pins
#i2c pins can be enabled high at boot - see http://www.raspberrypi.org/phpBB3/viewtopic.php?f=44&t=35321
_l_enable_pin = 4
_l_forward_pin = 3
_l_backward_pin = 2
_r_enable_pin = 17
_r_forward_pin = 27
_r_backward_pin = 22

#constants
LEFT = 1
RIGHT = 2

#setup the pins
RPIO.setup(_l_forward_pin, RPIO.OUT)
RPIO.setup(_r_forward_pin, RPIO.OUT)
RPIO.setup(_l_backward_pin, RPIO.OUT)
RPIO.setup(_r_backward_pin, RPIO.OUT)
            
#pwm setup
_dma_l = 0
_dma_r = 1
PWM.init_channel(_dma_l)
PWM.init_channel(_dma_r)
#this is silly, but otherwise pwm will complain if we try and clear a channel that hasn't been already used
PWM.add_channel_pulse(_dma_l,_l_enable_pin,0,0)
PWM.add_channel_pulse(_dma_r,_r_enable_pin,0,0)

def stop_all():
    """Stop all movement."""
    print "stop"
    PWM.clear_channel_gpio(_dma_l, _l_enable_pin)
    PWM.clear_channel_gpio(_dma_r, _r_enable_pin)

#direction, how long to drive for, how fast to drive
def drive(wheel,speed):
    """Drive each wheel separately."""
    if wheel == LEFT:
        print "left",
        dma = _dma_l
        enable_pin = _l_enable_pin
        forward_pin = _l_forward_pin
        backward_pin = _l_backward_pin
    elif wheel == RIGHT:
        print "right",
        dma = _dma_r
        enable_pin = _r_enable_pin
        forward_pin = _r_forward_pin
        backward_pin = _r_backward_pin
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

def end():
    """Cleanup after usage."""
    PWM.cleanup()

def error_msg(msg):
    """Deal with error messages."""
    sys.stderr.write(msg + "\n")
