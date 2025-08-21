import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import projects, budgets, alt, relatorio



@st.cache_data(ttl=300)
def getCredentials():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    # client = gspread.authorize(creds)
    # # aqui você abre a planilha
    # spreadsheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc")
    # sheet = spreadsheet.worksheet("Exportar")
    # data = sheet.get_all_records()
    return creds

st.cred = getCredentials()

# Simulando um banco de dados em memória (pode depois salvar em CSV/Google Sheets/SQL)
if "projetos" not in st.session_state:
    st.session_state.projetos = []
if "budgets" not in st.session_state:
    st.session_state.budgets = []
if "gastos" not in st.session_state:
    st.session_state.gastos = []
if "page" not in st.session_state:
    st.session_state.page = 'relatorio'

st.sidebar.title("Menu")

with st.sidebar.expander("📁 Projetos"):
    if st.button("➕ Adicionar Projeto"):
        st.session_state.page = "criar"
    if st.button("💰 Adicionar Budget"):
        st.session_state.page = "budget"
    if st.button("🧾 Registrar Alternativa"):
        st.session_state.page = "alt"

with st.sidebar.expander("📊 Relatórios"):
    if st.button("📈 DASHBOARD"):
        st.session_state.page = "relatorio"



if st.session_state.page == "criar":
    projects.show()
elif st.session_state.page  == 'relatorio':
    relatorio.show()
elif st.session_state.page  == 'budget':
    budgets.show()
elif st.session_state.page  == 'alt':
    alt.show()