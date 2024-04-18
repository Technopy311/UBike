#Controlador diodo RGB
from machine import Pin
class RGB:
    #Defina los pins GPIO donde se conectará el diodo
    def __init__(self, r, g, b):
        self.colorSet = ["red", "green", "blue", "yellow", "cyan", "magenta", "black", "white"]
        self.colors = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1],[0,0,0],[1,1,1]]
        self.red = Pin(r, Pin.OUT)
        self.green = Pin(g, Pin.OUT)
        self.blue = Pin(b, Pin.OUT)
    def setColor(self, color):
        if color in self.colorSet:
            set = self.colors[self.colorSet.index(color)]
            self.red.set(set[0])
            self.green.set(set[1])
            self.blue.set(set[2])