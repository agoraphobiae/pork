WELCOME_MSG = """Welcome."""
PROMPT = "> "

DEBUG = False
def debug(*args):
    if DEBUG:
        print("DEBUG: ", end='')
        for arg in args:
            print(arg, end=' | ')
        print()

EXIT = False #because event handling is for chumps