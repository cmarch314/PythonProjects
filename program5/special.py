from prey import Prey
from hunter import Hunter
from ball import Ball
from floater import Floater
class Special(Ball):
    mode = "move"
    delay_counter = 20
    unleash_counter = 2
    def __init__(self,x,y):
        Ball.__init__(self,x,y)
        self._color = "BROWN"
        self.set_dimension(10, 10)
        self.time_count = 0
        self.set_speed(6)
    def update(self,model):
        self.time_count+=1
        if self.mode == "move":
            self.move()
            if self.time_count == self.delay_counter:
                self.mode = "unleash"
                self.time_count = 0
        else:
            model.add(Ball(self.get_location()[0],self.get_location()[1]))
            model.add(Floater(self.get_location()[0],self.get_location()[1]))
            if self.time_count == self.unleash_counter:
                self.mode = "move"
                self.time_count = 0 
    
    def display(self,canvas):
        
        canvas.create_oval(self.get_location()[0] - self.get_dimension()[0], self.get_location()[1] - self.get_dimension()[1],
                                self.get_location()[0] + self.get_dimension()[0], self.get_location()[1] + self.get_dimension()[1],
                                )
        canvas.create_oval(self.get_location()[0] - self.get_dimension()[0]/2, self.get_location()[1] - self.get_dimension()[1]/2,
                                self.get_location()[0] + self.get_dimension()[0]/2, self.get_location()[1] + self.get_dimension()[1]/2,
                                fill=self._color)
        