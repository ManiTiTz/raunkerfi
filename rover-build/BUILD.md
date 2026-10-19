# Rover build — condensed from Canvas

Source: CPSY Canvas pages **Lab 4/5: Power distribution** and **Lab 5: Make Things Move**.
Photos in this folder are Marcel's, downloaded from those pages.
plus the **Double Decker Robot** page (Robotics & IoT common course, 6589).

**Look at these first:**
- `ASM-Rover.PNG` / `SWCAD/SWCAD/ASM-robot-chassis-2026.pdf` — 3D render of the finished rover
- `SWCAD/SWCAD/ASM-Rover-drawings.pdf` — 4-sheet assembly drawing with full bill of materials (which screw goes where)
- `SWCAD/SWCAD/baseplate-marcel.pdf` — baseplate hole layout
- `SWCAD/SWCAD/ASM-robot-chassis-2026-sensorboard.pdf` — sensor board layout
- `MECH-CPSY-Checkoff.pdf` — checkoff list

Two acrylic plates = **lower deck** (motors, caster, power board) and **upper deck** (Pi, breadboard, IR sensor, battery). Peel the protective foil off both sides first.

## 1. Power distribution board (solder first, off the plate)
See `6-pdboard.png`, `7-pdboard-soldered.jpeg`, `schematic.pdf`.
- Female 3-pin headers → J2, J11, J12
- Female 6-pin headers → J4, J7
- 8-pin + 6-pin female headers → U2 (motor driver sits here)
- 5-pin headers: cut off one pin each → J5, J8
- Single male pin → J14
- Terminal blocks → J1, J9, J10 (ask in lab if you're one short)
- Slide switch → SW1 · 330 Ω → R1 · LED → LED1
- JST connectors → J3, J6. **White lines on the silkscreen must stay visible — if the plastic covers the line it's backwards. Check with staff before soldering.**
- Capacitor → C1, **the white "−" stripe faces the C1 label.**
- LEDs: **longer leg = +**. Pin 1 is marked with little white dots.
- JST-ZH pads are tiny: small tip, little solder, then **multimeter-check no adjacent pins are shorted** — a short can put 9 V on a 3.3 V Pi pin and kill it.
- No third terminal block for BAT? Solder red/black stranded wire directly.

## 2. HUSB238 (USB-C PD trigger) → 9 V
See `8-husb238.png`.
- Cut the trace in the **1A** and **5V** pads with a craft knife, then solder-bridge the **9V** pad **and the 2A pad** (Double Decker page; Lab 4/5 only mentions 9V). Keep solder on those pads only.
- Terminal block on +/−: wire openings face **away** from the board centre.
- Wrap the HUSB238 in electrical tape and keep it away from other electronics (a short dumps a lot of current). Rubber-band it to the power bank.
- HUSB238 out → BAT on the board (+ to +, GND to −; red/black wires).
- 7VOUT → IN of the DC/DC converter; converter OUT → 5VIN. (`9-converter.png`, `10-power-wired.jpeg`)

## 3. Calibrate the voltage regulator (LM2596)
See `2-resistive-load.jpeg`.
- Load the output with **4 × 150–160 Ω resistors in parallel** (power bank shuts off without a load). They get hot.
- Use the thicker stranded "DIY PVC" wire; twist and tin the ends before screwing/soldering.
- Multimeter on the output. Turn the brass screw on the blue pot **counter-clockwise** to lower it until ~**5.1 V** (Lab 5 says 5.1–5.2, Double Decker says 5.0–5.1 — 5.1 satisfies both). Can take 10+ turns. **It may start well above 5 V — never connect the Pi before adjusting.**
- Screw the regulator to the plate afterwards (easier to solder unmounted).

## 4. Lower deck — wheels and caster
See `1-caster-lower-deck.jpeg`.
- Motors mount to the lower deck with the **white brackets** + nuts/washers/screws. Encoder connectors go through the holes.
- Bracket trick: **put the M2 nuts in the bracket and tape them in before fitting the motor.** The bracket has dents that fit the gearbox — the plate only accepts motor+bracket when aligned with them.
- Tight clearances everywhere; a decent small screwdriver set helps.
- Caster at the back with the M4 20 mm screws. Use the **two plastic cylinders** as spacers so the deck is level — **not** the aluminium ones (too tall).
- Colour sensor at the front on the 15 mm (kit: 20 mm) standoffs, facing down.

## 5. Motor driver (DRV8833)
- Solder to its pin headers, generously (high current). Plug into U2.
- **SLP must be high** or nothing moves. Recommended: wire SLP to **its own GPIO** you set high (libraries choke on a shared SLP between two motors).
- **Unplug a motor from the driver before spinning its wheel by hand** to test the encoder — back-EMF can fry the DRV8833.

## 6. Upper deck
See `3-upper-deck-top.jpeg`, `4-upper-deck-b.jpeg`.
- Holds Pi, breadboard, IR distance sensor, battery.
- Pi on 8 mm standoffs, oriented so **USB and HDMI are reachable** (debugging when WiFi is dead).
- Soldering the Pi's GPIO header: **don't use the breadboard as a jig** (they're not flat → bent pins). Use cardboard or perfboard.
- IR sensor on its bracket **under** the plate. It needs **5 V** (unreliable at 3.3 V) and its 3 pins must go in the right holes — wrong holes = it gets hot and dies.
- Battery pack strapped to the **underside** with rubber bands.
- Display face down is fine — flip the robot to read it.

## 7. IMU
See `5-imu-on-standoffs.jpeg`.
- On the **30 mm standoffs in the centre holes** — keeps it away from the (ferromagnetic) breadboard so the compass works.
- Attach the jumper wires **before** mounting. **AD0 → GND or VDD, nCS → VDD** — required, not optional.
- Tip: put a 6-pin female socket on pins VCC…AD0 to save wires.

## 8. Join the decks
- Long (40 mm) standoffs between the decks. Clip screws if too long.
- If the IR sensor hits the interface board, or header cables don't fit, add (printed) washers/discs between standoff and upper deck.

## 9. Powering the Pi
- Regulator **OUT− → Pi pin 6 (GND)**, **OUT+ → Pi pin 2 (5V)**.
- **Never** power the Pi from USB and battery at the same time. Remove other wires from Pi 5V / driver Vm.

## 10. Motor wiring
Motor cable colours:

| Label | Pin | Colour |
|---|---|---|
| M2 | Motor+ | Red |
| VCC | Encoder+ | **Black** (yes, black) |
| C2 | Encoder A | Yellow |
| C1 | Encoder B | Green |
| GND | Encoder GND | Blue |
| M1 | Motor− | White |

Board headers (pin 1 = next to the tiny dot):

| MOTA (J5) | | MOTB (J6) | |
|---|---|---|---|
| 1 | AIN1 | 1 | BIN1 |
| 2 | AIN2 | 2 | BIN2 |
| 3 | Motor A C1 | 3 | Motor B C1 |
| 4 | Motor A C2 | 4 | Motor B C2 |

Driver out: AOUT1→A M1, AOUT2→A M2, BOUT1→B M1, BOUT2→B M2. Swapping M1/M2 reverses the wheel — fixable in code.

## 11. Test drive
gpiozero `Robot(left=Motor(...), right=Motor(...))` with PWM pins; `RotaryEncoder(max_steps=0)` to check encoders. Canvas example uses SLP=GPIO26, left GPIO12/18, right GPIO13/19 — use your own pins.

## 12. WiFi drops after ~15 min
```
sudo nano /etc/NetworkManager/conf.d/wifi-powersave-off.conf
```
```
[connection]
wifi.powersave = 2
```
```
sudo systemctl restart NetworkManager
```
Also: the power bank may sleep at low draw — having the OLED and colour sensor powered helps.
