from porkglobals import *

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
    """Refreshes the nextnodes list everytime it is queried, by running:
    refreshf(refreshi), or if a tuple is supplied as the refresh info,
    refreshf(*refreshi)
    sets the self.nextnodes to the value returned."""
    def __init__(self, names, data, refreshf, refreshi, nextnodes=[]):
        self.refreshf = refreshf
        self.refreshi = refreshi # the info for refreshing, usually Player
        CommandNode.__init__(self, names, data, nextnodes)

    def moveTo(self, desirednext):
        if type(self.refreshi) == tuple:
            # called with a suffix or something
            self.nextnodes = self.refreshf(*self.refreshi)
        else:
            self.nextnodes = self.refreshf(self.refreshi)
        debug("DynCmdNode refreshed nextnodes list.")
        return CommandNode.moveTo(self, desirednext)
    
