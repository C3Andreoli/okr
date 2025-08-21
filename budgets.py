import streamlit as st  
import pandas as pd
import random
import string
import gspread
import re
import projects

# === Funções utilitárias ===
def gerar_id(tamanho=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))

def normalizar_nome(nome: str) -> str:
    """Remove espaços, traços e deixa em minúsculo para comparação."""
    return re.sub(r'\s+|-|_', '', nome.strip().lower())

@st.cache_data(ttl = 300)
def getBudgets():
    client = gspread.authorize(st.cred) 
    sheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc").worksheet('budgets')
    print('EU RODEI')
    data = sheet.get_all_records()

    if not data:  # só cabeçalho, sem registros
        return None
    
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()
    return df


# === Google Sheets ===



# === Interface principal ===
def show():
    st.projetos = projects.getProjects()
    st.budgets = getBudgets()
    print(st.projetos)
    if st.projetos is not None and not st.projetos.empty:
        st.title("Adicionar Budget")
        projeto = st.selectbox("Selecione o Projeto", [p for p in st.projetos['projeto'].values])
        tipo = st.text_input("Tipo de budget")
        valor = st.number_input("Valor do Budget", min_value=0.0, step=100.0)
        if st.button("Salvar Budget"):
            client = gspread.authorize(st.cred)
            sheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc").worksheet('budgets')
            sheet.append_row([projeto,st.projetos.loc[st.projetos["projeto"] == projeto, "id"].iloc[0], tipo, valor, gerar_id()])
            st.success("Budget adicionado com sucesso!")
            st.cache_data.clear()
            st.cache_resource.clear()
            st.budgets = getBudgets()
        if st.budgets is not None and not st.budgets.empty:
            st.subheader("Budgets Registrados")
            st.table(pd.DataFrame(st.budgets))
    else:
        st.warning("Crie um projeto um projeto primeiro!")