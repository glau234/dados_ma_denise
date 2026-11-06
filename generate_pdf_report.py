# -*- coding: utf-8 -*-
"""
Script para geração do Relatório Completo em PDF
Combina análises estatísticas, tabelas analíticas e gráficos vetoriais/alta resolução em PDF A4.
"""

import json
import base64
import os
import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright

print("Iniciando geração de gráficos e relatório PDF...")

# 1. Carregar dados consolidados
with open('analise_dados_completa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Configurações visuais do Matplotlib
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=220, bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{b64}"

# -------------------------------------------------------------
# GRÁFICO 1: Q1 (Correspondência Survey) & Q2 (Renovação Eventos)
# -------------------------------------------------------------
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

# Subplot 1: Q1
labels1 = ['Público Externo aos Eventos\n(166 pessoas - 73,5%)', 'Participantes de Eventos\n(60 pessoas - 26,5%)']
sizes1 = [data['q1']['external'], data['q1']['any_match']]
colors1 = ['#e11d48', '#10b981']
explode1 = (0.05, 0)
wedges1, texts1, autotexts1 = ax1.pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%',
                                      startangle=140, explode=explode1,
                                      textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
for at in autotexts1: at.set_color('white'); at.set_weight('bold')
ax1.set_title('P1: Correspondência do Survey com os Eventos\n(Amostra com Identificação N=226)', fontsize=11, fontweight='bold', pad=10)

# Subplot 2: Q2
labels2 = ['Novos Inscritos Atraídos\n(344 pessoas - 89,1%)', 'Participantes Recorrentes\n(42 pessoas - 10,9%)']
sizes2 = [data['q2']['e2_new'], data['q2']['overlap']]
colors2 = ['#2563eb', '#f59e0b']
explode2 = (0.05, 0)
wedges2, texts2, autotexts2 = ax2.pie(sizes2, labels=labels2, colors=colors2, autopct='%1.1f%%',
                                      startangle=140, explode=explode2,
                                      textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
for at in autotexts2: at.set_color('white'); at.set_weight('bold')
ax2.set_title('P2: Renovação de Público no Evento 2\n(Total de Inscritos N=386)', fontsize=11, fontweight='bold', pad=10)

plt.tight_layout()
b64_fig1 = fig_to_base64(fig1)

# -------------------------------------------------------------
# GRÁFICO 2: Q3 Mapa Perceptual da ACM (MCA 2D)
# -------------------------------------------------------------
fig2, ax = plt.subplots(figsize=(10, 6.2))

points = data['q3']['points']
var_colors = {
    'faixa_tempo': '#2563eb',
    'titulacao_clean': '#9333ea',
    'funcao_clean': '#d97706'
}
var_markers = {
    'faixa_tempo': 'o',
    'titulacao_clean': 's',
    'funcao_clean': '^'
}
var_labels = {
    'faixa_tempo': 'Tempo de Atuação',
    'titulacao_clean': 'Titulação Acadêmica',
    'funcao_clean': 'Função Profissional'
}

ax.axhline(0, color='#94a3b8', linestyle='--', linewidth=0.9, alpha=0.8)
ax.axvline(0, color='#94a3b8', linestyle='--', linewidth=0.9, alpha=0.8)

seen_vars = set()
for p in points:
    v = p['variable']
    cat = p['category']
    x, y = p['dim1'], p['dim2']
    lbl = var_labels[v] if v not in seen_vars else ""
    seen_vars.add(v)
    
    ax.scatter(x, y, color=var_colors[v], marker=var_markers[v], s=120, edgecolors='black', linewidth=0.8, label=lbl, zorder=5)
    
    # Anotações inteligentes com pequeno deslocamento
    offset_x = 0.04
    offset_y = 0.04
    if 'gerente' in cat.lower():
        offset_y = -0.15
    elif 'pós-doutorado' in cat.lower():
        offset_x = -0.3
    ax.annotate(cat, (x + offset_x, y + offset_y), fontsize=8.5, fontweight='semibold',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#cbd5e1", alpha=0.85), zorder=6)

ax.set_xlabel(f"Dimensão 1 ({data['q3']['inertia_dim1']}% da Inércia)  ←  Polo Acadêmico/Pesquisa  vs  Polo Prática/Gestão  →", fontsize=10, fontweight='bold', labelpad=8)
ax.set_ylabel(f"Dimensão 2 ({data['q3']['inertia_dim2']}% da Inércia)  ←  Técnico/Execução  vs  Liderança/Gerência  →", fontsize=10, fontweight='bold', labelpad=8)
ax.set_title("P3: Mapa Perceptual da Análise de Correspondência Múltipla (ACM)\nRelação entre Tempo de Atuação, Titulação Acadêmica e Função Profissional (N=243)", fontsize=11, fontweight='bold', pad=12)
ax.grid(True, linestyle=':', alpha=0.5)
ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)

plt.tight_layout()
b64_fig2 = fig_to_base64(fig2)

# -------------------------------------------------------------
# GRÁFICO 3: Q4 Distribuição Espacial e Esfera x Saúde
# -------------------------------------------------------------
fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

# Regiões
regs = list(data['q4']['regioes'].keys())
vals_reg = list(data['q4']['regioes'].values())
colors_reg = ['#1d4ed8', '#0284c7', '#0d9488', '#ca8a04', '#e11d48', '#64748b']

bars1 = ax1.bar(regs, vals_reg, color=colors_reg, edgecolor='black', linewidth=0.6)
ax1.set_title('Distribuição Regional dos Inscritos nos Eventos\n(Total N=1.128)', fontsize=10.5, fontweight='bold')
ax1.set_ylabel('Inscrições', fontsize=9.5)
ax1.tick_params(axis='x', rotation=25, labelsize=8.5)
for bar in bars1:
    h = bar.get_height()
    pct = h / 1128 * 100
    ax1.annotate(f'{h}\n({pct:.1f}%)',
                 xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=8)

# Esfera x Saúde
esferas = ['Público Federal', 'Público Estadual', 'Público Municipal', 'Outros/Academia']
saude_sim = [210, 123, 64, 73]
saude_nao = [277, 97, 31, 134]

y_pos = np.arange(len(esferas))
w = 0.38
b_sim = ax2.barh(y_pos - w/2, saude_sim, w, label='Saúde (SUS/Hospitais)', color='#0284c7', edgecolor='black', linewidth=0.6)
b_nao = ax2.barh(y_pos + w/2, saude_nao, w, label='Outras Políticas Públicas', color='#64748b', edgecolor='black', linewidth=0.6)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(esferas, fontsize=9)
ax2.invert_yaxis()
ax2.set_title('P4: Esfera de Atuação x Área da Saúde\n(Correlação Federativa)', fontsize=10.5, fontweight='bold')
ax2.set_xlabel('Quantidade de Inscritos', fontsize=9.5)
ax2.legend(loc='lower right', fontsize=8.5)

plt.tight_layout()
b64_fig3 = fig_to_base64(fig3)

# -------------------------------------------------------------
# GRÁFICO 4: Q5 Perfis dos 3 Clusters (Atribuições Cotidianas)
# -------------------------------------------------------------
fig4, ax = plt.subplots(figsize=(10, 5.2))

met_names = ['Estatística', 'Qualitativo', 'Indicadores', 'Síntese Evid.', 'ATS (Saúde)', 'Participativo', 'Questionários', 'Decisores']
keys = ['met_estatistica', 'met_qualitativa', 'met_indicadores', 'met_sintese', 'met_ats', 'met_participativa', 'met_questionarios', 'diss_decisores']

c0_vals = [data['q5']['means']['0'][k] * 100 for k in keys]
c1_vals = [data['q5']['means']['1'][k] * 100 for k in keys]
c2_vals = [data['q5']['means']['2'][k] * 100 for k in keys]

x_ind = np.arange(len(met_names))
bar_w = 0.27

ax.bar(x_ind - bar_w, c0_vals, bar_w, label='Cluster 1: Especialistas ATS (13,1%)', color='#3b82f6', edgecolor='black', linewidth=0.5)
ax.bar(x_ind, c1_vals, bar_w, label='Cluster 2: Ocasionais / Periféricos (37,1%)', color='#94a3b8', edgecolor='black', linewidth=0.5)
ax.bar(x_ind + bar_w, c2_vals, bar_w, label='Cluster 3: Núcleo Multimetodológico (49,8%)', color='#10b981', edgecolor='black', linewidth=0.5)

ax.set_xticks(x_ind)
ax.set_xticklabels(met_names, fontsize=9, fontweight='medium')
ax.set_ylabel('% de Adoção na Rotina de Trabalho', fontsize=9.5, fontweight='bold')
ax.set_title("P5: Análise de Clusters das Atribuições Cotidianas (K-Means, N=245)\nComparativo de Metodologias e Práticas de Trabalho", fontsize=11, fontweight='bold', pad=12)
ax.set_ylim(0, 115)
ax.grid(axis='y', linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)

for i in range(len(met_names)):
    ax.annotate(f"{c0_vals[i]:.0f}%", (x_ind[i] - bar_w, c0_vals[i] + 2), ha='center', fontsize=7.5, color='#1d4ed8', fontweight='bold')
    ax.annotate(f"{c1_vals[i]:.0f}%", (x_ind[i], c1_vals[i] + 2), ha='center', fontsize=7.5, color='#475569')
    ax.annotate(f"{c2_vals[i]:.0f}%", (x_ind[i] + bar_w, c2_vals[i] + 2), ha='center', fontsize=7.5, color='#047857', fontweight='bold')

plt.tight_layout()
b64_fig4 = fig_to_base64(fig4)

# -------------------------------------------------------------
# GRÁFICO 5: Insights Adicionais (Gênero, Raça e Disseminação)
# -------------------------------------------------------------
fig5, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11.5, 3.8))

