from customFormat import *
import time
import StarTheory


class Story(object):

    def __init__(self, gameManager):
        self.game = gameManager

    def firstStart(self):
        clearScreen()
        time.sleep(3)
        print("Get in.")
        time.sleep(2)
        printItalics("You stare back at him.")
        time.sleep(3)
        print("Get in! Get in now!")
        time.sleep(1.5)
        printItalics("You don't really want to.")
        time.sleep(2)
        print("...Please!")
        time.sleep(3)
        printItalics("You climb into the cryo-sleep casket.")
        time.sleep(3)
        print("Did you remember to check the coolant pump? and the p-generator?")
        time.sleep(2)
        printItalics("You had checked 4 times.")
        time.sleep(3)
        print("Fine, I know you’re angry with me. Talk to me.")
        time.sleep(2)
        printItalics("You lay down, feeling the cool foam press against your shoulder blades. You reach for the control pad. It’s more comfortable down here than you expected.")
        time.sleep(5)
        print("This isn’t something I can let you help me with, it’s too dangerous. And I have to stay—I need to try to fix this, otherwise I’d be no better than them. You understand that, don’t you?")
        time.sleep(6)
        printItalics(
            "You’d already had this argument with him. Why didn’t he see the irony?")
        time.sleep(4)
        print("Please say something? You do understand, right?")
        time.sleep(3)
        printItalics(
            "The date was already sequenced. You just needed to enter the security pin and the lid would seal.")
        time.sleep(4)
        print("Anything? ...Son?")
        time.sleep(4)
        printItalics("There, that was it. Five years. Just five years.")
        time.sleep(4)
        print("...{0}?".format(self.game.player.name))
        time.sleep(2)
        printItalics(
            "Just a nap, you imagine... Was it getting colder already?")
        time.sleep(3)
        print("Can you still hear me?")
        time.sleep(3)
        printItalics("It was definitely getting cold. So very, very, cold...")
        time.sleep(5)
        print("I love you.")
        time.sleep(4)
        printItalics("Darkness")
        time.sleep(5)
        print("")
        clearScreen()
        self.yearsGoBy()

    def yearsGoBy(self):
        p = 2
        i = 0
        max = 384
        while i < max:
            clearScreen()
            print("Year: {0}".format(i + 3429))
            if i > 5 and i < (max - 15):
                p -= .1
            else:
                p += .1
            if p < 0:
                p = .01
            time.sleep(p)
            i += 1
        time.sleep(3)
        clearScreen()
        printItalics("Oh no")
        time.sleep(4)
        printItalics("press any key to continue")
        input()
