import streamlit as st  
import pandas as pd
import random
import string
import gspread
import re
import projects
import budgets
# === Funções utilitárias ===
def gerar_id(tamanho=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))

def normalizar_nome(nome: str) -> str:
    """Remove espaços, traços e deixa em minúsculo para comparação."""
    return re.sub(r'\s+|-|_', '', nome.strip().lower())

@st.cache_data(ttl = 300)
def getAlts():
    client = gspread.authorize(st.cred) 
    sheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc").worksheet('alt')
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
    st.budgets = budgets.getBudgets()
    st.alternatives = getAlts()
    print(st.projetos)
    if st.projetos is not None and st.budgets is not None:
        st.title("Adicionar Budget")
        projeto = st.selectbox("Selecione o Projeto", [p for p in st.projetos['projeto'].values])
        alternativa = st.text_area("Alternativa")
        categoria = st.selectbox(
    "Selecione a Categoria do budget",
    st.budgets.loc[st.budgets["projeto"] == projeto, "tipo - budget"].unique()
)
        valor = st.number_input("Valor do Item", min_value=0.0, step=10000.0)
        gasto = st.number_input("Valor Gasto", min_value=0.0, step=10000.0)
        if st.button("Salvar Alternativa"):
            client = gspread.authorize(st.cred)
            sheet = client.open_by_key("1RbwC8JYPz8glm-qIuQswRP3ouG6uDJlyNcL7rTNdUIc").worksheet('alt')
            sheet.append_row([
                projeto,
                alternativa,
                gerar_id(), 
                categoria,
                valor, 
                gasto,
                (valor - gasto),
                (valor - gasto)/valor * 1,
                (valor - gasto)/st.projetos.loc[st.projetos["projeto"] == projeto, "budget"].iloc[0] * 1])
            st.success("Budget adicionado com sucesso!")
            st.cache_data.clear()
            st.cache_resource.clear()
            st.alternatives = getAlts()
        if st.alternatives is not None and not st.budgets.empty:
            st.subheader("Alternativas Registrados")
            st.table(pd.DataFrame(st.alternatives))
    elif st.projetos is not None:
        st.warning("É necessário cadastrar algum budget primeiro!")
    else:
        st.warning("É necessário cadastrar algum projeto primeiro!")