from gpiozero import Device, PWMPin

with Device() as d:
    print(type(d.pin_factory).__name__)
    for name in ('GPIO12', 'GPIO13', 'GPIO18', 'GPIO19'):
        try:
            PWMPin(name).close()
            print(name, 'PWM ok')
        except Exception as e:
            print(name, '->', type(e).__name__, e)

