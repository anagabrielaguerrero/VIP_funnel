import streamlit as st


conn = st.connection('mysql', type='sql')


old_new = conn.query('select * from users limit 1 ')
