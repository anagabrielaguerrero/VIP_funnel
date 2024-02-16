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

nodes = list(prev.prev_action)
nodes.append('Click on Button for purchase membership')
nodes_post = np.unique(post.Target, return_index=True)
nodes_post1_t = np.unique(post1.Target, return_index=True)
nodes_post1_s = np.unique(post1.Source, return_index=True)

colors =mcp.gen_color(cmap="viridis",n=len(nodes)+len(nodes_post[1])+len(nodes_post1_t[1]))

#Links de prev actions
links = []
for i in range(len(nodes)-1):
    links.append({'source': i, 'target': len(nodes)-1, 'value': prev.num_actions[i], 'color': colors[i]})

#Links de post1 actions 
for i in range(len(nodes_post1_s[1])): 
        for j in indices_por_valor['Indices'][nodes_post[1][i]]:
                links.append({'source':nodes_post[1][i] +len(nodes), 
                        'target': j+ len(nodes_post[0]) +len(nodes),
                        'value': post1.Clicks[j],
                        'color': colors[i+len(nodes)+len(nodes_post)]})

indices_por_valor = post1.groupby('Source').apply(lambda x: x.index.tolist()).reset_index(name='Indices')

#Links de post1 actions 
for i in range(len(nodes_post1_s[1])): 
    for j in post1.Target[post1.Source == nodes_post1_s[0][i]].index:
        links.append({'source':nodes_post[1][i] +len(nodes), 
                'target': labels.index(nodes_post1_t[0][j]), 
                'value': post1.Clicks[nodes_post1_t[1][j]],
                'color': colors[i+len(nodes)+len(nodes_post)]})

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.3),
        label=nodes + list(nodes_post[0]) + list(nodes_post1_t)
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links], color =[link['color'] for link in links]
    ),
)],)

fig.update_layout(title_text=option, font_size=15, autosize=False, width=1500, height=1000)

prev.rename(columns= {'num_actions':'# Clicks','prev_action':'Acción previa'}, inplace = True)

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Acciones previas")
    st.table(prev)

    # st.dataframe(prev,use_container_width=True)
    # st.markdown(prev.style.hide(axis="index").to_html(), unsafe_allow_html=True)

with col2:
    st.write("Cambio de flujo")
    # st.dataframe(post,use_container_width=True)
    st.table(post)

    # st.markdown(post.style.hide(axis="index").to_html(), unsafe_allow_html=True)

with col3:
    st.write("Acciones posteriores")
    st.table(post1)
    # st.dataframe(post1,use_container_width=True)
    # st.markdown(post1.style.hide(axis="index").to_html(), unsafe_allow_html=True)

