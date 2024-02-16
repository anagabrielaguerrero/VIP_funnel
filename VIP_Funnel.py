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
nodes_post1_t = list(post1.Target)
nodes_post1_s = np.unique(post1.Source, return_index=True)

colors =mcp.gen_color(cmap="viridis",n=len(nodes)+len(nodes_post[1])+len(nodes_post1_t))
#Links de prev actions
links = []
for i in range(len(nodes)-1):
    links.append({'source': i, 'target': len(nodes)-1, 'value': prev.num_actions[i], 'color': colors[i]})

#Links de post actions 
for i in range(len(nodes_post[1])):
    links.append({'source':len(nodes)-1, 'target': nodes_post[1][i] +len(nodes), 'value': post.Clicks[nodes_post[1][i]], 'color': colors[i]})

indices_por_valor = post1.groupby('Source').apply(lambda x: x.index.tolist()).reset_index(name='Indices')

index = [indices_por_valor.Source[indices_por_valor.Source == nodes_post1_s[0][x]].index for x in range(len(nodes_post1_s))]
index = [indice[0] for indice in index]


#Links de post1 actions 
for i in nodes_post1_s[1]: 
        a = 0
        for j in indices_por_valor['Indices'][i]:
                links.append({'source':nodes_post[1][i] +len(nodes), 
                        'Source name': nodes_post[0][i],
                        'target': j+ len(nodes_post[0]) +len(nodes),
                        'Target name': post1.Target[j],
                        'value': post1.Clicks[j],
                        'color': colors[i+len(nodes)+len(nodes_post)]})


prev.rename(columns= {'num_actions':'# Clicks','prev_action':'Acción previa'}, inplace = True)

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

tab0, tab1, tab2, tab3 = st.tabs(['Funnel Subscriptions',"Acciones previas", "Cambio de flujo", "Acciones posteriores "])


with tab0:
    st.header("Funnel Subscriptions")
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    st.header("Acciones previas")
    st.table(prev)


with tab2:
    st.header("Cambio de flujo")
    st.table(post)

with tab3:
    st.write("Acciones posteriores")
    st.table(post1)

