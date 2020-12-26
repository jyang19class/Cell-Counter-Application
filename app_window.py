from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2
import count
import numpy as np

class WindowDetails():
    def __init__(self):
        self.originalImg = None
        self.img = None
        self.imagePath = None
        self.imagePanel = None
        self.count = None
        self.loaded = False
        self.mouseActivated = False
        self.saturation = 0
        self.hue = 0

def openfilename():
	# open file dialog box to select image
    filename = filedialog.askopenfilename(title='Open')
    return filename

def open_img(details):
    # Select the Imagename from a folder
    details.imagePath = openfilename()
    #Check if no file chosen
    if details.imagePath == '':
        return
    #Opens the image
    details.img = Image.open(details.imagePath) 
    details.img = ImageTk.PhotoImage(details.img)
    details.originalImg = details.img

    imageData = cv2.imread(details.imagePath)
    _height, _width, channels = imageData.shape

    details.imagePanel.config(width=_width, height=_height)
    details.imagePanel.create_image(0,0, image=details.img, anchor='nw')
    details.count.configure(text='  0')

    _height = _height + 10
    _width = _width + 125
    dimensions = str(_width) + 'x' + str(_height)
    root.geometry(dimensions)

    details.loaded = True
    if details.mouseActivated:
        deactivateMouse(details)

def countCell(event, details):
    x = event.x
    y = event.y
    deactivateMouse(details)

    #reformat cv2 img
    newImage, countNumber = count.countCells(x,y, details.imagePath, details.saturation, details.hue)
    formatted = Image.fromarray(newImage)
    details.img = ImageTk.PhotoImage(formatted)
    details.imagePanel.create_image(0,0, image=details.img, anchor='nw')
    details.count.configure(text='  '+ str(countNumber))


def activateMouse(details):
    details.imagePanel.bind('<Button-1>', lambda event: countCell(event, details))
    root.config(cursor="crosshair")
    details.mouseActivated = True

def deactivateMouse(details):
    details.imagePanel.unbind('<Button-1>')
    root.config(cursor="arrow")
    details.mouseActivated = False

def selectColor(details):
    if not details.loaded:
        return
    activateMouse(details)

def setSaturation(value, details):
    details.saturation = value

def setHue(value, details):
    details.hue = value

def undo(details):
    details.img = details.originalImg
    details.imagePanel.create_image(0,0, image=details.img, anchor='nw')
    details.count.configure(text='  0')

if __name__ == "__main__":
    windowInfo = WindowDetails()
    root = Tk()
    windowInfo.imagePanel = Canvas(root, width = 400, height = 400)
    windowInfo.imagePanel.grid(row=1, rowspan=5)
    # Set Title
    root.title("Cell Counter")

    # Set the resolution of window
    root.geometry("600x400")

    # Allow Window to be resizable
    root.resizable(width = True, height = True) 

    # Create buttons
    openButton = Button(root, text ='Open Image', command = lambda: open_img(windowInfo), width=10)
    openButton.grid(row = 1, column = 2) 

    countFrame = Frame(root)
    countFrame.grid(row = 2, column = 2)
    colorButton = Button(countFrame, text='Count',command = lambda: selectColor(windowInfo), width=6)
    colorButton.pack(side=LEFT)
    countLabel = Label(countFrame, text='   0')
    countLabel.pack(side=RIGHT)
    windowInfo.count = countLabel

    undoButton = Button(root, text='Undo',command = lambda: undo(windowInfo), height=1, width=5)
    undoButton.grid(row = 3, column = 2)

    #Create Sliders
    saturationSlider = Scale(root, from_=40, to=80, orient=HORIZONTAL, tickinterval = 10, label='Saturation',
         command=lambda value: setSaturation(value, windowInfo))
    saturationSlider.grid(row = 4, column = 2)
    saturationSlider.set(80)

    hueSlider = Scale(root, from_=10, to=20, orient=HORIZONTAL, tickinterval = 5, label= 'Hue Threshold',
         command = lambda value: setHue(value, windowInfo))
    hueSlider.grid(row = 5, column = 2)
    hueSlider.set(20)
    root.mainloop()
    