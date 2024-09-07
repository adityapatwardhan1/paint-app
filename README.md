## paint-app
Implementation of a paintbrush app in Python using the Pygame library.
## Prerequisites
As prerequisites, one must install Python3 and the Pip package manager.
On Debian Linux, the corresponding commands are
```
sudo apt install python3
sudo apt install python3-pip
```
Instructions for other Linux Distributions are probably similar.

## How to Paint
To start the program, use the command
```
python3 paint.py
```
The paintbrush thickness can be selected using the numbered buttons, 1, 2, 3, 4, with 1 being the thinnest and 4 being the thickest brush.

The F command fills a bounded region with a color.

The D command can be used to draw freestyle with the paintbrush.

The E command stands for eraser.

The R command re-colors pixels with the same color as the clicked pixel, to be the selected color in the color palette.

The C command clears the screen.
