WELCOME_MSG = """Welcome."""
PROMPT = "> "

DEBUG = True
def debug(*args):
    if DEBUG == True:
        print("DEBUG: ", args)

class Place:
    """Each place is like a node in a graph
    Places have relations to next places, and items[]
    and people[]"""
    def __init__(self, desc, items=[], next={}, features=[]):
        # desc should be written in 2nd person: You are standing here
        self.desc = desc
        self.items = items
        # next should be a dict with key values 'N' 'E' 'W' 'S' 'U' 'D'
        self.next = next
        self.features = features

    def additem(self, item):
        self.items.append(item)

    def removeitem(self, item):
        return self.items.pop(self.items.index(item))

class Feature:
    """Features are like doors or chests in Places,
    and have special functionality which idk how ima make work.
    They can be <examine>'d """
    def __init__(self, name, desc):
        pass


class Item:
    """Items contain information about themselves, but
    information about them (held, place) is stored in Player
    or Place"""

    # make these derived classes?
    PLAIN = "plain"
    WEAPON = "weapon"
    FOOD = "food"

    def __init__(self, name, desc, itype=PLAIN):
        """Items need to be understandable in English; a sword, the sword
        distinctions need to be made. This will be done with 'adjectives'.
        Only the last word will be treated as the 'name' of the object; the
        words before it will be considered adjectives."""
        self.name = name.split()[-1]
        self.adjectives = name.split()[:-1]
        self.desc = desc
        self.itype = itype

    @property
    def stradj(self):
        stradj = ""
        for adj in self.adjectives:
            stradj += adj + ' '
        return stradj

    @property
    def specname(self):
        return "The " + self.stradj + self.name

    @property
    def genname(self):
        return "A " + self.stradj + self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Item(%s, %s, %s)"%(repr(self.name), repr(self.desc), repr(self.itype))

class Player:
    """All of the functions that the player can interactively
    run."""

    TAKEMSG = "Took %s."
    PUTMSG = "Put %s down."

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
        self.place = self.place.next[direc]
        return self.place.desc

    def take(self, item):
        # what if the place doesn't have that obj?
        self.inventory.append(self.place.removeitem(item))
        return Player.TAKEMSG%item.specname.lower()

    def put(self, item):
        self.place.additem(self.inventory.pop(self.inventory.index(item)))
        return Player.PUTMSG%item.specname.lower()

    def look(self): #add *info?
        # add support for "looking" up?
        # would require Place shit
        retval = self.place.desc + '\n'
        for item in self.place.items:
            retval += 'There is ' + item.genname.lower() + ' here. \n'
        return retval.strip()

    def error(self, info):
        return "Did not understand: " + str(info)

    def inv(self):
        if len(self.inventory) == 0:
            return "You're carrying nothing."
        retval = ""
        for i in self.inventory:
            retval += i.genname + '.\n'
        return retval.strip()

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

"""Alright. Commands will be parsed using a tree. I MEAN GRAPH
Paths will be complete, valid commands.
Each branch is a valid word following the current one.

Once reaching the end leaves, the path defines the function
which should be called.
This means, while traveling down the tree, relevant information
must be saved - so, each tree entry will have:
    a name
    a relevant piece of data (what object), if valid

If the next word does not correspond to a valid branch,
call error() with whatever information has be found so far.
"""

class CommandNode:
    def __init__(self, names, data, nextnodes=[]):
        self.nextnodes = nextnodes
        # add support for dif names, like n=north
        self.names = names
        self.data = data

    def moveTo(self, desirednext):
        debug("Looking for ", desirednext)
        for nextnode in self.nextnodes:
            debug("nextnodes.names:", nextnode.names)
            if desirednext in nextnode.names:
                # is a valid node to move to
                return nextnode
        return None # did not find valid node

    def __repr__(self):
        return "CommandNode(%s, %s, %s)"%(repr(self.names), repr(self.data), repr(self.nextnodes))