# Subplot 1: Gênero Evento 1
ax1.pie([60.2, 39.8], labels=['Feminino\n(60,2%)', 'Masculino\n(39,8%)'], colors=['#8b5cf6', '#38bdf8'],
        autopct='%1.1f%%', startangle=140, textprops={'fontsize': 8.5}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.2})
ax1.set_title("Protagonismo Feminino\n(Inscritos Evento 1)", fontsize=10, fontweight='bold')

# Subplot 2: Raça/Etnia Survey
ax2.bar(['Branca', 'Parda', 'Preta', 'Outros'], [66.5, 24.9, 5.7, 2.9], color=['#f59e0b', '#d97706', '#78350f', '#94a3b8'], edgecolor='black', linewidth=0.5)
ax2.set_ylabel('% Respondentes', fontsize=8.5)
ax2.set_title("Composição Racial\n(Survey M&A)", fontsize=10, fontweight='bold')
ax2.tick_params(axis='x', labelsize=8)
for i, v in enumerate([66.5, 24.9, 5.7, 2.9]):
    ax2.annotate(f"{v}%", (i, v + 1.5), ha='center', fontsize=8, fontweight='bold')
ax2.set_ylim(0, 80)

# Subplot 3: Abismo da Comunicação
ax3.bar(['Tomadores de\nDecisão', 'Público Geral\n(Sociedade)'], [73.5, 33.1], color=['#2563eb', '#e11d48'], edgecolor='black', linewidth=0.5)
ax3.set_ylabel('% Praticam Disseminação', fontsize=8.5)
ax3.set_title("O 'Abismo da Comunicação'\n(Canais de Tradução)", fontsize=10, fontweight='bold')
ax3.tick_params(axis='x', labelsize=8)
for i, v in enumerate([73.5, 33.1]):
    ax3.annotate(f"{v}%", (i, v + 2), ha='center', fontsize=8.5, fontweight='bold')
ax3.set_ylim(0, 90)

plt.tight_layout()
b64_fig5 = fig_to_base64(fig5)

print("Gráficos gerados com sucesso em Base64.")

