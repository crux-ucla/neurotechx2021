from tkinter import *
import numpy as np
import time as t

class SampleApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.x = 0
        self.b = Button(self, text="PRESS TO START", command=self.change_x_won)  # choose text of the button here
        self.b.pack()
        self.configure(bg="Black")  # choose color of the background before the light starts flashing here

    def change_x_won(self):

        self.canvas = Canvas(self.master) #create canvas to draw on

        #initialize stuff
        h = root.winfo_height() #gets height of screen
        w_rects = np.linspace(0,root.winfo_width(),6) #splits screen horizontally (n+1)
        sec = 20 * 10 #time for flash (in tenths of second, I tested most precise. Not sure if multithreading can make faster) (CHANGE THIS VALUE)

        # set colors
        color = [[]*2 for _ in range(5)]
        color[0] = ["Red","Black"]
        color[1] = ["Green","Black"]
        color[2] = ["Blue","Black"]
        color[3] = ["Magenta","Black"]
        color[4] = ["Yellow","Black"]

        freqs = [1,2,3,4,5] #changes per second (CHANGE THESE VALUES)

        # create time array
        def times(time_end, freq):
            return np.arange(0, time_end, 1 / freq * 10)
        
        #make 2D array for later access
        time = []
        rec = []
        for i in range(5):
            #list of times to change color in seconds (can do more... like to 5)
            time.append(times(sec, freqs[i]))
            
            #create objects, (if set as variable, can later create loops to change color)
            rec.append(self.canvas.create_rectangle(w_rects[i],0,w_rects[i+1],h,fill = color[i][0],outline=""))

        self.canvas.pack(fill = BOTH, expand = 1)

        temptime = np.zeros(5, dtype=int)
        colors = np.zeros(5, dtype = bool)

        #Run thing
        for i in range(sec):
            for j in range(5):
                if i >= time[j][temptime[j]] and time[j][temptime[j]] != time[j][-1]:
                    colors[j] = not colors[j]
                    self.canvas.itemconfig(rec[j],fill=color[j][colors[j]]) #example of changing rectangle color
                    temptime[j] += 1
                    print(j, " changes color at ", i, " time and new time is ", time[j][temptime[j]])
        
            self.canvas.update() # draw canvas (loop needs to be centered around this)
            print(i)
            t.sleep(0.1)


if __name__ == "__main__":
    root = SampleApp()
    root.geometry("1500x800")  # size dimensions of the pop-up window
    root.mainloop()
