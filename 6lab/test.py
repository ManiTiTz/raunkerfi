#!/usr/bin/env python3
# Holds the motor pins on so you can measure them with a multimeter.
# Commands: a = motor A forward, b = motor B forward, s = stop, q = quit

from gpiozero import Device, DigitalOutputDevice, Motor

slp = DigitalOutputDevice('GPIO26')
motor_a = Motor('GPIO12', 'GPIO18')
motor_b = Motor('GPIO13', 'GPIO19')

print("Pin factory:", Device.pin_factory)

try:
    slp.on()
    print("Driver awake (SLEEP pin = 3.3 V)")
    while True:
        cmd = input("a / b / s / q + Enter: ").strip().lower()
        if cmd == 'a':
            motor_b.stop()
            motor_a.forward()
            print("Motor A forward: AIN1 should read ~3.3 V, AIN2 ~0 V")
        elif cmd == 'b':
            motor_a.stop()
            motor_b.forward()
            print("Motor B forward: BIN1 should read ~3.3 V, BIN2 ~0 V")
        elif cmd == 's':
            motor_a.stop()
            motor_b.stop()
            print("Stopped")
        elif cmd == 'q':
            break
finally:
    motor_a.stop()
    motor_b.stop()
    slp.off()
    print("All off")
