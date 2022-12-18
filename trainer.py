#import libraries
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import tkinter as tk

#Deccomment this if there is an error in training
##nltk.download('punkt')
##nltk.download('wordnet')

#load global variables
lemmatizer = WordNetLemmatizer() #to analize words
botSele= 'intents.json' #intents path
words = [] #declare words
classes = [] #declare classes
documents = [] #declare documents
ignore_words = ['?', '!'] #words we ignore
#load intents from its path
data_file = open(botSele).read()
intents = json.loads(data_file)


#intents: groups of conversations
#patterns: iteractions from the user
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #tokenize every words
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        #append it to documents
        documents.append((w, intent['tag']))
        #adding classes to class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

pickle.dump(words, open('System/words.pkl','wb'))
pickle.dump(classes, open('System/classes.pkl','wb'))

#prepare to train the neural network
training = []
output_empty = [0] * len(classes)
for doc in documents:
    #bag of words
    bag = []
    #tokens' list
    pattern_words = doc[0]
    #lemmatizing the tokens
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    #if the word is right write 1, otherwise 0
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

training = np.array(training)
#creating fit and test set: X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

#building the model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#opening
file = open('System/values.txt','r')
fileValue = file.read()
file.close()
epoche = int(fileValue.split('#')[0])
bach = int(fileValue.split('#')[1])
verbi = int(fileValue.split('#')[2])

#fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=epoche, batch_size=bach, verbose=verbi)
model.save('System/chatbot_model.h5', hist)
print("")
print("")
print("Model Completed!")

#GUI
win = tk.Tk()
win.resizable(False,False)
win.title('Trainer')
win.geometry("130x50")
win.configure(bg='black')
win.iconbitmap('System/image/radioactive.ico')
msgbx = tk.Label(text='Model Completed!', bg='black', fg='white').pack(pady=5)

win.mainloop()


















