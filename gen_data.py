import tkinter as tk
from tkinter import messagebox
import random
from pandas import read_csv
import datetime
import pickle

def date_minus(now_time,time):
    try:
      duration = min((now_time - time).days,50)
    except:
      duration = -1
    return duration

class gen_data:
    def __init__(self,typ):
        self.words_db = read_csv("process_db.csv",header=0,names=["word","attr","trans","marktimes","lasttime","have_learn"],encoding="gbk")
        #self.words_db['lasttime'] = self.words_db['lasttime'].apply(lambda p:0)   #注意此处如何改
        #self.words_db['marktimes'] = self.words_db['marktimes'].apply(lambda p:0) 
        #self.words_db['have_learn'] = self.words_db['have_learn'].apply(lambda p:0)
        with open('example.pickle', 'rb') as handle:
             self.example = pickle.load(handle)
        self.have_change = False #例句是否发生了改变
        
        self.typ = typ
        self.is_newword = True            #用于标记记录
        self.word_idx = 0                 #单词编号
        self.word_text = tk.StringVar()   #单词文本内容
        self.word_attr = tk.StringVar()   #单词词性
        self.word_trans = tk.StringVar()   #单词释义
        self.master_words = tk.IntVar()   #已掌握的单词数/已复习单词数
        self.left_words = tk.IntVar()    #剩余单词数
        self.status=tk.IntVar()          #是否显示例句
        self.state = "off"              #显示例句的值/用于简单表征以指示next word
        self.sentences = tk.StringVar()  #显示的句子的值
    
    
    def sample_word(self,num):
        wordlist = []
        now_time = datetime.datetime.now()
        recitetime = [3,7,9,12,17,19,50]  #记忆的相关天数
        self.words_db['time_span'] = self.words_db['lasttime'].apply(lambda p: date_minus(now_time,p))
        if self.typ == "recite":
           samplelist = self.words_db.loc[self.words_db["marktimes"] != -1]  #simple的word就不要出现了
           samplelist["weight"] = 0
           samplelist.loc[samplelist["time_span"].isin(recitetime),"weight"] += 1
           samplelist.loc[:,"weight"] += samplelist["marktimes"]
           samplelist = samplelist.sort_values("weight",ascending=False)  #按照优先级来选词
           samplelist.reset_index(drop=True,inplace=True)
           if len(samplelist) < num:
               num = len(samplelist)
               messagebox.showinfo(title='提示', message='没有那么多剩余单词啦！')
               for idx in range(num):
                  temp = []
                  temp.append(samplelist.iloc[idx,0])
                  temp.append(samplelist.iloc[idx,1])
                  temp.append(samplelist.iloc[idx,2])
                  wordlist.append(temp)
           else:
               left_num = num
               for pick_weight in range(5):
                  df = samplelist.loc[samplelist["weight"]==4-pick_weight]
                  if len(df):
                     if left_num - len(df) >= 0 and not left_num:
                         for idx in range(len(df)):
                             temp = []
                             temp.append(df.iloc[idx,0])
                             temp.append(df.iloc[idx,1])
                             temp.append(df.iloc[idx,2])
                             wordlist.append(temp)
                         left_num -= len(df)
                     elif left_num > 0:  #还有要选的词
                         whole_idx = [i for i in range(len(df))]
                         sample_idx = random.sample(whole_idx,left_num)
                         for idx in sample_idx:
                            temp = []
                            temp.append(df.iloc[idx,0])
                            temp.append(df.iloc[idx,1])
                            temp.append(df.iloc[idx,2])
                            wordlist.append(temp)
                         left_num = 0
        elif self.typ == "review1" or self.typ == "review2":
            samplelist = self.words_db[self.words_db['have_learn'] != 0]
            if len(samplelist) >= num and num:
              samplelist["weight"] = 0
              samplelist.loc[samplelist["time_span"].isin(recitetime),"weight"] += 1
              samplelist.loc[:,"weight"] += samplelist["marktimes"]  #此处可以这样写！
              samplelist = samplelist.sort_values("weight",ascending=False)  #按照优先级来选词
              samplelist.reset_index(drop=True,inplace=True)  #重置的结果是否作用在之前的数据上——inplace；drop是否去掉原来的编号
              left_num = num
              for pick_weight in range(5):
                  df = samplelist.loc[samplelist["weight"]==4-pick_weight]
                  if len(df):
                     if left_num - len(df) >= 0 and not left_num:
                         for idx in range(len(df)):
                             temp = []
                             temp.append(df.iloc[idx,0])
                             temp.append(df.iloc[idx,1])
                             temp.append(df.iloc[idx,2])
                             wordlist.append(temp)
                         left_num -= len(df)
                     elif left_num > 0:  #还有要选的词
                         whole_idx = [i for i in range(len(df))]
                         sample_idx = random.sample(whole_idx,left_num)
                         for idx in sample_idx:
                            temp = []
                            temp.append(df.iloc[idx,0])
                            temp.append(df.iloc[idx,1])
                            temp.append(df.iloc[idx,2])
                            wordlist.append(temp)
                         left_num = 0
            elif len(samplelist) < num:
              supplist = self.words_db[self.words_db['have_learn'] == 0]
              choose_list = random.sample([i for i in range(len(supplist))],num-len(samplelist))
              if len(samplelist):
                 for idx in range(len(samplelist)):
                    temp = []
                    temp.append(samplelist.iloc[idx,0])
                    temp.append(samplelist.iloc[idx,1])
                    temp.append(samplelist.iloc[idx,2])
                    wordlist.append(temp)
              for idx in choose_list:
                  temp = []
                  temp.append(supplist.iloc[idx,0])
                  temp.append(supplist.iloc[idx,1])
                  temp.append(supplist.iloc[idx,2])
                  wordlist.append(temp)
        random.shuffle(wordlist)  #打乱次序
        self.wordlist = wordlist
    
    def get_Chinese_db(self):
        if self.typ == "review1" or "recite":
           self.translist = list(self.words_db["trans"].values)
        elif self.typ == "review2":
            with open('translation.pickle', 'rb') as handle:
               self.transdic = pickle.load(handle)  #此处要创建一个
    
    def start(self,num):  #应该是其中一个按钮的关联  #这个函数既可以用在背的部分，也可以用在复习的部分
        self.get_Chinese_db()
        self.count_of_unknown = 0
        self.count_of_learnt = 0   #剩下的只需要总数减这个就好了
        self.difficult = []
        self.difficult_mark = []
        self.extend_word = []   #按照原有的格式记录该背的词，并且背过就pop掉
        if self.typ == "recite":
          self.simple = []
          self.have_learnt = []        
        self.sample_word(num)
        self.length = len(self.wordlist)  #不一定等于num(中间num有可能变过)
        self.count_of_unknown = self.length
        if self.word_idx == self.length:
           messagebox.showinfo(title='提示', message='没有可背的词哟！') 
        else:
           self.word = self.wordlist[self.word_idx]  #是一个三元列表
           self.word_text.set(self.word[0])  #显示初始单词
           if self.typ == "recite":
             self.have_learnt.append(self.word[0])
           self.master_words.set(0)
           self.left_words.set(self.length)
    
    def show_sentences(self):
        if self.status.get():
           self.state = "on"
           sentence = self.example[self.word[0]]
           self.sentences.set(sentence[0])  #先只显示第一句，之后可以随机显示
        else:
           self.state = "off"
           self.sentences.set("")
    
    def insert_st(self,sentence):
        #也可以进行values匹配
        sentences = self.example[self.word[0]]
        if sentences[0] == "not match yet":
           sentences[0] = sentence
        else:
           sentences[1] = sentence
        self.example[self.word[0]] = sentences
        self.have_change = True
    
    def gen_choices(self):
        self.response = tk.StringVar()  #显示回答正确还是错误
        if self.typ == "review1" or "recite":
          self.answer1 = tk.StringVar()
          self.answer2 = tk.StringVar()
          self.answer3 = tk.StringVar()
          self.answer4 = tk.StringVar()        
        self.choose_trans()
    
    def choose_trans(self):
        self.rightanswer = self.word[2]
        if self.typ == "review1" or self.typ == "recite":
          wrong_answer = random.sample(self.translist,4)
          answer = []
          #right_answer = self.word[2]
          #self.rightanswer = right_answer
          answer.append(self.rightanswer)
          if not wrong_answer.count(self.rightanswer):  #判断下是不是正确答案
             for idx in range(3):
                 answer.append(wrong_answer[idx])     
          else:
             pop_idx = wrong_answer.index(self.rightanswer)
             for idx in range(4):
                 if not idx == pop_idx:
                    answer.append(wrong_answer[idx])
          random.shuffle(answer)
          self.answer1.set(answer[0])
          self.answer2.set(answer[1])
          self.answer3.set(answer[2])
          self.answer4.set(answer[3])
            
    
    def next_words(self):   #并且一定几率显示出自己不懂的单词
        self.mark = 1
        if not self.extend_word and self.word_idx < self.length-1:      #没有不懂的词，并且还有剩余未背的词(word_idx从0开始)
           self.is_newword = True
           self.word_idx += 1
           self.word = self.wordlist[self.word_idx]
           if self.state == "on":
              sentence = self.example[self.word[0]]
              self.sentences.set(sentence[0])
        elif not self.extend_word and self.word_idx == self.length-1:   #没有不懂的词，并且没有剩余的词
           messagebox.showinfo(title='恭喜', message='单词已经背完了，你真棒！')
           self.mark = 0
        elif self.extend_word and self.word_idx == self.length-1:      #有不懂的词，并且没有剩余的
            self.is_newword = False
            self.word = random.choice(self.extend_word)
            self.extend_word.remove(self.word)
            if self.state == "on":
               sentence = self.example[self.word[0]]
               self.sentences.set(sentence[0])
        elif self.extend_word:                                                      #既有剩余，又有不懂的
            prop = random.random()
            if prop <= 0.9:
               self.is_newword = True
               self.word_idx += 1
               self.word = self.wordlist[self.word_idx]
               if self.state == "on":
                 sentence = self.example[self.word[0]]
                 self.sentences.set(sentence[0])
            else:
               self.is_newword = False
               self.word = random.choice(self.extend_word)
               self.extend_word.remove(self.word)
               if self.state == "on":
                 sentence = self.example[self.word[0]]
                 self.sentences.set(sentence[0])

           
    def recite_next(self):
        self.next_words()
        if self.mark:
          self.word_text.set(self.word[0])
          self.word_attr.set("")
          self.word_trans.set("")
          if self.is_newword and not self.have_learnt.count(self.word[0]):
             self.have_learnt.append(self.word[0])
        else:
          self.record_data()
    
    def review_next(self):
        self.next_words()
        if self.mark:
           self.word_text.set(self.word[0])  
           self.response.set("")  #重新设置正确还是错误               
        else:   #之前已经有弹出框弹出过了
           self.record_data()
        return self.mark
    
    def check_answer(self,word):
        justice = False
        if (self.typ == "review1" or self.typ == "recite") and word == self.rightanswer:
           justice = True
        elif self.typ == "review2":
           justice = self.check_fuzzy(word)
        if justice:
           self.response.set("correct")
          #不会在复习的时候无穷地加下去，因为只会复习一次
           self.count_of_unknown -= 1
           self.count_of_learnt += 1
           self.master_words.set(self.count_of_learnt)
           self.left_words.set(self.count_of_unknown)
           if self.difficult.count(self.word[0]):
              pos = self.difficult.index(self.word[0])
              self.difficult_mark[pos] = self.difficult_mark[pos] - 1
              if self.extend_word.count(self.word):
                 self.extend_word.remove(self.word)   #会了就去掉
           else:
              self.difficult.append(self.word[0])
              self.difficult_mark.append(-1)  #在总和中会减
        else:
           res = "wrong,the correct answer is:"+self.rightanswer
           self.response.set(res)            
           if self.difficult.count(self.word[0]):
              pos = self.difficult.index(self.word[0])
              self.difficult_mark[pos] = self.difficult_mark[pos] + 1
           else:
              self.difficult.append(self.word[0])
              self.difficult_mark.append(1)  #在总和中会减
              self.extend_word.append(self.word)    #只有历史上未出现的新词才入选，不反复appenddifficult
            
    def check_fuzzy(self,word):
        key = self.word[0]
        try:
           rightanswer = self.transdic[key]
           if word in rightanswer:
              return True
           else:
              return False
        except:
           messagebox.showinfo(title='提示', message='词库里没有这个单词') 
           return False

    
    def record_data(self):   #review只需要只输入前面的变量就好了
        now_time = datetime.date.today()
        df = self.words_db.loc[:,"word":"have_learn"]  #一定要写完整的，之后要代替写入的
        if self.typ == "recite":
          if self.have_learnt:
            df.loc[df['word'].isin(self.have_learnt),'lasttime'] = now_time
            df.loc[df['word'].isin(self.have_learnt),'have_learn'] = 1
          if self.simple:
            df.loc[df['word'].isin(self.simple),'marktimes'] = -1
        if self.difficult:
          for i,word in enumerate(self.difficult):
              if len(df.loc[df['word']==word,'marktimes']):  #一些字符匹配错误，导致没有这样的元素
                if df.loc[df['word']==word,'marktimes'].values[0] + self.difficult_mark[i] > -1:
                  if df.loc[df['word']==word,'marktimes'].values[0] + self.difficult_mark[i] <= 3:  #要实行累加！
                     df.loc[df['word']==word,'marktimes'] += self.difficult_mark[i]
                  else:
                     df.loc[df['word']==word,'marktimes'] = 3   #这样的loc是在原df上改来着！
                else:
                   df.loc[df['word']==word,'marktimes'] = -1
                df.loc[df['word']==word,'lasttime'] = now_time
        df.to_csv("process_db.csv",encoding="gbk")
        if self.have_change:
           with open("example.pickle","wb") as handle:
               pickle.dump(self.example,handle,protocol=pickle.HIGHEST_PROTOCOL)