import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Configuração da página
st.set_page_config(page_title="KPI Radar Chart", layout="wide")

# Título
st.title("📊 Comparação de KPIs - Gráfico Radar")

# Dados dos KPIs
data = {
    'KPI': [
        'Precisão geral de acerto',
        'Precisão acerto pequena Launcher',
        'Precisão acerto grande Launcher',
        'Média geral de acertos',
        'Média acertos pequena Launcher',
        'Média acertos grande Launcher',
        'Média artefatos geral',
        'Média artefatos pequena Launcher',
        'Média artefatos grande Launcher',
        'Média ciclo geral',
        'Média ciclo pequena Launcher',
        'Média ciclo grande Launcher'
    ],
    'Valor Antigo': [74, np.nan, 74, 19, np.nan, 19, 25, np.nan, 25, 7.4, np.nan, 7.4],
    'Valor Atual': [76, 62, 79, 21, 4, 17, 28, 6, 11, 8.2, 7.12, 7.4],
    'Meta': [86.6, 54.54, 63.88, 26, 7, 19, 30, 11, 19, 7, 7, 5]
}

df = pd.DataFrame(data)

# Mostrar tabela
st.subheader("📋 Dados dos KPIs")
st.dataframe(df, use_container_width=True)

# Opção para download CSV
csv = df.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="kpis_dados.csv",
    mime="text/csv"
)

st.divider()

# Seletor de KPIs para visualizar
st.subheader("🎯 Selecione os KPIs para visualizar")
selected_kpis = st.multiselect(
    "Escolha os KPIs:",
    options=df['KPI'].tolist(),
    default=df['KPI'].tolist()[:6]  # Seleciona os 6 primeiros por padrão
)

# Filtrar dados selecionados
df_filtered = df[df['KPI'].isin(selected_kpis)].copy()

if len(df_filtered) > 0:
    # Normalizar os valores para escala 0-100 para melhor visualização
    st.subheader("⚙️ Opções de Normalização")
    normalize = st.checkbox("Normalizar valores (0-100)", value=True)
    
    if normalize:
        # Para cada KPI, normalizar baseado no valor máximo entre valor antigo, atual e meta
        df_plot = df_filtered.copy()
        for idx, row in df_plot.iterrows():
            max_val = max([v for v in [row['Valor Antigo'], row['Valor Atual'], row['Meta']] if pd.notna(v)])
            if max_val > 0:
                if pd.notna(row['Valor Antigo']):
                    df_plot.at[idx, 'Valor Antigo'] = (row['Valor Antigo'] / max_val) * 100
                if pd.notna(row['Valor Atual']):
                    df_plot.at[idx, 'Valor Atual'] = (row['Valor Atual'] / max_val) * 100
                if pd.notna(row['Meta']):
                    df_plot.at[idx, 'Meta'] = (row['Meta'] / max_val) * 100
    else:
        df_plot = df_filtered.copy()
    
    # Criar gráfico radar
    st.subheader("📈 Gráfico Radar - Comparação de Estágios")
    
    fig = go.Figure()

     # Adicionar traço para Meta
    fig.add_trace(go.Scatterpolar(
        r=df_plot['Meta'].fillna(0).tolist() + [df_plot['Meta'].fillna(0).tolist()[0]],
        theta=df_plot['KPI'].tolist() + [df_plot['KPI'].tolist()[0]],
        fill='toself',
        name='Meta',
        line=dict(color='#000000', width=1, dash='dash'),
            fillcolor='rgba(0, 0, 0, 0.5)'

    ))
   
    # Adicionar traço para Valor Atual
    fig.add_trace(go.Scatterpolar(
        r=df_plot['Valor Atual'].fillna(0).tolist() + [df_plot['Valor Atual'].fillna(0).tolist()[0]],
        theta=df_plot['KPI'].tolist() + [df_plot['KPI'].tolist()[0]],
        fill='toself',
        name='Valor Atual',
        line=dict(color='#7B1B10', width=2),
        fillcolor='rgba(123, 27, 16, 0.5)'

    ))
     
    # Adicionar traço para Valor Antigo
    if df_plot['Valor Antigo'].notna().any():
        fig.add_trace(go.Scatterpolar(
            r=df_plot['Valor Antigo'].fillna(0).tolist() + [df_plot['Valor Antigo'].fillna(0).tolist()[0]],
            theta=df_plot['KPI'].tolist() + [df_plot['KPI'].tolist()[0]],
            fill='toself',
            name='Valor Antigo',
         line=dict(color='#D4AD53', width=2),
         fillcolor='rgba(212, 173, 83, 0.5)'

        ))
    
    # Configurar layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100] if normalize else [0, df_plot[['Valor Antigo', 'Valor Atual', 'Meta']].max().max() * 1.1]
            ),
            angularaxis=dict(
                tickfont=dict(size=25)  # ← AQUI muda o tamanho da fonte das KPIs
            )

        ),
        showlegend=True,
        title="Comparação de KPIs - Três Estágios",
        height=700,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise rápida
    st.subheader("📊 Análise Rápida")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        acima_meta = len(df_filtered[df_filtered['Valor Atual'] >= df_filtered['Meta']])
        st.metric("KPIs acima da meta", f"{acima_meta}/{len(df_filtered)}")
    
    with col2:
        melhorou = len(df_filtered[(df_filtered['Valor Atual'] > df_filtered['Valor Antigo']) & df_filtered['Valor Antigo'].notna()])
        total_com_historico = len(df_filtered[df_filtered['Valor Antigo'].notna()])
        st.metric("KPIs que melhoraram", f"{melhorou}/{total_com_historico}")
    
    with col3:
        media_atingimento = ((df_filtered['Valor Atual'] / df_filtered['Meta']) * 100).mean()
        st.metric("Atingimento médio da meta", f"{media_atingimento:.1f}%")

else:
    st.warning("⚠️ Selecione pelo menos um KPI para visualizar o gráfico.")