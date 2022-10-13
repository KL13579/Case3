#!/usr/bin/env python
# coding: utf-8

# Groep 18: Irina van Dam, Pien van Dongen, Kevin Linders & Floor Wesselink

# In[1]:


import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


st.header('Toename van elektrisch vervoer')


# In[3]:


#Inladen van alle auto's vanaf het jaar 2015, met de variabelen kenteken en datum_eerste_tenaamstelling_in_nederland
response1 = requests.get('https://opendata.rdw.nl/resource/m9d7-ebf2.json?$$app_token=qXFPxMddONVr63MCrFtrxLUrN&$where=datum_eerste_tenaamstelling_in_nederland>20141231&$select=kenteken, datum_eerste_tenaamstelling_in_nederland&$limit=7000000')        
data1 = response1.json()
df1 = pd.DataFrame.from_dict(data1)     


# In[4]:


#Inladen van kenteken, brandstof omschrijving en klasse hybride elektrisch voertuig
response2 = requests.get('https://opendata.rdw.nl/resource/8ys7-d773.json?$$app_token=qXFPxMddONVr63MCrFtrxLUrN&$select=kenteken, brandstof_omschrijving, klasse_hybride_elektrisch_voertuig&$limit=15000000')
data2 = response2.json()
df2 = pd.DataFrame.from_dict(data2)


# In[5]:


#Brandstof koppelen aan de juiste auto's
auto_brandstof = df1.merge(df2, on = 'kenteken', how = 'left')


# In[6]:


#Data bekijken
auto_brandstof.head()


# In[7]:


#Data verder inspecteren
auto_brandstof.info()


# In[8]:


#Datum naar datetime omzetten
auto_brandstof['datum'] = pd.to_datetime(auto_brandstof['datum_eerste_tenaamstelling_in_nederland'], format = '%Y%m%d')
auto_brandstof['jaar'] = auto_brandstof['datum'].dt.year
auto_brandstof['maand'] = auto_brandstof['datum'].dt.month
auto_brandstof['dag'] = 1
auto_brandstof['datum'] = pd.to_datetime(dict(year = auto_brandstof.jaar, month = auto_brandstof.maand, day = auto_brandstof.dag))
auto_brandstof.head()


# In[9]:


df = auto_brandstof[['brandstof_omschrijving', 'datum']]


# In[10]:


#Per brandstofsoort een dataframe aanmaken.
benzine = df[df['brandstof_omschrijving'] == 'Benzine']
diesel = df[df['brandstof_omschrijving'] == 'Diesel']
elektriciteit = df[df['brandstof_omschrijving'] == 'Elektriciteit']
lpg = df[df['brandstof_omschrijving'] == 'LPG']
cng = df[df['brandstof_omschrijving'] == 'CNG']
alcohol = df[df['brandstof_omschrijving'] == 'Alcohol']
lng = df[df['brandstof_omschrijving'] == 'LNG']
waterstof = df[df['brandstof_omschrijving'] == 'Waterstof']


# In[11]:


#Deze functie telt het aantal auto's dat binnen een maand aangeschaft wordt.
def counting(colom, list_name):
    list_name = {}
    for entry in colom:
        if entry in list_name.keys():
            list_name[entry] = list_name[entry] + 1
        else:
            list_name[entry] = 1
    return list_name


# In[12]:


#Een lege lijst per brandstofsoort aanmaken voor het tellen
counts1 = {}
counts2 = {}
counts3 = {}
counts4 = {}
counts5 = {}
counts6 = {}
counts7 = {}
counts8 = {}

#Hier wordt per brandstofsoort het aantal auto's per maand geteld en opgeslagen.
counts1 = counting(benzine['datum'], counts1)
counts2 = counting(diesel['datum'], counts2)
counts3 = counting(elektriciteit['datum'], counts3)
counts4 = counting(lpg['datum'], counts4)
counts5 = counting(cng['datum'], counts5)
counts6 = counting(alcohol['datum'], counts6)
counts7 = counting(lng['datum'], counts7)
counts8 = counting(waterstof['datum'], counts8)


# In[13]:


#Hier worden de dictionarys naar dataframes omgezet
benzine1 = pd.DataFrame(counts1.items(), columns = ['Datum', 'Aantal'])
diesel1 = pd.DataFrame(counts2.items(), columns = ['Datum', 'Aantal'])
elektriciteit1 = pd.DataFrame(counts3.items(), columns = ['Datum', 'Aantal'])
lpg1 = pd.DataFrame(counts4.items(), columns = ['Datum', 'Aantal'])
cng1 = pd.DataFrame(counts5.items(), columns = ['Datum', 'Aantal'])
alcohol1 = pd.DataFrame(counts6.items(), columns = ['Datum', 'Aantal'])
lng1 = pd.DataFrame(counts7.items(), columns = ['Datum', 'Aantal'])
waterstof1 = pd.DataFrame(counts8.items(), columns = ['Datum', 'Aantal'])


# In[14]:


