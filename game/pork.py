from __future__ import print_function

# jesus h christ that namespacing
from porkcmd import *
from porkglobals import *
from gameinfo import *
from game import *

from time import sleep
import sys

class Player:
    """All of the functions that the player can interactively
    run."""

    TAKEMSG = "Took %s."
    PUTMSG = "Put %s down."
    INVMAX = 25 #kg
    INVMAXMSG = "You are carrying too much, you must drop something first."
    DIRERRMSG = "You can't go that way."
    EXITMSGSTART = "Your eyes slowly close"
    EXITMSGEND = "Goodnight.\n\n"

    def __init__(self, place):
        self.name = ""
        self.place = place
        self.inventory = []

    def move(self, *direc):
        """Returns what to print"""
        # if user types just "move", this will be called with no params
        if len(direc) == 0:
            return "Move where?"
        direc = direc[0]
        if direc in self.place.next:
            if self.place.isNextPlace(direc):
                self.place = self.place.next[direc]
                return self.look()
            else:
                return self.place.next[direc]
        else:
            # really, each next dict should be made with a msg for nonvalid direcs
            # but just in case.
            return self.DIRERRMSG

    def take(self, *item):
        """Appends item to inventory by removing it from self.place, checking
        if the inventory can fit it first."""
        if len(item) == 0:
            return "Take what?"
        item = item[0]
        if item.weight + self.invweight > self.INVMAX:
            return self.INVMAXMSG
        self.inventory.append(self.place.removeitem(item))
        return self.TAKEMSG%item.specname.lower()

    def drop(self, *item):
        """Appends item into self.place, by popping it off the inventory."""
        if len(item) == 0:
            return "Drop what?"
        item = item[0]
        debug("Placing item down: ", item)
        self.place.additem(self.inventory.pop(self.inventory.index(item)))
        return self.PUTMSG%item.specname.lower()

    def look(self): #add *info?
        # add support for "looking" up?
        # would require Place shit
        retval = self.place.desc + '\n'
        for item in self.place.items:
            retval += 'There is ' + item.genname.lower() + ' here. \n'
        return retval.strip()

    def error(self, info):
        debug("Error. Player is at: ", self.place.desc)
        return "Did not understand: " + str(info)

    def inv(self):
        if len(self.inventory) == 0:
            return "You're carrying nothing."
        retval = ""
        for i in self.inventory:
            retval += i.genname + '.\n'
        return retval.strip()

    def exit(self, *args):
        global EXIT
        EXIT = True
        print(self.EXITMSGSTART, end='')
        #print self.EXITMSGSTART,
        for _ in range(3):
        #for _ in xrange(3):
            sys.stdout.flush()
            sleep(0.5)
            print('.', end='')
            #sys.stdout.write('.')
        print()
        #print
        return self.EXITMSGEND

    @property
    def invweight(self):
        weight = 0
        for i in self.inventory:
            weight += i.weight
        return weight

    # was going to use this dictionary but realized useless
    # if the CommandGraph stores function info, we don't need
    # to look it up.
    #
    # keys are values that parseCommand() returns
    # cmd = {'move':move,
    #     'error':error,
    #     'inv':inv,
    #     'put':put,
    #     'take':take}

def genItemGraph(itemlist, suffix=None):
    """Takes a list of items and a suffix, which is a word which
    must come after the item name to form a complete command.
    i.e. suffix="down" -> "put sword" invalid, "put sword down" valid
    Returns a list of nodes with valid words to refer to items in 
    itemlist.
    Allows us to extend our CommandGraph with straight (single option)
    branches which allow for the use of adjectives"""

    def descendIntoItem(itemadjs, item):
        """Helper to make a straight (single option)
        branch of graph for a single item"""
        if len(itemadjs) == 0:
            if suffix:
                debug("Making item node with suffix: ", suffix)
                return CommandNode([item.name], None, nextnodes=[CommandNode([suffix], item)])
            return CommandNode([item.name], item)
        return CommandNode([itemadjs[0]], None, nextnodes=[descendIntoItem(itemadjs[1:], item)])

    # allow user to call item by adjectiveless name
    if suffix:
        branches = [CommandNode([i.name], None, nextnodes=[CommandNode([suffix], i)]) for i in itemlist]
    else:
        branches = [CommandNode([i.name], i) for i in itemlist]
    for item in itemlist:
        branches.append(descendIntoItem(item.adjectives, item))

    # reuse of adjectives may cause collisions!
    # also, multiple swords causes confusion
    for node in branches[:]:
        brancheswithoutcurnode = [x for x in branches if x != node]
        for othernode in brancheswithoutcurnode:
            if node.names == othernode.names:
                node.nextnodes.extend(othernode.nextnodes)
                branches.remove(othernode)

    debug("Item graph:", branches)
    return branches


