# Custom Satellite Control Interface

A custom PCB-based controller designed as a physical interface for controlling software on a computer. It can be used as a general-purpose control pad, with a focus on eventually controlling a **satellite antenna rotator**.

## Features

* 4× MX-style buttons
* EC11E rotary encoder with push button
* 0.91" OLED display
* Seeed XIAO RP2040
* Custom KiCad PCB
* 3D-printed Onshape enclosure

## How It Works

The XIAO RP2040 reads the buttons and rotary encoder and sends their inputs to software running on a computer. The OLED provides feedback to the user.

For my satellite project, the controller can be used to send commands to software controlling an antenna rotator.

## Tools

* **KiCad** — PCB design
* **Onshape** — enclosure design
* **Arduino/C++** — programming
* **JLCPCB** — PCB manufacturing

