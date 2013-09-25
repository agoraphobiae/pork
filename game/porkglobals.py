WELCOME_MSG = """Welcome."""
PROMPT = "> "

DEBUG = False
def debug(*args):
    if DEBUG:
        #print("DEBUG: ", end = '')
        print "DEBUG: ",
        for arg in args:
            print arg, ' | ',
        print
        print
        #     print(arg, end=' | ')
        # print()
        # print()

EXIT = False #because event handling is for chumps