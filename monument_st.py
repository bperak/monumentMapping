# Streamlit app for visualizing Monument Hunter app

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import requests
import dms2dec


# import dependencies with functions
import monuments_maps as mm

st.title('Monument Hunter')


link='https://docs.google.com/spreadsheets/d/e/2PACX-1vTEQoPh4WL5BeVLtfXksmBovzvELDEuVjn9edaLlRnNdotBOcIraykPaWCyUxepB3WFiGWog7ziJ2yZ/pub?output=xlsx'
sheets=('main', 'dodatno')


df= mm.data_import(link, sheets, 0)
# pretvori 
# df.replace({'geolokacija':r'^°.*'}, {'geolokacija'= NaN}  , regex=True)


# dodaj lat, lon stupce
try:
    df['lat']= df['geolokacija'].str.split(',').str[0].astype('float')
    df['lon']= df['geolokacija'].str.split(',').str[1].astype('float')
except:
    pass
df
df.columns


# Izbornici
slide= st.slider('Moj slider', 1,2000,3)
# pogledaj slider
slide

# Po nazivu spomenika
monument_name = st.text_input('Naziv spomenika')
if monument_name:
    df[df.nazivSpomenika.str.contains(monument_name)]

# Po mjestu
monument_place = st.text_input('Mjesto spomenika')
if monument_place:
    df[df.nazivSpomenika.str.contains(monument_place)]

# Po materijalu
df['materijal izgradnje spomenika'] = df['materijal izgradnje spomenika'].fillna('nepoznato')
material_set= df['materijal izgradnje spomenika'].str.split(',', expand=True).stack().unique()
monument_material = st.multiselect('Materijal spomenika', material_set)
if monument_material:
    df[df['materijal izgradnje spomenika'].apply(lambda x: any([i in x for i in monument_material]))]

# Wikidata upit
wiki_query = st.text_input('Wikidata upit')
if wiki_query:
    st.write(mm.wikidata_get(wiki_query))

# Wikidata upit o entitetu
wiki_entity = st.text_input('Wikidata entitet')
if wiki_entity:
    st.write(mm.wikidata_info(wiki_entity))




# folium  implementacija

# center on Liberty Bell
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
# add marker for Liberty Bell
tooltip = "Liberty Bell"
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
    ).add_to(m)
# call to render Folium map in Streamlit
folium_static(m)

folium_static(mm.map_monument(df))
