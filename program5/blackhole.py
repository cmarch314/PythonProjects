# A Black_Hole is a Simulton; it updates by removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    def __init__(self,x,y):
        Simulton.__init__(self,x,y,20,20)
        self._color = "BLACK"
    def update(self,model):
        preys = model.find(Prey)
        eaten = set([s for s in preys if self.contains(s.get_location())])
        for s in eaten:
            model.remove(s)
        return eaten
        
    def display(self,canvas):
        canvas.create_oval(self.get_location()[0] - self.get_dimension()[0]/2, self.get_location()[1] - self.get_dimension()[1]/2,
                                self.get_location()[0] + self.get_dimension()[0]/2, self.get_location()[1] + self.get_dimension()[1]/2,
                                fill=self._color)