#Hier wordt per dataframe een kolom toegevoegd met de cummulatieve som toegevoegd
benzine1['Cumsum'] = benzine1['Aantal'].cumsum()
diesel1['Cumsum'] = diesel1['Aantal'].cumsum()
elektriciteit1['Cumsum'] = elektriciteit1['Aantal'].cumsum()
lpg1['Cumsum'] = lpg1['Aantal'].cumsum()
cng1['Cumsum'] = cng1['Aantal'].cumsum()
alcohol1['Cumsum'] = alcohol1['Aantal'].cumsum()
lng1['Cumsum'] = lng1['Aantal'].cumsum()
waterstof1['Cumsum'] = waterstof1['Aantal'].cumsum()


# In[15]:


#De brandstofsoort wordt per dataframe toegevoegd.
benzine1['Brandstoftype'] = 'Benzine'
diesel1['Brandstoftype'] = 'Diesel'
elektriciteit1['Brandstoftype'] = 'Elektriciteit'
lpg1['Brandstoftype'] = 'LPG'
cng1['Brandstoftype'] = 'CNG'
alcohol1['Brandstoftype'] = 'Alcohol'
lng1['Brandstoftype'] = 'LNG'
waterstof1['Brandstoftype'] = 'Waterstof'


# In[16]:


#Alle dataframes in een lijst.
dataframes = [benzine1, diesel1, elektriciteit1, lpg1, cng1, alcohol1, lng1, waterstof1]

#Alle dataframes weer aan elkaar toevoegen en brandstoftype omzetten naar een string.
df2 = pd.concat(dataframes)
df2['Brandstoftype'] = df2['Brandstoftype'].astype('string')


# In[17]:


#Een checkbox om de schaal in de lijnplot aan te passen
checkbox = st.checkbox(label = 'Logaritmische schaal')

#Code voor de lijnplot
if checkbox:
    px.line(x = df2['Datum'], y = df2['Cumsum'], color = df2['Brandstoftype'], log_y = True)
else:
    px.line(x = df2['Datum'], y = df2['Cumsum'], color = df2['Brandstoftype'])


#  
#  

# Hieronder worden de stappen ondernomen voor het maken van een histogram over de laadpaal data.

# In[18]:


#Inladen van de data
df3 = pd.read_csv('laadpaaldata.csv')

#Bekijken van de data
df3.info()


# In[19]:


#De onderstaande code geeft een error omdat er verschillende rijen die aangeven op 29 februari 2018 te laden, 
#echter bestaat die datum niet.

#df3['Started'] = pd.to_datetime(df3['Started'])
#df3['Ended'] = pd.to_datetime(df3['Ended'])

#Zoeken naar verschillende rijen die aangeven op 29 februari 2018 te laden, echter bestaat die datum niet.
#De onderstaande regels zijn de regels met 29 februari 2018
df3.loc[1731]
df3.loc[1732]


# In[20]:


#Droppen van rijen met ongeldige waarden.
df3 = df3.drop([1731,1732])


# In[21]:


#Omzetten naar datetime.
df3['Started'] = pd.to_datetime(df3['Started'])
df3['Ended'] = pd.to_datetime(df3['Ended'])


# In[22]:


#Filteren zodat de eindtijd na de starttijd ligt.
df3 = df3[df3['Started'] < df3['Ended']]
df3


# In[23]:


#De Charge time moet altijd kleiner of gelijk zijn aan de Connected time
#Hier worden de rijen gedropt waarbij dit niet het geval is
df3 = df3[df3['ChargeTime'] <= df3['ConnectedTime']]
df3


# In[24]:


#Onderzoeken van de kolom Charge Time.
df3['ChargeTime'].describe()


# In[25]:


#Negatieve Charge Time droppen.
df3 = df3[df3['ChargeTime'] > 0]

#Waarde boven 20 droppen
df3 = df3[df3['ChargeTime'] <= 15]


# In[26]:


#Kolom Connected Time inspecteren
df3['ConnectedTime'].describe()


# In[27]:


#Hier wordt er gefilterd zodat de connected time onder de 30 uur zit.
df3 = df3[df3['ConnectedTime'] <= 30]


# In[28]:


#Hier worden strings aangemaakt voor de histogram
string1 = 'Mean: ' + str(round(df3['ConnectedTime'].mean(), 4))
string2 = 'Median: ' + str(round(df3['ConnectedTime'].median(), 4))
string3 = 'Mean: ' + str(round(df3['ChargeTime'].mean(), 4))
string4 = 'Median: ' + str(round(df3['ChargeTime'].median(), 4))


# In[29]:


#Hier wordt een histogram gemaakt voor zowel de Charge time en Connected time. 
fig, ax = plt.subplots()

sns.histplot(data = df3, x = 'ConnectedTime', bins = 39, label = 'Connected time', color = 'Blue')
sns.histplot(data = df3, x = 'ChargeTime', bins = 20, label = 'Charge time', color = 'Red')

ax.set_title('Histogram met de verdeling van tijd voor opladen van voertuigen')
ax.set_xlabel('Laadtijd in uren')
ax.set_ylabel('Aantal voertuigen')

plt.annotate(string1, xy = (10, 2000), color = 'Blue')
plt.annotate(string2, xy = (10, 1850), color = 'Blue')
plt.annotate(string3, xy = (10, 1600), color = 'Red')
plt.annotate(string4, xy = (10, 1450), color = 'Red')

plt.legend()

plt.show()


# Uit de plot valt te halen, dat veel auto's langer connected zijn dan dat er daadwerkelijk geladen wordt.

# In[ ]:





# In[ ]:




