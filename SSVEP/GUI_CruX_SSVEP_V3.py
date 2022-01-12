from tkinter import *
import numpy as np
import time as t
import sys

class SampleApp(Tk):
        
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.x = 0
        self.b = Button(self, text="PRESS TO START", command=self.change_x_won)  # choose text of the button here
        self.b.pack()
        self.configure(bg="Black")  # choose color of the background before the light starts flashing here

    def change_x_won(self):
        
        self.b.pack_forget()
        self.canvas = Canvas(self.master) #create canvas to draw on
        self.canvas.configure(bg = 'black')

        #initialize stuff
        h = self.winfo_height()
        w = self.winfo_width()
        size = h / 4

        #placement
        centerx = [w/2, size/2, w-size/2, size/2, w-size/2]
        centery = [h/2, size/2, size/2, h-size/2, h-size/2]
        x1 = centerx - size/2 * np.ones(5)
        x2 = centerx + size/2 * np.ones(5)
        y1 = centery - size/2 * np.ones(5)
        y2 = centery + size/2 * np.ones(5)

        sec = 50 * 1000 #time for flash (in ms)

        color = [[]*2 for _ in range(5)]
        color[0] = ["Red","Black"]
        color[1] = ["Green","Black"]
        color[2] = ["Blue","Black"]
        color[3] = ["Magenta","Black"]
        color[4] = ["White","Black"]
        
        #letters
        textletter =["a","b","c","d","e"]
        freqs = [2,2.6,3.5,4.4,5.3] #flashing frequency

        def times(time_end, freq):
            full = np.arange(0, time_end, freq)
            return full
            
        text = []
        time = []
        rec = []
        for i in range(5):
            #list of times to change color in seconds (can do more... like to 5)
            time.append(times(sec, freqs[i]))
            
            #create objects, (if set as variable, can later create loops to change color)
            rec.append(self.canvas.create_rectangle(x1[i],y1[i],x2[i],y2[i],fill = color[i][0],outline=""))
            text.append(Label(self, text = textletter[i], bg = color[i][0], bd = 0,
                         font = ("Helvetica", 40)))
            text[i].place(x=centerx[i],y=centery[i], anchor="center")
        self.canvas.pack(fill = BOTH, expand = 1)

        temptime = np.zeros(5, dtype=int)
        colors = np.zeros(5, dtype = bool)

        for i in range(sec):
            for j in range(5):
                if i >= time[j][temptime[j]] and time[j][temptime[j]] != time[j][-1]:
                    colors[j] = not colors[j]
                    self.canvas.itemconfig(rec[j],fill=color[j][colors[j]]) #example of changing rectangle color
                    text[j].configure(bg = color[j][colors[j]])
                    temptime[j] += 1
        
            self.canvas.update() # draw canvas (loop needs to be centered around this)
            t.sleep(0.001)


if __name__ == "__main__":
    root = SampleApp()
    #root.attributes('-fullscreen',True)  # size dimensions of the pop-up window
    root.geometry("1100x800")
    root.bind("<Escape>", lambda event:root.destroy())
    root.mainloop()