# -------------------------------------------------------------
# CONSTRUÇÃO DO HTML DOCUMENTO CORPORATIVO/OFICIAL
# -------------------------------------------------------------
html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório Analítico Oficial: Monitoramento, Avaliação e Evidências em Políticas Públicas</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 18mm 16mm 20mm 16mm;
      @bottom-right {{
        content: "Página " counter(page) " de " counter(pages);
        font-size: 8pt;
        color: #64748b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }}
      @bottom-left {{
        content: "Relatório de Pesquisa • Monitoramento, Avaliação e Políticas por Evidências (2024)";
        font-size: 8pt;
        color: #64748b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }}
    }}
    
    body {{
      font-family: 'Helvetica Neue', Arial, sans-serif;
      font-size: 9.5pt;
      line-height: 1.5;
      color: #1e293b;
      margin: 0;
      padding: 0;
    }}
    
    .cover-banner {{
      background: linear-gradient(135deg, #0c182b 0%, #1e3a8a 60%, #1e1b4b 100%);
      color: #ffffff;
      padding: 24px;
      border-radius: 8px;
      margin-bottom: 20px;
      border-bottom: 4px solid #00875f;
    }}
    
    .badge {{
      display: inline-block;
      background-color: #2563eb;
      color: #ffffff;
      font-size: 7.5pt;
      font-weight: bold;
      padding: 2px 8px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }}
    
    h1 {{
      font-size: 17pt;
      font-weight: 800;
      margin: 0 0 6px 0;
      color: #ffffff;
      line-height: 1.25;
    }}
    
    .subtitle {{
      font-size: 10pt;
      color: #cbd5e1;
      margin: 0;
    }}
    
    .meta-grid {{
      display: table;
      width: 100%;
      margin-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.2);
      padding-top: 10px;
    }}
    
    .meta-col {{
      display: table-cell;
      font-size: 8pt;
      color: #94a3b8;
    }}
    
    .meta-col strong {{
      color: #ffffff;
      display: block;
      font-size: 8.5pt;
    }}
    
    /* Indicadores de Destaque */
    .kpi-row {{
      display: table;
      width: 100%;
      margin-bottom: 18px;
    }}
    
    .kpi-card {{
      display: table-cell;
      width: 16.6%;
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 8px 10px;
      text-align: center;
      border-radius: 6px;
    }}
    
    .kpi-title {{
      font-size: 7pt;
      color: #64748b;
      font-weight: bold;
      text-transform: uppercase;
    }}
    
    .kpi-value {{
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      margin-top: 2px;
    }}
    
    .kpi-sub {{
      font-size: 6.8pt;
      color: #2563eb;
      font-weight: 500;
    }}
    
    /* Seções */
    h2 {{
      font-size: 12pt;
      font-weight: 700;
      color: #0c182b;
      border-bottom: 2px solid #00875f;
      padding-bottom: 4px;
      margin-top: 22px;
      margin-bottom: 10px;
      page-break-after: avoid;
    }}
    
    h3 {{
      font-size: 10pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-top: 14px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }}
    
    p {{
      margin-top: 0;
      margin-bottom: 8px;
      text-align: justify;
    }}
    
    /* Tabelas */
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8pt;
      margin: 10px 0 14px 0;
      page-break-inside: avoid;
    }}
    
    th {{
      background-color: #0c182b;
      color: #ffffff;
      font-weight: 700;
      padding: 6px 8px;
      text-align: left;
      border: 1px solid #0c182b;
    }}
    
    td {{
      padding: 5px 8px;
      border: 1px solid #cbd5e1;
    }}
    
    tr:nth-child(even) {{
      background-color: #f8fafc;
    }}
    
    .alert-box {{
      background-color: #f0fdf4;
      border-left: 4px solid #16a34a;
      padding: 8px 12px;
      font-size: 8.5pt;
      color: #166534;
      margin: 10px 0;
      border-radius: 0 4px 4px 0;
    }}
    
    .alert-warn {{
      background-color: #fffbeb;
      border-left: 4px solid #f59e0b;
      color: #92400e;
    }}
    
    .alert-info {{
      background-color: #eff6ff;
      border-left: 4px solid #2563eb;
      color: #1e40af;
    }}
    
    .chart-container {{
      text-align: center;
      margin: 14px 0;
      page-break-inside: avoid;
    }}
    
    .chart-img {{
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
    }}
    
    .page-break {{
      page-break-after: always;
    }}
  </style>