class DynCommandNode(CommandNode):
    """Refreshes the nextnodes list everytime it is queried"""
    def __init__(self, names, data, refreshf, refreshi, nextnodes=[]):
        self.refreshf = refreshf
        self.refreshi = refreshi # the info for refreshing, usually Player
        CommandNode.__init__(self, names, data, nextnodes)

    def moveTo(self, desirednext):
        self.nextnodes = self.refreshf(self.refreshi)
        debug("DynCmdNode refreshed nextnodes list.")
        return CommandNode.moveTo(self, desirednext)
    
def genItemGraph(itemlist):
    """Returns a list of nodes with valid words to refer to items in 
    itemlist.
    Allows us to extend our CommandGraph with straight (single option)
    branches which allow for the use of adjectives"""
    # add support for using "old sword" to refer to "rusty old sword"?

    def descendIntoItem(itemadjs, item):
        """Helper to make a straight (single option)
        branch of graph for a single item"""
        if len(itemadjs) == 0:
            return CommandNode([item.name], item)
        return CommandNode([itemadjs[0]], None, nextnodes=[descendIntoItem(itemadjs[1:], item)])

    # allow user to call item by adjectiveless name
    branches = [CommandNode(i.name, i) for i in itemlist]
    for item in itemlist:
        branches.append(descendIntoItem(item.adjectives, item))

    # reuse of adjectives may cause collisions!
    # this is really not memory efficient lol.
    for node in branches[:]:
        brancheswithoutcurnode = branches[:]
        brancheswithoutcurnode.remove(node)
        for othernode in brancheswithoutcurnode:
            if node.names == othernode.names:
                node.nextnodes.extend(othernode.nextnodes)
                branches.remove(othernode)

    debug("Inv graph:", branches)
    return branches


def genCommandGraph(player):
    """Sets up the graph which will represent valid commands.
    Takes player as a param to use pointers to player's data."""
    # constants & definitions:
    directionslist = [ ['n', "north"], ['e', "east"], ['s', "south"], ['w', "west"], ['u', "up"], ['d', "down"] ]
    firstlvlcmds = []
    # refresh functions, since the inv and place is dynamically changing
    invnodesf = genItemGraph # make sure to pass player.inventory as refreshi
    placeinodesf = genItemGraph # make sure to pass player.place.items as refreshi


    """ Zeroth level command """
    # contains all valid first words, and the error func to be called
    zerothnode = CommandNode(["basenode"], player.error, nextnodes=firstlvlcmds)
    """ First level commands """
    movecmd = CommandNode(["move", "go", "head"], player.move, nextnodes=[CommandNode(i,i[0]) for i in directionslist])
    firstlvlcmds.append(movecmd)

    invcmd = CommandNode(["inv", "inventory"], player.inv)
    firstlvlcmds.append(invcmd)

    putcmd = DynCommandNode(["put", "drop"], player.put, 
        invnodesf, player.inventory,
        nextnodes=invnodesf(player.inventory))
    firstlvlcmds.append(putcmd)

    takecmd = DynCommandNode(["take"], player.take,
        placeinodesf, player.place.items,
        nextnodes=placeinodesf(player.place.items))
    firstlvlcmds.append(takecmd)

    lookcmd = CommandNode(["look"], player.look)
    firstlvlcmds.append(lookcmd)

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


def genGameMap():
    """Connects all the Places, this is a graph, but simpler than Command
    Returns the starting location"""
    startloc = Place("Starting location",
        items=[Item("old, rusty sword", "A simple sword", itype=Item.WEAPON)],
        next={'n':Place("north of startloc")})

    return startloc



def pork():
    startloc = genGameMap()
    player = Player(startloc)
    print(WELCOME_MSG)
    print(player.look())
    cmdg = genCommandGraph(player)

    mainGameLoop(player, cmdg)

def mainGameLoop(player, cmdg):
    while 1:
        print()

        usrinput = input(PROMPT).strip()
        if usrinput != "":
            # parseCommand's return value still in design debate
            cmdinfo = parseCommand(usrinput, cmdg)
            debug("Command info: ", cmdinfo)
            for i in cmdinfo.items():
                debug("Ran function:", i)
                print( i[0](*i[1]) )


if __name__ == "__main__":
    pork()