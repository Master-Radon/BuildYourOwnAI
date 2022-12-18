#import libraries
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import tkinter as tk
from PIL import ImageTk, Image

#load global variables
lemmatizer = WordNetLemmatizer() #to analize words
botSele= 'intents.json' #intents path
model = load_model('System/chatbot_model.h5') #load model
intents = json.loads(open(botSele).read()) #load intents from its path
words = pickle.load(open('System/words.pkl','rb')) #load words
classes = pickle.load(open('System/classes.pkl','rb')) #load classes

#preprocessing user input
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

#create the bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))

#calculate the right answer for the question
def calcola_pred(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    #sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

#get result, the answer
def getRisposta(ints, intents_json):
    try:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result
    except Exception as e:
        #try again to process data if there is an error
        filer = open('System/values.txt','r')
        fileValue = filer.read()
        filer.close()
        tentF = int(fileValue.split('#')[3])
        filer = open('System/tent.txt','r')
        tentD = int(filer.read())
        tentD=tentD+1
        filer.close()
        filer = open('System/tent.txt','w')
        filer.write(str(tentD))
        filer.close()
        if tentD<tentF: #try tentF times. Default: 10
            #trying again
            inizia(test.get())
        else:
            #if there is still an error pass away
            filer = open('System/tent.txt','w')
            filer.write('0')
            filer.close()
            #out of range

#start, take the message and call all functions to process it
def inizia(msg):
    ints = calcola_pred(msg, model)
    res = getRisposta(ints, intents)
    return res #get answer

#GUI
win = tk.Tk()
win.resizable(False,False)
win.title('Build Your Own AI')
win.geometry("500x600")
win.configure(bg='black')
win.iconbitmap('System/image/radioactive.ico')
#GUI variables
namaBot = open('name.txt','r')
nama = namaBot.read()
namaBot.close()
fontTitle = ('Algerian',20)
fontTitle2 = ('Algerian',18)
fontButton = ('Arial',15)
#GUI Objects
titolo = tk.Label(text='Build Your Own AI', font=fontTitle, bg='black',fg='white').pack(pady=10)
titolo2 = tk.Label(text=nama, font=fontTitle2, bg='black',fg='white').pack(pady=15)
propic = ImageTk.PhotoImage(Image.open('propic.png').resize((150,150)))
panel = tk.Label(win, bg='black',image=propic)
panel.pack()
responsta = tk.Label(text='', font=fontButton, bg='black',fg='white')
test = tk.Entry(font=fontButton)
test.pack(pady=50)

#answer the question
def parla():
    lingua = open('lang.txt','r')
    ling = lingua.read()
    lingua.close()
    mess = test.get()
    test.delete(0,tk.END)
    res = inizia(mess)
    try:
        res=nama+": "+res
    except Exception as e: #error messages
        if ling=='en':
            res = nama+": I don't understand"
        elif ling=='it':
            res = nama+': Non ho capito'
        elif ling=='id':
            res = nama+': Aku belum mengerti'
        elif ling=='es':
            res = nama+': No entendía'
        elif ling=='esp':
            res = nama+': Mi ne komprenis'
        elif ling=='kl':
            res = nama+": jIyajbe'"
        else:
            res = nama+': Error'
    responsta['text']=res #write the answer on the screen

#button to send message to AI
invio = tk.Button(text='Send', font=fontButton, bg='black',fg='white', command=parla).pack(pady=5)
responsta.pack(pady=5)

win.mainloop()
