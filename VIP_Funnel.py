import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
from mycolorpy import colorlist as mcp
import numpy as np

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets


# Authenticate using the service account credentials
gauth = GoogleAuth()
gauth.service_account_email = 'drive-prueba@theta-actor-415016.iam.gserviceaccount.com'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
service_info = st.secrets['credentials']
gauth.credentials  = ServiceAccountCredentials.from_json_keyfile_dict(service_info,scope)
gauth.Authorize()
drive = GoogleDrive(gauth)

st.set_page_config(
    page_title="Subscriptions",
    page_icon="🟢",
    layout="wide"
)

st.title('VIP Funnel')

st.sidebar.header("Subscriptions")





option = st.selectbox(
    'Mes',
    ('Octubre 2023','Noviembre 2023','Diciembre 2023', 'Enero 2024'))
if option == 'Octubre 2023':
    spreadsheet_name = '202310'
    # prev = pd.read_csv('Fil/logs_202310_prev.csv')
    # post = pd.read_csv('Mau/202310_post.txt',sep= '	')  
    # post1 = pd.read_csv('Mau/202310_post1.txt', sep =  '	',index_col=False) 
elif option == 'Noviembre 2023':
    spreadsheet_name = '202311'
if option == 'Diciembre 2023':
    spreadsheet_name = '202312'
if option == 'Enero 2024':
    spreadsheet_name = '202401'

#Extraemos los los ID de los sheets según el que se pida 
spreadsheet_query = f"title='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
spreadsheets = drive.ListFile({'q': spreadsheet_query}).GetList()
if spreadsheets:
    target_spreadsheet = spreadsheets[0]
    print(f"Found Spreadsheet: {target_spreadsheet['title']} (ID: {target_spreadsheet['id']})")
    ID = target_spreadsheet['id']

#abrimos el spreadsheet con pygsheets 
gc = pygsheets.authorize(service_file='theta-actor-415016-cb72513aed67.json')
sh = gc.open_by_key(ID)
worksheet1 = sh.worksheet('title','prev')
worksheet2 = sh.worksheet('title','post')
worksheet3 = sh.worksheet('title','post1')

prev = worksheet1.get_as_df(has_header=True)
post = worksheet2.get_as_df(has_header=True)
post1 = worksheet3.get_as_df(has_header=True)




#Format -----------
prev['Target'] = 'Click on Button for purchase membership' 
prev.rename(columns= {'num_actions':'Clicks','prev_action':'Source'}, inplace = True)
carousel = prev[prev.apply(lambda row: row.astype(str).str.contains('Clicked carousel image').any(), axis=1)]
prev2 = prev.drop(index=carousel.index)
new_row = pd.DataFrame.from_dict({'Clicks':[carousel.Clicks.sum()], 'Source':['Clicked carousel image'],'Target':['Click on Button for purchase membership']})
prev2 = pd.concat([prev2,new_row], ignore_index=True)

#% en dataframe 
prev.insert(1,'%',[round(x*100/prev.Clicks.sum(),2) for x in list(prev.Clicks) ])
post.insert(1,'%',[round(x*100/post.Clicks.sum(),2) for x in list(post.Clicks) ])
post1.insert(1,'%',[round(x*100/post1.Clicks.sum(),2) for x in list(post1.Clicks) ])
prev2.insert(1,'%',[round(x*100/prev2.Clicks.sum(),2) for x in list(prev2.Clicks) ])

#4% en otros
otros_prev2 = prev2[prev2['%']<4]
otros_post1 =  post1[post1['%']<4] 
otros_int = otros_post1[otros_post1.Source == 'Interacting With Payment Page']
otros_change = otros_post1[otros_post1.Source == 'Change Flow']

new_prev2 = prev2.drop(index= otros_prev2.index)
new_post1 =  post1.drop(index= otros_post1.index)
new_row_prev2 = pd.DataFrame.from_dict({'Clicks':[otros_prev2.Clicks.sum()], 'Source':['Otras acciones'],'Target':['Click on Button for purchase membership']})
new_row_post1_1 = pd.DataFrame.from_dict({'Clicks':[otros_int.Clicks.sum()], 'Source':['Interacting With Payment Page'],'Target':['Otras acciones en payment']})
new_row_post1_2 = pd.DataFrame.from_dict({'Clicks':[otros_change.Clicks.sum()], 'Source':['Change Flow'],'Target':['Otras acciones en flujo']})
new_prev2 = pd.concat([new_prev2,new_row_prev2], ignore_index=True)
new_post1 = pd.concat([new_post1,new_row_post1_1,new_row_post1_2], ignore_index=True)

funnel = pd.concat([new_prev2,post,new_post1], ignore_index=True)
colors =mcp.gen_color(cmap="viridis",n=len(funnel))
funnel['Colors'] = colors



#Diagrama ---------------------------------------------------------
unique_source_target = list(pd.unique(funnel[['Source', 'Target']].values.ravel('K')))
mapping_dict = {k: v for v, k in enumerate(unique_source_target)}


funnel['Source'] = funnel['Source'].map(mapping_dict)
funnel['Target'] = funnel['Target'].map(mapping_dict)  
links_dict = funnel.to_dict(orient='list')

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
      value = links_dict["Clicks"],
      color = links_dict["Colors"]
    ),
)],)

# Update layout
fig.update_layout(title_text=option, font_size=15, autosize=False, width=1500, height=1000)


def highlight_low_values(val):
    color = '#AF1F00' if val < 4 else None 
    return f'background-color: {color}'

def highlight_low_values1(val):
    color = '#AF1F00' if val < 4 else None 
    return f'background-color: {color}'

def highlight_low_values2(val):
    color = '#bd4d4d' if val < 4 else None 
    return f'background-color: {color}'

subset_index = otros_change.index.tolist()
styled_df = post1.style.map(highlight_low_values1, subset=pd.IndexSlice[subset_index, '%'])
subset_index = otros_int.index.tolist()
styled_df = styled_df.map(highlight_low_values2, subset=pd.IndexSlice[subset_index, '%'])

tab0, tab1, tab2, tab3 = st.tabs(['Funnel Subscriptions',"Acciones previas", "Cambio de flujo", "Acciones posteriores "])


with tab0:
    st.header("Funnel Subscriptions")
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    st.header("Acciones previas")
    st.write(f'Nota: Los porcentajes menores al 4% se añadieron a "Otras acciones" (resaldados en rojo)')

    st.table(prev.style.map(highlight_low_values,subset=['%']))

with tab2:
    
    st.header("Cambio de flujo")
    st.table(post.style.map(highlight_low_values,subset=['%']))

with tab3:
    st.header("Acciones posteriores")
    st.write(f'Nota: Los porcentajes menores al 4% se añadieron a "Otras acciones en flujo" y a "Otras acciones en payment" (resaldados en rojo)')
    st.table(styled_df)

