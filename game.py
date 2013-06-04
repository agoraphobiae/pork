from gameinfo import *
from porkglobals import *

def testGameMap():
    """ ***TEST CASES*** """
    # testing item adj/name collision
    testsword = Weapon("elvish sword", "A blade of Elvish make.", 2, weight=2)
    testsword2 = Weapon("rusty elvish sword", "A discarded old blade of Elvish steel.", 2)
    testsword3 = Weapon("sword elvish rusty", "A mix of adjectives to fuck with you.", 2)

    startlocnext = {}
    startloc = Place("Sword testing location.",
        items=[testsword,testsword2,testsword3],
        next=startlocnext)

    return startloc


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

    field2next = {'n':startloc}
    field2 = Place("You are in a field with golden, swaying grass in all directions.",
        next=field2next)
    startlocnext['s'] = field2


    return startloc

if DEBUG:
    genGameMap = testGameMap