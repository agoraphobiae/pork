WELCOME_MSG = """Welcome."""
PROMPT = "> "

DEBUG = True
def debug(*args):
    if DEBUG:
        print("DEBUG: ", end='')
        for arg in args:
            print(arg, end=' | ')
        print()
        print()

EXIT = False #because event handling is for chumps