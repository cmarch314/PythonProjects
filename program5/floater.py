# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


class Floater(Prey):
    def __init__(self,x,y):
        Prey.__init__(self,x,y,10,8,0,5)
        self.randomize_angle()
    
    def update(self,model):
        print()
        
        if random()*10 < 3:
            self.randomize_angle()
            self._speed += random()*10-5
            if self._speed > 7:
                self._speed =7
            if self._speed < 3:
                self._speed = 2
        
        self.move()
        self.wall_bounce()

    def display(self,canvas):
        '''
        ufo = PhotoImage(file='ufo.gif')
        canvas.create_image(*self.get_location(),image = ufo)
        '''
        canvas.create_oval(self.get_location()[0] - self.get_dimension()[0]/2, self.get_location()[1] - self.get_dimension()[1]/2,
                                self.get_location()[0] + self.get_dimension()[0]/2, self.get_location()[1] + self.get_dimension()[1]/2,
                                fill="RED")
        canvas.create_oval(self.get_location()[0] - self.get_dimension()[0]/4, self.get_location()[1] - self.get_dimension()[0]/4*1.5,
                                self.get_location()[0] + self.get_dimension()[0]/4, self.get_location()[1] + self.get_dimension()[1]/4*0.5,
                                fill="RED")
        