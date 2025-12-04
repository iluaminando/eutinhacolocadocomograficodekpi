import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="KPIs de Precisão", layout="wide")

st.title("KPIs de Precisão - Decode 25-26 Regional")
st.markdown("### Análise de Precisão com Linhas de Meta")

geral_data = {
    'Ponto': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'Precisao': [68.16, 80.00, 80.76, 93.50, 73.40, 55.50, 92.80, 77.70, 85.10, 90.40, 58.30]
}

pequena_area_data = {
    'Ponto': [1, 2, 3, 4, 5],
    'Precisao': [80.00, 42.80, 47.80, 83.30, 66.60]
}

grande_area_data = {
    'Ponto': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'Precisao': [68.16, 80.00, 80.76, 93.50, 73.40, 72.40, 79.80, 56.25, 85.10, 87.87, 61.90]
}

df_geral = pd.DataFrame(geral_data)
df_pequena = pd.DataFrame(pequena_area_data)
df_grande = pd.DataFrame(grande_area_data)

META_GERAL = 80.0
META_PEQUENA = 70.0
META_GRANDE = 75.0

def criar_grafico(df, meta, cor):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Ponto'],
        y=df['Precisao'],
        mode='markers',
        name='Precisão',
        marker=dict(size=12, color=cor, line=dict(width=2, color='white')),
        hovertemplate='Ponto %{x}<br>Precisão: %{y:.2f}%<extra></extra>'
    ))
    
    x_min = df['Ponto'].min() - 0.5
    x_max = df['Ponto'].max() + 0.5
    
    fig.add_trace(go.Scatter(
        x=[x_min, x_max],
        y=[meta, meta],
        mode='lines',
        name='Meta: ' + str(meta) + '%',
        line=dict(color='red', width=3, dash='dash'),
        hovertemplate='Meta: ' + str(meta) + '%<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Índice do Ponto',
        yaxis_title='Precisão (%)',
        yaxis=dict(range=[0, 100]),
        xaxis=dict(range=[0, df['Ponto'].max() + 1]),
        height=450,
        hovermode='closest',
        showlegend=True
    )
    
    return fig

st.subheader("1. Precisão Geral de Acerto")
fig1 = criar_grafico(df_geral, META_GERAL, '#667eea')
st.plotly_chart(fig1, use_container_width=True)

pontos_acima_geral = len(df_geral[df_geral['Precisao'] >= META_GERAL])
st.info('Meta: ' + str(META_GERAL) + '% | Pontos acima da meta: ' + str(pontos_acima_geral) + ' de ' + str(len(df_geral)))

st.markdown("---")

st.subheader("2. Precisão da Pequena Área de Acerto")
fig2 = criar_grafico(df_pequena, META_PEQUENA, '#f5576c')
st.plotly_chart(fig2, use_container_width=True)

pontos_acima_pequena = len(df_pequena[df_pequena['Precisao'] >= META_PEQUENA])
st.info('Meta: ' + str(META_PEQUENA) + '% | Pontos acima da meta: ' + str(pontos_acima_pequena) + ' de ' + str(len(df_pequena)))

st.markdown("---")

st.subheader("3. Precisão da Grande Área de Acerto")
fig3 = criar_grafico(df_grande, META_GRANDE, '#4facfe')
st.plotly_chart(fig3, use_container_width=True)

pontos_acima_grande = len(df_grande[df_grande['Precisao'] >= META_GRANDE])
st.info('Meta: ' + str(META_GRANDE) + '% | Pontos acima da meta: ' + str(pontos_acima_grande) + ' de ' + str(len(df_grande)))

st.markdown("---")
st.subheader("Estatísticas Resumidas")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Precisão Geral")
    st.metric("Média", str(round(df_geral['Precisao'].mean(), 2)) + "%")
    st.metric("Mínima", str(round(df_geral['Precisao'].min(), 2)) + "%")
    st.metric("Máxima", str(round(df_geral['Precisao'].max(), 2)) + "%")
    st.metric("Meta", str(META_GERAL) + "%")

with col2:
    st.markdown("#### Pequena Área")
    st.metric("Média", str(round(df_pequena['Precisao'].mean(), 2)) + "%")
    st.metric("Mínima", str(round(df_pequena['Precisao'].min(), 2)) + "%")
    st.metric("Máxima", str(round(df_pequena['Precisao'].max(), 2)) + "%")
    st.metric("Meta", str(META_PEQUENA) + "%")

with col3:
    st.markdown("#### Grande Área")
    st.metric("Média", str(round(df_grande['Precisao'].mean(), 2)) + "%")
    st.metric("Mínima", str(round(df_grande['Precisao'].min(), 2)) + "%")
    st.metric("Máxima", str(round(df_grande['Precisao'].max(), 2)) + "%")
    st.metric("Meta", str(META_GRANDE) + "%")

st.markdown("---")
st.subheader("Dados Detalhados")

tab1, tab2, tab3 = st.tabs(["Precisão Geral", "Pequena Área", "Grande Área"])

with tab1:
    st.dataframe(df_geral, use_container_width=True)

with tab2:
    st.dataframe(df_pequena, use_container_width=True)

with tab3:
    st.dataframe(df_grande, use_container_width=True)