import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Acidentes Recife", #Aqui eu configuro o setpage ou seja, informo as infos da página quando eu criar
    page_icon=":warning:",
    layout="wide")

st.title("Acidentes Recife")
st.title("Página descritiva, destinada a documentação, introdução, referenciais e links.")

# Link de acesso ao artigo correlato
link = '[Artigo](https://docs.google.com/document/d/16mC5oM3nUT6DJhnNMtkyC2ZlLozQH8P38HERggJOL_E/edit)'
st.markdown(link, unsafe_allow_html=True)

# Repositório
link = '[GitHub](https://github.com/Budcaze/Projetos-3)'
st.markdown(link, unsafe_allow_html=True)