</head>
<body>

  <!-- BANNER CABEÇALHO -->
  <div class="cover-banner">
    <div class="badge">Relatório Analítico Executivo & Técnico</div>
    <h1>Redes de Monitoramento, Avaliação e Evidências em Políticas Públicas (2024)</h1>
    <div class="subtitle">Análise Empírica Integrada entre Inscritos nos Eventos Nacionais e o Survey de Escuta Setorial</div>
    <div class="meta-grid">
      <div class="meta-col">
        <strong>Ano Base dos Dados:</strong> 2024
      </div>
      <div class="meta-col">
        <strong>Universo de Inscrições:</strong> 1.128 participações (1.086 indivíduos)
      </div>
      <div class="meta-col">
        <strong>Amostra do Survey:</strong> 521 respondentes (245 prática ativa)
      </div>
      <div class="meta-col">
        <strong>Metodologias:</strong> Pareamento, ACM (MCA), K-Means, $\chi^2$
      </div>
    </div>
  </div>

  <!-- LINHA DE CARDS / KPIS -->
  <div class="kpi-row">
    <div class="kpi-card" style="margin-right: 5px;">
      <div class="kpi-title">Inscrições Eventos</div>
      <div class="kpi-value">1.128</div>
      <div class="kpi-sub">1.086 indivíduos únicos</div>
    </div>
    <div class="kpi-card" style="margin-right: 5px;">
      <div class="kpi-title">Respondentes Survey</div>
      <div class="kpi-value">521</div>
      <div class="kpi-sub">245 na bateria prática</div>
    </div>
    <div class="kpi-card" style="margin-right: 5px;">
      <div class="kpi-title">Taxa Renovação E2</div>
      <div class="kpi-value" style="color: #16a34a;">89,1%</div>
      <div class="kpi-sub">344 novos participantes</div>
    </div>
    <div class="kpi-card" style="margin-right: 5px;">
      <div class="kpi-title">Recorrência Geral</div>
      <div class="kpi-value" style="color: #d97706;">3,87%</div>
      <div class="kpi-sub">42 em ambos os eventos</div>
    </div>
    <div class="kpi-card" style="margin-right: 5px;">
      <div class="kpi-title">Participação Feminina</div>
      <div class="kpi-value" style="color: #7c3aed;">60,2%</div>
      <div class="kpi-sub">63,0% no Survey</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-title">Tradução Decisores</div>
      <div class="kpi-value" style="color: #0284c7;">73,5%</div>
      <div class="kpi-sub">33,1% p/ público geral</div>
    </div>
  </div>

  <!-- SUMÁRIO EXECUTIVO -->
  <h2>Sumário Executivo e Principais Conclusões</h2>
  <p>
    Este relatório consolida a investigação quantitativa e qualitativa das três bases estruturantes de 2024: <em>Inscritos-Politicas-Publicas-Informadas-por-Evidencias-2024.xlsx</em> (Evento 1, 742 inscritos), <em>Inscritos-Praticas-em-Avaliacao-e-Evidencias-para-Politicas-Publicas-2024.xlsx</em> (Evento 2, 386 inscritos) e <em>Survey-Escuta-Redes-de-Monitoramento-Avaliacao-Politicas-Publicas.xlsx</em> (Survey, 521 respondentes).
  </p>
  <div class="alert-box">
    <strong>Principais Achados em Síntese:</strong>
    <ul style="margin: 4px 0 0 16px; padding: 0;">
      <li><strong>Independência entre Survey e Eventos:</strong> 73,5% dos respondentes identificados do survey são profissionais externos que não participaram dos eventos de 2024. O survey atingiu uma rede muito mais ampla.</li>
      <li><strong>Alta Renovação de Público:</strong> No Evento 2, 89,1% dos profissionais eram estreantes. Houve apenas 42 pessoas recorrentes entre os dois eventos (taxa de sobreposição de apenas 3,87%).</li>
      <li><strong>Clivagem Estrutural (ACM):</strong> A Análise de Correspondência Múltipla demonstrou uma oposição clara entre o Polo Acadêmico-Sênior (Doutores e Pós-doutores, >10 anos de atuação, pesquisadores) e o Polo Governamental-Operacional (Especialistas, até 5 anos, atuando na gestão).</li>
      <li><strong>Padrão Federativo da Saúde:</strong> Quase metade dos inscritos (49,4%) é da área de Saúde. O setor Saúde concentra 67,4% dos participantes municipais e 55,9% dos estaduais, enquanto o governo federal abriga diversidade de políticas.</li>
      <li><strong>Três Perfis Operacionais (Clusters):</strong> 13,1% são especialistas altamente técnicos em ATS e Síntese; 37,1% são avaliadores ocasionais/periféricos; e 49,8% formam o núcleo multimetodológico ativo do Estado brasileiro.</li>
    </ul>
  </div>

  <!-- SEÇÃO 1: PERGUNTA 1 -->
  <h2>1. As pessoas que responderam ao survey são as mesmas dos eventos?</h2>
  <p>
    <strong>Diagnóstico: Não.</strong> O survey não é um reflexo estrito do público participante dos eventos, funcionando como um instrumento abrangente de escuta setorial.
  </p>
  <p>
    <strong>Metodologia de Pareamento:</strong> O questionário no Microsoft Forms foi configurado sem exigência de autenticação de login corporativo, gerando a resposta literal <code>anonymous</code> para a totalidade dos 521 registros na coluna <em>Email</em>. Todavia, em blocos opcionais ao final (autorização para entrevista e consentimento com o Ministério da Saúde), <strong>226 respondentes (43,4%) forneceram voluntariamente seus dados</strong> (Nome completo, CPF e/ou e-mail). Os outros <strong>295 participantes (56,6%)</strong> mantiveram anonimato.
  </p>
  <p>
    O cruzamento determinístico dos 226 identificados contra o banco unificado de inscritos dos eventos (1.086 indivíduos únicos) apresentou o seguinte resultado:
  </p>

  <table>
    <thead>
      <tr>
        <th>Segmento Analítico (Survey Identificado)</th>
        <th style="text-align: center;">Frequência</th>
        <th style="text-align: center;">% dos Identificados (N=226)</th>
        <th style="text-align: center;">% do Survey Total (N=521)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Público Externo aos Eventos (Sem correspondência)</strong></td>
        <td style="text-align: center; font-weight: bold; color: #e11d48;">166</td>
        <td style="text-align: center; font-weight: bold; color: #e11d48;">73,45%</td>
        <td style="text-align: center;">31,86%</td>
      </tr>
      <tr>
        <td>Presentes no Evento 1 (Políticas Informadas por Evidências)</td>
        <td style="text-align: center;">47</td>
        <td style="text-align: center;">20,80%</td>
        <td style="text-align: center;">9,02%</td>
      </tr>
      <tr>
        <td>Presentes no Evento 2 (Práticas em Avaliação)</td>
        <td style="text-align: center;">17</td>
        <td style="text-align: center;">7,52%</td>
        <td style="text-align: center;">3,26%</td>
      </tr>
      <tr>
        <td>Presentes em Ambos os Eventos Simultaneamente</td>
        <td style="text-align: center;">4</td>
        <td style="text-align: center;">1,77%</td>
        <td style="text-align: center;">0,77%</td>
      </tr>
      <tr style="background-color: #f1f5f9; font-weight: bold;">
        <td>Total com Presença Confirmada em pelo menos um Evento</td>
        <td style="text-align: center; color: #10b981;">60</td>
        <td style="text-align: center; color: #10b981;">26,55%</td>
        <td style="text-align: center;">11,52%</td>
      </tr>
      <tr>
        <td>Respondentes Anônimos (Sem dados de contato fornecidos)</td>
        <td style="text-align: center; color: #64748b;">295</td>
        <td style="text-align: center; color: #64748b;">-</td>
        <td style="text-align: center;">56,62%</td>
      </tr>
    </tbody>
  </table>

  <!-- SEÇÃO 2: PERGUNTA 2 -->
  <h2>2. Recorrência ou Renovação de Profissionais nos Dois Eventos?</h2>
  <p>
    <strong>Diagnóstico: Predomínio absoluto de renovação e atração de novos profissionais.</strong>
  </p>
  <p>
    Ao comparar o Evento 1 (742 participantes) com o Evento 2 (386 participantes), constata-se uma intersecção de apenas **42 indivíduos**. Isso demonstra que o segundo evento mobilizou massivamente novos públicos técnicos que não haviam aderido ao evento anterior.
  </p>

  <table>
    <thead>
      <tr>
        <th>Métrica de Transição e Fidelidade</th>
        <th style="text-align: center;">Quantidade</th>
        <th style="text-align: center;">Taxa (%)</th>
        <th>Interpretação Substantiva</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Taxa de Renovação no Evento 2</strong></td>
        <td style="text-align: center; font-weight: bold; color: #16a34a;">344</td>
        <td style="text-align: center; font-weight: bold; color: #16a34a;">89,12%</td>
        <td>Novos profissionais atraídos pelo recorte prático</td>
      </tr>
      <tr>
        <td>Taxa de Recorrência no Evento 2</td>
        <td style="text-align: center; color: #d97706;">42</td>
        <td style="text-align: center; color: #d97706;">10,88%</td>
        <td>Público fiel vindo do Evento 1</td>
      </tr>
      <tr>
        <td>Retenção do Evento 1 no Evento 2</td>
        <td style="text-align: center;">42 / 742</td>
        <td style="text-align: center;">5,66%</td>
        <td>Baixa migração direta entre os eventos</td>
      </tr>
      <tr style="background-color: #f1f5f9; font-weight: bold;">
        <td>Total de Indivíduos Únicos na Comunidade</td>
        <td style="text-align: center;">1.086</td>
        <td style="text-align: center;">100,00%</td>
        <td>Sobreposição global representa apenas 3,87%</td>
      </tr>
    </tbody>
  </table>

  <div class="chart-container">
    <img src="{b64_fig1}" class="chart-img" alt="Gráficos Q1 e Q2">
  </div>

  <div class="page-break"></div>

  <!-- SEÇÃO 3: PERGUNTA 3 -->
  <h2>3. Relação entre Tempo de Atuação, Titulação e Formação (ACM)</h2>
  <p>
    Para investigar a inter-relação multidimensional entre maturidade profissional, grau acadêmico e função exercida, processou-se a <strong>Análise de Correspondência Múltipla (ACM / MCA)</strong> sobre a amostra de profissionais com prática profunda em M&A (N = 243 casos completos no Survey).
  </p>

  <h3>3.1 Testes de Independência Qui-Quadrado ($\chi^2$)</h3>
  <ul>
    <li><strong>Titulação Acadêmica $\times$ Função Profissional:</strong> $\chi^2 = 70,06$, $p = 3,12 \times 10^{-10}$ ($gl = 12$). Forte associação estatística. Quase a totalidade dos pós-doutores (95,8%) e doutores (77,0%) desempenham a função de <em>Pesquisador</em>, enquanto os especialistas concentram-se na <em>Gestão Pública</em> (61,5%).</li>
    <li><strong>Tempo de Atuação $\times$ Titulação Acadêmica:</strong> $\chi^2 = 46,02$, $p = 0,0001$ ($gl = 16$). Associação altamente significante. Titulações mais altas correlacionam-se positivamente com mais de 10 a 20 anos de experiência acumulada.</li>
    <li><strong>Tempo de Atuação $\times$ Função Profissional:</strong> $\chi^2 = 17,86$, $p = 0,1201$ ($gl = 12$). A função em si é mediada prioritariamente pelo nível educacional formal do que puramente pelos anos de casa.</li>
  </ul>

  <h3>3.2 Mapa Perceptual Bidimensional da ACM</h3>
  <p>
    O plano fatorial explica <strong>26,59% da inércia acumulada</strong> (Dimensão 1 = 15,07%, Dimensão 2 = 11,52%), revelando uma divisão clara do ecossistema:
    <br>• <strong>Dimensão 1 (Eixo Horizontal):</strong> Clivagem entre o <em>Polo Acadêmico-Sênior</em> (Doutores e Pós-doutores no lado negativo, com mais de 10 a 20 anos de carreira e foco em pesquisa) e o <em>Polo Governamental-Operacional</em> (Especialistas, graduados e mestres no lado positivo, atuando na gestão direta e aplicação prática com até 5 anos de atuação).
    <br>• <strong>Dimensão 2 (Eixo Vertical):</strong> Isola a <em>Gerência Estratégica</em> (coordenada vertical +2,75), diferenciando os gestores e líderes de equipes dos analistas de base técnica.
  </p>

  <div class="chart-container">
    <img src="{b64_fig2}" class="chart-img" alt="Mapa Perceptual ACM">
  </div>

  <table>
    <thead>
      <tr>
        <th>Variável Analítica</th>
        <th>Categoria</th>
        <th style="text-align: center;">Coord. Dim 1</th>
        <th style="text-align: center;">Coord. Dim 2</th>
        <th>Associação Estrutural no Espaço Fatorial</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Tempo de Atuação</td><td>Mais de 20 anos</td><td style="text-align: center;">-0,8482</td><td style="text-align: center;">-1,1549</td><td>Polo Sênior / Pós-Doutorado</td></tr>
      <tr><td>Tempo de Atuação</td><td>De 11 a 20 anos</td><td style="text-align: center;">-0,7256</td><td style="text-align: center;">+0,2241</td><td>Polo Pleno-Sênior / Pesquisa Consolidada</td></tr>
      <tr><td>Tempo de Atuação</td><td>De 6 a 10 anos</td><td style="text-align: center;">+0,1026</td><td style="text-align: center;">+0,4613</td><td>Polo Intermediário / Liderança de Equipes</td></tr>
      <tr><td>Tempo de Atuação</td><td>De 3 a 5 anos</td><td style="text-align: center;">+0,3779</td><td style="text-align: center;">-0,2265</td><td>Polo Júnior / Mestrado / Gestão Aplicada</td></tr>
      <tr><td>Tempo de Atuação</td><td>Até 2 anos</td><td style="text-align: center;">+1,1213</td><td style="text-align: center;">-0,5354</td><td>Polo Iniciante / Gestão Pública</td></tr>
      <tr><td>Titulação Acadêmica</td><td>Pós-doutorado</td><td style="text-align: center;">-1,2565</td><td style="text-align: center;">-0,5999</td><td>Alta Pesquisa Científica</td></tr>
      <tr><td>Titulação Acadêmica</td><td>Doutorado</td><td style="text-align: center;">-0,4911</td><td style="text-align: center;">+0,4073</td><td>Pesquisa e Docência Aplicada</td></tr>
      <tr><td>Titulação Acadêmica</td><td>Mestrado</td><td style="text-align: center;">+0,6926</td><td style="text-align: center;">+0,5148</td><td>Gestão Intermediária e Gerência</td></tr>
      <tr><td>Titulação Acadêmica</td><td>Especialização</td><td style="text-align: center;">+1,1132</td><td style="text-align: center;">-1,3283</td><td>Operação e Gestão Pública Direta</td></tr>
      <tr><td>Função Profissional</td><td>Como pesquisador(a)</td><td style="text-align: center;">-0,6356</td><td style="text-align: center;">-0,1593</td><td>Polo Acadêmico / Produção de Estudos</td></tr>
      <tr><td>Função Profissional</td><td>Como gerente</td><td style="text-align: center;">+0,4802</td><td style="text-align: center;">+2,7542</td><td>Liderança Institucional e Articulação</td></tr>
      <tr><td>Função Profissional</td><td>Na gestão</td><td style="text-align: center;">+1,0408</td><td style="text-align: center;">-0,5037</td><td>Polo de Decisão Governamental e Programas</td></tr>
      <tr><td>Função Profissional</td><td>Como prático(a)</td><td style="text-align: center;">+0,6062</td><td style="text-align: center;">+0,2806</td><td>Polo de Campo e Aplicação Metodológica</td></tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- SEÇÃO 4: PERGUNTA 4 -->
  <h2>4. Distribuição Espacial, Esfera de Atuação e Área Setorial</h2>
  <p>
    A caracterização federativa e setorial das 1.128 participações em eventos e dos 521 respondentes do survey evidencia padrões nítidos de concentração e complementaridade.
  </p>

  <h3>4.1 Distribuição Geográfica e Federativa</h3>
  <p>
    O Centro-Oeste concentra quase a metade do público dos eventos (**49,56%** / 559 inscrições), com primazia do Distrito Federal (**45,39%** / 512 inscrições), motivada pela presença dos ministérios federais e órgãos setoriais. O Sudeste representa **23,85%** (destaque para SP com 11,0% e RJ com 8,0%), seguido pelo Nordeste (**12,23%**, com BA e CE), Sul (**6,47%**) e Norte (**5,76%**). No survey, a distribuição é mais desconcentrada, alcançando mais de 20 UFs.
  </p>

  <h3>4.2 Esfera de Atuação e a Correlação Estrutural com a Saúde</h3>
  <p>
    Nos eventos, a esfera <strong>Federal</strong> lidera com 43,17% (487 pessoas), seguida pela <strong>Estadual</strong> (19,50%), <strong>Outros/Academia</strong> (18,35%), <strong>Municipal</strong> (8,42%), <strong>Privado</strong> (6,21%) e <strong>Autônomo</strong> (3,99%).
  </p>
  <div class="alert-info">
    <strong>Achado Relevante sobre a Saúde nos Níveis Federativos:</strong>
    <br>Nos municípios, <strong>67,4% dos profissionais atuam na Saúde</strong> (Atenção Primária, Vigilância Epidemiológica e Hospitais). Nos estados, <strong>55,9% são da Saúde</strong>. Já na esfera Federal, apenas 43,1% são da Saúde, com 56,9% atuando em Educação (MEC/INEP), Desenvolvimento Social (MDS), Planejamento (MGI/IPEA) e Meio Ambiente (MMA/Ibama).
  </div>

  <div class="chart-container">
    <img src="{b64_fig3}" class="chart-img" alt="Distribuição Espacial e Esfera x Saúde">
  </div>

  <!-- SEÇÃO 5: PERGUNTA 5 -->
  <h2>5. Análise de Clusters: Perfis Profissionais segundo Atribuições Cotidianas</h2>
  <p>
    A partir de 14 variáveis comportamentais sobre o dia a dia de trabalho em M&A (N = 245), o modelo de agrupamento K-Means identificou <strong>3 perfis funcionais nítidos</strong> que estruturam a atuação profissional no Brasil:
  </p>

  <table>
    <thead>
      <tr>
        <th>Dimensão Operacional da Prática</th>
        <th style="text-align: center;">Cluster 1: Especialistas ATS (13,1% / N=32)</th>
        <th style="text-align: center;">Cluster 2: Ocasionais (37,1% / N=91)</th>
        <th style="text-align: center;">Cluster 3: Núcleo M&A (49,8% / N=122)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>M&A é Atividade Principal</strong></td><td style="text-align: center;">56,2%</td><td style="text-align: center;">26,4%</td><td style="text-align: center; font-weight: bold; color: #16a34a;">75,4%</td></tr>
      <tr><td><strong>Possui Projetos Ativos no Momento</strong></td><td style="text-align: center;">87,5%</td><td style="text-align: center;">50,5%</td><td style="text-align: center; font-weight: bold; color: #16a34a;">94,3%</td></tr>
      <tr><td><strong>Parcerias Internacionais Ativas</strong></td><td style="text-align: center;">31,2%</td><td style="text-align: center;">7,7%</td><td style="text-align: center; font-weight: bold;">33,6%</td></tr>
      <tr><td><strong>Tamanho Médio da Equipe</strong></td><td style="text-align: center; font-weight: bold; color: #2563eb;">8,7 pessoas</td><td style="text-align: center;">4,4 pessoas</td><td style="text-align: center;">5,7 pessoas</td></tr>
      <tr><td>Uso de Análise Estatística Aplicada</td><td style="text-align: center;">62,5%</td><td style="text-align: center;">19,8%</td><td style="text-align: center; font-weight: bold;">63,9%</td></tr>
      <tr><td>Uso de Métodos Qualitativos de Pesquisa</td><td style="text-align: center;">56,2%</td><td style="text-align: center;">38,5%</td><td style="text-align: center; font-weight: bold;">65,6%</td></tr>
      <tr><td>Desenvolvimento e Monitoramento de Indicadores</td><td style="text-align: center;">71,9%</td><td style="text-align: center;">38,5%</td><td style="text-align: center; font-weight: bold;">78,7%</td></tr>
      <tr><td>Síntese de Evidências (Revisões Sistemáticas/Escopo)</td><td style="text-align: center; font-weight: bold; color: #2563eb;">68,8%</td><td style="text-align: center;">14,3%</td><td style="text-align: center;">38,5%</td></tr>
      <tr><td><strong>Avaliação de Tecnologias em Saúde (ATS)</strong></td><td style="text-align: center; font-weight: bold; color: #2563eb;">100,0%</td><td style="text-align: center;">2,2%</td><td style="text-align: center;">0,0%</td></tr>
      <tr><td>Métodos Participativos e Facilitação</td><td style="text-align: center;">43,8%</td><td style="text-align: center;">16,5%</td><td style="text-align: center; font-weight: bold;">54,1%</td></tr>
      <tr><td>Desenvolvimento e Aplicação de Questionários</td><td style="text-align: center;">62,5%</td><td style="text-align: center;">20,9%</td><td style="text-align: center; font-weight: bold;">72,1%</td></tr>
      <tr><td><strong>Disseminação para Tomadores de Decisão</strong></td><td style="text-align: center;">78,1%</td><td style="text-align: center;">49,5%</td><td style="text-align: center; font-weight: bold; color: #16a34a;">90,2%</td></tr>
      <tr><td>Disseminação para o Público Geral</td><td style="text-align: center;">28,1%</td><td style="text-align: center;">19,8%</td><td style="text-align: center;">44,3%</td></tr>
      <tr><td>Realizou Capacitação Recente (3 anos)</td><td style="text-align: center; font-weight: bold;">75,0%</td><td style="text-align: center;">56,0%</td><td style="text-align: center;">65,6%</td></tr>
    </tbody>
  </table>

  <div class="chart-container">
    <img src="{b64_fig4}" class="chart-img" alt="Comparativo de Clusters">
  </div>

  <div class="page-break"></div>

  <!-- SEÇÃO 6: ECOSSISTEMA E DISSEMINAÇÃO -->
  <h2>6. Ecossistema Institucional, Veículos de Comunicação e Capacitação</h2>
  
  <h3>6.1 Instituições Âncoras</h3>
  <p>
    As instituições com maior presença agregada no ecossistema de avaliação foram:
    <br>1. <strong>Ministério da Saúde (MS):</strong> 71 menções diretas (forte indução em políticas informadas por evidências);
    <br>2. <strong>Fundação Oswaldo Cruz (Fiocruz):</strong> 41 menções (referência científica e formação em saúde coletiva);
    <br>3. <strong>Empresa Brasileira de Pesquisa Agropecuária (Embrapa):</strong> 17 menções (tradição em avaliação ex-ante e ex-post);
    <br>4. <strong>Instituto de Pesquisa Econômica Aplicada (IPEA):</strong> 15 menções (avaliação de impacto e formulação de políticas);
    <br>5. <strong>Secretaria de Saúde do DF (SES-DF) e Universidade de Brasília (UnB):</strong> 11 menções cada;
    <br>6. <strong>Ministério da Igualdade Racial (MIR) e ENAP:</strong> 10 e 8 menções.
  </p>

  <h3>6.2 O "Abismo da Comunicação Pública"</h3>
  <p>
    A análise comparativa revelou uma grave assimetria de tradução do conhecimento:
    <br>• <strong>Para Tomadores de Decisão (73,5%):</strong> Os veículos prioritários são <em>Relatórios e Notas Técnicas</em> (42,4%), <em>Seminários de Apresentação Interna</em> (41,3%), <em>Reuniões Estratégicas de Trabalho</em> (25,0%) e <em>Sumários Executivos</em> (15,2%). A circulação é altamente institucionalizada e interna aos gabinetes.
    <br>• <strong>Para o Público Geral (apenas 33,1%):</strong> Aqueles que divulgam utilizam prioritariamente o <em>Instagram</em> (45,7%) e o <em>LinkedIn</em> (39,1%). Dois terços dos avaliadores não possuem nenhuma rotina de diálogo direto com a sociedade civil.
  </p>

  <h3>6.3 Temas Críticos em Capacitação Recente</h3>
  <p>
    Nos últimos 3 anos, 63,7% dos profissionais realizaram cursos e treinamentos (mediana de 40 horas, predominantemente em modalidade autoinstrucional / EAD assíncrono). Os tópicos mais demandados foram:
    <em>Avaliação de Impacto Contrafactual</em>, <em>Ciência de Dados em Políticas Públicas</em>, <em>Construção de Indicadores</em>, <em>Teoria da Mudança / Modelos Lógicos</em> e <em>Síntese de Evidências</em>.
  </p>

  <!-- SEÇÃO 7: INSIGHTS ADICIONAIS APLICADOS -->
  <h2>7. Aplicação e Cruzamento dos Insights Adicionais na Gestão de M&A</h2>
  <p>
    Com a validação dos insights adicionais, aprofundou-se o cruzamento multivariado entre os fenômenos demográficos, comunicacionais e espaciais com os <strong>três clusters operacionais</strong> e as <strong>variáveis federativas</strong>:
  </p>

  <div class="chart-container">
    <img src="{b64_fig5}" class="chart-img" alt="Gráficos de Insights Extras">
  </div>

  <h3>7.1 Modalidade de Participação x Origem Geográfica: O Fator Crítico da Interiorização</h3>
  <p>
    A análise cruzada entre o domicílio do participante e a opção de acompanhamento no Evento 1 revelou que a oferta remota é a principal barreira de entrada superada:
  </p>
  <table>
    <thead>
      <tr>
        <th>Origem Federativa</th>
        <th style="text-align: center;">Optou pelo Online</th>
        <th style="text-align: center;">Optou pelo Presencial</th>
        <th style="text-align: center;">Outro / Não Especificado</th>
        <th style="text-align: center;">Proporção Efetiva Online (Declarados)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Participantes de Fora do DF (Demais Estados)</strong></td>
        <td style="text-align: center; font-weight: bold; color: #2563eb;">68,1%</td>
        <td style="text-align: center;">10,3%</td>
        <td style="text-align: center;">21,6%</td>
        <td style="text-align: center; font-weight: bold; color: #16a34a;">86,9% Online</td>
      </tr>
      <tr>
        <td><strong>Participantes Residentes no Distrito Federal</strong></td>
        <td style="text-align: center;">35,9%</td>
        <td style="text-align: center; font-weight: bold; color: #7c3aed;">41,0%</td>
        <td style="text-align: center;">23,1%</td>
        <td style="text-align: center;">46,7% Online</td>
      </tr>
    </tbody>
  </table>
  <p class="alert-info">
    <strong>Implicação para Gestão:</strong> Eventos estritamente presenciais em Brasília excluem quase 90% da rede nacional de avaliadores externos. O formato híbrido ou online é indispensável para a governança federativa de evidências.
  </p>

  <h3>7.2 Cruzamento de Gênero e Raça/Etnia nos Três Clusters Operacionais</h3>
  <p>
    Ao desagregar os dados demográficos pelos três agrupamentos funcionais identificados pelo algoritmo K-Means (N = 245), emergem clivagens de diversidade de extrema relevância:
  </p>
  <table>
    <thead>
      <tr>
        <th>Cluster de Atuação Cotidiana</th>
        <th style="text-align: center;">% Mulheres</th>
        <th style="text-align: center;">% Brancos</th>
        <th style="text-align: center;">% Pardos</th>
        <th style="text-align: center;">% Pretos</th>
        <th style="text-align: center;">Difusão para Público Geral</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Cluster 1: Especialistas em ATS e Síntese</strong> (N=32)</td>
        <td style="text-align: center; font-weight: bold; color: #7c3aed;">75,0%</td>
        <td style="text-align: center;">62,5%</td>
        <td style="text-align: center;">25,0%</td>
        <td style="text-align: center; font-weight: bold; color: #0f172a;">9,4%</td>
        <td style="text-align: center; color: #e11d48;">28,1%</td>
      </tr>
      <tr>
        <td><strong>Cluster 2: Avaliadores Ocasionais / Periféricos</strong> (N=91)</td>
        <td style="text-align: center;">58,2%</td>
        <td style="text-align: center;">61,5%</td>
        <td style="text-align: center; font-weight: bold; color: #d97706;">34,1%</td>
        <td style="text-align: center;">2,2%</td>
        <td style="text-align: center; color: #e11d48;">19,8%</td>
      </tr>
      <tr>
        <td><strong>Cluster 3: Núcleo Multimetodológico Ativo</strong> (N=122)</td>
        <td style="text-align: center;">63,1%</td>
        <td style="text-align: center; font-weight: bold; color: #2563eb;">71,3%</td>
        <td style="text-align: center;">18,0%</td>
        <td style="text-align: center;">7,4%</td>
        <td style="text-align: center; font-weight: bold; color: #16a34a;">44,3%</td>
      </tr>
    </tbody>
  </table>

  <div class="alert-warn">
    <strong>Diagnóstico de Equidade Racial:</strong> O núcleo mais consolidado de M&A (Cluster 3, que detém 94% dos projetos ativos e alta liderança) é o segmento com maior concentração de pessoas brancas (71,3%). Por outro lado, profissionais pardos encontram-se proporcionalmente mais retidos no Cluster 2 (34,1%), caracterizado por práticas secundárias, menor complexidade metodológica e menor visibilidade.
  </div>

  <!-- SEÇÃO 8: RECOMENDAÇÕES APLICADAS -->
  <h2>8. Plano de Diretrizes e Ações Estratégicas para a Rede de Evidências</h2>
  <ol style="margin-left: 20px; padding: 0;">
    <li>
      <strong>Programa de Transição e Capacitação de Avaliadores Ocasionais (Cluster 2 → Cluster 3):</strong>
      <br>Estruturar oficinas práticas de desenho de indicadores e estatística aplicada voltadas aos 37,1% de profissionais que realizam M&A de modo acessório, integrando-os aos projetos ativos dos ministérios.
    </li>
    <li>
      <strong>Política Ativa de Equidade Racial em Avaliação e Ciência de Dados:</strong>
      <br>Instituir cotas e bolsas afirmativas em cursos de especialização e mestrado em políticas públicas e economia aplicada para nivelar a presença de pessoas negras nas posições de alta titulação (doutorado e pós-doutorado, atualmente com >73% de brancos).
    </li>
    <li>
      <strong>Plano Institucional de Superação do "Abismo da Comunicação":</strong>
      <br>Obrigatoriedade de elaboração de um <em>Sumário Leigo para o Cidadão</em> e infográficos em todas as avaliações financiadas por fundos públicos, democratizando o conhecimento para além dos relatórios técnicos governamentais.
    </li>
    <li>
      <strong>Garantia de Modelo Híbrido Contínuo em Eventos de Evidências:</strong>
      <br>Manter a transmissão e participação síncrona online estruturada em todos os fóruns nacionais para garantir a permanência da rede nos estados do Norte, Nordeste e Sul, onde 86,9% dependem exclusivamente da modalidade virtual.
    </li>
  </ol>

</body>
</html>
"""

# Salvar HTML gerado
with open('relatorio_final_impressao.html', 'w', encoding='utf-8') as f:
    f.write(html_doc)

print("HTML base do relatório gerado em relatorio_final_impressao.html.")

# Converter para PDF via Playwright Chromium
pdf_output_path = os.path.abspath('Relatorio_Completo_Monitoramento_Avaliacao_2024.pdf')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_doc, wait_until='networkidle')
    page.pdf(
        path=pdf_output_path,
        format='A4',
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size: 7.5pt; color: #94a3b8; width: 100%; text-align: right; padding-right: 16mm; font-family: Helvetica, Arial, sans-serif;">Relatório Oficial de Pesquisa • M&A e Evidências 2024</div>',
        footer_template='<div style="font-size: 7.5pt; color: #94a3b8; width: 100%; text-align: center; font-family: Helvetica, Arial, sans-serif;">Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>',
        margin={
            'top': '18mm',
            'bottom': '20mm',
            'left': '16mm',
            'right': '16mm'
        }
    )
    browser.close()

print(f"PDF gerado com sucesso em: {pdf_output_path}")

