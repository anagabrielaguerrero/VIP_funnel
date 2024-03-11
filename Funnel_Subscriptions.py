import pandas as pd 
import streamlit as st
import plotly.graph_objects as go
from mycolorpy import colorlist as mcp
import numpy as np
from gspread_pandas import Spread,Client
import seaborn as sns
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import calendar 
# Authenticate using the service account credentials --------------------------------------------------------------------
gauth = GoogleAuth()
gauth.service_account_email = 'drive-prueba@theta-actor-415016.iam.gserviceaccount.com'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# service_info = st.secrets['credentials']
service_info = {
  "type": "service_account",
  "project_id": "theta-actor-415016",
  "private_key_id": "cb72513aed67a84afa89bb182aaead4983281ed4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAc4mZrjvQWWWi\njXSCdxjw1BTVcYmaV52DJUWPnYWk2+pQ5/R2uWgju+f0kvkQOkcvCzSVZGy15Rq/\nLTNdrPiqN/nbY0AEol2FKXMsHCH38v9kXYgaSNmJvp9RZD8xyHck6aDjMuYuMRlY\nZFvSTgMaGBAGORvUChewWtw2J5MghMDawc7mJmEBnamViNqFyGyGv5LWTNWrsHXn\nNm5ffXPd5nF4w/eg1hxLBzfnUVGXe+Kh/sKOiG/9m3tLjIA+WeRDg5yquZe7P9kM\nLrjjh7p3RY5NT7ityEZr7FbUxhSrF/INf2e49DRnXqDZxb2y9I+/OqJTk7H4Wcw4\nYiT1rPDtAgMBAAECggEADETRVtzGr2ejlRNThCW3j1LV6S2NyisfvYaYwqkWJgZn\nD7VZ3l+/hdeq1+quuhwdAaDDP2rhi08Jv3pQNf6a868R3KydHi6Dq8OSthMtDzOM\nmIdl79cJF0DxwyyS4seW4OGMAi/ygKtcpEfxmpyikf1KuDrXzVK/Y9zHASTQulff\n1BO0/qjTmncCG+3TuprI7xmz+0J9aU1a2bu3JGMtGJfuIJScoUN91YDqHsbrGMLO\nyxXMNe6e+vmpWOcywhL0a8ODyaxnhta4Bk5Y92ztxyiajno2rX2aRy40muQix2MY\nfmQh6XsynQaq31ytHcH5QZprn7E5egM9sAUa4M3tAQKBgQDxxXOShO1bK73cg5GT\nly9Rhbionu7KZXEqcYG1LSFrJ/ZNQqlehlyEKNVCm3/avqp8DeFJqgSKYfJwB3GM\npH0zEu/j87iv9UZ7Om2MGN2YfZfymIiy5HIXPIzMFZs+fZCftGbU4zIBVeqLtAuS\nbgsLmHnWP9bYd7JIx7U2qRRTjQKBgQDLxwbZGDIk4hdm7m5p1NTvwIdHDDO5bQwu\n9lhkY1vSEamiCRV/3c6TDFYCjNOthby3tgY7RKnUmUrojPy0Czw/i4K3DIeCt/0c\nzouqqTc7lQtAV7eiLJUQn3lKOFISYKNkZNJ1Uy2qyFZPWvCsSMRSi8Batur6ZE1W\nY2RUBLwK4QKBgFRPbNwdasAuYskxQGTdhezB2wFCWzdNZMdOSdMqZ8r8ZpHOu01x\nQXX831GY9F8NuloEZRnRJkAzo92ZWumWuupColE1vqPtvqReXbFLQotY0NISiykH\nLRoZTWgl6LtEAlkPCgUXLWr10RLiuF5Z7ZQfme0y2fMm2o8yxWjIUYRJAoGBAMV/\n6nUybDcvIftTD5RnANI1yWbkvqTyuaIyhE0Xt4CMOdqf70R0l6gRhrMGBorhWZy8\nQKHk1K0GvYFSVAGz+fqknlYHQLdC14C59se7JZsLw1HjMklt6DOqPIXgvDqviuzc\ngtXPfi1N6ckTnLt98zkF1bKWInv4BrS5tB1yUUZBAoGAQK0yUBEKSSbRAV2Nhx6X\n4b0nX1bXNMedWoaWRezrk1BoQtFtpnRB7enpVsDRU9XJU61of41VdRG4UE8Fh+rm\n9m6Tr08mYprlvw+AnYizS7MN+6Nazrpk9sWUeMokoz3kPZco4/iEd5eVgAqeL1uP\neMoKigSNdbCFCA/oIUNiOo8=\n-----END PRIVATE KEY-----\n",
  "client_email": "drive-prueba@theta-actor-415016.iam.gserviceaccount.com",
  "client_id": "100476254397966367091",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/drive-prueba%40theta-actor-415016.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
gauth.credentials  = ServiceAccountCredentials.from_json_keyfile_dict(service_info,scope)
gauth.Authorize()
drive = GoogleDrive(gauth)
#%% ---------------------------------------------------------------------------------------------------------------------
#Configuración pág principal 
st.set_page_config(
    page_title="Subscriptions",
    page_icon="🟢",
    layout="wide"
)
st.title('VIP Funnel')
st.sidebar.header("Subscriptions")
#%%  ---------
start_date = datetime.now()  #para tener en cuenta el mes actual 

with st.expander('Mes'):
    this_year = start_date.year
    this_month = start_date.month
    report_year = st.selectbox('', range(this_year, this_year - 5, -1))
    month_abbr = calendar.month_abbr[1:]
    report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
    report_month = month_abbr.index(report_month_str) + 1
st.write(f'{report_year} {report_month_str}')
if report_month <= 9:
    spreadsheet_name  = f'{report_year}'+'0'+f'{report_month}'
else: 
    spreadsheet_name  = f'{report_year}{report_month}'
option = f'{report_year} {report_month_str}'
#%%% Para abrir los sheets 
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_info(service_info, scopes = scope)
client = Client(scope=scope,creds=credentials)
spread = Spread(spreadsheet_name,client = client)
sh = client.open(spreadsheet_name)
worksheet_list = sh.worksheets()

folder_id = '1juC34pcnAZu5QeTDB-k5xbyOnNlamxJ3'
file_name = spreadsheet_name
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Funciones para abrir los sheets 
@st.cache()
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

prev = load_the_spreadsheet('prev')
post1 = load_the_spreadsheet('post1')
#%% Transformacion datos post para funnel ----------
post = pd.DataFrame(post1.groupby('Source')['Clicks'].sum()).reset_index()
post.rename(columns= {'Source':'Target'}, inplace = True)
post['Source'] = 'Click on Button for purchase membership' 
post1 = post1[post1.Source != 'No more actions']

#%% Transformacion datos prev para funnel -----------
prev['Target'] = 'Click on Button for purchase membership' 
carousel = prev[prev.apply(lambda row: row.astype(str).str.contains('Clicked carousel image').any(), axis=1)]
prev2 = prev.drop(index=carousel.index)
new_row = pd.DataFrame.from_dict({'Clicks':[carousel['Clicks'].sum()], 'Source':['Clicked carousel image'],'Target':['Click on Button for purchase membership']})
prev2 = pd.concat([prev2,new_row], ignore_index=True)

#% Transformacion datos para dataframe 
prev.insert(1,'%',[round(x*100/prev['Clicks'].sum(),2) for x in list(prev['Clicks']) ])
post.insert(1,'%',[round(x*100/post['Clicks'].sum(),2) for x in list(post['Clicks']) ])
post1.insert(1,'%',[round(x*100/post1['Clicks'].sum(),2) for x in list(post1['Clicks']) ])
prev2.insert(1,'%',[round(x*100/prev2['Clicks'].sum(),2) for x in list(prev2['Clicks']) ])

#%% 4% en otros en Funnel 
otros_prev2 = prev2[prev2['%']<4]
otros_post1 =  post1[post1['%']<4] 
otros_int = otros_post1[otros_post1.Source == 'Interacting With Payment Page']
otros_change = otros_post1[otros_post1.Source == 'Change Flow']

#Datos transformados para Funnel 
new_prev2 = prev2.drop(index= otros_prev2.index)
new_post1 =  post1.drop(index= otros_post1.index)
new_row_prev2 = pd.DataFrame.from_dict({'Clicks':[otros_prev2['Clicks'].sum()], 'Source':['Otras acciones'],'Target':['Click on Button for purchase membership']})
new_row_post1_1 = pd.DataFrame.from_dict({'Clicks':[otros_int['Clicks'].sum()], 'Source':['Interacting With Payment Page'],'Target':['Otras acciones en payment']})
new_row_post1_2 = pd.DataFrame.from_dict({'Clicks':[otros_change['Clicks'].sum()], 'Source':['Change Flow'],'Target':['Otras acciones en flujo']})
new_prev2 = pd.concat([new_prev2,new_row_prev2], ignore_index=True)
new_post1 = pd.concat([new_post1,new_row_post1_1,new_row_post1_2], ignore_index=True)

funnel = pd.concat([new_prev2,post,new_post1], ignore_index=True)
colors =mcp.gen_color(cmap="viridis",n=len(funnel))
funnel['Colors'] = colors
#Métricas -------------------------------------------------------------
#porcentaje de txns vip = txns_vip/activos 
#Porcentaje de suscripciones vip = comp_memb/activos 
#porcentje de usuarios en app que dieron click en botón = post.Clicks.sum()/Activos_en app

folder_id = '1juC34pcnAZu5QeTDB-k5xbyOnNlamxJ3'
sh = client.open("MAUs")
worksheet_list = sh.worksheets()
MAUs = load_the_spreadsheet('MAUs')
col1, col2 = st.columns(2)

txns_vip = round(MAUs.loc[MAUs['Fecha']== int(spreadsheet_name), ['Activos VIP']].values[0][0] / MAUs.loc[MAUs['Fecha']== int(spreadsheet_name), ['Activos']].values[0][0] * 100,2)
suscrip_vip = round(post.Clicks.sum() / MAUs.loc[MAUs['Fecha']== int(spreadsheet_name), ['Activos_en_app']].values[0][0] * 100,2)
compras_click = round( MAUs.loc[MAUs['Fecha']== int(spreadsheet_name), ['Compra_memb']].values[0][0] / post.Clicks.sum()* 100,2)

index = MAUs.index[MAUs['Fecha']== int(spreadsheet_name)].tolist()
#mesanterior para calculare el delta 

selected_row = MAUs.iloc[index[0] - 1]

txns_vip_a = round(selected_row['Activos VIP'] / selected_row['Activos'] * 100,2)
suscrip_vip_a = round(post.Clicks.sum() / selected_row['Activos_en_app'] * 100,2)
compras_click_a = round(selected_row['Compra_memb']/post.Clicks.sum() * 100,2)


with col1:
    st.header("Users")
    st.markdown(MAUs[MAUs['Fecha']== int(spreadsheet_name)].style.hide(axis="index").to_html(), unsafe_allow_html=True)
with col2:        
    st.header("Porcentajes")
    col21, col22,col23 = st.columns(3)
    with col21:
        st.metric(label="Txns VIP", value=str(txns_vip)+'%', delta=str(round(txns_vip-txns_vip_a,2))+"%",help = 'a')
    with col22: 
        st.metric(label="Activos en app que hicieron click", value=str(suscrip_vip)+'%', delta=str(round(suscrip_vip-suscrip_vip_a,2))+"%")
    with col23: 
        st.metric(label="Suscripciones VIP", value=str(compras_click)+'%', delta=str(round(compras_click-compras_click_a,2))+"%")


#Diagrama ---------------------------------------------------------
unique_source_target = list(pd.unique(funnel[['Source', 'Target']].values.ravel('K')))
mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
funnel['Source'] = funnel['Source'].map(mapping_dict)
funnel['Target'] = funnel['Target'].map(mapping_dict)  
links_dict = funnel.to_dict(orient='list')

fig = go.Figure(data=[go.Sankey(node=dict(pad=15,thickness=20,line=dict(color="black", width=0.3),label= unique_source_target),
                                link=dict(source = links_dict["Source"], target = links_dict["Target"],value = links_dict["Clicks"], color = links_dict["Colors"]),)],)
fig.update_layout(title_text=option, font_size=15, autosize=True)
# fig.update_layout(title_text=option, font_size=15, autosize=False, width=1500, height=1000,align='left')


#%% Funciones para dataframes --------------------------------------
def select_col(x):
    c1 = 'background-color: #fed487'
    c2 = '' 
    mask = x['%'] < 4
    df1 =  pd.DataFrame(c2, index=x.index, columns=x.columns)
    df1.loc[mask, 'Source'] = c1
    return df1

def select_col1(x):
    c1 = 'background-color: #fed487'
    c2 = ''
    c3 = 'background-color: #bfa5f4' 
    x2 = x[x['Source']=='Change Flow']
    mask = x2['%'] < 4 
    df1 =  pd.DataFrame(c2, index=x2.index, columns=x2.columns)
    df1.loc[mask, 'Source'] = c1
    x3 = x[x['Source']=='Interacting With Payment Page']
    mask3 = x3['%'] < 4 
    df2 =  pd.DataFrame(c2, index=x3.index, columns=x3.columns)
    df2.loc[mask3, 'Source'] = c3
    df = pd.concat([df1,df2])
    return df

def pct_change(piv_df):
    columns = piv_df.columns
    num_columns = len(columns)
    for i in range(num_columns - 1): 
        col1 = columns[i]
        col2 = columns[i + 1]
        new_col_name = f'{col2} '
        piv_df[columns[0]+ ' '] = float('nan') #cambio_porcentual = pivot_df.pct_change(axis='columns')
        piv_df[new_col_name] =( piv_df[col2] / piv_df[col1] - 1)
        mask_inf_nan = (piv_df[new_col_name] == float('inf')) | piv_df[new_col_name].isna()
        piv_df.loc[mask_inf_nan, new_col_name] =  float('nan') 
    return piv_df, columns, num_columns

def abs_change(piv_df):
    columns = piv_df.columns
    num_columns = len(columns)
    for i in range(num_columns - 1): 
        col1 = columns[i]
        col2 = columns[i + 1]
        new_col_name = f'{col2} '
        piv_df[columns[0]+ ' '] = float('nan') 
        piv_df[new_col_name] =( piv_df[col2] - piv_df[col1])
        mask_inf_nan = (piv_df[new_col_name] == float('inf')) | piv_df[new_col_name].isna()
        piv_df.loc[mask_inf_nan, new_col_name] =  float('nan') 
    return piv_df, columns, num_columns    

def color_nan_background(val):
    if np.isnan(val):
        return 'background-color: black'
    
def format_nan(val):
    if np.isnan(val):
        return 'NA'
    else: 
        return '{:.2%}'.format(val) 

def format_nan_abs(val):
    if np.isnan(val):
        return 'NA'
    else: 
        return '{:,.0f}'.format(val) 
    
def styled_dataframe(DF, group_by, Index, diferencia):
    for i, month_df in enumerate(DF):
        # Para dfs_prev             group_by = 'Source', Index = 'Acciones previas'
        # Para dfs_post, dfs_pos1,  group_by = 'Target', Index = 'Cambio de flujo'
        month_df['Month'] = hist_sh[i]
    result_df = pd.concat(DF, ignore_index=True)
    aggregated_df = result_df.groupby([group_by, 'Month'])['Clicks'].sum().reset_index()
    aggregated_df.rename(columns= {group_by : Index,'Month': ' '}, inplace = True)
    pivot_df = aggregated_df.pivot(index= Index, columns=' ', values='Clicks').fillna(0)
    if diferencia == 'pct':
        pivot_df, columns, num_columns = pct_change(pivot_df)
        pivot_df.sort_values(by = list(pivot_df.columns[num_columns:]), inplace=True, ascending= False)
        cm = sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x))) 
    else: 
        pivot_df, columns, num_columns = abs_change(pivot_df)
        pivot_df.sort_values(by = list(pivot_df.columns[num_columns:]), inplace=True, ascending= False)
        cm =sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan_abs,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
    return styled_pivot_df 
