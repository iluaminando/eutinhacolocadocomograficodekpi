import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Lances x Acertos", layout="wide")

st.title("📊 Análise de Lances x Acertos")
st.markdown("### Gráfico de Área - Decode 25-26 Regional")

# Dados da tabela
dados = {
    'Rodada': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'Lances': [44, 25, 26, 31, 23, 29, 24, 32, 27, 33, 21],
    'Acertos': [30, 20, 21, 29, 17, 21, 19, 18, 23, 29, 17]
}

df = pd.DataFrame(dados)

# Criar gráfico de área
fig = go.Figure()

# Adicionar área de Lances
fig.add_trace(go.Scatter(
    x=df['Rodada'],
    y=df['Lances'],
    mode='lines',
    name='Lances',
    line=dict(color='#667eea', width=2),
    fill='tozeroy',
    fillcolor='rgba(102, 126, 234, 0.3)',
    hovertemplate='Rodada %{x}<br>Lances: %{y} bolas<extra></extra>'
))

# Adicionar área de Acertos
fig.add_trace(go.Scatter(
    x=df['Rodada'],
    y=df['Acertos'],
    mode='lines',
    name='Acertos',
    line=dict(color='#f5576c', width=2),
    fill='tozeroy',
    fillcolor='rgba(245, 87, 108, 0.3)',
    hovertemplate='Rodada %{x}<br>Acertos: %{y} bolas<extra></extra>'
))

# Configurar layout
fig.update_layout(
    xaxis_title='Rodada',
    yaxis_title='Quantidade de Bolas',
    height=500,
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    xaxis=dict(dtick=1)
)

st.plotly_chart(fig, use_container_width=True)

# Estatísticas
st.markdown("---")
st.subheader("📈 Estatísticas")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🎯 Lances")
    st.metric("Total", str(df['Lances'].sum()) + " bolas")
    st.metric("Média", str(round(df['Lances'].mean(), 2)) + " bolas")
    st.metric("Mínimo", str(df['Lances'].min()) + " bolas")
    st.metric("Máximo", str(df['Lances'].max()) + " bolas")

with col2:
    st.markdown("#### ✅ Acertos")
    st.metric("Total", str(df['Acertos'].sum()) + " bolas")
    st.metric("Média", str(round(df['Acertos'].mean(), 2)) + " bolas")
    st.metric("Mínimo", str(df['Acertos'].min()) + " bolas")
    st.metric("Máximo", str(df['Acertos'].max()) + " bolas")

with col3:
    st.markdown("#### 📊 Taxa de Acerto")
    taxa_acerto = (df['Acertos'].sum() / df['Lances'].sum()) * 100
    st.metric("Taxa Geral", str(round(taxa_acerto, 2)) + "%")
    st.metric("Melhor Rodada", "Rodada " + str(df['Rodada'][df['Acertos'] / df['Lances'] == (df['Acertos'] / df['Lances']).max()].values[0]))
    st.metric("Pior Rodada", "Rodada " + str(df['Rodada'][df['Acertos'] / df['Lances'] == (df['Acertos'] / df['Lances']).min()].values[0]))

# Adicionar coluna de taxa de acerto
df['Taxa_Acerto'] = round((df['Acertos'] / df['Lances']) * 100, 2)

# Tabela de dados
st.markdown("---")
st.subheader("📋 Dados Detalhados")

st.dataframe(df, use_container_width=True)