import os
from tkinter import *
import numpy as np
import time as t
from PIL import Image, ImageTk

os.chdir(os.path.dirname(__file__))
os.chdir("../P300_Online_Programs/face_images")
pathdir = os.getcwd()
class SampleApp(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.x = 0
        self.b = Button(self, text="PRESS TO START", command=self.change_x_won)  # choose text of the button here
        self.b.pack()
        self.configure(bg="Black")  # choose color of the background before the light starts flashing here

    def getIm(num, size):
        pic = Image.open(str(num) + ".jpg")
        resize_im = pic.resize((size,size))
        return ImageTk.PhotoImage(resize_im)


    def change_x_won(self):
        
        #canvas setup
        self.b.pack_forget()
        self.canvas = Canvas(self.master,highlightthickness=0) #create canvas to draw on
        self.canvas.configure(bg = 'black')

        #initialize stuff
        h = self.winfo_height()
        w = self.winfo_width()
        size = round(h / 4)
        
        #image choose
        imtype = [[]*2 for _ in range(5)]
        imtype[0] = [0,5]
        imtype[1] = [1,5]
        imtype[2] = [2,5]
        imtype[3] = [3,5]
        imtype[4] = [4,5]

        #get image path
        os.chdir(os.path.dirname(__file__))
        os.chdir("../P300_Online_Programs/face_images")

        #placement
        centerx = [w/2, size/2, w-size/2, size/2, w-size/2]
        centery = [h/2, size/2, size/2, h-size/2, h-size/2]
        
        #times
        sec = 50 * 1000 #time for flash (in ms)
        freqs = [2,2.6,3.5,4.4,5.3] #flashing frequency

        def times(time_end, freq):
            full = np.arange(0, time_end, freq)
            return full

        #intitialize display
        time = []
        images = []
        label = []
        for i in range(5):
            time.append(times(sec, freqs[i]))
            
            images.append(SampleApp.getIm(i,size))
           
            #generate image
            label.append(Label(image=images[i],bd = 0))
            label[i].image = images[i]
            label[i].place(x=centerx[i],y=centery[i],anchor="center")
        
        self.canvas.pack(fill = BOTH, expand = 1)

        #generate black box image
        images.append(ImageTk.PhotoImage(Image.new('RGB',(size,size))))

        #main flashing loop
        temptime = np.zeros(5, dtype=int)
        states = np.zeros(5, dtype = bool)
        
        for i in range(sec):
            for j in range(5):
                if i >= time[j][temptime[j]] and time[j][temptime[j]] != time[j][-1]:
                    states[j] = not states[j]
                    label[j].configure(image = images[imtype[j][states[j]]])
                    temptime[j] += 1
        
            self.canvas.update() # draw canvas (loop needs to be centered around this)
            t.sleep(0.001)

if __name__ == "__main__":
    root = SampleApp()
    #root.attributes('-fullscreen',True)  # size dimensions of the pop-up window
    root.geometry("1100x800")
    root.bind("<Escape>", lambda event:root.destroy())
    root.mainloop()
