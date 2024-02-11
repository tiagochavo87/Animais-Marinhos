import streamlit as st
import pandas as pd
import plotly.express as px

# Adicionar ícones à aba do navegador
st.set_page_config(
    page_title=" Animais Marinhos",
    page_icon="🌊"
)

# Carregando os dados do arquivo CSV
df = pd.read_csv("animaissc.csv", sep=';', encoding='ISO-8859-1')

# Renomeando as colunas para melhor legibilidade
df = df.rename(columns={
    'Individual Identifier': 'Identificador Individual',
    'Occurrence Identifier': 'Identificador de Ocorrência',
    'Date/time (ISO 8601 / Local time)': 'Data/Hora (ISO 8601 / Hora Local)',
    'Animal condition': 'Condição do Animal',
    'Developmental stage': 'Estágio de Desenvolvimento',
    'Latitude': 'LAT',
    'Longitude': 'LON',
    'State': 'Estado',
    'County': 'Município',
    'Beach': 'Praia',
    'Class': 'Classe',
    'Order': 'Ordem',
    'Suborder': 'Subordem',
    'Family': 'Família',
    'Genus': 'Gênero',
    'Species': 'Espécie'
})

# Substituir vírgulas por pontos nas colunas LAT e LON
df['LAT'] = df['LAT'].str.replace(',', '.')
df['LON'] = df['LON'].str.replace(',', '.')

# Certifique-se de que as colunas 'LAT' e 'LON' sejam do tipo numérico
df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LON'] = pd.to_numeric(df['LON'], errors='coerce')

# Convertendo a coluna de data/hora para o formato datetime
df['Data/Hora (ISO 8601 / Hora Local)'] = pd.to_datetime(df['Data/Hora (ISO 8601 / Hora Local)'])

# Adicionar opção "Todas as Espécies" no menu suspenso de filtragem
especies = ['Todas as Espécies'] + sorted(df['Espécie'].astype(str).unique())
species_filter = st.sidebar.selectbox("Filtrar por Espécie", especies)

# Filtragem por ano (opcional)
ano_filter = st.sidebar.slider("Filtrar por Ano", int(df['Data/Hora (ISO 8601 / Hora Local)'].dt.year.min()), int(df['Data/Hora (ISO 8601 / Hora Local)'].dt.year.max()), (2018, 2023))
filtered_df = df[df['Data/Hora (ISO 8601 / Hora Local)'].dt.year.between(ano_filter[0], ano_filter[1])]

# Exibir título principal acima dos gráficos
st.markdown("<h1 style='text-align: center; font-size: 2em;'>🐋 Mamíferos Marinhos, 🐢 Tartarugas Marinhas e 🐦 Aves Marinhas Encalhados no Paraná e Santa Catarina (2018-2023)</h1>", unsafe_allow_html=True)

# Sidebar com opções de visualização
menu = st.sidebar.selectbox("Selecione a opção de visualização:", 
                            ["Distribuição por Estado", "Distribuição por County", "Distribuição por Beach", "Distribuição por Class", "Condição dos Animais", "Mapa de Ocorrências"])

# Filtragem por espécie (opcional)
if species_filter != 'Todas as Espécies':
    filtered_df = filtered_df[filtered_df['Espécie'] == species_filter]

# Removendo valores nulos nas colunas de interesse
filtered_df = filtered_df.dropna(subset=['LAT', 'LON', 'Estado', 'Condição do Animal'])  # Adicione as colunas de interesse

# Visualizações
if menu == "Distribuição por Estado":
    st.subheader("Distribuição por Estado")
    state_distribution = filtered_df['Estado'].value_counts()
    state_colors = px.colors.qualitative.Set1[:len(state_distribution)]
    fig = px.bar(state_distribution, color=state_distribution.index, color_discrete_sequence=state_colors)
    st.plotly_chart(fig)

    st.subheader("Totais por Estado")
    total_por_estado = filtered_df.groupby('Estado')['Identificador de Ocorrência'].count()
    st.dataframe(total_por_estado.rename('Total de Ocorrências'))

elif menu == "Distribuição por County":
    st.subheader("Distribuição por Município")
    county_distribution = filtered_df['Município'].value_counts()
    st.bar_chart(county_distribution)

    st.subheader("Totais por Município")
    total_por_municipio = filtered_df.groupby('Município')['Identificador de Ocorrência'].count()
    st.dataframe(total_por_municipio.rename('Total de Ocorrências'))

elif menu == "Distribuição por Beach":
    st.subheader("Distribuição por Praia")
    beach_distribution = filtered_df['Praia'].value_counts()
    st.bar_chart(beach_distribution)

    st.subheader("Totais por Praia")
    total_por_praia = filtered_df.groupby('Praia')['Identificador de Ocorrência'].count()
    st.dataframe(total_por_praia.rename('Total de Ocorrências'))

elif menu == "Distribuição por Class":
    st.subheader("Distribuição por Classe")
    class_distribution = filtered_df['Classe'].value_counts()
    st.bar_chart(class_distribution)

    st.subheader("Totais por Classe")
    total_por_classe = filtered_df.groupby('Classe')['Identificador de Ocorrência'].count()
    st.dataframe(total_por_classe.rename('Total de Ocorrências'))

elif menu == "Condição dos Animais":
    st.subheader("Condição dos Animais")
    condition_pie = filtered_df['Condição do Animal'].value_counts()
    fig = px.pie(filtered_df, names='Condição do Animal', title='Condição dos Animais')
    st.plotly_chart(fig)

elif menu == "Mapa de Ocorrências":
    st.subheader("Mapa de Ocorrências")
    st.map(filtered_df[['LAT', 'LON']].dropna())

# Rodapé
st.sidebar.markdown("<p style='font-size: 0.8em; text-align: center;'>Baseado em: Barreto, André et al. (2023). Mamíferos marinhos, tartarugas marinhas e aves marinhas encalhados no Paraná e Santa Catarina de agosto de 2018 a agosto de 2023 [Conjunto de dados]. Dríade. https://doi.org/10.5061/dryad.2rbnzs7v9</p>", unsafe_allow_html=True)
