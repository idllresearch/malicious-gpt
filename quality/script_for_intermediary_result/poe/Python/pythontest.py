import codeop


def syntaxChecker(src):
    try:
        codeop.compile_command(src, symbol='exec')
        return True
    except:
        return False