#%% ------------------------------------------------
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(['Funnel Subscriptions',"Acciones previas", "Cambio de flujo", "Acciones posteriores ", "Comparación histórica: acciones", "Comparación histórica: campañas"])

with tab0:
    st.header("Funnel Subscriptions")
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    st.header("Acciones previas")
    st.write(f'Nota: Los porcentajes menores al 4% se añadieron a "Otras acciones" (resaldados en naranja)')
    prev= prev.reindex(['Source', 'Target', 'Clicks','%'], axis=1)
    # st.table(prev.style.map(highlight_low_values,subset=['%']).format( precision=1))
    st.table(prev.style.apply(select_col, axis=None).format( precision=2))

with tab2:
    post= post.reindex(['Source', 'Target', 'Clicks','%'], axis=1)
    st.header("Cambio de flujo")
    st.table(post.style.apply(select_col1, axis=None).format( precision=2))

with tab3:
    post1= post1.reindex(['Source', 'Target', 'Clicks','%'], axis=1)
    styled_df = post1.style.apply(select_col1, axis=None)
    st.header("Acciones posteriores")
    st.write(f'Nota: Los porcentajes menores al 4% se añadieron a "Otras acciones en flujo" (resaltados en naranja) y a "Otras acciones en payment" (resaldados en morado)')
    st.table(styled_df.format( precision=2))

