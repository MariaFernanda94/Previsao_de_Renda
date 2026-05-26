import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# 1. Configuração da página
st.set_page_config(
     page_title="Análise de Renda",
     page_icon="💰",
     layout="wide",
)

st.write('# 💰 Painel de Análise de Renda')
st.markdown("---")

# 2. Carregamento dos dados
try:
    renda = pd.read_csv('previsao_de_renda.csv')
except:
    try:
        renda = pd.read_csv('./input/previsao_de_renda.csv')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()

# Limpeza e Tipagem
renda['tempo_emprego'] = renda['tempo_emprego'].fillna(0)
renda['data_ref'] = pd.to_datetime(renda['data_ref'])

# --- BARRA LATERAL: FILTROS DINÂMICOS ---
st.sidebar.header("Filtros de Visualização")

# 1) Idade (Dinâmica até o mais velho)
max_idade = int(renda['idade'].max())
# Slider de intervalo: permite escolher "de 18 até X"
idade_range = st.sidebar.slider("Faixa Etária", 18, max_idade, (18, max_idade))

# 2) Tempo de emprego (Dinâmico até o máximo do CSV)
max_tempo = int(renda['tempo_emprego'].max())
tempo_selecionado = st.sidebar.slider("Tempo de Emprego", 0, max_tempo, max_tempo)

# 3) Sexo (Com opção "Ambos")
opcoes_sexo = ['Ambos', 'M', 'F']
sexo_selecionado = st.sidebar.selectbox("Gênero", opcoes_sexo)

# 4) Escolaridade (Apenas as existentes no CSV)
escolaridades_disponiveis = renda['educacao'].unique().tolist()
esc_selecionada = st.sidebar.multiselect("Nível de Escolaridade", escolaridades_disponiveis, default=escolaridades_disponiveis)

# --- APLICAÇÃO DOS FILTROS ---
df_filtrado = renda[
    (renda['idade'] >= idade_range[0]) & (renda['idade'] <= idade_range[1]) &
    (renda['tempo_emprego'] <= tempo_selecionado) &
    (renda['educacao'].isin(esc_selecionada))
]

if sexo_selecionado != 'Ambos':
    df_filtrado = df_filtrado[df_filtrado['sexo'] == sexo_selecionado]

# --- ÁREA DE GRÁFICOS ---
st.write("## 📈 Resultados da Análise")
st.info(f"Exibindo dados para: {sexo_selecionado} | Idade até {idade_range[1]} anos | Tempo de emprego até {tempo_selecionado} anos.")

# Gráfico 1: Evolução da Renda por Categoria Selecionada
st.subheader("Evolução da Renda ao Longo do Tempo")
fig1, ax1 = plt.subplots(figsize=(15, 6))
sns.lineplot(x='data_ref', y='renda', hue='posse_de_imovel', data=df_filtrado, ax=ax1)
ax1.tick_params(axis='x', rotation=45)
ax1.set_title("Renda Média Mensal por Posse de Imóvel", fontsize=14)
st.pyplot(fig1)

st.markdown("---")

# Gráfico 2: Renda por Escolaridade (Barras para facilitar o entendimento de qualquer pessoa)
st.subheader("Distribuição de Renda por Escolaridade")
fig2, ax2 = plt.subplots(figsize=(15, 7))
sns.barplot(x='educacao', y='renda', data=df_filtrado, ax=ax2, palette="viridis")
ax2.set_title("Média de Renda por Nível de Instrução", fontsize=14)
plt.xticks(rotation=15)
st.pyplot(fig2)

# Tabela Resumo Simples
st.write("### Resumo Numérico")
col1, col2, col3 = st.columns(3)
col1.metric("Quantidade de Pessoas", len(df_filtrado))
col2.metric("Média de Renda", f"R$ {df_filtrado['renda'].mean():.2f}")
col3.metric("Maior Renda no Grupo", f"R$ {df_filtrado['renda'].max():.2f}")