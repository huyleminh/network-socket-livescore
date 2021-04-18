from tkinter import *
import math

class Login:
    def __init__(self, root):
        self.frame = Frame(root)
        # frame = Frame(root)
        # frame.pack()

        self.loginBtn = Button(self.frame, width = 25, height = 10, bg = "#DDDDDD", text = "Login", command = self.onClick)
        # self.loginBtn.pack()
    def onClick(self):
        pass
    def render(self):
        self.frame.pack()

        self.loginBtn.pack()

root = Tk()
root.title("Demo login client")

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

print({"witdh" : WIDTH, "height" : HEIGHT})

PADDING_LEFT = math.ceil(WIDTH / 4)
PADDING_TOP = math.ceil(HEIGHT / 8)

root.geometry(str(math.ceil(WIDTH / 2)) + "x" + str(math.ceil(HEIGHT / 2)) + "+" + str(PADDING_LEFT) + "+" + str(PADDING_TOP))

login = Login(root)
login.render()

root.mainloop()