
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 17:35:39 2019

@author: Korisnik
"""
#%%
# coding: utf-8
# pip install folium
# https://python-visualization.github.io/folium/quickstart.html
# data source: https://docs.google.com/spreadsheets/d/1akLiE6N2QNMNumkePVYzKwQfL8qQ6f3HWbQBW56SVYg/edit#gid=1861864601

#%% 1 Imports
import streamlit as st
import folium
import numpy as np
import pandas as pd
from folium.plugins import MarkerCluster #više objekata na istom mjestu pretvoreno u klaster
import time
import requests
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty



#%%
def version_time():
    seconds=time.time()
    local_time=time.ctime(seconds)
    with open("time.txt", "w") as file:
        file.write(local_time)

def read_version_time():
    with open("time.txt", "r") as file:
        version_time=file.read()
        #print(version_time)
        return(version_time)

        
# #%% Defining data links, sheets on Googlesheet
# link='https://docs.google.com/spreadsheets/d/e/2PACX-1vTEQoPh4WL5BeVLtfXksmBovzvELDEuVjn9edaLlRnNdotBOcIraykPaWCyUxepB3WFiGWog7ziJ2yZ/pub?output=xlsx'
#%% Data import
@st.cache(allow_output_mutation=True)
def data_import(link, sheetsTuple, sheetIndex):
    data=pd.read_excel(link, sheet_name=sheetsTuple[sheetIndex])
    #strip column names from spaces
    data.columns = data.columns.str.strip()
    return (data)
# primjer: data_import(link, 0)


def wikidata_get(query):
    # Wikidata obogaćivanje podataka
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'hr',
        'search': query
    }
    r = requests.get(API_ENDPOINT, params = params)
    return r.json()['search']

def wikidata_info(query):
    q_dict = get_entity_dict_from_api(query)
    q = WikidataItem(q_dict)
    res_dict = {'entity_id': q.entity_id,
    'entity_type': q.entity_type,
    'label()': q.get_label(),
    'description()':q.get_description(),
    'aliases()': [q.get_aliases()],
    'enwiki_title()': q.get_enwiki_title(), 
    'q.get_sitelinks()':[q.get_sitelinks()]
    }
    res_dict
    return pd.DataFrame().from_dict(res_dict)
#%%
# df= data_import(link, 0)
# slika=(df.uploadSlike)
#%%
# slika[1]
#%%
def map_monument(df):
    centerPoint=[df.lon.dropna().mean(), df.lat.dropna().mean()] #df.geoCoord_lat.median(), df.geoCoord_lon.median()
    #creating a map frame
    mMonument = folium.Map(centerPoint, zoom_start = 6,tiles='Stamen Terrain')
    #creating marker clusters
    mcMonument = MarkerCluster()
    
    #Boravi
    for row in df.itertuples(): 
        try:
            #formatiranje teksta i ikona
            text=folium.Html(f'<img src={row.uploadSlike}+"/edit" class="img-responsive">'+
								f'<br><b>{row.nazivSpomenika}</b>'+
                             " "+f'<br>{row.opis}<br>'+
                             " izgrađen "+f'<i>{row.datumGradnje}</i><br>'+
                             " autor  "+f'{row.autorSpomenika}<br>'+
                             " text "+f'{row.tekstSpomenika}<br>'+
                             " stanje: "+f'{row.stanjeSpomenika}<br>',
                            script=True)
            popup = folium.Popup(text, max_width=300,min_width=300)
            
            #colors marker
            if row.rat== "WW1":
                colors = "red"
            elif row.rat== "WW2":
                colors = "blue"
            elif row.rat == "domovinski":
                colors = "green"
            else:
                colors = "gray"
                   
            icon=folium.Icon(icon='stop', color = colors)
            
            #georeferencija 
            mcMonument.add_child(folium.Marker(location=[row.geoCoord_lat, row.geoCoord_lon], 
                                       popup = popup,
                                       icon=icon))
        except:
            pass


    mMonument.add_child(mcMonument)
    mMonument.save('static/htmls/map_monument.html')
    return(mcMonument)


# map_monument()