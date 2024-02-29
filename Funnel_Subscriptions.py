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


# Authenticate using the service account credentials
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

st.set_page_config(
    page_title="Subscriptions",
    page_icon="🟢",
    layout="wide"
)

st.title('VIP Funnel')

st.sidebar.header("Subscriptions")

start_date = datetime.now()

with st.expander('Mes'):
    this_year = start_date.year
    this_month = start_date.month
    report_year = st.selectbox('', range(this_year, this_year - 5, -1))
    month_abbr = calendar.month_abbr[1:]
    report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
    report_month = month_abbr.index(report_month_str) + 1
st.write(f'{report_year} {report_month_str}')
if report_month <= 9:
    # st.text (f'{report_year}'+'0'+f'{report_month}')
    spreadsheet_name  = f'{report_year}'+'0'+f'{report_month}'

else: 
    # st.text (f'{report_year}{report_month}')
    spreadsheet_name  = f'{report_year}{report_month}'

option = f'{report_year} {report_month_str}'

from google.oauth2 import service_account
#abrimos el spreadsheet 

credentials = service_account.Credentials.from_service_account_info(service_info, scopes = scope)
client = Client(scope=scope,creds=credentials)
spread = Spread(spreadsheet_name,client = client)

# st.write(spread.url)
sh = client.open(spreadsheet_name)
worksheet_list = sh.worksheets()

folder_id = '1juC34pcnAZu5QeTDB-k5xbyOnNlamxJ3'
file_name = spreadsheet_name
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

prev = load_the_spreadsheet('prev')
post1 = load_the_spreadsheet('post1')
prev.rename(columns= {'num_actions':'Clicks','prev_action':'Source'}, inplace = True)
post1.rename(columns= {'SUM(conteo)':'Clicks','category':'Source','subcategory':'Target'}, inplace = True)
post = pd.DataFrame(post1.groupby('Source')['Clicks'].sum()).reset_index()
post.rename(columns= {'Source':'Target'}, inplace = True)
post['Source'] = 'Click on Button for purchase membership' 
post1 = post1[post1.Source != 'No more actions']

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

def select_col(x):
    c1 = 'background-color: #fed487'
    c2 = '' 
    #compare columns
    mask = x['%'] < 4
    #DataFrame with same index and columns names as original filled empty strings
    df1 =  pd.DataFrame(c2, index=x.index, columns=x.columns)
    #modify values of df1 column by boolean mask
    df1.loc[mask, 'Source'] = c1
    return df1

def select_col1(x):
    c1 = 'background-color: #fed487'
    c2 = ''
    c3 = 'background-color: #bfa5f4' 
    #compare columns
    x2 = x[x['Source']=='Change Flow']
    mask = x2['%'] < 4 
    #DataFrame with same index and columns names as original filled empty strings
    df1 =  pd.DataFrame(c2, index=x2.index, columns=x2.columns)
    #modify values of df1 column by boolean mask
    df1.loc[mask, 'Source'] = c1
    #compare columns
    x3 = x[x['Source']=='Interacting With Payment Page']
    mask3 = x3['%'] < 4 
    #DataFrame with same index and columns names as original filled empty strings
    df2 =  pd.DataFrame(c2, index=x3.index, columns=x3.columns)
    df2.loc[mask3, 'Source'] = c3
    #modify values of df1 column by boolean mask
    df = pd.concat([df1,df2])
    # df1.merge(df2)
    return df

subset_index = otros_change.index.tolist()
post1= post1.reindex(['Source', 'Target', 'Clicks','%'], axis=1)
styled_df = post1.style.apply(select_col1, axis=None)


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
    st.header("Acciones posteriores")
    st.write(f'Nota: Los porcentajes menores al 4% se añadieron a "Otras acciones en flujo" (resaltados en naranja) y a "Otras acciones en payment" (resaldados en morado)')
    st.table(styled_df.format( precision=2))

