import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Airbnb NYC", layout="wide")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("AB_NYC_2019.csv")
    return df
df = carregar_dados()
def aplicar_filtros(df):
    st.sidebar.title("Filtros")
    bairros = st.sidebar.multiselect("Selecione o Bairro", options=df["neighbourhood_group"].unique())
    tipos = st.sidebar.multiselect("Tipo de Acomodação", options=df["room_type"].unique())
    faixa_preco = st.sidebar.slider("Faixa de Preço ($)", float(df["price"].min()), float(df["price"].max()), (50.0, 500.0))
    df_filtrado = df.copy()
    if bairros:
        df_filtrado = df_filtrado[df_filtrado["neighbourhood_group"].isin(bairros)]
    if tipos:
        df_filtrado = df_filtrado[df_filtrado["room_type"].isin(tipos)]
    df_filtrado = df_filtrado[(df_filtrado["price"] >= faixa_preco[0]) & (df_filtrado["price"] <= faixa_preco[1])]
    return df_filtrado
df_filtrado = aplicar_filtros(df)

with st.expander("Sobre o Dashboard - Airbnb NYC"):
    st.markdown("""
    ### Trabalho realizado por Luís Eduardo e Kairo Ruan
                
    ### Objetivo do Dashboard  
    Este dashboard foi desenvolvido para explorar visualmente os dados de hospedagens do Airbnb em Nova York (ano de 2019).  
    Através de gráficos interativos, mapas e análises estatísticas, o objetivo é facilitar a identificação de padrões, tendências e insights sobre o mercado de aluguel de curto prazo na cidade.

    ### Como Navegar  
    Utilize o menu lateral (à esquerda) para acessar as seguintes seções:  
    - **Visão Geral**: Visualização básica dos dados e contagem de anúncios.  
    - **Gráficos Interativos**: Mapa e análises dinâmicas utilizando Plotly.  
    - **Análises Avançadas**: Gráficos detalhados como histogramas e comparativos por bairro.

    ### Como os Filtros Influenciam os Dados  
    Os filtros na barra lateral permitem refinar as análises em tempo real:  
    - **Bairro**: Filtra anúncios por região da cidade.  
    - **Tipo de Acomodação**: Exibe apenas o(s) tipo(s) de hospedagem selecionados.  
    - **Faixa de Preço**: Limita a análise a uma faixa de preço específica.

    Os gráficos e métricas se atualizam automaticamente conforme os filtros são modificados.
    """)

def pagina_visao_geral(df_filtrado):
    st.title("Dashboard Airbnb NYC - Visão Geral")
    st.write(df_filtrado.head())
    st.metric("Total de Anúncios", len(df_filtrado))

    st.subheader("Distribuição por Bairro")
    fig1, ax1 = plt.subplots()
    df_filtrado["neighbourhood_group"].value_counts().plot(kind="bar", ax=ax1)
    st.pyplot(fig1)

    st.subheader("Distribuição dos Tipos de Acomodação")
    fig2, ax2 = plt.subplots()
    df_filtrado["room_type"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2)
    st.pyplot(fig2)

def pagina_graficos_interativos(df_filtrado):
    st.title("Gráficos Interativos com Plotly")

    st.subheader("Mapa das Localizações dos Anúncios")
    fig3 = px.scatter_mapbox(df_filtrado, lat="latitude", lon="longitude",
                             color="neighbourhood_group", zoom=10,
                             hover_data=["name", "price"])
    fig3.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig3)

    st.subheader("Preço x Número de Avaliações")
    fig4 = px.scatter(df_filtrado, x="number_of_reviews", y="price",
                      color="room_type", size="availability_365",
                      hover_data=["name"])
    st.plotly_chart(fig4)

def pagina_analises_avancadas(df_filtrado):
    st.title("Análises Avançadas")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Histograma de Preços")
        fig5, ax5 = plt.subplots()
        df_filtrado["price"].hist(ax=ax5, bins=30)
        st.pyplot(fig5)

    with col2:
        st.subheader("Preço Médio por Bairro")
        preco_medio = df_filtrado.groupby("neighbourhood_group")["price"].mean().sort_values()
        fig6, ax6 = plt.subplots()
        preco_medio.plot(kind="barh", ax=ax6)
        st.pyplot(fig6)

pagina = st.sidebar.radio("Navegação", ["Visão Geral", "Gráficos Interativos", "Análises Avançadas"])

if pagina == "Visão Geral":
    pagina_visao_geral(df_filtrado)
elif pagina == "Gráficos Interativos":
    pagina_graficos_interativos(df_filtrado)
elif pagina == "Análises Avançadas":
    pagina_analises_avancadas(df_filtrado)
