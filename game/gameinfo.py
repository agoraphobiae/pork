from porkglobals import *

class Place:
    """Each place is like a node in a graph
    Places have relations to next places, and items[]
    and people[]

    Each Place's self.next ought to have a key for each direction,
    even if that direction does not lead to another place."""
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

    def isNextPlace(self, direc):
        return isinstance(self.next[direc], Place)

    def __str__(self):
        return self.desc

    def __repr__(self):
        return "Place(%s, %s, %s, %s)"%(repr(self.desc), repr(self.items), repr(self.next), repr(self.features))


class Adjectiveable:
    """God what a gross name. Adjs are things that need to be understood
    in an English way, with adjectives. We need the data set up to support
    generating the proper command graph with the adjectives."""
    
    def __init__(self, name, desc):
        """Items need to be understandable in English; a sword, the sword
        distinctions need to be made. This will be done with 'adjectives'.
        Only the last word will be treated as the 'name' of the object; the
        words before it will be considered adjectives."""
        self.name = name.split()[-1]
        self.adjectives = name.split()[:-1]
        self.desc = desc

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
        return "Adjectiveable(%s, %s)"%(repr(self.name), repr(self.desc))


class Item(Adjectiveable):
    """Items contain information about themselves, but
    information about them (held, place) is stored in Player
    or Place"""

    def __init__(self, name, desc, weight=2):
        self.weight = weight
        Adjectiveable.__init__(self, name, desc)

    def __repr__(self):
        return "Item(%s, %s, %s)"%(repr(self.name), repr(self.desc), repr(self.weight))

class Food(Item):
    """An edible item, which replenishes hunger and heals.
    and is delicious."""
    # is a hunger system like minecraft necessary or just annoying?
    def __init__(self, name, desc, hungerval, hungerdecay, healval, weight=1):
        """hungerval determines how much the food will heal, and hungerdecay
        is the strength of fullness: how fast the fullness will decay after eating."""
        self.hungerval = hungerval
        self.hungerdecay = hungerdecay
        self.healval = healval
        Item.__init__(self, name, desc, weight=weight)

    def __repr__(self):
        return "Food(%s, %s, %s, %s, %s)"%(repr(self.name), repr(self.desc),
            repr(self.hungerval), repr(self.hungerdecay), repr(self.healval), repr(self.weight))

class Weapon(Item):
    def __init__(self, name, desc, dmgamt, weight=1):
        self.dmgamt = dmgamt
        Item.__init__(self, name, desc, weight=weight)

    def __repr__(self):
        return "Weapon(%s, %s, %s, %s)"%(repr(self.name), repr(self.desc), repr(self.dmgamt), repr(self.weight))


class Feature(Adjectiveable):
    """Features are like doors or chests in Places,
    and have special functionality which idk how ima make work.
    They can be <examine>'d """
    def __init__(self, name, desc):
        Adjectiveable.__init__(self, name, desc)