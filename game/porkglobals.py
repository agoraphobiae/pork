from __future__ import print_function

WELCOME_MSG = """Welcome."""
PROMPT = "> "

DEBUG = False
def debug(*args):
    if DEBUG:
        print("DEBUG: ", end = '')
        #print "DEBUG: ",
        for arg in args:
            print(arg, end=' | ')
        print()
        print()
        #     print arg, ' | ',
        # print
        # print

EXIT = False #because event handling is for chumps