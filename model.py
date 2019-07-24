# Accuracy on test set :- 90% !!
import sklearn.utils
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import csv
from bs4 import BeautifulSoup
import requests

def loader(filename):
    file=open(filename, "r")
    lines=csv.reader(file)
    dataset=list(lines)
    return dataset

url='https://karki23.github.io/Weather-Data/assignment.html'
page=requests.get(url)
src=BeautifulSoup(page.content, "html.parser")
new_file=open("dataset\\all_data.csv", "a", newline="")
df=pd.read_csv("dataset\\albury.csv")
writer=csv.writer(new_file)
writer.writerow(list(df.keys()))

all_cities=src.find_all('a')
for i in all_cities:
    s=i.get('href')[0:len(i)-5:]
    file_name="dataset\\"+s+"csv"
    dataset=loader(file_name)
    
    train_set=dataset[1:]   
    for i in train_set:
        writer.writerow(i)
new_file.close()    

df = pd.read_csv('dataset\\all_data.csv', low_memory = False)
df=sklearn.utils.shuffle(df[1:])
df=df.drop(columns=['Date', 'Location'])

df['WindGustDir'] = pd.Categorical(df['WindGustDir'])
df['WindGustDir'] = df.WindGustDir.cat.codes
df['WindDir9am'] = pd.Categorical(df['WindDir9am'])
df['WindDir9am'] = df.WindDir9am.cat.codes
df['WindDir3pm'] = pd.Categorical(df['WindDir3pm'])                 #Line 39 - 48 converts specific column values to descrete numerical values.
df['WindDir3pm'] = df.WindDir3pm.cat.codes
df['RainToday'] = pd.Categorical(df['RainToday'])
df['RainToday'] = df.RainToday.cat.codes
df['RainTomorrow'] = pd.Categorical(df['RainTomorrow'])
df['RainTomorrow'] = df.RainTomorrow.cat.codes
df[['WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday', 'RainTomorrow']] = df[['WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday', 'RainTomorrow']].astype(float)               # This line converts all datatypes to int so that the entire file is made up of single datatype

for i in df.keys():
    df[i].fillna(df[i].mean(), inplace=True)                #Handling missing/NaN values by replacing them with the mean value of each column.



data = df.drop(columns=['RainTomorrow'])
target = df[['RainTomorrow']]


model=Sequential()
n_cols=data.shape[1]
model.add(Dense(21, activation='relu', input_shape=(n_cols,)))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics = ['accuracy'])

model.fit(data[1: int(0.8*len(data))]  , target[1:int(0.8*len(target))], epochs=5)  

test_loss, test_acc = model.evaluate(data[int((0.8*len(data))): ], target[int((0.8*len(data))): ])
print("\nTHE TEST ACCURACY IS : ", test_acc)