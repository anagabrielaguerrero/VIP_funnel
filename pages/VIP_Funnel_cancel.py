import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
from mycolorpy import colorlist as mcp
import numpy as np

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets


spreadsheet_name = 'Cancelations'
spreadsheet_query = f"title='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
spreadsheets = drive.ListFile({'q': spreadsheet_query}).GetList()
if spreadsheets:
    target_spreadsheet = spreadsheets[0]
    print(f"Found Spreadsheet: {target_spreadsheet['title']} (ID: {target_spreadsheet['id']})")
    ID = target_spreadsheet['id']

#abrimos el spreadsheet con pygsheets 
gc = pygsheets.authorize(service_file='theta-actor-415016-cb72513aed67.json')
sh = gc.open_by_key(ID)
worksheet1 = sh.worksheet('title','old_new')
worksheet2 = sh.worksheet('title','upgrades')

old_new = worksheet1.get_as_df(has_header=True)
success = worksheet2.get_as_df(has_header=True)


st.set_page_config(
    page_title="Cancellations",
    page_icon="🔴",
    layout="wide"
)

st.title('VIP Funnel')

st.sidebar.header("Cancellations")

#format 
old = old_new[old_new['is_first_subscription']==0]   #ord(b'\x00' 
new = old_new[old_new['is_first_subscription']==1] 
old_m = old.groupby('yearmo').agg({'total': 'sum'})  # todos por mes 
new_m = new.groupby('yearmo').agg({'total': 'sum'})
old_success = success[success['is_first_subscription']==0]  
new_success = success[success['is_first_subscription']== 1] 
old['Source'] = 'Old' #añadiendo nodos 
new['Source'] = 'New'
old_success['Source'] = 'Upgrade Attempt Old'
new_success['Source'] = 'Upgrade Attempt New'
old.loc[old['type'] == 'Upgrade Attempt', 'type'] = 'Upgrade Attempt Old'
new.loc[new['type'] == 'Upgrade Attempt', 'type'] = 'Upgrade Attempt New'
old.loc[old['type'] == 'Upgrade Attempt', 'type'] = 'Upgrade Attempt Old'
new.loc[new['type'] == 'Upgrade Attempt', 'type'] = 'Upgrade Attempt New'


option = st.selectbox(
    'Mes',
    ('Septiembre 2023','Octubre 2023','Noviembre 2023','Diciembre 2023', 'Enero 2024'))
if option == 'Septiembre 2023':
    yearmo = 202309
elif option == 'Octubre 2023':
    yearmo = 202310
elif option == 'Noviembre 2023':
    yearmo = 202311
if option == 'Diciembre 2023':
    yearmo = 202312
if option == 'Enero 2024':
    yearmo = 202401

funnel = pd.DataFrame.from_dict({'Source':['Total Manual','Total Manual'], 'Target': ['Old','New'], 'Value': [old_m.loc[yearmo, 'total'],new_m.loc[yearmo, 'total']]})
flux_old = pd.DataFrame({'Source':list(old[old['yearmo'] == yearmo]['Source']), 'Target':list(old[old['yearmo'] == yearmo]['type']), 'Value':list(old[old['yearmo'] == yearmo]['total'])})
flux_new = pd.DataFrame({'Source':list(new[new['yearmo'] == yearmo]['Source']), 'Target':list(new[new['yearmo'] == yearmo]['type']), 'Value':list(new[new['yearmo'] == yearmo]['total'])})
flux_old_success = pd.DataFrame({'Source':list(old_success[old_success['yearmo'] == yearmo]['Source']), 'Target':['Successful '], 'Value':list(old_success[old_success['yearmo'] == yearmo]['count(*)'])})
flux_new_success = pd.DataFrame({'Source':list(new_success[new_success['yearmo'] == yearmo]['Source']), 'Target':['Successful '], 'Value':list(new_success[new_success['yearmo'] == yearmo]['count(*)'])})
flux_new_fail = pd.DataFrame({'Source':'Upgrade Attempt New', 'Target': 'Failed upgrade', 'Value':[flux_new[flux_new['Target'] == 'Upgrade Attempt New']['Value'].values[0]-new_success[new_success['yearmo'] == yearmo]['count(*)'].values[0]]}) 
flux_old_fail = pd.DataFrame({'Source':'Upgrade Attempt Old', 'Target': 'Failed upgrade', 'Value': [flux_old[flux_old['Target'] == 'Upgrade Attempt Old']['Value'].values[0]- old_success[old_success['yearmo'] == yearmo]['count(*)'].values[0]]})

funnel = pd.concat([funnel,flux_old,flux_new,flux_old_success,flux_new_success,flux_old_fail,flux_new_fail], ignore_index=True)
colors =mcp.gen_color(cmap="viridis",n=len(funnel))
funnel['Colors'] = colors

#Diagrama ---------------------------------------------------------
unique_source_target = list(pd.unique(funnel[['Source', 'Target']].values.ravel('K')))
mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
funnel['Source'] = funnel['Source'].map(mapping_dict)
funnel['Target'] = funnel['Target'].map(mapping_dict)  
links_dict = funnel.to_dict(orient='list')

# Create figure
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.3),
        label= unique_source_target
    ),
    link=dict(
      source = links_dict["Source"],
      target = links_dict["Target"],
      value = links_dict["Value"],
      color = links_dict["Colors"]
    ),
)],)

# Update layout
fig.update_layout(title_text="Enero 2024", font_size=15, autosize=False, width=1500, height=1000)

tab0, tab1 = st.tabs(['Funnel Cancellations',"True cancel reasons"])


with tab0:
    st.header("Funnel Cancellations")
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    st.header("True cancel reasons")
    st.write(f'Nota: PENDIENTE')