#%%%------------------------------------------------------------------------------------------------------------------------------------------------------------
## Comparación histórica 
    
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

hist_sh = []
for file in file_list:
    if file['title'].isdigit():
        hist_sh.append(file['title']) 

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


#%%% 
dfs_prev = []
dfs_post = []
dfs_post1 = []
dfs_click = []
for i,j in enumerate(hist_sh):
    sh = client.open(j)
    worksheet_list = sh.worksheets()
    prev = load_the_spreadsheet('prev')
    prev.rename(columns= {'num_actions':'Clicks','prev_action':'Source'}, inplace = True)
    prev['Target'] = 'Click on Button for purchase membership' 
    prev.rename(columns= {'num_actions':'Clicks','prev_action':'Source'}, inplace = True)
    carousel = prev[prev.apply(lambda row: row.astype(str).str.contains('Clicked carousel image').any(), axis=1)]
    prev2 = prev.drop(index=carousel.index)
    new_row = pd.DataFrame.from_dict({'Clicks':[carousel.Clicks.sum()], 'Source':['Clicked carousel image'],'Target':['Click on Button for purchase membership']})
    prev2 = pd.concat([prev2,new_row], ignore_index=True)
    prev.insert(1,'%',[round(x*100/prev.Clicks.sum(),2) for x in list(prev.Clicks) ])
    prev2.insert(1,'%',[round(x*100/prev2.Clicks.sum(),2) for x in list(prev2.Clicks) ])
    otros_prev2 = prev2[prev2['%']<4]
    new_prev2 = prev2.drop(index= otros_prev2.index)
    new_row_prev2 = pd.DataFrame.from_dict({'Clicks':[otros_prev2.Clicks.sum()], 'Source':['Otras acciones'],'Target':['Click on Button for purchase membership']})
    new_prev2 = pd.concat([new_prev2,new_row_prev2], ignore_index=True)
    post1 = load_the_spreadsheet('post1')
    post1.rename(columns= {'SUM(conteo)':'Clicks','category':'Source','subcategory':'Target'}, inplace = True)
    post = pd.DataFrame(post1.groupby('Source')['Clicks'].sum()).reset_index()
    post.rename(columns= {'Source':'Target'}, inplace = True)
    post['Source'] = 'Click on Button for purchase membership' 
    click = post.groupby('Source')['Clicks'].sum().reset_index()
    post1 = post1[post1.Source != 'No more actions']
    post.insert(1,'%',[round(x*100/post.Clicks.sum(),2) for x in list(post.Clicks) ])
    post1.insert(1,'%',[round(x*100/post1.Clicks.sum(),2) for x in list(post1.Clicks) ])
    otros_post1 =  post1[post1['%']<4] 
    otros_int = otros_post1[otros_post1.Source == 'Interacting With Payment Page']
    otros_change = otros_post1[otros_post1.Source == 'Change Flow']
    new_post1 =  post1.drop(index= otros_post1.index)
    new_row_post1_1 = pd.DataFrame.from_dict({'Clicks':[otros_int.Clicks.sum()], 'Source':['Interacting With Payment Page'],'Target':['Otras acciones en payment']})
    new_row_post1_2 = pd.DataFrame.from_dict({'Clicks':[otros_change.Clicks.sum()], 'Source':['Change Flow'],'Target':['Otras acciones en flujo']})
    new_post1 = pd.concat([new_post1,new_row_post1_1,new_row_post1_2], ignore_index=True)
    dfs_prev.append(new_prev2)
    dfs_post.append(post)
    dfs_post1.append(new_post1)
    dfs_click.append(click)


#%%--------------------------------------------

