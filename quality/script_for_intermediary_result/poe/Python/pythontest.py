import ast
import codeop


def syntaxChecker(src):
    try:
        ast.parse(src)
        codeop.compile_command(src, symbol='exec')
        return True
    except:
        return False


if __name__ == '__main__':
    src = "def hello():\n    print(\'abc\')"
    if not codeop.compile_command(src, symbol='exec'):
        print("The source is not a complete command.")

