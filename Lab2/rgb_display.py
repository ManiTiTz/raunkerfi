import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_tcs34725

WIDTH, HEIGHT = 128, 64

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

try:
    reset_pin = digitalio.DigitalInOut(board.D4)
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=reset_pin)
except:
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    r, g, b = sensor.color_rgb_bytes
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    draw.text((0, 0),  f"R: {r}", font=font, fill=255)
    draw.text((0, 12), f"G: {g}", font=font, fill=255)
    draw.text((0, 24), f"B: {b}", font=font, fill=255)
    oled.image(image)
    oled.show()
    time.sleep(1.0)
