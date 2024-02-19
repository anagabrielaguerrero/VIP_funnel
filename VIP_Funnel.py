import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
from mycolorpy import colorlist as mcp
import numpy as np



st.set_page_config(layout="wide")

st.title('VIP Funnel')




option = st.selectbox(
    'Mes',
    ('Octubre 2023','Noviembre 2023','Diciembre 2023', 'Enero 2024'))
if option == 'Octubre 2023':
    prev = pd.read_csv('Fil/logs_202310_prev.csv')
    post = pd.read_csv('Mau/202310_post.txt',sep= '	')  
    post1 = pd.read_csv('Mau/202310_post1.txt', sep =  '	',index_col=False) 
elif option == 'Noviembre 2023':
    prev = pd.read_csv('Fil/logs_202311_prev.csv')
    post = pd.read_csv('Mau/202311_post.txt',sep= '	')  
    post1 = pd.read_csv('Mau/202311_post1.txt', sep =  '	',index_col=False) 
if option == 'Diciembre 2023':
    prev = pd.read_csv('Fil/logs_202312_prev.csv')
    post = pd.read_csv('Mau/202312_post.txt',sep= '	')  
    post1 = pd.read_csv('Mau/202312_post1.txt', sep =  '	',index_col=False) 
if option == 'Enero 2024':
    prev = pd.read_csv('Fil/logs_202401_prev.csv')
    post = pd.read_csv('Mau/202401_post.txt',sep= '	')  
    post1 = pd.read_csv('Mau/202401_post1.txt', sep =  '	',index_col=False) 

#Format
prev['Target'] = 'Click on Button for purchase membership' 
prev.rename(columns= {'num_actions':'Clicks','prev_action':'Source'}, inplace = True)
carousel = prev[prev.apply(lambda row: row.astype(str).str.contains('Clicked carousel image').any(), axis=1)]
prev2 = prev.drop(index=carousel.index)
new_row = pd.DataFrame.from_dict({'Clicks':[carousel.Clicks.sum()], 'Source':['Clicked carousel image'],'Target':['Click on Button for purchase membership']})
funnel = pd.concat([prev2,new_row,post,post1], ignore_index=True)
colors =mcp.gen_color(cmap="viridis",n=len(funnel))
funnel['Colors'] = colors
#% en dataframe 
prev.insert(1,'%',[round(x*100/prev.Clicks.sum(),2) for x in list(prev.Clicks) ])
post.insert(1,'%',[round(x*100/post.Clicks.sum(),2) for x in list(post.Clicks) ])
post1.insert(1,'%',[round(x*100/post1.Clicks.sum(),2) for x in list(post1.Clicks) ])


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
    color = 'red' if val < 5 else 'black'
    return f'color: {color}'

tab0, tab1, tab2, tab3 = st.tabs(['Funnel Subscriptions',"Acciones previas", "Cambio de flujo", "Acciones posteriores "])


with tab0:
    st.header("Funnel Subscriptions")
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    st.header("Acciones previas")
    st.table(prev.style.map(highlight_low_values,subset=['%']))


with tab2:
    st.header("Cambio de flujo")
    st.table(post)

with tab3:
    st.write("Acciones posteriores")
    st.table(post1)

