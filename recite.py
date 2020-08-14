import gen_data
import tkinter as tk
from tkinter import messagebox

class recite:
    def __init__(self,root,word_num):  #word_num是一个变量        
        self.root = root
        self.data = gen_data.gen_data("recite")
        self.word_num = word_num
        self.seq = 1

    def openFrame(self): 
        self.words_num = self.word_num.get()
        self.root.withdraw()
        if not self.word_num:
           messagebox.showinfo(title='提示', message='请输入正确的单词数！') 
        else:
           self.workFrame = tk.Toplevel()
           self.workFrame.geometry("500x400")
           self.workFrame.title("Insistency leads to success")
               #之后按一次按钮调用函数后要加1          
           self.data.start(int(self.words_num))
           
           tk.Label(self.workFrame,text="您已掌握了",font=('楷体',12)).place(x=90,y=10,anchor=tk.NW)
           tk.Label(self.workFrame,textvariable=self.data.master_words,font=('Times New Roman',12)).place(x=200,y=10,anchor=tk.NW)
           tk.Label(self.workFrame,text="个单词",font=('楷体',12)).place(x=320,y=10,anchor=tk.NW)
           tk.Label(self.workFrame,text="现还剩",font=('楷体',12)).place(x=90,y=30,anchor=tk.NW)
           tk.Label(self.workFrame,textvariable=self.data.left_words,font=('Times New Roman',12)).place(x=200,y=30,anchor=tk.NW)
           tk.Label(self.workFrame,text="个单词",font=('楷体',12)).place(x=320,y=30,anchor=tk.NW)
           
           tk.Label(self.workFrame,textvariable=self.data.word_text,font=('Times New Roman',20)).place(x=200,y=60,anchor=tk.NW)
           tk.Label(self.workFrame,textvariable=self.data.word_attr,font=('Times New Roman',10)).place(x=240,y=100,anchor=tk.NW)
           tk.Label(self.workFrame,textvariable=self.data.word_trans,font=('Times New Roman',15)).place(x=220,y=120,anchor=tk.NW)
           
           
           checkbox = tk.Checkbutton(self.workFrame,text="show sentences",variable=self.data.status,command=self.data.show_sentences)
           #checkbox.select()
           checkbox.place(x=370,y=150,anchor=tk.NW)
           
           self.sentences = tk.StringVar()
           tk.Label(self.workFrame,textvariable=self.data.sentences,wraplength = 400,font=('Times New Roman',10)).place(x=50,y=170,anchor=tk.NW)
           
           button1 = tk.Button(self.workFrame,text="Master")
           button1.place(x=50,y=280,anchor=tk.NW)  #已知并且掌握
           button2 = tk.Button(self.workFrame,text="KnownButNotTry")
           button2.place(x=130,y=280,anchor=tk.NW) #知道这个词的意思
           button3 = tk.Button(self.workFrame,text="LetMetry")
           button3.place(x=270,y=280,anchor=tk.NW)  #尝试写出这个词的意思
           button4 = tk.Button(self.workFrame,text="Unclear")
           button4.place(x=370,y=280,anchor=tk.NW)  #加入未知标记
           button5 = tk.Button(self.workFrame,text="Next")
           button5.place(x=350,y=330,anchor=tk.NW)
           button6 = tk.Button(self.workFrame,text="Exit")
           button6.place(x=400,y=330,anchor=tk.NW)
           self.workFrame.bind('<a>',self.clear_words)
           self.workFrame.bind('<b>',self.show_words)
           self.workFrame.bind('<c>',self.try_words)
           self.workFrame.bind('<d>',self.mark_words)
           self.workFrame.bind('<n>',self.next_one)
           self.workFrame.bind('<q>',self.save_and_quit)
           button1.bind('<Button-1>',self.clear_words)
           button2.bind('<Button-1>',self.show_words)
           button3.bind('<Button-1>',self.try_words)
           button4.bind('<Button-1>',self.mark_words)
           button5.bind('<Button-1>',self.next_one)
           button6.bind('<Button-1>',self.save_and_quit)
           self.buttonlist1 = [button1,button2,button3,button4]
           self.buttonlist2 = [button5]
           
           newsentence = tk.StringVar()
           self.addsentence = tk.Entry(self.workFrame,textvariable=newsentence,font=('Times New Roman',12),width=48,fg='black')
           self.addsentence.place(x=30,y=370,anchor=tk.NW)
           tk.Button(self.workFrame,text="Add",command=self.addin).place(x=430,y=370,anchor=tk.NW)
                
    def clear_words(self,event): 
        if self.seq == 1:
          self.show_words(event)
          self.data.simple.append(self.data.word[0])
        else:
          messagebox.showinfo(title='提示', message='您已经选择了答案！')
    
    def show_words(self,event):   #在show和clear部分都会造成数量增减
        if self.seq == 1:
          self.seq = 0
          for button in self.buttonlist2:
              if button['relief'] != tk.RAISED:
                 button['relief'] = tk.RAISED   #保证按钮重新弹出！
          self.data.count_of_unknown -= 1
          self.data.count_of_learnt += 1
          self.data.master_words.set(self.data.count_of_learnt)
          self.data.left_words.set(self.data.count_of_unknown)
          self.data.word_attr.set(self.data.word[1])  #结束和清理都在next_words中
          self.data.word_trans.set(self.data.word[2])
        else:
           messagebox.showinfo(title='提示', message='您已经选择了答案！')
           
    
    def try_words(self,event):
        if self.seq == 1:
          self.seq = 0
          for button in self.buttonlist2:
              if button['relief'] != tk.RAISED:
                 button['relief'] = tk.RAISED 
        self.tempFrame = tk.Toplevel()
        self.tempFrame.geometry("300x350")
        self.tempFrame.title("Now Let's try")
        self.data.gen_choices()
        tk.Button(self.tempFrame,textvariable=self.data.answer1,command=self.check_answer1).place(x=50,y=20,anchor=tk.NW)
        tk.Button(self.tempFrame,textvariable=self.data.answer2,command=self.check_answer2).place(x=50,y=70,anchor=tk.NW)
        tk.Button(self.tempFrame,textvariable=self.data.answer3,command=self.check_answer3).place(x=50,y=120,anchor=tk.NW)
        tk.Button(self.tempFrame,textvariable=self.data.answer4,command=self.check_answer4).place(x=50,y=170,anchor=tk.NW)
        tk.Label(self.tempFrame,textvariable=self.data.response,font=('Times New Roman',12)).place(x=50,y=200,anchor=tk.NW)
        tk.Button(self.tempFrame,text="Exit",command=self.exit_temp).place(x=50,y=300)
    
    def check_answer1(self):
        word = self.data.answer1.get()
        self.data.check_answer(word)
    
    def check_answer2(self):
        word = self.data.answer2.get()
        self.data.check_answer(word)
    
    def check_answer3(self):
        word = self.data.answer3.get()
        self.data.check_answer(word)
    
    def check_answer4(self):
        word = self.data.answer4.get()
        self.data.check_answer(word)
    
    def exit_temp(self):
        self.tempFrame.destroy()
    
    def mark_words(self,event):
        if self.seq == 1:
           self.seq = 0
           for button in self.buttonlist2:
              if button['relief'] != tk.RAISED:
                 button['relief'] = tk.RAISED 
           self.data.word_attr.set(self.data.word[1])  
           self.data.word_trans.set(self.data.word[2])
           if self.data.is_newword:
              self.data.difficult.append(self.data.word[0])
              self.data.difficult_mark.append(1)
              self.data.extend_word.append(self.data.word)
           elif self.data.difficult.count(self.data.word[0]):  #如果能够找到这个词
              idx = self.data.difficult.index(self.word[0])
              if self.data.difficult_mark[idx] < 3:  #大于3的被标记为3
                 self.data.difficult_mark[idx] += 1 
        else:
           messagebox.showinfo(title='提示', message='您已经选择了答案！')
        
    def next_one(self,event):
        if self.seq == 0:
           self.data.recite_next()
           self.seq = 1
           for button in self.buttonlist1:
               if button['relief'] != tk.RAISED:
                  button['relief'] = tk.RAISED
        else:
           messagebox.showinfo(title='提示', message='请先选择您的答案！')
    
    def addin(self):
        try:
           sentence = self.addsentence.get()
        except:
           messagebox.showinfo(title='提示', message='您还没有输入句子！')
        else:
           self.data.insert_st(sentence)
           self.addsentence.delete(0,"end")
           self.addsentence.insert(0,"")
    
    def save_and_quit(self,event):
        self.data.record_data()
        self.workFrame.destroy()
        self.root.quit()
