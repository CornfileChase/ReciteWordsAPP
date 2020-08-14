import gen_data
import tkinter as tk
from tkinter import messagebox
import pickle

class review:
    def __init__(self,root,word_num):
        self.word_num = word_num
        self.root = root
        self.isupdate = False
        self.seq = 1
        
    
    def chooseFrame(self,v):
        try:
          value = v.get()
        except:
          messagebox.showinfo(title='提示', message='请选择复习方式！')  #其实是一定要选的，不try也可以
        else:
          if value == 1:
             self.openFrame()
          else:
             self.openFrame2()
    
    def openFrame(self):
        self.data = gen_data.gen_data("review1")
        self.words_num = self.word_num.get()
        self.root.withdraw()
        if not self.word_num:
           messagebox.showinfo(title='提示', message='请输入正确的单词数！')
        else:
           self.reviewFrame = tk.Toplevel()
           self.reviewFrame.geometry("500x450")
           self.reviewFrame.title("review")
           self.data.start(int(self.words_num))   
           tk.Label(self.reviewFrame,text="您已掌握了",font=('楷体',12)).place(x=90,y=10,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.master_words,font=('Times New Roman',12)).place(x=200,y=10,anchor=tk.NW)
           tk.Label(self.reviewFrame,text="个单词",font=('楷体',12)).place(x=320,y=10,anchor=tk.NW)
           tk.Label(self.reviewFrame,text="现还剩",font=('楷体',12)).place(x=90,y=30,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.left_words,font=('Times New Roman',12)).place(x=200,y=30,anchor=tk.NW)
           tk.Label(self.reviewFrame,text="个单词",font=('楷体',12)).place(x=320,y=30,anchor=tk.NW)

           tk.Label(self.reviewFrame,textvariable=self.data.word_text,font=('Times New Roman',20)).place(x=200,y=60,anchor=tk.NW)
                
           checkbox = tk.Checkbutton(self.reviewFrame,text="show sentences",variable=self.data.status,command=self.data.show_sentences)
           checkbox.place(x=370,y=90,anchor=tk.NW)
           
           tk.Label(self.reviewFrame,textvariable=self.data.sentences,wraplength = 400,font=('Times New Roman',10)).place(x=50,y=120,anchor=tk.NW)
           
           self.data.gen_choices()
           button1 = tk.Button(self.reviewFrame,textvariable=self.data.answer1,height=1,width=25)
           button1.place(x=150,y=220,anchor=tk.NW)
           button2 = tk.Button(self.reviewFrame,textvariable=self.data.answer2,height=1,width=25)
           button2.place(x=150,y=270,anchor=tk.NW)
           button3 = tk.Button(self.reviewFrame,textvariable=self.data.answer3,height=1,width=25)
           button3.place(x=150,y=320,anchor=tk.NW)
           button4 = tk.Button(self.reviewFrame,textvariable=self.data.answer4,height=1,width=25)
           button4.place(x=150,y=370,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.response,font=('Times New Roman',12)).place(x=50,y=400,anchor=tk.NW)
           button5 = tk.Button(self.reviewFrame,text="Next")
           button5.place(x=350,y=420,anchor=tk.NW)
           button6 = tk.Button(self.reviewFrame,text="Exit")
           button6.place(x=400,y=420,anchor=tk.NW)
           self.reviewFrame.bind('<a>',self.check_answer1)
           self.reviewFrame.bind('<b>',self.check_answer2)
           self.reviewFrame.bind('<c>',self.check_answer3)
           self.reviewFrame.bind('<d>',self.check_answer4)
           self.reviewFrame.bind('<n>',self.review_next1)
           self.reviewFrame.bind('<q>',self.save_and_quit)
           button1.bind('<Button-1>',self.check_answer1)
           button2.bind('<Button-1>',self.check_answer2)
           button3.bind('<Button-1>',self.check_answer3)
           button4.bind('<Button-1>',self.check_answer4)
           button5.bind('<Button-1>',self.review_next1)
           button6.bind('<Button-1>',self.save_and_quit)
           self.buttonlist1 = [button1,button2,button3,button4]
           self.buttonlist2 = [button5]
    
    
    def review_next1(self,event):
        if self.seq == 0:
          mark = self.data.review_next()
          if mark:
             self.data.choose_trans()
             self.seq = 1
             for button in self.buttonlist1:
                if button['relief'] != tk.RAISED:
                   button['relief'] = tk.RAISED   #保证按钮重新弹出！
        else:
           messagebox.showinfo(title='提示', message='请先选择您的答案！')
        
    
    def check_answer1(self,event):
        if self.seq == 1:
           word = self.data.answer1.get()
           self.data.check_answer(word)
           self.seq = 0
           for button in self.buttonlist2:
                if button['relief'] != tk.RAISED:
                   button['relief'] = tk.RAISED   
        else:
           messagebox.showinfo(title='提示', message='您已经选择了答案！')
        
    
    def check_answer2(self,event):
        if self.seq == 1:
           word = self.data.answer2.get()
           self.data.check_answer(word)
           self.seq = 0
           for button in self.buttonlist2:
                if button['relief'] != tk.RAISED:
                   button['relief'] = tk.RAISED   
        else:
           messagebox.showinfo(title='提示', message='您已经选择了答案！')
    
    def check_answer3(self,event):
        if self.seq == 1:
           word = self.data.answer3.get()
           self.data.check_answer(word)
           self.seq = 0
           for button in self.buttonlist2:
                if button['relief'] != tk.RAISED:
                   button['relief'] = tk.RAISED   
        else:
           messagebox.showinfo(title='提示', message='您已经选择了答案！')
    
    def check_answer4(self,event):
        if self.seq == 1:
           word = self.data.answer4.get()
           self.data.check_answer(word)
           self.seq = 0
           for button in self.buttonlist2:
                if button['relief'] != tk.RAISED:
                   button['relief'] = tk.RAISED   
        else:
           messagebox.showinfo(title='提示', message='您已经选择了答案！')
    
    def openFrame2(self):
        self.data = gen_data.gen_data("review2")
        self.words_num = self.word_num.get()
        self.root.withdraw()
        if not self.word_num:
           messagebox.showinfo(title='提示', message='请输入正确的单词数！')
        else:
           self.reviewFrame = tk.Toplevel()
           self.reviewFrame.geometry("500x370")
           self.reviewFrame.title("review")
           self.data.start(int(self.words_num))   
           tk.Label(self.reviewFrame,text="您已掌握了",font=('楷体',12)).place(x=90,y=10,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.master_words,font=('Times New Roman',12)).place(x=200,y=10,anchor=tk.NW)
           tk.Label(self.reviewFrame,text="个单词",font=('楷体',12)).place(x=320,y=10,anchor=tk.NW)
           tk.Label(self.reviewFrame,text="现还剩",font=('楷体',12)).place(x=90,y=30,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.left_words,font=('Times New Roman',12)).place(x=200,y=30,anchor=tk.NW)
           tk.Label(self.reviewFrame,text="个单词",font=('楷体',12)).place(x=320,y=30,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.word_text,font=('Times New Roman',20)).place(x=200,y=60,anchor=tk.NW)                
           checkbox = tk.Checkbutton(self.reviewFrame,text="show sentences",variable=self.data.status,command=self.data.show_sentences)
           checkbox.place(x=370,y=90,anchor=tk.NW)           
           tk.Label(self.reviewFrame,textvariable=self.data.sentences,wraplength = 400,font=('Times New Roman',10)).place(x=50,y=120,anchor=tk.NW)
           
           self.data.gen_choices()
           self.Myanswer = tk.StringVar()
           self.myanswer = tk.Entry(self.reviewFrame,textvariable=self.Myanswer,font=('Times New Roman',12),width=50,fg='black')
           self.myanswer.place(x=30,y=220,anchor=tk.NW)
           tk.Label(self.reviewFrame,textvariable=self.data.response,font=('Times New Roman',12)).place(x=50,y=250,anchor=tk.NW)
           button1 = tk.Button(self.reviewFrame,text="Confirm")
           button1.place(x=120,y=280,anchor=tk.NW)
           button2 = tk.Button(self.reviewFrame,text="Add",command=self.add_trans)
           button2.place(x=300,y=280,anchor=tk.NW)
           button3 = tk.Button(self.reviewFrame,text="Next")
           button3.place(x=350,y=330,anchor=tk.NW)
           button4 = tk.Button(self.reviewFrame,text="Exit")
           button4.place(x=400,y=330,anchor=tk.NW)
           
           self.reviewFrame.bind('<y>',self.check_my)
           self.reviewFrame.bind('<n>',self.review_next2)
           self.reviewFrame.bind('<q>',self.save_and_quit)
           button1.bind('<Button-1>',self.check_my)
           button3.bind('<Button-1>',self.review_next2)
           button4.bind('<Button-1>',self.save_and_quit)
    
    def review_next2(self,event):
        mark = self.data.review_next()
        if mark:
          self.myanswer.delete(0,"end")
          self.myanswer.insert(0,"")
          self.data.choose_trans()
    
    def check_my(self,event):
        word = self.myanswer.get()
        self.data.check_answer(word)
    
    def add_trans(self):
        word = self.myanswer.get()
        e_word = self.data.word[0]
        try:
           transl = self.data.transdic[e_word]
           if not word in transl:
              transl += "，" + word   #此处是中文的逗号
              self.isupdate = True
              self.data.transdic[e_word] = transl
        except:
           pass
    
    def save_and_quit(self,event):
        self.data.record_data()
        if self.isupdate:
           with open("translation.pickle","wb") as handle:
              pickle.dump(self.data.transdic,handle,protocol=pickle.HIGHEST_PROTOCOL)
        self.reviewFrame.destroy()
        self.root.quit()
