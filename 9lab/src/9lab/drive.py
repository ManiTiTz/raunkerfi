#!/usr/bin/env python3
import curses
import time

from gpiozero import DigitalOutputDevice, Motor, Robot, MCP3008

STOP_VOLTAGE = 1.5  # V; above this the object is close enough to halt the rover


def read_voltage(sensor):
    return sensor.value * 3.3


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
    stdscr.addstr(0, 10, "Hit 'q' to quit")

    slp = DigitalOutputDevice('GPIO26')
    slp.on()

    sensor = MCP3008(channel=0)  # CH0, where the sensor's yellow wire lands

    robot = Robot(left=Motor('GPIO19', 'GPIO13'),
                  right=Motor('GPIO12', 'GPIO18'))

    moves = {
        ord('w'): robot.forward,
        ord('a'): robot.left,
        ord('s'): robot.backward,
        ord('d'): robot.right,
    }

    try:
        while True:
            if read_voltage(sensor) > STOP_VOLTAGE:
                robot.stop()
                stdscr.addstr(1, 10, "Obstacle ")
                time.sleep(0.04)
                continue

            key = stdscr.getch()
            if key == ord('q'):
                break
            if key == ord('e'):
                robot.stop()
                stdscr.addstr(1, 10, "Stop     ")
            elif key in moves:
                move = moves[key]
                robot.stop()
                move()
                stdscr.addstr(1, 10, f"{move.__name__:8s}")

            time.sleep(0.04)
    finally:
        slp.off()
        robot.stop()


if __name__ == '__main__':
    curses.wrapper(main)

