from gameinfo import *
from porkglobals import *

def genGameMap():
    """This is an "abstract function" to hold this docstring and information. 
    A GameMap function defines Places and connects all the Places it defines in 
    a graph, but simpler graph than CommandGraph. It simply uses Place.nextnodes.
    
    A GameMap function returns the starting location."""

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


def goldenfieldMap():
    # python objs are pointers, putting an object in two places on accident
    # would make some weird behavior
    shittystartersword = Weapon("old, rusty sword", "A simple sword, obviously aged and covered in rust.", 2, weight=2)
    
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

    # wait why the hell am i not just doing Place.next = {}
    aSecretRoomNext = {'u':startloc}
    aSecretRoom = Place(("You find yourself in a secret room. The walls glare down at you, but otherwise the room is quiet. There "
        "is a painting on the wall in front of you, flanked by two statues of what appear to be kneeling warriors."),
        next=aSecretRoomNext)
    warriorStatue = Feature("warrior statue", ("A statue of a kneeling warrior. He faces down, with one hand on the hilt of his sheathed sword and "
        "the other in a fist."))
    painting = Feature("painting", "A painting of a bowl of fruit. A note attached to it says, do not to this.")
    aSecretRoom.features = [warriorStatue, painting]
    startlocnext['d'] = aSecretRoom

    return startloc

if DEBUG:
    genGameMap = testGameMap

# ghetto map choosing
genGameMap = goldenfieldMap