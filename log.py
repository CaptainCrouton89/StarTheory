class Log(object):

    def __init__(self, fname):
        fname = "logs/" + fname + ".txt"
        self.file = open(fname, "w+")

    def log(self, *args, console=False):
        string = "\n\nINFO:"
        for arg in args:
            string += " " + str(arg)
            if console:
                print(str(arg))
        self.file.write(string)
