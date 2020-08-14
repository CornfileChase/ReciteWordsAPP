import recite
import review
import tkinter as tk
from pandas import read_csv

class open_Frame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WordsMemory")
        self.root.geometry("200x300")
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        button1 = tk.Button(self.frame, text="Recite words")
        button1.pack(padx=0,pady=25)
        button2 = tk.Button(self.frame, text="Review words")
        button2.pack(padx=0,pady=25)
        tk.Button(self.frame,text="Reset",command=self.reset).pack(padx=0,pady=25)
        self.root.bind('<a>',self.ask1)
        self.root.bind('<b>',self.ask2)
        button1.bind('<Button-1>',self.ask1)
        button2.bind('<Button-1>',self.ask2)
        
    def ask_info(self):
        self.root.withdraw()
        askFrame = tk.Toplevel()
        askFrame.geometry("400x300")
        askFrame.title("Query")
        tk.Label(askFrame,text="I will learn",font=('Times New Roman',12)).place(x=80,y=60,anchor=tk.NW)
        wordnum = tk.IntVar()
        self.word_num = tk.Entry(askFrame,textvariable=wordnum,font=('Times New Roman',12),fg='black')
        self.word_num.place(x=150,y=60,anchor=tk.NW)
        tk.Label(askFrame,text="words this time",font=('Times New Roman',12)).place(x=230,y=60,anchor=tk.NW)
        return askFrame  #此处可以传递
    
    def ask1(self,event):
        askFrame = self.ask_info()
        mainFrame = recite.recite(askFrame,self.word_num)
        tk.Button(askFrame, text="Start reciting", command=mainFrame.openFrame).place(x=150,y=150,anchor=tk.NW)
        
    def ask2(self,event):
        askFrame = self.ask_info()
        mainFrame = review.review(askFrame,self.word_num)
        v = tk.IntVar()
        choice1 = tk.Radiobutton(askFrame,text="choose",variable=v,value=1)
        choice1.place(x=100,y=110,anchor=tk.NW)
        choice1.select()
        choice2 = tk.Radiobutton(askFrame,text="type",variable=v,value=2)
        choice2.place(x=230,y=110,anchor=tk.NW)        
        tk.Button(askFrame, text="Start reviewing", command=lambda: mainFrame.chooseFrame(v)).place(x=150,y=150,anchor=tk.NW)
     
    def reset(self):
        df = read_csv("process_db.csv",header=0,names=["word","attr","trans","marktimes","lasttime","have_learn"],encoding="gbk")
        df['lasttime'] = df['lasttime'].apply(lambda p:0)
        df['marktimes'] = df['marktimes'].apply(lambda p:0)
        df['have_learn'] = df['have_learn'].apply(lambda p:0)
        df.to_csv("process_db.csv",encoding="gbk")


if __name__ == "__main__":
   app = open_Frame()
   app.root.mainloop()