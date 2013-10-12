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

    def visualize(self):
        if len(self.nextnodes) == 0:
            return self.names[0]
        retval = ""
        for node in self.nextnodes:
            retval += node.visualize() + ' '
        retval = self.names[0] + '-'*(len(retval)-len(self.names[0])) + '\n' + retval

    def __repr__(self):
        """This only has doctests/docstring because it has
        weird infinite recursion problems, which I think
        come from repr()ing CommandNodes inside self.nextnodes

        >>> node1 = CommandNode(["repr"], 10, nextnodes=["repr"])
        >>> node1
        CommandNode(['repr'], 10, nextnodes=['repr'])
        >>> node2 = CommandNode(['now for a neg test'], -1, nextnodes=[node1])
        >>> node2
        CommandNode(['now for a neg test'], -1, nextnodes=[CommandNode(['repr'], 10, nextnodes=['repr'])])
        >>> node3n = []; node3 = CommandNode(['break already'], 2, nextnodes=node3n)
        >>> node4 = CommandNode(['inf loop'], 10, nextnodes=[node3]); node3n.append(node4)
        >>> node3
        CommandNode(['break already'], 2, nextnodes=[CommandNode(['inf loop'], 10, nextnodes=[...])])
        """
        return "CommandNode(%s, %s, nextnodes=%s)"%(repr(self.names), repr(self.data), repr(self.nextnodes))

    def __eq__(self, other):
        """A CommandNode is equal to another CommandNode if the
        list of names for each are equal, the data they contain
        is equal, and the lists of valid nextnodes is equal.

        >>> node1 = CommandNode(["equal"], 4, nextnodes=["equal"])
        >>> node2 = CommandNode(["equal"], 4, nextnodes=["equal"])
        >>> node1 == node2
        True
        >>> node3 = CommandNode("equal", 4, nextnodes=["equal"]) #not equal
        >>> node2 == node3
        False
        >>> node4 = CommandNode(["equal"], 5, nextnodes=["equal"]) #not equal
        >>> node4 == node2
        False
        >>> node5 = CommandNode(["equal"], 4, nextnodes=["equal", "not"])
        >>> node5 == node1
        False
        """
        # # Robert Huang CS61A disc
        # if self.names != other.names:
        #     return False
        # if len(self.nextnodes) != len(other.nextnodes):
        #     return False

        return isinstance(other, type(self)) and self.names == other.names and self.data == other.data and self.nextnodes == other.nextnodes

    def __ne__(self, other):
        return not self.__eq__(other)

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
        if isinstance(self.refreshi, tuple):
            # called with a suffix or something
            self.nextnodes = self.refreshf(*self.refreshi)
        else:
            self.nextnodes = self.refreshf(self.refreshi)
        debug("DynCmdNode refreshed nextnodes list.")
        return CommandNode.moveTo(self, desirednext)
    