#%%%------------------------------------------------------------------------------------------------------------------------------------------------------------
## Comparación histórica 
hist_sh = []
for file in file_list:
    if file['title'].isdigit():
        hist_sh.append(file['title']) 
hist_sh = sorted(hist_sh)
#%%% 
dfs_prev,dfs_post,dfs_post1,dfs_click  = [],[],[],[]
for i,j in enumerate(hist_sh[:-1]):
    sh = client.open(j)
    worksheet_list = sh.worksheets()
    prev = load_the_spreadsheet('prev')
    prev['Target'] = 'Click on Button for purchase membership' 
    carousel = prev[prev.apply(lambda row: row.astype(str).str.contains('Clicked carousel image').any(), axis=1)]
    prev2 = prev.drop(index=carousel.index)
    new_row = pd.DataFrame.from_dict({'Clicks':[carousel['Clicks'].sum()], 'Source':['Clicked carousel image'],'Target':['Click on Button for purchase membership']})
    prev2 = pd.concat([prev2,new_row], ignore_index=True)
    prev.insert(1,'%',[round(x*100/prev['Clicks'].sum(),2) for x in list(prev['Clicks']) ])
    prev2.insert(1,'%',[round(x*100/prev2['Clicks'].sum(),2) for x in list(prev2['Clicks']) ])
    otros_prev2 = prev2[prev2['%']<4]
    new_prev2 = prev2.drop(index= otros_prev2.index)
    new_row_prev2 = pd.DataFrame.from_dict({'Clicks':[otros_prev2['Clicks'].sum()], 'Source':['Otras acciones'],'Target':['Click on Button for purchase membership']})
    new_prev2 = pd.concat([new_prev2,new_row_prev2], ignore_index=True)

    post1 = load_the_spreadsheet('post1')
    post = pd.DataFrame(post1.groupby('Source')['Clicks'].sum()).reset_index()
    post.rename(columns= {'Source':'Target'}, inplace = True)
    post['Source'] = 'Click on Button for purchase membership' 
    click = post.groupby('Source')['Clicks'].sum().reset_index()
    post1 = post1[post1.Source != 'No more actions']
    post.insert(1,'%',[round(x*100/post['Clicks'].sum(),2) for x in list(post['Clicks']) ])
    post1.insert(1,'%',[round(x*100/post1['Clicks'].sum(),2) for x in list(post1['Clicks']) ])
    otros_post1 =  post1[post1['%']<4] 
    otros_int = otros_post1[otros_post1.Source == 'Interacting With Payment Page']
    otros_change = otros_post1[otros_post1.Source == 'Change Flow']
    new_post1 =  post1.drop(index= otros_post1.index)
    new_row_post1_1 = pd.DataFrame.from_dict({'Clicks':[otros_int['Clicks'].sum()], 'Source':['Interacting With Payment Page'],'Target':['Otras acciones en payment']})
    new_row_post1_2 = pd.DataFrame.from_dict({'Clicks':[otros_change['Clicks'].sum()], 'Source':['Change Flow'],'Target':['Otras acciones en flujo']})
    new_post1 = pd.concat([new_post1,new_row_post1_1,new_row_post1_2], ignore_index=True)
    dfs_prev.append(new_prev2)
    dfs_post.append(post)
    dfs_post1.append(new_post1)
    dfs_click.append(click)



