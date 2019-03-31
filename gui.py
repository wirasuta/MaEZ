from tkinter import *

class UI:
    def __init__(self, maze, title, interval):
        self.interval = interval
        self.drawqueue = []
        self.size = 10

        self.root = Tk()
        self.frame = Frame(self.root)
        self.w = Canvas(self.frame)
        self.w.configure(bg="gray99")

        self.scroll_x = Scrollbar(self.frame, orient="horizontal", command=self.w.xview)
        self.scroll_y = Scrollbar(self.frame, orient="vertical", command=self.w.yview)
        self.w.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.w.pack(fill=BOTH, expand=1)
        self.frame.pack(fill = BOTH, expand=1)

        self.drawMaze(maze)
        self.root.title(title)
        self.w.configure(scrollregion=self.w.bbox("all"))

    def startdraw(self,drawqueue):
        self.drawqueue = drawqueue
        self.root.after(self.interval, self.refresh)
        self.root.after(0, self.exit)  
        self.root.mainloop()

    def exit(self):
        user_input = input()
        if user_input == "x":
            self.root.quit()

    def refresh(self):
        self.drawQueue()
        self.root.after(self.interval, self.refresh)

    def drawQueue(self):
        if len(self.drawqueue) > 0:
            drawsquare = self.drawqueue[0][0]
            drawcolor = self.drawqueue[0][1]
            x = drawsquare[0]*self.size+self.size
            y = drawsquare[1]*self.size+self.size
            self.w.create_rectangle(x, y, x+self.size, y+self.size, fill=drawcolor)
            self.w.update()
            self.drawqueue = self.drawqueue[1:]

    def drawMaze(self, maze):
        x = 10
        y = 10
        for line in maze:
            for char in line:
                if char == 1:
                    self.w.create_rectangle(x, y, x+self.size, y+self.size, fill="#000")
                x += self.size
            x = 10
            y += self.size