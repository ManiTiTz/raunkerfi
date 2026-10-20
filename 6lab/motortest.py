from gpiozero import Motor, DigitalOutputDevice
import time

slp = DigitalOutputDevice('GPIO26')
slp.on()          # ← this is what wakes the driver up

left_motor  = Motor('GPIO12', 'GPIO18')
right_motor = Motor('GPIO13', 'GPIO19')

print("Left  forward")
left_motor.forward();  time.sleep(1); left_motor.stop()

print("Left  back")
left_motor.backward(); time.sleep(1); left_motor.stop()

print("Right forward")
right_motor.forward();  time.sleep(1); right_motor.stop()

print("Right back")
right_motor.backward(); time.sleep(1); right_motor.stop()

slp.off()

