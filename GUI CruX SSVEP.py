from tkinter import Tk, Button 

class SampleApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.x = 0
        self.b = Button(self, text ="PRESS TO START", command = self.change_x_won) #choose text of the button here
        self.b.pack()
        self.configure(bg="Black") #choose color of the background before the light starts flashing here

    def change_x_won(self):
        if self["bg"] == "Black": #need to change background color here too
            self.configure(bg="Red") #choose color of the flashing light here
        elif self["bg"] == "Red": #need to change flashing light color here too
            self.configure(bg="Black") #need to change background color here too
        self.x += 1
        if self.x < 2*10: #the latter number is the amount of times the light flashes
            self.after(250, self.change_x_won) #the first parameter is how long the light is on in ms, this determines the frequency 
        else:
            self.x = 0
            self.configure(bg="Black") #need to change background color here too

if __name__ == "__main__":
    root = SampleApp()
    root.geometry("1500x800") #size dimensions of the pop-up window 
    root.mainloop()
