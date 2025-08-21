import streamlit as st  
import pandas as pd
import random
import string
import gspread
import re


# === Funções utilitárias ===
def gerar_id(tamanho=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))

def normalizar_nome(nome: str) -> str:
    """Remove espaços, traços e deixa em minúsculo para comparação."""
    return re.sub(r'\s+|-|_', '', nome.strip().lower())


# === Google 9Sheets ===
@st.cache_data(ttl = 300)
def getProjects():
    client = gspread.authorize(st.cred) 
    sheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc").worksheet('projetos')
    print('EU RODEI')
    data = sheet.get_all_records()

    if not data:  # só cabeçalho, sem registros
        return None
    
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()
    return df


# === Interface principal ===
def show():
    st.title("Cadastrar um novo projeto")
    
    # carrega projetos e guarda no estado
    st.projetos = getProjects()

    nome = st.text_input("Nome do Projeto")
    tipo = st.selectbox("Tipo", ['LED', 'SOLAR'])
    budget = st.number_input("Budget Geral",min_value=0,step=10000)
    if st.button("Salvar Projeto"):
        client = gspread.authorize(st.cred)
        sheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc").worksheet('projetos')

        # 🔹 Verifica duplicados usando st.projetos
        
        if st.projetos is not None and nome in st.projetos['projeto'].values:
            st.warning("Esse projeto já foi cadastrado!!")
        else:
        # 🔹 Se não duplicado → adiciona
            sheet.append_row([nome, tipo, gerar_id(), budget])
            st.success(f"Projeto **{nome}** criado!")
            st.cache_data.clear()
            st.cache_resource.clear()
        # 🔹 Atualiza st.projetos depois de salvar
        st.projetos = getProjects()
    # 🔹 Só mostra tabela se tiver registros
    if st.projetos is not None and not st.projetos.empty:
        st.subheader("Projetos Cadastrados")
        st.dataframe(st.projetos)
