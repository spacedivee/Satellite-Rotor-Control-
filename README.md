[BOM.csv](https://github.com/user-attachments/files/32779077/BOM.csv)<img width="1408" height="836" alt="iso all2" src="https://github.com/user-attachments/assets/0256e4ad-3018-49b3-a669-decc6f51a243" />


## *$FOR THE STARDANCE REVIEWERS$*
- In case you haven't read it through my comments already , my BOM.csv is irrelevant if you guys can **ship me a HackPad kit** +(the PCB grant). I need the exact same components as the components in the kit, so sending me my grant isn't necessary(Either way its the same components bought individually which just costs more, so its a win win for both of us if you ship a HackPad kit). I would submit this project as a hackpad, but previous reviewers have been agaisnt that. Thank you for your understanding.


## Custom Satellite Control Interface
A custom PCB-based controller designed as a physical interface for controlling software on a computer. It can be used as a general-purpose control pad, with a focus on eventually controlling a **satellite antenna rotator** (which is another project I am building).

## Components and buidling materials.
* 4× MX-style buttons
* EC11E rotary encoder with push button
* 0.91" OLED display
* Seeed XIAO RP2040
* Custom KiCad PCB
* 3D-printed Onshape enclosure

## PCB+Circuit

<img width="771.5" height="572.53" alt="pcb ctrl" src="https://github.com/user-attachments/assets/2bf69843-6900-4f06-9400-bb481facef3b" > <img width="771.5" height="258" alt="circuit1" src="https://github.com/user-attachments/assets/78b19082-43b2-425e-b3b1-5cc115486cb1" />

## How It Works
The XIAO RP2040 reads the buttons and rotary encoder and sends their inputs to software running on a computer. The OLED provides feedback to the user. In my case, the OLED will display Azimuth and Elevation as they are being changed so the antenna adjustmenet can be simplified. The Encoder will be used to manually adjust the increment of the motors, such that each press will be greater or smaller, depending on the input. 
All of the information will then be sent to the XIAO, which will then sent it to my computer as keystroke data (my current method), which my antenna rotator software will then acknowledge. 

## Tools

* **KiCad** — PCB design
* **Onshape** — enclosure design
* **Arduino/C++** — programming
* **JLCPCB** — PCB manufacturing


## Firmware
For the record, this is the only aspect of my project that was completely made by AI. The current firmware is a placeholder and I plan on writing it myself once I have built the board. I believe this is a better way
of doing things since I get to actively troubleshoot issues. I hope yall feel the same way about this ❤️.

## Bill of Materials

| Item | Component Name | Qty | Price (USD) | Notes |
| :---: | :--- | :---: | :---: | :--- |
| 1 | [Seeed XIAO RP2040](https://amazon.ca) | 1 | $19.32 | Main microcontroller |
| 2 | [1N4148 through-hole diodes](https://amazon.ca) | 4 | $1.50 | Button/switch matrix |
| 3 | [MX-style switches](https://amazon.ca) | 4 | $5.99 | Main input buttons |
| 4 | [EC11E rotary encoder with switch](https://amazon.ca) | 1 | $8.79 | - |
| 5 | [0.91 inch OLED display](https://amazon.ca) | 1 | $6.67 | GND-VCC-SCL-SDA pin order |
| 6 | [White blank DSA keycaps](https://amazon.ca) | 4 | $12.50 | Keycaps for MX switches |
| 7 | [M3x16mm screws](https://amazon.ca) | 4 | $8.59 | Case assembly |
| 8 | [M3x5mmx4mm heat-set inserts](https://amazon.ca) | 4 | $8.49 | Case assembly |
| 9 | $10 JLCPCB credit | 1 | $10.00 | PCB manufacturing |
| 10 | LED | 1 | $0.00 | - supplied by me |
| 11 | Resistor | 1 | $0.00 | - supplied by me |
| | **Total Estimated Cost:** | | **$81.85** | |

> **Note:** If you have an existing hackpad kit available, I would happily accept that as an alternative. It may be more cost-effective and prevents acquiring unnecessary duplicate components.

