#! /usr/bin/env python3

from tkinter import *
from tkinter import ttk
from re import findall

import subprocess

#cam_props = {'brightness': 128, 'contrast': 128, 'saturation': 180,
#             'gain': 0, 'sharpness': 128, 'exposure_auto': 1,
#             'exposure_absolute': 150, 'exposure_auto_priority': 0,
#             'focus_auto': 0, 'focus_absolute': 30, 'zoom_absolute': 250,
#             'white_balance_temperature_auto': 0, 'white_balance_temperature': 3300}

#for key in cam_props:
#    subprocess.call(['v4l2-ctl -d /dev/video3 -c {}={}'.format(key, str(cam_props[key]))],
#                    shell=True)

#cam = cv2.VideoCapture(1)

#test = subprocess.call(['v4l2-ctl -d 2 -l'.format()],shell=True)
#print(test)

def cameraCheck():
  camNum = int(cameraNumber.get("1.0"))
  fOut.delete("1.0", "end")
  checkPan = subprocess.getoutput('v4l2-ctl -d {} -l | grep "pan_absolute"'.format(camNum))
  checkTilt = subprocess.getoutput('v4l2-ctl -d {} -l | grep "tilt_absolute"'.format(camNum))
  checkZoom = subprocess.getoutput('v4l2-ctl -d {} -l | grep "zoom_absolute"'.format(camNum))
  fOut.insert("end", "{}\n {}\n {}".format(checkPan, checkTilt, checkZoom))
  

def change_position(panTilt, chPosition):
  camNum = int(cameraNumber.get("1.0"))
  fOut.delete("1.0", "end")
  
  check = subprocess.getoutput('v4l2-ctl -d {} -C "{}"'.format(camNum,panTilt))
  num_only = findall("{}: ([-\d]*)".format(panTilt), check)
  
  num = int(num_only[0]) + chPosition
  subprocess.call(['v4l2-ctl -d 2 -c "{}"={}'.format(panTilt, num)],shell=True)
  
  check = subprocess.getoutput('v4l2-ctl -d 0 -C "{}"'.format(panTilt))
  num_only = findall("{}: ([-\d]*)".format(panTilt), check)
  
  fOut.insert("end", "{}: {}".format(panTilt, num_only[0]))

positionDelta = 50000

def panLeft():
  change_position("pan_absolute", -positionDelta)
  
def panRight():
  change_position("pan_absolute", positionDelta)

def panUp():
  change_position("tilt_absolute", positionDelta)
  
def panDown():
  change_position("tilt_absolute", -positionDelta)
  
zoomDelta = 10
def zoomIn():
  change_position("zoom_absolute", zoomDelta)
  
def zoomOut():
  change_position("zoom_absolute", -zoomDelta)
  
tk = Tk()
tk.title("ptzPython")
mainFrame = Frame(tk, relief=RIDGE, borderwidth=2, bg="grey")

cameraFrame = Frame(mainFrame, relief=RIDGE, borderwidth=2, bg="grey")
cameraTitle = Label(cameraFrame, text="CameraNumber", font=('Arial', 14))
cameraNumber = Text(cameraFrame, width=2, height=1, font=('Arial', 14))
btnCamera = Button(cameraFrame, text="Check", command=cameraCheck)

positionFrame = Frame(mainFrame, relief=RIDGE, borderwidth=2, bg="grey")
btnLeft = Button(positionFrame, text="left", command=panLeft)
btnRight = Button(positionFrame, text="right", command=panRight)
btnUp = Button(positionFrame, text="up", command=panUp)
btnDown = Button(positionFrame, text="down", command=panDown)

zoomFrame = Frame(mainFrame, relief=RIDGE, borderwidth=2, bg="grey")
btnIn = Button(zoomFrame, text="in", command=zoomIn)
btnOut = Button(zoomFrame, text="out", command=zoomOut)

outFrame = Frame(tk, relief=RIDGE, borderwidth=2, bg="grey")
fOut = Text(outFrame, width=40, height=4, font=('Arial', 14))

mainFrame.pack()

cameraFrame.pack(side=LEFT, anchor=W)
cameraTitle.pack(side=TOP, anchor=N)
cameraNumber.pack(side=LEFT, anchor=W)
btnCamera.pack(side=RIGHT, anchor=E)

positionFrame.pack(side=LEFT, anchor=W)
btnLeft.pack(side=LEFT, anchor=SW)
btnRight.pack(side=RIGHT, anchor=SE)
btnUp.pack(side=TOP, anchor=N)
btnDown.pack(side=BOTTOM, anchor=S)

zoomFrame.pack(side=RIGHT, anchor=E)
btnIn.pack(side=TOP)
btnOut.pack(side=TOP)

outFrame.pack()
fOut.pack(pady=10, side=TOP)

tk.mainloop()
