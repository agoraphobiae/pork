from gameinfo import *
from porkglobals import *

def genGameMap():
    """Connects all the Places, this is a graph, but simpler than Command
    Returns the starting location"""

    # python objs are pointers, putting an object in two places on accident
    # would make some weird behavior
    shittystartersword = Weapon("old, rusty sword", "A simple sword", 2, weight=2)

    startlocnext = {'e':"There is a wall there."}
    startloc = Place("You are in a field. Swaying, golden grass surrounds you in all directions.",
        items=[shittystartersword],
        next=startlocnext)

    field1next = {'s':startloc}
    field1 = Place("You are in a field. Golden, swaying grass surrounds you in all directions.",
        next=field1next)
    startlocnext['n'] = field1

    return startloc