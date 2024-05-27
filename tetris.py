# remeber this is only for pycharm
from tkinter import *
from time import sleep
from random import *
from tkinter import messagebox


class Teris:
    def __init__(self):
      
        self.color = ['red', 'orange', 'yellow', 'purple', 'blue', 'green', 'pink']
      
        self.shapeDict = {1: [(0, 0), (0, -1), (0, -2), (0, 1)], 
                          2: [(0, 0), (0, -1), (1, -1), (1, 0)],  
                          3: [(0, 0), (-1, 0), (0, -1), (1, 0)],  
                          4: [(0, 0), (0, -1), (1, 0), (2, 0)], 
                          5: [(0, 0), (0, -1), (-1, 0), (-2, 0)],  
                          6: [(0, 0), (0, -1), (-1, -1), (1, 0)], 
                          7: [(0, 0), (-1, 0), (0, -1), (1, -1)]}  
       
        self.rotateDict = {(0, 0): (0, 0), (0, 1): (-1, 0), (0, 2): (-2, 0), (0, -1): (1, 0),
                           (0, -2): (2, 0), (1, 0): (0, 1), (2, 0): (0, 2), (-1, 0): (0, -1),
                           (-2, 0): (0, -2), (1, 1): (-1, 1), (-1, 1): (-1, -1),
                           (-1, -1): (1, -1), (1, -1): (1, 1)}
      
        self.coreLocation = [4, -2]
        self.height, self.width = 20, 10
        self.size = 32
     
        self.map = {}
        
        for i in range(self.width):
            for j in range(-4, self.height):
                self.map[(i, j)] = 0
      
        for i in range(-4, self.width + 4):
            self.map[(i, self.height)] = 1
        for j in range(-4, self.height + 4):
            for i in range(-4, 0):
                self.map[(i, j)] = 1
        for j in range(-4, self.height + 4):
            for i in range(self.width, self.width + 4):
                self.map[(i, j)] = 1

      
        self.score = 0
        self.isFaster = False
       
        self.root = Tk()
        self.root.title("Teris")
        self.root.geometry("500x645")
        self.area = Canvas(self.root, width=320, height=640, bg='white')
        self.area.grid(row=2)
        self.pauseBut = Button(self.root, text="Pause", height=2, width=13, font=(18), command=self.isPause)
        self.pauseBut.place(x=340, y=100)
        self.startBut = Button(self.root, text="Start", height=2, width=13, font=(18), command=self.play)
        self.startBut.place(x=340, y=20)
        self.restartBut = Button(self.root, text="Restart", height=2, width=13, font=(18), command=self.isRestart)
        self.restartBut.place(x=340, y=180)
        self.quitBut = Button(self.root, text="Quit", height=2, width=13, font=(18), command=self.isQuit)
        self.quitBut.place(x=340, y=260)
        self.scoreLabel1 = Label(self.root, text="Score:", font=(24))
        self.scoreLabel1.place(x=340, y=600)
        self.scoreLabel2 = Label(self.root, text="0", fg='red', font=(24))
        self.scoreLabel2.place(x=410, y=600)
       
        self.area.bind("<Up>", self.rotate)
        self.area.bind("<Left>", self.moveLeft)
        self.area.bind("<Right>", self.moveRight)
        self.area.bind("<Down>", self.moveFaster)
        self.area.bind("<Key-w>", self.rotate)
        self.area.bind("<Key-a>", self.moveLeft)
        self.area.bind("<Key-d>", self.moveRight)
        self.area.bind("<Key-s>", self.moveFaster)
        self.area.focus_set()
        
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.startMenu = Menu(self.menu)
        self.menu.add_cascade(label='Start', menu=self.startMenu)
        self.startMenu.add_command(label='New Game', command=self.isRestart)
        self.startMenu.add_separator()
        self.startMenu.add_command(label='Continue', command=self.play)
        self.exitMenu = Menu(self.menu)
        self.menu.add_cascade(label='Exit', command=self.isQuit)
        self.helpMenu = Menu(self.root)
        self.menu.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='How to play', command=self.rule)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='About...', command=self.about)

   
    def getLocation(self):
        map[(core[0], core[1])] = 1
        for i in range(4):
            map[((core[0] + getNew[i][0]),
                 (core[1] + getNew[i][1]))] = 1

   
    def canMove(self):
        for i in range(4):
            if map[(core[0] + getNew[i][0]), (core[1] + 1 + getNew[i][1])] == 1:
                return False
        return True

   
    def drawNew(self):
        global next
        global getNew
        global core
        next = randrange(1, 8)
       
        self.getNew = self.shapeDict[next]
        getNew = self.getNew
        core = [4, -2]
        time = 0.2
        while self.canMove():
            if isPause:
                core[1] += 1
                self.drawSquare()
                if self.isFaster:
                    sleep(time - 0.15)
                else:
                    sleep(time + 0.22)
                self.isFaster = False
            else:
                self.drawSquare()
                sleep(time)
        self.getLocation()

    
    def drawSquare(self):
        self.area.delete("new")
        for i in range(4):
            self.area.create_rectangle((core[0] + self.getNew[i][0]) * self.size,
                                       (core[1] + self.getNew[i][1]) * self.size,
                                       (core[0] + self.getNew[i][0] + 1) * self.size,
                                       (core[1] + self.getNew[i][1] + 1) * self.size,
                                       fill=self.color[next - 1], tags="new")
        self.area.update()

    def drawBottom(self):
        for j in range(self.height):
            self.area.delete('bottom' + str(j))
            for i in range(self.width):
                if map[(i, j)] == 1:
                    self.area.create_rectangle(self.size * i, self.size * j, self.size * (i + 1),
                                               self.size * (j + 1), fill='grey', tags='bottom' + str(j))
            self.area.update()

   
    def isFill(self):
        for j in range(self.height):
            t = 0
            for i in range(self.width):
                if map[(i, j)] == 1:
                    t = t + 1
            if t == self.width:
                self.getScore()
                self.deleteLine(j)

    
    def getScore(self):
        scoreValue = eval(self.scoreLabel2['text'])
        scoreValue += 10
        self.scoreLabel2.config(text=str(scoreValue))

    
    def deleteLine(self, j):
        for t in range(j, 2, -1):
            for i in range(self.width):
                map[(i, t)] = map[(i, t - 1)]
        for i in range(self.width):
            map[(i, 0)] = 0
        self.drawBottom()

    def isOver(self):
        t = 0
        for j in range(self.height):
            for i in range(self.width):
                if self.map[(i, j)] == 1:
                    t += 1
                    break
        if t >= self.height:
            return False
        else:
            return True

  
    def canRotate(self):
        for i in range(4):
            map[((core[0] + getNew[i][0]),
                 (core[1] + getNew[i][1]))] = 0
        for i in range(4):
            if map[((core[0] + self.rotateDict[getNew[i]][0]),
                    (core[1] + self.rotateDict[getNew[i]][1]))] == 1:
                return False
        return True

  
    def rotate(self, event):
        if next != 2:
            if self.canRotate():
                for i in range(4):
                    getNew[i] = self.rotateDict[getNew[i]]
                self.drawSquare()
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

    
    def canLeft(self):
        coreNow = core
        for i in range(4):
            map[((coreNow[0] + getNew[i][0]), (coreNow[1] + getNew[i][1]))] = 0
        for i in range(4):
            if map[((coreNow[0] + getNew[i][0] - 1), (coreNow[1] + getNew[i][1]))] == 1:
                return False
        return True

    
    def moveLeft(self, event):
        if self.canLeft():
            core[0] -= 1
            self.drawSquare()
            self.drawBottom()
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

   
    def canRight(self):
        for i in range(4):
            map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 0
        for i in range(4):
            if map[((core[0] + getNew[i][0] + 1), (core[1] + getNew[i][1]))] == 1:
                return False
        return True

    
    def moveRight(self, event):
        if self.canRight():
            core[0] += 1
            self.drawSquare()
            self.drawBottom()
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

    
    def moveFaster(self, event):
        self.isFaster = True
        if not self.canMove():
            for i in range(4):
                map[((core[0] + getNew[i][0]), (core[1] + getNew[i][1]))] = 1

    
    def run(self):
        self.isFill()
        self.drawNew()
        self.drawBottom()

 
    def play(self):
        self.startBut.config(state=DISABLED)
        global isPause
        isPause = True
        global map
        map = self.map
        while True:
            if self.isOver():
                self.run()
            else:
                break
        self.over()

        

    def restart(self):
        self.core = [4, -2]
        self.map = {}
        for i in range(self.width):
            for j in range(-4, self.height):
                self.map[(i, j)] = 0
        for i in range(-1, self.width):
            self.map[(i, self.height)] = 1
        for j in range(-4, self.height + 1):
            self.map[(-1, j)] = 1
            self.map[(self.width, j)] = 1
        self.score = 0
        self.t = 0.07
        for j in range(self.height):
            self.area.delete('bottom' + str(j))
        self.play()

    
    def over(self):
        feedback = messagebox.askquestion("You Lose!", "You Lose!\nDo you want to restart?")
        if feedback == 'yes':
            self.restart()
        else:
            self.root.destroy()

    
    def isQuit(self):
        askQuit = messagebox.askquestion("Quit", "Are you sure to quit?")
        if askQuit == 'yes':
            self.root.destroy()
            exit()

    
    def isRestart(self):
        askRestart = messagebox.askquestion("Restart", "Are you sure to restart?")
        if askRestart == 'yes':
            self.restart()
        else:
            return

 
    def isPause(self):
        global isPause
        isPause = not isPause
        if not isPause:
            self.pauseBut["text"] = "Resume"
        else:
            self.pauseBut["text"] = "Pause"

 
    def rule(self):
        ruleTop = Toplevel()
        ruleTop.title('Help')
        ruleTop.geometry('800x400')
        rule = "Start: Press the start button or choose the option 'Continue' to start the game.\n%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s%-s" % (
        "Restart: Press the restart button or choose the option 'New Game' to resatrt the game.\n",
        "Enjoy the Teris game! Have fun!")
        ruleLabel = Label(ruleTop, text=rule, fg='blue', font=(18))
        ruleLabel.place(x=50, y=50)

   
    def about(self):
        aboutTop = Toplevel()
        aboutTop.title('About')
        aboutTop.geometry('300x150')
        about = "Teris.py\n\
By Programmer ZhangYuyi\n\
All Rights Reserved."
        aboutLabel = Label(aboutTop, font=('Curier', 20), fg='darkblue', text=about)
        aboutLabel.pack()

       

    def mainloop(self):
        self.root.mainloop()
def main():
    teris = Teris()
    teris.mainloop()


main()
