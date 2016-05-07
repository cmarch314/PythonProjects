# Ho Choi, Lab 1
# I certify that I written all the code in this programming assignment
#   by myself.

import controller, sys
import model   #strange, but we need a reference to this module to pass this module to update

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special

# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running = False
cycle_count = 0;
simulations = set();
cur_kind = "Ball"


#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running,cycle_count,simulations
    running = False;
    cycle_count = 0;
    simulations = set()
    display_all()
    


#start running the simulation
def start ():
    global running
    running = True



#stop running the simulation (freezing it)
def stop ():
    global running
    running = False 


#step just one update in the simulation
def step ():
    global running
    running = False 

    global cycle_count
    cycle_count += 1
    for s in simulations:
        s.update(model)


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global cur_kind 
    cur_kind = kind
    


#add the kind of remembered object to the simulation (or remove any objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    global cur_kind
    if cur_kind == "Remove":
        for s in simulations.copy():
            if s.contains((x,y)):
                remove(s)
    else:
        simulation = eval(cur_kind+"("+str(x)+","+str(y)+")")
        add(simulation)
    

#add simulton s to the simulation
def add(s):
    simulations.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    simulations.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    return set([s for s in simulations if isinstance(s,p)])


#call update for every simulton in the simulation
def update_all():
    global cycle_count
    if running:
        cycle_count += 1
        for s in simulations.copy():
            s.update(model)

    


#delete from the canvas every simulton in the simulation, and then call display for every
#  simulton in the simulation to add it back to the canvas possibly in a new location: to
#  animate it; also, update the progress label defined in the controller
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    
    for s in simulations:
        s.display(controller.the_canvas)
    
    controller.the_progress.config(text=str(len(simulations))+" objects/"+str(cycle_count)+" cycles")