def genCommandGraph(player):
    """Sets up the graph which will represent valid commands.
    Takes player as a param to use pointers to player's data."""
    # constants & definitions:
    directionslist = [ ['n', "north"], ['e', "east"], ['s', "south"], ['w', "west"], ['u', "up"], ['d', "down"] ]
    firstlvlcmds = []
    # refresh functions, since the inv and place is dynamically changing


    """ Zeroth level command """
    # contains all valid first words, and the error func to be called
    zerothnode = CommandNode(["basenode"], player.error, nextnodes=firstlvlcmds)
    """ First level commands """
    movecmd = CommandNode(["move", "go", "head"], player.move, nextnodes=[CommandNode(i,i[0]) for i in directionslist])
    firstlvlcmds.append(movecmd)

    invcmd = CommandNode(["inv", "inventory"], player.inv)
    firstlvlcmds.append(invcmd)

    # player.inventory is a pointer to the current Player obj's inv
    # but since player is static, this is not a problem.. yet
    dropcmd = DynCommandNode(["drop"], player.drop, 
        genItemGraph, player.inventory,
        nextnodes=genItemGraph(player.inventory))
    firstlvlcmds.append(dropcmd)

    # needed for proper refresh
    # because if player.place changes
    # player.place.items won't change accordingly.
    takerefresh = lambda player: genItemGraph(player.place.items)
    takecmd = DynCommandNode(["take"], player.take,
        takerefresh, player,
        nextnodes=genItemGraph(player.place.items))
    firstlvlcmds.append(takecmd)

    def pickrefresh(player, suffix):
        l = genItemGraph(player.place.items, suffix)
        l.append(CommandNode([suffix], None, nextnodes=genItemGraph(player.place.items)))
        return l
    # supports "pick item up", "pick up item"
    pickupcmd = DynCommandNode(["pick"], player.take,
        pickrefresh, (player, "up"),
        nextnodes=[
        DynCommandNode(["up"], None, takerefresh, player, nextnodes=genItemGraph(player.place.items)),
        pickrefresh(player, "up")
        ])
    firstlvlcmds.append(pickupcmd)

    def putrefresh(player, suffix):
        l = genItemGraph(player.inventory, suffix)
        l.append(CommandNode([suffix], None, nextnodes=genItemGraph(player.inventory)))
        return l
    putcmd = DynCommandNode(["put"], player.drop,
        putrefresh, (player, "down"),
        nextnodes=[
        DynCommandNode(["down"], None, genItemGraph, player.inventory, nextnodes=genItemGraph(player.inventory)),
        putrefresh(player, "down")
        ])
    firstlvlcmds.append(putcmd)

    lookcmd = CommandNode(["look"], player.look)
    firstlvlcmds.append(lookcmd)

    exitcmd = CommandNode(["exit", "leave"], player.exit)
    firstlvlcmds.append(exitcmd)

    return zerothnode

def parseCommand(cmd, cmdg):
    """Reads through each word in the user's command, travels
    down the CommandGraph using these words, and returns a dictionary
    with keys as functions to be called and values as parameters for those
    functions"""

    cmd = cmd.lower() #maybe care about caps for pronouns?
    cmd = cmd.split()

    retdata = []
    curnode = cmdg
    # for each word, check if in graph
    # if is valid next node, save some data and move to that node
    for i in cmd:
        curnode = curnode.moveTo(i)
        if curnode == None: #no valid node
            return {cmdg.data:[i]} #return error func
        # we may travel down dataless nodes: like adjectives for items,
        # only the last node, the item name, need to have info
        if curnode.data != None:
            retdata.append(curnode.data)
        elif i == cmd[-1]:
            # last node cant be empty; this happens when items adjs
            # are used without the item name at the end, e.g. "take old"
            debug("Last commandnode found to be empty. Calling error.")
            return {cmdg.data:[i]}

    debug("parseCommand returndata: ", retdata)

    # turn retdata into a function dictionary
    # keys: function values: params
    retdatad = {}
    i = 0
    # look at each item in list. if item is func,
    # add it and the immediate following non func
    # items to dict.
    while i < len(retdata):
        if hasattr(retdata[i], "__call__"):
            j = i + 1
            retdatad[retdata[i]] = []
            while j < len(retdata) and hasattr(retdata[j], "__call__") == False:
                retdatad[retdata[i]].append(retdata[j])
                j += 1
                i += 1
        i += 1

    return retdatad


def pork():
    startloc = genGameMap()
    player = Player(startloc)
    print(WELCOME_MSG)
    print(player.look())
    #print WELCOME_MSG
    #print player.look()
    cmdg = genCommandGraph(player)

    mainGameLoop(player, cmdg)

def mainGameLoop(player, cmdg):
    while not EXIT:
        print()
        #print

        try:
            # usrinput = input(PROMPT).strip()
            usrinput = raw_input(PROMPT).strip()
        except EOFError as e:
            # ^D ends the game
            usrinput = ""
            print(player.exit())
            #print player.exit()
        except NameError as e:
            # alright. python 3 wrangling. ugh.
            if e.args[0].find("raw_input") != -1:
                usrinput = input(PROMPT).strip()

        if usrinput != "":
            # parseCommand's return value still in design debate
            cmdinfo = parseCommand(usrinput, cmdg)
            debug("Command info: ", cmdinfo)
            for i in cmdinfo.items():
                debug("Ran function:", i)
                # print i[0](*i[1]) 
                print( i[0](*i[1]) )
                # jesus h christ that readability


if __name__ == "__main__":
    pork()