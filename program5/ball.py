# A Ball is Prey; it updates by moving in a straight
#   line and displays as blue circle with a radius
#   of 5 (width/height 10).

from prey import Prey

class Ball(Prey):
    def __init__(self,x,y):
        Prey.__init__(self,x,y,10,10,0,5)
        self.randomize_angle()
        self._color = "BLUE"
    def update(self,model):
        self.move()
        self.wall_bounce()

    def display(self,canvas):
        canvas.create_oval(self.get_location()[0] - self.get_dimension()[0]/2, self.get_location()[1] - self.get_dimension()[1]/2,
                                self.get_location()[0] + self.get_dimension()[0]/2, self.get_location()[1] + self.get_dimension()[1]/2,
                                fill=self._color)