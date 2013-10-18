import RPIO
import time

class distance(object):
    """Use PiBot's Ultrasound to track distance."""
                
    def __init__(self):
        """Initialise ultrasound parameters."""
        self._RPIO_TRIGGER = 18
        self._RPIO_ECHO    = 23
        # Set pins as output and input
        RPIO.setup(self._RPIO_TRIGGER,RPIO.OUT)  # Trigger
        RPIO.setup(self._RPIO_ECHO,RPIO.IN)      # Echo

    def measure(self):
        """Get a measurement."""
            
        # Set trigger to False (Low)
        RPIO.output(self._RPIO_TRIGGER, False)
            
        # Allow module to settle
        time.sleep(0.5)
            
        # Send 10us pulse to trigger
        RPIO.output(self._RPIO_TRIGGER, True)
        time.sleep(0.00001)
        RPIO.output(self._RPIO_TRIGGER, False)
        start = time.time()
            
        while RPIO.input(self._RPIO_ECHO)==0:
            start = time.time()
            
        while RPIO.input(self._RPIO_ECHO)==1:
            stop = time.time()
            
        # Calculate pulse length
        elapsed = stop-start
            
        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        # That was the distance there and back so halve the value
        distance = (elapsed * 34300) / 2
            
        return distance