#%%%-------------------------------------------------------------------------------------------------------------
with tab4:
    st.header("Comparación histórica: Acciones")
    st.button("Mostrar diferencia absoluta", type="primary", key = 'acciones')
    if st.button('Mostrar diferencia porcentual', key ='acciones1'):
        st.write('Diferencia porcentual ')

        styled_pivot_df = styled_dataframe(dfs_prev,group_by = 'Source', Index = 'Acciones previas', diferencia = 'pct')
        styled_pivot_df2 = styled_dataframe(dfs_post,group_by = 'Target', Index = 'Cambio de flujo', diferencia = 'pct')
        styled_pivot_df3 = styled_dataframe(dfs_post1,group_by = 'Target', Index = 'Cambio de flujo', diferencia = 'pct')
        #se queda igual 
        for i, month_df in enumerate(dfs_click):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_click, ignore_index=True)
        aggregated_df = result_df.groupby(['Month','Source'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Month': ' ', 'Source': 'Action'}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Action', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = pct_change(pivot_df)
        pivot_df.sort_values(by = list(pivot_df.columns[num_columns:]), inplace=True, ascending= False)
        cm =sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df0 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
    else:
        st.write('Diferencia absoluta')

        styled_pivot_df = styled_dataframe(dfs_prev,group_by = 'Source', Index = 'Acciones previas', diferencia = 'abs')
        styled_pivot_df2 = styled_dataframe(dfs_post,group_by = 'Target', Index = 'Cambio de flujo', diferencia = 'abs')
        styled_pivot_df3 = styled_dataframe(dfs_post1,group_by = 'Target', Index = 'Cambio de flujo', diferencia = 'abs')
        # se queda igual 
        for i, month_df in enumerate(dfs_click):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_click, ignore_index=True)
        aggregated_df = result_df.groupby(['Month','Source'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Month': ' ', 'Source': 'Action'}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Action', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = abs_change(pivot_df)
        pivot_df.sort_values(by = list(pivot_df.columns[num_columns:]), inplace=True, ascending= False)
        clicks_pivot = pivot_df 
        cm =sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df0 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan_abs,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))

    st.markdown("<h3>Click on Button for purchase membership</h3>", unsafe_allow_html=True)
    st.table(styled_pivot_df0)
    st.markdown("<h3>Acciones previas</h3>", unsafe_allow_html=True)
    st.table(styled_pivot_df)
    st.markdown("<h3>Cambio de flujo</h3>", unsafe_allow_html=True)
    st.table(styled_pivot_df2)
    st.markdown("<h3>Acciones posteriores</h3>", unsafe_allow_html=True)
    st.table(styled_pivot_df3)

#%%% Campañas 
sh = client.open('campaign_names_transform')
worksheet_list = sh.worksheets()
df = load_the_spreadsheet('transformed')
pivot_df = df.pivot(index='extracted_substring', columns='ym', values='Cuentas').fillna(0)
pivot_df.columns = pivot_df.columns.astype(str)
data = []
for i in pivot_df.columns:
    column_sum = pivot_df[i].sum()
    data.append({'Year_Month': i, 'Clicks por campaña': column_sum})

def make_bar_style(x):
    return f"background: linear-gradient(90deg,#5fba7d {x}%, transparent {x}%); width: 10em"    

#%%%%
cm =sns.diverging_palette(220, 20, as_cmap=True).reversed()
with tab5:
    st.button("Mostrar diferencia absoluta", type="primary", key = 'campaigns')
    if st.button('Mostrar diferencia porcentual', key = 'campaigns1'):
        st.write('Diferencia porcentual ')    
        pivot_df, columns, num_columns = pct_change(pivot_df)
        styled_pivot_df4 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
        df_tot= pd.DataFrame(data)
        df_tot = df_tot.transpose()
        head = df_tot.iloc[0]
        df_tot = df_tot[1:]
        df_tot.columns = head
        df_tot.columns = df_tot.columns.astype(int)
        df_tot.columns = df_tot.columns.astype(str)
        df_tot, columns, num_columns = pct_change(df_tot)

        fila1 = df_tot.iloc[0]
        fila2 = clicks_pivot.iloc[0]
        resultado_division = fila1 / fila2
        resultado_division = pd.DataFrame(resultado_division).T
        resultado_division.index = ['Porcentaje de campañas en Clicks totales']
        comp = pd.concat([df_tot, resultado_division])
        for column in comp.columns[num_columns:]:
            comp.at['Porcentaje de campañas en Clicks totales', column] = np.nan # Setting the cell to None (NaN) or any other desired value
        styled_pivot = (comp.style
                        .background_gradient(cmap=cm,subset=comp.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset = (comp.index[0], columns))
                        .format(format_nan,subset=(comp.index[0],comp.columns[num_columns:]))
                        .bar( subset=(comp.index[1], columns) , color='#d65f5f',  vmin=0, vmax=1)
                        .format(format_nan,subset=(comp.index[1], columns))
                        .applymap(lambda x: color_nan_background(x))
                        )
        row_to_plot1 = comp.iloc[0]

    else:
        st.write('Diferencia absoluta')
        pivot_df, columns, num_columns = abs_change(pivot_df)
        pivot_df.sort_values(by = list(pivot_df.columns[num_columns:]), inplace=True, ascending= False)
        styled_pivot_df4 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan_abs,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
        df_tot= pd.DataFrame(data)
        df_tot = df_tot.transpose()
        head = df_tot.iloc[0]
        df_tot = df_tot[1:]
        df_tot.columns = head
        df_tot.columns = df_tot.columns.astype(int)
        df_tot.columns = df_tot.columns.astype(str)
        df_tot, columns, num_columns = abs_change(df_tot)
        fila1 = df_tot.iloc[0]
        fila2 = clicks_pivot.iloc[0]
        resultado_division = fila1 / fila2
        resultado_division = pd.DataFrame(resultado_division).T
        resultado_division.index = ['Porcentaje de campañas en Clicks totales']
        comp = pd.concat([df_tot, resultado_division])

        for column in comp.columns[num_columns:]:
            comp.at['Porcentaje de campañas en Clicks totales', column] = np.nan  # Setting the cell to None (NaN) or any other desired value

        styled_pivot = (comp.style
                        .background_gradient(cmap=cm,subset=comp.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset = (comp.index[0], columns))
                        .format(format_nan_abs,subset=(comp.index[0],comp.columns[num_columns:]))
                        .bar( subset=(comp.index[1], columns) , color='#d65f5f',  vmin=0, vmax=1)
                        .format(format_nan,subset=(comp.index[1], comp.columns))
                        .applymap(lambda x: color_nan_background(x))
                        )
        row_to_plot1 = comp.iloc[0]

    st.header("Comparación histórica: Campañas")
    st.markdown("<h3>Clicks por campañas</h3>", unsafe_allow_html=True)   
    st.table(styled_pivot)
    combined_values = pd.concat([row_to_plot1[num_columns:], clicks_pivot[num_columns:]], axis=1)
    st.bar_chart(combined_values)


    st.markdown("<h3>Campañas</h3>", unsafe_allow_html=True)   
    st.table(styled_pivot_df4)


# %%
