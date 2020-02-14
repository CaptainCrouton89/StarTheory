# customformat.py
import os

styleDict = {"normal": 0, "bold":1, "faint":2, "italics":3}
fgDict = {"black": 30, "red":31, "green":32, "yellow":33,
    "blue":34, "magenta":35, "cyan":36, "white":37}
bgDict = {"black": 40, "red": 41, "green": 42, "yellow": 43,
    "blue": 44, "magenta": 45, "cyan": 46, "white": 47}


def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[0;38;40m", end="")

def getSize():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns), int(rows)


def printHeader0(string):
    clearScreen()
    x, y = getSize()
    print("——*——"*(int(x)//5)+"\n")
    print(f"{string:^{x}}".upper() + "\n")
    print("——*——"*(int(x)//5)+"\n")


def printHeader1(string, clear=True):
    if clear:
        clearScreen()
    x, y = getSize()
    # print('{0:*^{1}}'.format("*", x) + "\n")
    # print('{0:_<{1}}'.format("", x) + "\n")
    print("\n")
    print('{0:^{1}}'.format(string, x).upper() + "\n\n")
    print('{0:_<{1}}'.format("", x))
    # qprint('{0:*^{1}}\n'.format("*", x))

def printHeader2(string):
    x, y = getSize()
    print('{0:<{1}}'.format(string, x))
    print('{0:—<{1}}'.format("", x))

def printHeader3(string):
    x, y = getSize()
    print('{0:—^{1}}'.format(string, x).upper())

def printArray(lists):
    x, y = getSize()
    rows = len(lists[0])
    columns = len(lists)
    spacing = ' ' * (3)
    for row in range(rows):
        for column in range(columns):
            print("{0:>5}".format(str(lists[column][row])), end="")
        print()

def printCentered(string):
    x, y = getSize()
    print(string.center(x))

def printBalanced(row, size=1):
    x, y = getSize()
    blockSize = int(x) // (len(row) * size)
    for string in row:
        print("{0:<{1}}".format(string, blockSize), end="")
    print("\033[0;38;40m")


def printItalics(string):
    print("\033[3;38;40m{0}\033[3;38;40m".format(string), "\033[0;38;40m")

def font(string, style="normal", fg="white", bg="black"):
    f = "\033[" + str(styleDict[style]) + ";" + str(fgDict[fg]) + ";" + str(bgDict[bg]) + "m"
    return "{0}{1}".format(f, string)




