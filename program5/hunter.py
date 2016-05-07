# A Hunter is both Mobile_Simulton and Pulsator; it updates
#   as a Pulsator, but also moves (either in a straight line
#   or in pursuit of Prey), and displays as a Pulsator.


from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from prey import Prey
from math import atan2


class Hunter(Pulsator,Mobile_Simulton):
    sight_distance = 200
    def __init__(self,x,y):
        Pulsator.__init__(self,x,y)
        Mobile_Simulton.__init__(self,x,y,20,20,0,5)
        self.randomize_angle()
        self._color = "GREEN"
        
    def update(self,model):
        self.move()
        self.wall_bounce()
        Pulsator.update(self,model)
        preys = model.find(Prey)
        target = None
        for p in preys:
            if target == None:
                target = (p,self.distance(p.get_location()))
            elif self.distance(p.get_location())<target[1]:
                target = (p,self.distance(p.get_location()))
        if target == None:
            pass
        else:
            self.set_angle(atan2(target[0].get_location()[1]-self.get_location()[1],target[0].get_location()[0]-self.get_location()[0]))