import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Análise FTC Robot",
    page_icon="🤖",
    layout="wide"
)

# CSS customizado para tema escuro
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
    }
    .stMetric {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 8px;
    }
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center; color: #ff3333;'>🤖 Tech Fenix - Análise FTC</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #cccccc;'>Evolução de Pontuação por Configuração</p>", unsafe_allow_html=True)
st.markdown("---")

# Dados de pontuação
data = {
    'Normal': [57, 60, 58, 51, 61, 49, 55],
    'PDFL': [77, 61, 84, 79, 70, 85],
    'PDFL + Limelight': [96, 89, 86, 86, 84, 90, 92]
}

# Preparar dados para o gráfico de barras empilhadas
rounds_data = []
max_rounds = max(len(scores) for scores in data.values())

for i in range(max_rounds):
    round_dict = {'Round': f'R{i+1}'}
    for config in ['Normal', 'PDFL', 'PDFL + Limelight']:
        if i < len(data[config]):
            round_dict[config] = data[config][i]
        else:
            round_dict[config] = 0
    rounds_data.append(round_dict)

rounds_df = pd.DataFrame(rounds_data)

# Cores estilo da imagem
colors = {
    'Normal': '#d4a574',  # Marrom/dourado claro
    'PDFL': '#b8894e',    # Marrom/dourado médio
    'PDFL + Limelight': '#8b6f47'  # Marrom/dourado escuro
}

# Criar gráfico de barras agrupadas estilo da imagem
fig = go.Figure()

# Adicionar barras para cada configuração
for config in ['Normal', 'PDFL', 'PDFL + Limelight']:
    fig.add_trace(go.Bar(
        name=config,
        x=rounds_df['Round'],
        y=rounds_df[config],
        marker_color=colors[config],
        marker_line_color='#1a1a1a',
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>' +
                      config + ': %{y} pts<br>' +
                      '<extra></extra>'
    ))

fig.update_layout(
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='#ffffff', size=12),
    height=450,
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        color='#ffffff'
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='#3a3a3a',
        showline=False,
        zeroline=False,
        color='#ffffff',
        title='Pontos'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=1.12,
        xanchor="center",
        x=0.5,
        bgcolor='rgba(0,0,0,0)',
        font=dict(size=13)
    ),
    margin=dict(t=80, b=40, l=40, r=40)
)

# Exibir gráfico
st.plotly_chart(fig, use_container_width=True)

# Estatísticas em cards
st.markdown("### 📊 Estatísticas por Configuração")
cols = st.columns(3)

config_names = ['Normal', 'PDFL', 'PDFL + Limelight']
config_colors = ['#d4a574', '#b8894e', '#8b6f47']

for idx, config in enumerate(config_names):
    with cols[idx]:
        scores = data[config]
        media = round(sum(scores) / len(scores))
        min_score = min(scores)
        max_score = max(scores)
        
        st.markdown(f"""
        <div style='background-color: #2d2d2d; padding: 20px; border-radius: 10px; border-left: 5px solid {config_colors[idx]};'>
            <h3 style='color: {config_colors[idx]}; margin-bottom: 15px;'>{config}</h3>
            <p style='font-size: 32px; font-weight: bold; color: #ffffff; margin: 10px 0;'>{media} pts</p>
            <p style='color: #aaaaaa; margin: 5px 0;'>📊 Média de {len(scores)} rounds</p>
            <hr style='border-color: #3a3a3a; margin: 15px 0;'>
            <p style='color: #cccccc;'>🔻 Mínimo: <span style='color: #ff6b6b;'>{min_score} pts</span></p>
            <p style='color: #cccccc;'>🔺 Máximo: <span style='color: #51cf66;'>{max_score} pts</span></p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Análise de melhorias
st.markdown("### 📈 Evolução e Melhorias")

normal_media = round(sum(data['Normal']) / len(data['Normal']))
pdfl_media = round(sum(data['PDFL']) / len(data['PDFL']))
limelight_media = round(sum(data['PDFL + Limelight']) / len(data['PDFL + Limelight']))

diff1 = pdfl_media - normal_media
diff2 = limelight_media - pdfl_media
diff_total = limelight_media - normal_media
perc_total = round((diff_total / normal_media) * 100, 1)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"""
    <div style='background-color: #2d2d2d; padding: 25px; border-radius: 10px;'>
        <h4 style='color: #ffffff; margin-bottom: 20px;'>Progressão de Desempenho</h4>
        
        <div style='margin: 15px 0;'>
            <span style='color: #d4a574; font-size: 18px; font-weight: bold;'>●</span>
            <span style='color: #ffffff; font-size: 16px;'> Normal: {normal_media} pts</span>
        </div>
        
        <div style='margin: 15px 0; padding-left: 20px;'>
            <span style='color: #51cf66;'>↗ +{diff1} pts</span>
        </div>
        
        <div style='margin: 15px 0;'>
            <span style='color: #b8894e; font-size: 18px; font-weight: bold;'>●</span>
            <span style='color: #ffffff; font-size: 16px;'> PDFL: {pdfl_media} pts</span>
        </div>
        
        <div style='margin: 15px 0; padding-left: 20px;'>
            <span style='color: #51cf66;'>↗ +{diff2} pts</span>
        </div>
        
        <div style='margin: 15px 0;'>
            <span style='color: #8b6f47; font-size: 18px; font-weight: bold;'>●</span>
            <span style='color: #ffffff; font-size: 16px;'> PDFL + Limelight: {limelight_media} pts</span>
        </div>
        
        <hr style='border-color: #3a3a3a; margin: 20px 0;'>
        
        <p style='color: #51cf66; font-size: 20px; font-weight: bold;'>
            ⚡ Melhoria Total: +{diff_total} pts (+{perc_total}%)
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background-color: #2d2d2d; padding: 25px; border-radius: 10px; border: 2px solid #8b6f47; text-align: center;'>
        <p style='color: #aaaaaa; font-size: 14px; margin-bottom: 10px;'>🏆 MELHOR</p>
        <h3 style='color: #8b6f47; margin: 10px 0;'>PDFL + Limelight</h3>
        <p style='font-size: 36px; font-weight: bold; color: #ffffff; margin: 15px 0;'>{limelight_media}</p>
        <p style='color: #aaaaaa; font-size: 14px;'>pontos médios</p>
    </div>
    """, unsafe_allow_html=True)

# Tabela de dados
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📋 Ver Todas as Pontuações"):
    display_data = {}
    max_len = max(len(scores) for scores in data.values())
    
    for config in ['Normal', 'PDFL', 'PDFL + Limelight']:
        scores = data[config] + ['-'] * (max_len - len(data[config]))
        display_data[config] = scores
    
    display_df = pd.DataFrame(display_data)
    display_df.index = [f'Round {i+1}' for i in range(max_len)]
    st.dataframe(display_df, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666666;'>Tech Fenix © 2024 - Análise de Desempenho FTC</p>", unsafe_allow_html=True)