#%%%-------------------------------------------------------------------------------------------------------------
with tab4:
    st.header("Comparación histórica: Acciones")
    st.button("Mostrar diferencia absoluta", type="primary")
    if st.button('Mostrar diferencia porcentual'):
        st.write('Diferencia porcentual ')
        for i, month_df in enumerate(dfs_prev):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_prev, ignore_index=True)
        aggregated_df = result_df.groupby(['Source', 'Month'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Source':'Acciones previas','Month': ' '}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Acciones previas', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = pct_change(pivot_df)
        num_colors = len(list((pivot_df[pivot_df.columns[num_columns:]]).stack().unique()))
        cm = sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))

        for i, month_df in enumerate(dfs_post):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_post, ignore_index=True)
        aggregated_df = result_df.groupby(['Target', 'Month'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Target':'Cambio de flujo','Month': ' '}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Cambio de flujo', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = pct_change(pivot_df)
        styled_pivot_df2 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))


        for i, month_df in enumerate(dfs_post1):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_post1, ignore_index=True)
        aggregated_df = result_df.groupby(['Target', 'Month'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Target':'Cambio de flujo','Month': ' '}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Cambio de flujo', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = pct_change(pivot_df)
        styled_pivot_df3 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))

        for i, month_df in enumerate(dfs_click):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_click, ignore_index=True)
        aggregated_df = result_df.groupby(['Month','Source'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Month': ' ', 'Source': 'Action'}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Action', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = pct_change(pivot_df)
        num_colors = len(list((pivot_df[pivot_df.columns[num_columns:]]).stack().unique()))
        cm =sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df0 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
    else:
        st.write('Diferencia absoluta')

        for i, month_df in enumerate(dfs_prev):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_prev, ignore_index=True)
        aggregated_df = result_df.groupby(['Source', 'Month'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Source':'Acciones previas','Month': ' '}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Acciones previas', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = abs_change(pivot_df)
        num_colors = abs(round(pivot_df[pivot_df.columns[num_columns:]].min().min())) + abs(round(pivot_df[pivot_df.columns[num_columns:]].max().max())) + 1 
        cm =sns.diverging_palette(220, 20, as_cmap=True).reversed()
        styled_pivot_df = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan_abs,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
        
        for i, month_df in enumerate(dfs_post):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_post, ignore_index=True)
        aggregated_df = result_df.groupby(['Target', 'Month'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Target':'Cambio de flujo','Month': ' '}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Cambio de flujo', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = abs_change(pivot_df)
        styled_pivot_df2 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan_abs,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))

        for i, month_df in enumerate(dfs_post1):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_post1, ignore_index=True)
        aggregated_df = result_df.groupby(['Target', 'Month'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Target':'Cambio de flujo','Month': ' '}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Cambio de flujo', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = abs_change(pivot_df)
        styled_pivot_df3 = (pivot_df.style
                        .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                        .format( '{:,.0f}', subset=columns)
                        .format(format_nan_abs,subset=pivot_df.columns[num_columns:])
                        .applymap(lambda x: color_nan_background(x)))
        
        for i, month_df in enumerate(dfs_click):
            month_df['Month'] = hist_sh[i]
        result_df = pd.concat(dfs_click, ignore_index=True)
        aggregated_df = result_df.groupby(['Month','Source'])['Clicks'].sum().reset_index()
        aggregated_df.rename(columns= {'Month': ' ', 'Source': 'Action'}, inplace = True)
        pivot_df = aggregated_df.pivot(index='Action', columns=' ', values='Clicks').fillna(0)
        pivot_df, columns, num_columns = abs_change(pivot_df)
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
pivot_df, columns, num_columns = pct_change(pivot_df)
styled_pivot_df4 = (pivot_df.style
                   .background_gradient(cmap=cm,subset=pivot_df.columns[num_columns:], axis=None)
                   .format( '{:,.0f}', subset=columns)
                   .format(format_nan,subset=pivot_df.columns[num_columns:])
                   .applymap(lambda x: color_nan_background(x)))

#%%%%
with tab5:
    st.header("Comparación histórica: Campañas")
    st.markdown("<h3>Campañas</h3>", unsafe_allow_html=True)
    st.table(styled_pivot_df4)
