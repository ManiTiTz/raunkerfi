#! /usr/bin/env python3

import os
import time
import curses

from gpiozero import DigitalOutputDevice, Motor, Robot

try:
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    stdscr.addstr(0, 10, "Hit 'q' to quit")
    stdscr.nodelay(1)  # nodelay(1) give us a -1 back when nothing is pressed
    direction = None

    # Configure your own pins.
    slp = DigitalOutputDevice('GPIO26')
    slp.on()

    # Motor(forward_pin, backward_pin). This line must get two things right
    # for each motor:
    #   side      -> is it passed as left= or right=
    #   direction -> which of its two pins comes first
    # Pins 12/18 drive the RIGHT wheel (12 = forward).
    # Pins 13/19 drive the LEFT wheel  (19 = forward).
    robot = Robot(left=Motor('GPIO19', 'GPIO13'), right=Motor('GPIO12', 'GPIO18'))

    # If turning is correct but w/s are reversed, the front of the car is the
    # other end. Use this line instead of the one above:
    # robot = Robot(left=Motor('GPIO18', 'GPIO12'), right=Motor('GPIO13', 'GPIO19'))

    # Here starts the code to make the robot move
    while direction != ord('q'):
        stdscr.refresh()
        direction = stdscr.getch()  # Gets the key which is pressed
        if direction == ord('e'):
            stdscr.addstr(1, 10, "Stop    ")
            robot.stop()
        if direction == ord('a'):
            stdscr.addstr(1, 10, "Left    ")
            robot.left()
        if direction == ord('s'):
            stdscr.addstr(1, 10, "Backward")
            robot.backward()
        if direction == ord('d'):
            stdscr.addstr(1, 10, "Right   ")
            robot.right()
        if direction == ord('w'):
            stdscr.addstr(1, 10, "Forward ")
            robot.forward()
        time.sleep(0.04)
finally:
    # Important to set everthing back by end of the script
    slp.off()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()

