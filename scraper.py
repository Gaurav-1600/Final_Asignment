import csv
import os 
import requests
from bs4 import BeautifulSoup
url='https://karki23.github.io/Weather-Data/assignment.html'
page=requests.get(url)
src=BeautifulSoup(page.content, "html.parser")
all_cities=src.find_all('a')
os.mkdir("dataset")
for i in all_cities:
    s=i.get('href')[0:len(i)-5:]
    url1='https://karki23.github.io/Weather-Data/'+i.get('href')
    page1=requests.get(url1)                                                       
    src1=BeautifulSoup(page1.content, "html.parser")
    rows=src1.find_all('tr')
    rows.pop(0) 
    file_name="dataset\\"+s+"csv"
    f=open(file_name, "w", newline="")
    headings=src1.find_all('th')
    headings_new=[i.text for i in headings]
    writer=csv.writer(f)
    writer.writerow(headings_new)
    for i in rows:    
        columns=i.find_all('td')
        column_new=[j.text for j in columns]
        writer.writerow(column_new)
    f.close()