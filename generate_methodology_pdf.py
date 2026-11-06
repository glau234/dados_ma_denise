# -*- coding: utf-8 -*-
"""
Script para geração do Relatório Técnico Completo de Metodologia, Métricas e Ferramentas de Análise em PDF.
Inclui diagramas e gráficos metodológicos em alta resolução (Matplotlib 300 DPI), catálogo mestre de métricas,
equações matemáticas completas, tabelas de validação estatística (Autovalores ACM, Silhueta/WCSS K-Means,
ANOVA F-test, V de Cramér e Cascata de Pareamento Determinístico).
"""

import os
import io
import base64
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from playwright.sync_api import sync_playwright

print("Iniciando geração dos gráficos metodológicos e compilação do Relatório Completo de Metodologia...")

# Configurações visuais do Matplotlib
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=260, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{b64}"

# ==============================================================================
# FIGURA METODOLÓGICA 1: Cascata de Resolução de Entidades (Camadas 1, 2 e 3)
# ==============================================================================
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))

# Painel A: Q1 (Survey vs Eventos - 60 matches)
layers = ['Camada 1:\nCPF Exato\n(11 dígitos)', 'Camada 2:\nE-mail Normalizado\n(Resgate incremental)', 'Camada 3:\nNome Fonético/ASCII\n(Resgate incremental)', 'Total Pareado\n(Acumulado)']
vals_q1 = [42, 10, 8, 60]
colors_q1 = ['#1e40af', '#2563eb', '#60a5fa', '#059669']
bars1 = ax1.bar(layers, vals_q1, color=colors_q1, width=0.55, edgecolor='#0f172a', linewidth=0.6)
ax1.set_title('A. Pareamento Survey × Eventos (N = 60 pareados)\nContribuição Marginal por Camada Determinística', fontsize=9.5, fontweight='bold', color='#0f172a', pad=10)
ax1.set_ylabel('Nº de Indivíduos Pareados', fontsize=8.5, fontweight='bold', color='#334155')
ax1.set_ylim(0, 72)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.tick_params(axis='x', labelsize=7.5)
for b, v in zip(bars1, vals_q1):
    pct = v / 60.0 * 100
    ax1.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v} ({pct:.1f}%)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0f172a')

# Painel B: Q2 (Evento 2 vs Evento 1 - 40 matches exatos por CPF)
vals_q2 = [40, 0, 0, 40]
colors_q2 = ['#0f766e', '#14b8a6', '#5eead4', '#d97706']
bars2 = ax2.bar(layers, vals_q2, color=colors_q2, width=0.55, edgecolor='#0f172a', linewidth=0.6)
ax2.set_title('B. Pareamento Evento 2 × Evento 1 (N = 40 recorrentes)\nContribuição Marginal c/ Trava Anti-Conflito de CPF', fontsize=9.5, fontweight='bold', color='#0f172a', pad=10)
ax2.set_ylabel('Nº de Indivíduos Pareados', fontsize=8.5, fontweight='bold', color='#334155')
ax2.set_ylim(0, 52)
ax2.grid(axis='y', linestyle='--', alpha=0.4)
ax2.tick_params(axis='x', labelsize=7.5)
for b, v in zip(bars2, vals_q2):
    pct = v / 40.0 * 100
    ax2.text(b.get_x() + b.get_width()/2, v + 1.2, f"{v} ({pct:.1f}%)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0f172a')

plt.tight_layout()
b64_fig1 = fig_to_base64(fig1)

# ==============================================================================
# FIGURA METODOLÓGICA 2: Scree Plot de Autovalores da ACM e V de Cramér
# ==============================================================================
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))

dims = [f"Dim {i}" for i in range(1, 12)]
eigenvalues = [0.553, 0.422, 0.399, 0.386, 0.357, 0.342, 0.323, 0.276, 0.240, 0.217, 0.151]
pct_var = [15.07, 11.52, 10.88, 10.53, 9.73, 9.32, 8.82, 7.54, 6.54, 5.93, 4.12]
cum_var = [15.07, 26.59, 37.47, 48.00, 57.73, 67.05, 75.87, 83.41, 89.95, 95.88, 100.00]

bar_colors = ['#2563eb', '#3b82f6'] + ['#94a3b8']*9
ax1.bar(dims, pct_var, color=bar_colors, width=0.6, label='% Inércia Individual')
ax1_twin = ax1.twinx()
ax1_twin.plot(dims, cum_var, color='#dc2626', marker='o', linewidth=2, markersize=4.5, label='% Inércia Acumulada')
ax1.set_title('A. Scree Plot da ACM: Decomposição dos 11 Autovalores\n(Matriz de Burt / SVD com Inércia Total = 3,6667)', fontsize=9.5, fontweight='bold', color='#0f172a', pad=10)
ax1.set_ylabel('% da Variância / Inércia Explicada', fontsize=8, fontweight='bold', color='#1e40af')
ax1_twin.set_ylabel('% Acumulada', fontsize=8, fontweight='bold', color='#dc2626')
ax1.set_ylim(0, 20)
ax1_twin.set_ylim(0, 110)
ax1.tick_params(axis='x', labelsize=7.5, rotation=30)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
for i in range(2):
    ax1.text(i, pct_var[i] + 0.5, f"{pct_var[i]:.1f}%", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1e40af')

# Painel B: Testes Qui-Quadrado e V de Cramér
pairs = ['Titulação ×\nFunção Principal', 'Faixa de Tempo ×\nTitulação', 'Faixa de Tempo ×\nFunção Principal']
chi2_vals = [70.06, 46.02, 17.86]
cramer_vals = [0.3100, 0.2176, 0.1565]
x_pos = np.arange(len(pairs))
w = 0.35
b_chi = ax2.bar(x_pos - w/2, chi2_vals, width=w, color='#4f46e5', label='Estatística χ²')
ax2_twin = ax2.twinx()
b_cra = ax2_twin.bar(x_pos + w/2, cramer_vals, width=w, color='#059669', label='V de Cramér')
ax2.set_title('B. Magnitude de Associação Bivariada Pré-ACM\nEstatística Qui-Quadrado (χ²) vs. V de Cramér', fontsize=9.5, fontweight='bold', color='#0f172a', pad=10)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(pairs, fontsize=8)
ax2.set_ylabel('Valor de χ² (Pearson)', fontsize=8, fontweight='bold', color='#4f46e5')
ax2_twin.set_ylabel('Índice V de Cramér (0 a 1)', fontsize=8, fontweight='bold', color='#059669')
ax2.set_ylim(0, 85)
ax2_twin.set_ylim(0, 0.40)
ax2.grid(axis='y', linestyle='--', alpha=0.4)
for i, (c2, cv) in enumerate(zip(chi2_vals, cramer_vals)):
    ax2.text(i - w/2, c2 + 1.5, f"χ²={c2:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#4f46e5')
    ax2_twin.text(i + w/2, cv + 0.01, f"V={cv:.3f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#059669')

plt.tight_layout()
b64_fig2 = fig_to_base64(fig2)

# ==============================================================================
# FIGURA METODOLÓGICA 3: Validação do K-Means (WCSS Cotovelo e Silhueta k=2..6)
# ==============================================================================
fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6))

k_vals = [2, 3, 4, 5, 6]
wcss_vals = [2985.94, 2767.55, 2585.03, 2444.79, 2359.04]
sil_vals = [0.1215, 0.1235, 0.1109, 0.1079, 0.1166]

ax1.plot(k_vals, wcss_vals, marker='o', color='#1e40af', linewidth=2.2, markersize=6)
ax1.scatter([3], [2767.55], color='#dc2626', s=110, zorder=5, label='Ponto de Inflexão Ótimo (k=3)')
ax1.set_title('A. Método do Cotovelo (Elbow Curve)\nSoma dos Quadrados Intra-Cluster (WCSS / Inércia)', fontsize=9.5, fontweight='bold', color='#0f172a', pad=10)
ax1.set_xlabel('Número de Clusters (k)', fontsize=8.5, fontweight='bold')
ax1.set_ylabel('WCSS (Distância Euclidiana Quadrática)', fontsize=8.5, fontweight='bold')
ax1.set_xticks(k_vals)
ax1.set_ylim(2250, 3150)
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.legend(loc='upper right', fontsize=8)
for k, w in zip(k_vals, wcss_vals):
    ax1.annotate(f"{w:.0f}", (k, w), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=7.5, fontweight='bold')

ax2.plot(k_vals, sil_vals, marker='s', color='#059669', linewidth=2.2, markersize=6)
ax2.scatter([3], [0.1235], color='#dc2626', s=110, zorder=5, label='Máximo Global de Silhueta (k=3)')
ax2.set_title('B. Coeficiente Médio de Silhueta de Rousseeuw\nCoesão Interna vs. Separação Externa (k = 2 a 6)', fontsize=9.5, fontweight='bold', color='#0f172a', pad=10)
ax2.set_xlabel('Número de Clusters (k)', fontsize=8.5, fontweight='bold')
ax2.set_ylabel('Score de Silhueta Médio', fontsize=8.5, fontweight='bold')
ax2.set_xticks(k_vals)
ax2.set_ylim(0.102, 0.130)
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.legend(loc='upper right', fontsize=8)
for k, s in zip(k_vals, sil_vals):
    ax2.annotate(f"{s:.4f}", (k, s), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=7.5, fontweight='bold')

plt.tight_layout()
b64_fig3 = fig_to_base64(fig3)

# ==============================================================================
# FIGURA METODOLÓGICA 4: Centroides Padronizados Z-Score e ANOVA F-Test
# ==============================================================================
fig4, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

features_labels = [
    'Uso de ATS', 'Projetos Ativos', 'Questionários', 'Atividade Principal',
    'Dissem. Decisores', 'Mét. Estatísticos', 'Indicadores', 'Síntese Evidências',
    'Mét. Participativos', 'Parceria Internac.', 'Tamanho Equipe', 'Mét. Qualitativos',
    'Dissem. Sociedade', 'Capacitação Recente'
]
f_stats = [1690.35, 38.14, 36.28, 31.51, 27.03, 26.60, 21.80, 19.72, 17.82, 11.59, 10.77, 8.17, 7.62, 2.24]
z_c1 = [2.49, 0.25, 0.21, 0.03, 0.11, 0.30, 0.19, 0.75, 0.10, 0.17, 0.66, 0.04, -0.10, 0.24]
z_c2 = [-0.34, -0.63, -0.62, -0.57, -0.54, -0.55, -0.50, -0.41, -0.46, -0.38, -0.26, -0.32, -0.28, -0.16]
z_c3 = [-0.40, 0.41, 0.41, 0.42, 0.38, 0.33, 0.33, 0.11, 0.31, 0.24, 0.02, 0.23, 0.24, 0.06]

y_pos = np.arange(len(features_labels))
ax1.plot(z_c1, y_pos, marker='o', color='#2563eb', linewidth=1.8, label='Cluster 1 (ATS)')
ax1.plot(z_c2, y_pos, marker='s', color='#64748b', linewidth=1.8, label='Cluster 2 (Ocasionais)')
ax1.plot(z_c3, y_pos, marker='^', color='#059669', linewidth=1.8, label='Cluster 3 (Núcleo M&A)')
ax1.axvline(0, color='#0f172a', linestyle='--', linewidth=1, alpha=0.7)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(features_labels, fontsize=7.5)
ax1.invert_yaxis()
ax1.set_xlabel('Desvios-Padrão da Média Global (Z-Score)', fontsize=8, fontweight='bold')
ax1.set_title('A. Coordenadas das Centroides Padronizadas (Z-Score)\nDesvio de cada Cluster em relação à Média (z = 0)', fontsize=9, fontweight='bold', color='#0f172a', pad=8)
ax1.grid(axis='x', linestyle='--', alpha=0.4)
ax1.legend(loc='lower right', fontsize=7.5)

log_f = np.log10(f_stats)
colors_f = ['#059669' if f > 5 else '#94a3b8' for f in f_stats]
ax2.barh(y_pos, log_f, color=colors_f, height=0.65, edgecolor='#0f172a', linewidth=0.5)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(features_labels, fontsize=7.5)
ax2.invert_yaxis()
ax2.set_xlabel('log10(Estatística F de Fisher-Snedecor)', fontsize=8, fontweight='bold')
ax2.set_title('B. Poder Discriminante Univariado (Teste ANOVA F)\nImportância Estatística das 14 Variáveis na Clusterização', fontsize=9, fontweight='bold', color='#0f172a', pad=8)
ax2.set_xlim(0, 3.8)
ax2.grid(axis='x', linestyle='--', alpha=0.4)
for i, (lf, fv) in enumerate(zip(log_f, f_stats)):
    sig = "***" if fv > 7 else ("ns" if fv < 3 else "*")
    ax2.text(lf + 0.06, i, f"F = {fv:.1f} ({sig})", va='center', fontsize=7, fontweight='bold', color='#0f172a')

plt.tight_layout()
b64_fig4 = fig_to_base64(fig4)

print("Gráficos metodológicos vetoriais gerados com sucesso.")

# ==============================================================================
# CONSTRUÇÃO DO DOCUMENTO HTML COMPLETO PARA RENDERIZAÇÃO PDF
# ==============================================================================
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório Completo de Metodologia, Métricas e Ferramentas Analíticas (2024)</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    @page {{
      size: A4 portrait;
      margin: 16mm 14mm 18mm 14mm;
    }}

    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}

    body {{
      font-family: 'Inter', sans-serif;
      font-size: 8.8pt;
      line-height: 1.5;
      color: #1e293b;
      margin: 0;
      padding: 0;
      background-color: #ffffff;
    }}

    .page-break {{
      page-break-before: always;
    }}

    .avoid-break {{
      page-break-inside: avoid;
    }}

    /* Cabeçalho da Capa */
    .header-box {{
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: #ffffff;
      padding: 18px 20px;
      border-radius: 10px;
      margin-bottom: 16px;
    }}

    .badge-bar {{
      display: flex;
      gap: 8px;
      margin-bottom: 8px;
    }}

    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 7pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .badge-gold {{ background-color: #f59e0b; color: #0f172a; }}
    .badge-blue {{ background-color: #3b82f6; color: #ffffff; }}
    .badge-green {{ background-color: #10b981; color: #0f172a; }}

    h1 {{
      font-size: 17pt;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      margin: 4px 0 6px 0;
      letter-spacing: -0.4px;
    }}

    .subtitle {{
      font-size: 9.2pt;
      color: #cbd5e1;
      margin: 0;
      font-weight: 400;
      line-height: 1.4;
    }}

    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      background-color: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 9px 12px;
      margin-bottom: 16px;
      font-size: 7.8pt;
    }}

    .meta-item strong {{
      display: block;
      color: #64748b;
      text-transform: uppercase;
      font-size: 6.5pt;
      margin-bottom: 2px;
    }}

    .meta-item span {{
      font-weight: 700;
      color: #0f172a;
    }}

    h2 {{
      font-size: 12pt;
      font-weight: 800;
      color: #0f172a;
      margin: 16px 0 8px 0;
      padding-bottom: 4px;
      border-bottom: 2px solid #1e3a8a;
      letter-spacing: -0.2px;
    }}

    h3 {{
      font-size: 10pt;
      font-weight: 700;
      color: #1e3a8a;
      margin: 12px 0 5px 0;
      background-color: #f1f5f9;
      padding: 4px 8px;
      border-left: 3.5px solid #2563eb;
      border-radius: 0 4px 4px 0;
    }}

    h4 {{
      font-size: 9pt;
      font-weight: 700;
      color: #0f172a;
      margin: 8px 0 4px 0;
    }}

    p {{
      margin: 0 0 8px 0;
      text-align: justify;
    }}

    /* Tabelas */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 12px 0;
      font-size: 7.5pt;
    }}

    th {{
      background-color: #0f172a;
      color: #ffffff;
      font-weight: 600;
      text-align: left;
      padding: 5.5px 7px;
      font-size: 7pt;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      border: 1px solid #0f172a;
    }}

    td {{
      padding: 5px 7px;
      border: 1px solid #e2e8f0;
      color: #334155;
      vertical-align: top;
    }}

    tr:nth-child(even) td {{
      background-color: #f8fafc;
    }}

    .num {{
      text-align: center;
      font-variant-numeric: tabular-nums;
    }}

    /* Caixas de Destaque */
    .callout {{
      border-left: 4px solid #2563eb;
      background-color: #eff6ff;
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      margin: 8px 0 12px 0;
      font-size: 8.2pt;
    }}

    .callout-title {{
      font-weight: 700;
      color: #1d4ed8;
      margin-bottom: 3px;
      font-size: 8.5pt;
    }}

    .callout-green {{
      border-left-color: #059669;
      background-color: #ecfdf5;
    }}
    .callout-green .callout-title {{ color: #047857; }}

    .callout-amber {{
      border-left-color: #d97706;
      background-color: #fffbeb;
    }}
    .callout-amber .callout-title {{ color: #b45309; }}

    .callout-purple {{
      border-left-color: #7c3aed;
      background-color: #f5f3ff;
    }}
    .callout-purple .callout-title {{ color: #6d28d9; }}

    /* Código e Fórmulas Matemáticas */
    .code-block {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 7pt;
      background-color: #0f172a;
      color: #f8fafc;
      padding: 8px 10px;
      border-radius: 6px;
      margin: 6px 0 10px 0;
      white-space: pre-wrap;
      line-height: 1.4;
    }}

    .formula-box {{
      background-color: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-left: 4px solid #0f172a;
      border-radius: 6px;
      padding: 8px 14px;
      margin: 6px 0 10px 0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      color: #0f172a;
      line-height: 1.55;
    }}

    .math {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: #0f172a;
      background-color: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
      font-size: 8pt;
    }}

    .fig-box {{
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 8px;
      background-color: #ffffff;
      margin: 10px 0 14px 0;
      text-align: center;
    }}

    .fig-box img {{
      width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
    }}

    .fig-caption {{
      font-size: 7.5pt;
      color: #475569;
      margin-top: 6px;
      text-align: left;
      padding: 0 4px;
    }}

    .card-grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 8px 0 12px 0;
    }}

    .card-grid-3 {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
      margin: 8px 0 12px 0;
    }}

    .card {{
      background-color: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px 10px;
    }}

    .card-title {{
      font-weight: 700;
      font-size: 8.2pt;
      color: #0f172a;
      margin-bottom: 4px;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 3px;
    }}

    ul, ol {{
      margin: 0 0 8px 0;
      padding-left: 16px;
    }}

    li {{
      margin-bottom: 3px;
    }}
  </style>
</head>
<body>

  <!-- ===================================================================== -->
  <!-- PÁGINA 1: CAPA, ESCOPO, ARQUITETURA E INVENTÁRIO DE FERRAMENTAS       -->
  <!-- ===================================================================== -->
  <div class="header-box">
    <div class="badge-bar">
      <span class="badge badge-gold">Memorial Metodológico &amp; Algorítmico</span>
      <span class="badge badge-blue">Catálogo Mestre de 28 Métricas</span>
      <span class="badge badge-green">Auditoria Reprodutível</span>
    </div>
    <h1>Relatório Completo de Ferramentas, Métodos e Construção de Métricas</h1>
    <p class="subtitle">
      Especificação matemática, engenharia de dados, parametrização estatística e algoritmos de aprendizado de máquina aplicados ao estudo sobre Redes de Monitoramento, Avaliação (M&amp;A) e Políticas Informadas por Evidências (PIE) no Brasil (2024)
    </p>
  </div>

  <div class="meta-grid">
    <div class="meta-item">
      <strong>Motor de Processamento</strong>
      <span>Python 3.12.x (64-bit)</span>
    </div>
    <div class="meta-item">
      <strong>Bibliotecas Científicas</strong>
      <span>pandas, scipy, prince, sklearn</span>
    </div>
    <div class="meta-item">
      <strong>Volume de Dados Brutos</strong>
      <span>1.649 Registros (3 Bases .xlsx)</span>
    </div>
    <div class="meta-item">
      <strong>Semente Determinística</strong>
      <span>random_state = 42 (Fixada)</span>
    </div>
  </div>

  <h2>1. Introdução e Arquitetura do Pipeline Científico</h2>
  <p>
    Este documento constitui o <strong>Memorial Metodológico e Dicionário de Engenharia de Métricas</strong> do estudo sobre a comunidade de Monitoramento e Avaliação (M&amp;A) e Políticas Públicas Informadas por Evidências (PIE) no Brasil. Seu objetivo é documentar com transparência científica absoluta: <strong>(i)</strong> quais ferramentas e bibliotecas computacionais foram empregadas; <strong>(ii)</strong> como os dados brutos das três planilhas originais foram limpos, padronizados e transformados; <strong>(iii)</strong> as equações matemáticas exatas de todas as <strong>28 métricas e indicadores</strong> gerados; e <strong>(iv)</strong> os critérios estatísticos de validação dos modelos multivariados (Pareamento Determinístico, Teoria dos Conjuntos, Testes Qui-Quadrado, Análise de Correspondência Múltipla e Clusterização K-Means++).
  </p>

  <div class="card-grid-3">
    <div class="card">
      <div class="card-title">Camada 1: Ingestão e Saneamento</div>
      <p style="font-size: 7.6pt; margin: 0;">Leitura nativa via <code>openpyxl</code>, decomposição Unicode <code>NFKD</code> para remoção de acentos, saneamento de CPFs (<code>zfill(11)</code>), tratamento de anomalias temporais e winsorização de <em>outliers</em>.</p>
    </div>
    <div class="card">
      <div class="card-title">Camada 2: Modelagem Estatística</div>
      <p style="font-size: 7.6pt; margin: 0;">Record Linkage determinístico em 3 chaves, álgebra de conjuntos, tabelas de contingência (&chi;&sup2; e <em>V</em> de Cramér), decomposição SVD em Matriz de Burt (ACM) e K-Means++ padronizado (Z-Score).</p>
    </div>
    <div class="card">
      <div class="card-title">Camada 3: Compilação Editorial</div>
      <p style="font-size: 7.6pt; margin: 0;">Serialização intermediária em JSON (<code>analise_dados_completa.json</code>) alimentando gráficos Matplotlib (300 DPI), relatórios PDF via Playwright Chromium, Excel de 9 abas, PPTX e Dashboard Web.</p>
    </div>
  </div>

  <h2>2. Ecossistema Tecnológico e Ferramentas Utilizadas</h2>
  <p>
    Cada etapa do trabalho utilizou ferramentas específicas selecionadas pela precisão numérica, reprodutibilidade por código-fonte (<em>Infrastructure as Code</em> para análise de dados) e ausência de edição manual humana sobre tabelas intermediárias:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 18%;">Ferramenta / Pacote</th>
        <th style="width: 14%;">Módulo / Classe</th>
        <th style="width: 40%;">Aplicação Exata na Análise dos Dados</th>
        <th style="width: 28%;">Parâmetros e Especificação Técnica</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Python 3.12</strong></td>
        <td><code>re</code>, <code>unicodedata</code>, <code>json</code></td>
        <td>Normalização lexical, decomposição canônica ASCII, expressões regulares de limpeza de CPF e serialização de estruturas de dados.</td>
        <td>Codificação estrita <code>UTF-8</code>; decomposição <code>NFKD</code> com filtro ASCII.</td>
      </tr>
      <tr>
        <td><strong>pandas 2.2+</strong></td>
        <td><code>DataFrame</code>, <code>crosstab</code>, <code>read_excel</code></td>
        <td>Leitura das 3 planilhas originais, criação de colunas derivadas, agregações por grupo (<code>groupby</code>) e matrizes de contingência.</td>
        <td>Indexação vetorial booleana; tratamento explícito de <code>NaN</code> sem exclusão cega de linhas.</td>
      </tr>
      <tr>
        <td><strong>NumPy 1.26+</strong></td>
        <td><code>ndarray</code>, <code>nan</code>, <code>sqrt</code></td>
        <td>Operações algébricas vetoriais, cálculo do coeficiente <em>V</em> de Cramér e manipulação das matrizes de coordenadas fatoriais.</td>
        <td>Precisão de ponto flutuante de 64 bits (<code>float64</code> / IEEE 754).</td>
      </tr>
      <tr>
        <td><strong>SciPy 1.12+</strong></td>
        <td><code>scipy.stats.chi2_contingency</code>, <code>f_oneway</code></td>
        <td>Testes de independência Qui-Quadrado de Pearson (&chi;&sup2;) nas tabelas cruzadas da Pergunta 3 e teste ANOVA <em>F</em> de Fisher nos clusters.</td>
        <td>Cálculo assintótico exato de graus de liberdade <code>gl = (r-1)(c-1)</code> e valor-<em>p</em> bilateral.</td>
      </tr>
      <tr>
        <td><strong>prince 0.13+</strong></td>
        <td><code>prince.MCA</code></td>
        <td>Análise de Correspondência Múltipla (ACM) sobre a matriz indicadora das variáveis Tempo, Titulação e Função (Pergunta 3).</td>
        <td><code>n_components=2</code> (e espectro total <code>K-Q=11</code>), <code>n_iter=10</code>, SVD, <code>random_state=42</code>.</td>
      </tr>
      <tr>
        <td><strong>scikit-learn 1.4+</strong></td>
        <td><code>StandardScaler</code>, <code>KMeans</code>, <code>silhouette_score</code></td>
        <td>Padronização Z-Score das 14 variáveis de rotina operacional e agrupamento não supervisionado em perfis profissionais (Pergunta 5).</td>
        <td><code>n_clusters=3</code>, inicialização <code>k-means++</code>, <code>n_init=25</code>, <code>max_iter=300</code>, <code>tol=1e-4</code>, <code>random_state=42</code>.</td>
      </tr>
      <tr>
        <td><strong>Matplotlib 3.8+</strong></td>
        <td><code>pyplot</code>, <code>subplots</code></td>
        <td>Renderização dos mapas fatoriais da ACM, gráficos de barras empilhadas, rosca e diagramas de validação estatística.</td>
        <td>Backend não-interativo <code>Agg</code>, exportação em buffer de memória PNG a 220–300 DPI em Base64.</td>
      </tr>
      <tr>
        <td><strong>openpyxl 3.1+</strong></td>
        <td><code>Workbook</code>, <code>PatternFill</code>, <code>Font</code></td>
        <td>Construção da planilha consolidada de 9 abas com estilização corporativa, bordas finas, cabeçalho Navy e larguras automáticas.</td>
        <td>Cabeçalho <code>#0C182B</code>, zebra striping <code>#F8FAFC</code>, congelamento de painel <code>A2</code>.</td>
      </tr>
      <tr>
        <td><strong>python-pptx</strong></td>
        <td><code>Presentation</code>, <code>Inches</code>, <code>Pt</code></td>
        <td>Geração automatizada da apresentação executiva widescreen (16:9) com 10 slides estruturados, tabelas e gráficos.</td>
        <td>Dimensões <code>13.333 x 7.5 in</code>, paleta Navy/Blue/Emerald.</td>
      </tr>
      <tr>
        <td><strong>Playwright</strong></td>
        <td><code>sync_playwright</code> (Chromium)</td>
        <td>Compilação tipográfica de HTML5/CSS3 para documentos PDF A4 vetoriais com cabeçalhos e numeração automática de páginas.</td>
        <td><code>format='A4'</code>, <code>print_background=True</code>, espera <code>networkidle</code>.</td>
      </tr>
      <tr>
        <td><strong>Chart.js &amp; Tailwind</strong></td>
        <td>CDN v4.x / CSS Grid</td>
        <td>Motor gráfico interativo do painel web (<code>painel_analise_evidencias.html</code>) com 7 abas navegáveis e tooltips dinâmicos.</td>
        <td>Gráficos <code>doughnut</code>, <code>bar</code>, <code>scatter</code>; layout responsivo single-file.</td>
      </tr>
    </tbody>
  </table>

  <!-- ===================================================================== -->
  <!-- PÁGINA 2: ENGENHARIA DE DADOS, SANEAMENTO E TRATAMENTO DE ANOMALIAS   -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h2>3. Arquitetura das Bases Brutas e Engenharia de Pré-Processamento</h2>
  <p>
    A primeira etapa metodológica consistiu na auditoria estrutural das três planilhas Excel fornecidas na pasta de trabalho. Como os formulários de inscrição dos eventos e o questionário do survey foram preenchidos manualmente pelos respondentes em plataformas distintas, os dados brutos apresentavam variações de grafia, pontuação, campos duplicados e entradas atípicas (<em>outliers</em>).
  </p>

  <h3>3.1. Mapeamento Estrutural das Fontes Primárias e Colunas Utilizadas</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 24%;">Arquivo Excel Original</th>
        <th style="width: 10%;">Linhas (N)</th>
        <th style="width: 36%;">Colunas Exatas Extraídas no Pipeline</th>
        <th style="width: 30%;">Desafios Técnicos Identificados na Base</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Base 1 (Evento 1):</strong><br><code>Inscritos-Politicas-Publicas-Informadas-por-Evidencias-2024.xlsx</code></td>
        <td class="num"><strong>742</strong></td>
        <td><code>CPF</code>, <code>E-mail</code>, <code>Nome completo</code>, <code>Estado</code>, <code>Esfera de atuação</code>, <code>É profissional da Área de Saúde?</code>, <code>Sexo</code>, <code>Você pretende acompanhar o evento de forma presencial ou online?</code></td>
        <td>CPFs armazenados ora como números inteiros (perdendo zeros à esquerda), ora como strings com pontos/traços; nomes com acentuação variada; 16,9% sem resposta na coluna de modalidade.</td>
      </tr>
      <tr>
        <td><strong>Base 2 (Evento 2):</strong><br><code>Inscritos-Praticas-em-Avaliacao-e-Evidencias-para-Politicas-Publicas-2024.xlsx</code></td>
        <td class="num"><strong>386</strong></td>
        <td><code>CPF</code>, <code>E-mail</code>, <code>Nome completo</code>, <code>Estado</code>, <code>Esfera de atuação</code>, <code>É profissional da Área de Saúde?</code></td>
        <td>Mesma estrutura de chave de identificação do Evento 1, porém sem colunas de sexo ou modalidade presencial/online. Presença de siglas e nomes de estados misturados na coluna <code>Estado</code>.</td>
      </tr>
      <tr>
        <td><strong>Base 3 (Survey Nacional):</strong><br><code>Survey-Escuta-Redes-de-Monitoramento-Avaliacao-Politicas-Publicas.xlsx</code></td>
        <td class="num"><strong>521</strong></td>
        <td><strong>Identificação Dupla:</strong> <code>CPF</code>, <code>CPF2</code>, <code>E-mail para contato</code>, <code>E-mail para contato2</code>, <code>Nome completo</code>, <code>Nome completo2</code>.<br><strong>Analíticas:</strong> 19 colunas de perfil, carreira, metodologias, equipe, disseminação e comentários abertos.</td>
        <td>Roteamento condicional no formulário original gerou <strong>dois blocos de colunas de identificação</strong> (bloco 1 e bloco 2); 295 respondentes anônimos; colunas com caracteres <code>\xa0</code> (<em>non-breaking space</em>) nos títulos; anos de experiência digitados como ano calendário (ex: <code>2018</code>).</td>
      </tr>
    </tbody>
  </table>

  <h3>3.2. Regras Algorítmicas de Saneamento e Transformação de Variáveis</h3>
  <p>
    Para garantir zero perda de informação válida e evitar falsos negativos nos cruzamentos ou distorções nas médias, foram implementadas cinco funções determinísticas de saneamento no script <code>generate_analysis.py</code>:
  </p>

  <ol>
    <li>
      <strong>Normalização Canônica de CPF (<code>norm_cpf</code>):</strong>
      Quando o Excel exporta CPFs numéricos para o Python, um CPF iniciado em zero (ex: <code>01234567890</code>) pode ser lido como float <code>1234567890.0</code> (10 dígitos com sufixo decimal). A função executa:
      <span class="math">digits = re.sub(r'\D', '', str(c).split('.')[0].strip())</span> e, caso não vazio, aplica preenchimento à esquerda <span class="math">digits.zfill(11)</span>, reconstruindo exatamente os 11 dígitos originais.
    </li>
    <li>
      <strong>Normalização Lexical e Fonética de Nomes (<code>norm_str</code>):</strong>
      Converte a string para caixa baixa, aplica decomposição Unicode <span class="math">unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')</span> (transformando <code>"João Cláudio d'Ávila"</code> em <code>"joao claudio davila"</code>), remove qualquer caractere não alfanumérico via <span class="math">re.sub(r'[^a-z0-9 ]', '', s)</span> e colapsa espaços múltiplos em espaço simples.
    </li>
    <li>
      <strong>Fusão dos Blocos Duplos de Identificação do Survey:</strong>
      No Survey, devido à ramificação do questionário entre quem já atuava ou não na área, os dados de identificação estavam divididos entre as colunas <code>CPF</code> e <code>CPF2</code>, <code>E-mail para contato</code> e <code>E-mail para contato2</code>, <code>Nome completo</code> e <code>Nome completo2</code>. Para cada linha <span class="math">i</span> do survey, o algoritmo construiu conjuntos unificados não vazios:
      <div class="formula-box">
        CPFs(i) = {{ norm_cpf(CPF_i), norm_cpf(CPF2_i) }} \ {{ "" }}<br>
        Emails(i) = {{ norm_email(Email_i), norm_email(Email2_i) }} \ {{ "" }}<br>
        Nomes(i) = {{ norm_str(Nome_i), norm_str(Nome2_i) }} \ {{ "" }}
      </div>
      Um respondente <span class="math">i</span> foi classificado como <strong>Identificado</strong> (<span class="math">has_id = True</span>) se e somente se <span class="math">|CPFs(i)| + |Emails(i)| + |Nomes(i)| &gt; 0</span>, resultando em exatos <strong>226 identificados</strong> e <strong>295 anônimos</strong>.
    </li>
    <li>
      <strong>Correção de Anomalias na Variável "Anos de Trabalho com M&amp;A" (<code>clean_years</code>):</strong>
      Na coluna de tempo de atuação (245 respostas não nulas), identificou-se que <strong>4 respondentes</strong> digitaram o ano calendário em que começaram a trabalhar (ex: <code>2014</code>, <code>2018</code>) em vez da duração em anos, e <strong>2 respondentes</strong> inseriram valores numéricos inválidos superiores a 2024. O filtro algorítmico aplicou a regra:
      <div class="formula-box">
        anos_clean(x) = 2024 - x, &nbsp; se 1900 &lt; x &lt; 2025 &nbsp; (4 casos corrigidos com sucesso)<br>
        anos_clean(x) = NaN, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; se x &gt; 100 e fora do intervalo acima &nbsp; (2 casos expurgados &rarr; N = 243 na ACM)<br>
        anos_clean(x) = x, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; se 0 &le; x &le; 100
      </div>
    </li>
    <li>
      <strong>Winsorização (Truncamento de Outliers) e Imputação Mediana no Tamanho de Equipe (<code>equipe_clean</code>):</strong>
      Na pergunta sobre o número médio de pessoas na equipe de M&amp;A, alguns respondentes informaram o efetivo inteiro de sua secretaria/órgão (valores entre 25 e 100 pessoas), o que distorceria severamente a média aritmética e o desvio-padrão no K-Means. Aplicou-se <strong>Winsorização superior no teto de 20,0 pessoas</strong> (<span class="math">min(float(x), 20.0)</span>, afetando 12 casos extremos) e imputação pela mediana (<span class="math">mediana = 4,0</span>) para eventuais valores ausentes ou acima de 100.
    </li>
  </ol>

  <!-- ===================================================================== -->
  <!-- PÁGINA 3: CATÁLOGO MESTRE DE TODAS AS 28 MÉTRICAS DO PROJETO          -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h2>4. Catálogo Mestre das 28 Métricas e Indicadores Calculados</h2>
  <p>
    A tabela abaixo documenta formalmente cada uma das <strong>28 métricas quantitativas</strong> reportadas nos documentos do projeto, apresentando sua fórmula matemática exata, como o numerador e o denominador foram construídos e o valor empírico obtido:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 7%;">Cód.</th>
        <th style="width: 25%;">Nome da Métrica / Indicador</th>
        <th style="width: 31%;">Fórmula Matemática Exata</th>
        <th style="width: 24%;">Construção Operacional (Numerador / Denominador)</th>
        <th style="width: 13%;" class="num">Valor Obtido</th>
      </tr>
    </thead>
    <tbody>
      <!-- BLOCO P1 -->
      <tr>
        <td class="num"><strong>M01</strong></td>
        <td>Universo Total do Survey</td>
        <td><span class="math">N_survey = |df3|</span></td>
        <td>Contagem total de linhas válidas na planilha do Survey.</td>
        <td class="num"><strong>521</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M02</strong></td>
        <td>Subamostra Identificada do Survey</td>
        <td><span class="math">N_id = &sum; I(has_id_i == True)</span></td>
        <td>Respondentes com pelo menos 1 chave preenchida (CPF, E-mail ou Nome nos blocos 1 ou 2).</td>
        <td class="num"><strong>226 (43,38%)</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M03</strong></td>
        <td>Subamostra Anônima do Survey</td>
        <td><span class="math">N_anon = N_survey - N_id</span></td>
        <td>Respondentes sem CPF, E-mail e Nome em ambos os blocos (<span class="math">521 - 226</span>).</td>
        <td class="num"><strong>295 (56,62%)</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M04</strong></td>
        <td>Sobreposição Survey &cap; Eventos</td>
        <td><span class="math">M_any = |S_id &cap; (E_1 &cup; E_2)|</span></td>
        <td>Identificados no Survey pareados por CPF (42), E-mail (+10) ou Nome (+8) em E1 ou E2.</td>
        <td class="num"><strong>60</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M05</strong></td>
        <td>Público Externo do Survey</td>
        <td><span class="math">M_ext = N_id - M_any</span></td>
        <td>Respondentes identificados no Survey ausentes tanto de E1 quanto de E2 (<span class="math">226 - 60</span>).</td>
        <td class="num"><strong>166</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M06</strong></td>
        <td>Taxa de Externalidade (s/ Identif.)</td>
        <td><span class="math">T_ext = (M_ext / N_id) &times; 100</span></td>
        <td>Razão entre os 166 externos e os 226 respondentes identificados (<span class="math">166 / 226</span>).</td>
        <td class="num"><strong>73,45%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M07</strong></td>
        <td>Taxa de Presença em Eventos (s/ Id.)</td>
        <td><span class="math">T_pres_id = (M_any / N_id) &times; 100</span></td>
        <td>Razão entre os 60 presentes em eventos e os 226 identificados (<span class="math">60 / 226</span>).</td>
        <td class="num"><strong>26,55%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M08</strong></td>
        <td>Taxa de Presença s/ Survey Total</td>
        <td><span class="math">T_pres_tot = (M_any / N_survey) &times; 100</span></td>
        <td>Limite inferior conservador sobre todo o survey (<span class="math">60 / 521</span>).</td>
        <td class="num"><strong>11,52%</strong></td>
      </tr>
      <!-- BLOCO P2 -->
      <tr>
        <td class="num"><strong>M09</strong></td>
        <td>Inscrições Brutas Combinadas</td>
        <td><span class="math">N_bruto = |E_1| + |E_2|</span></td>
        <td>Soma direta dos inscritos no Evento 1 (742) e no Evento 2 (386).</td>
        <td class="num"><strong>1.128</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M10</strong></td>
        <td>Sobreposição Entre Eventos (Recorrentes)</td>
        <td><span class="math">S_ev = |E_1 &cap; E_2|</span></td>
        <td>Inscritos do Evento 2 pareados no Evento 1 por CPF (40 exatos, s/ falsos positivos).</td>
        <td class="num"><strong>40</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M11</strong></td>
        <td>Comunidade Única de Eventos</td>
        <td><span class="math">|U| = |E_1| + |E_2| - |E_1 &cap; E_2|</span></td>
        <td>Princípio da Inclusão-Exclusão para deduplicação de indivíduos (<span class="math">742 + 386 - 40</span>).</td>
        <td class="num"><strong>1.088</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M12</strong></td>
        <td>Novos Profissionais Atraídos no E2</td>
        <td><span class="math">|N_2| = |E_2 \ E_1| = |E_2| - S_ev</span></td>
        <td>Participantes inéditos captados no segundo evento (<span class="math">386 - 40</span>).</td>
        <td class="num"><strong>346</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M13</strong></td>
        <td>Taxa de Renovação no Evento 2</td>
        <td><span class="math">T_renov = (|N_2| / |E_2|) &times; 100</span></td>
        <td>Proporção de estreantes dentro da audiência do Evento 2 (<span class="math">346 / 386</span>).</td>
        <td class="num"><strong>89,64%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M14</strong></td>
        <td>Taxa de Recorrência no Evento 2</td>
        <td><span class="math">T_rec_E2 = (S_ev / |E_2|) &times; 100</span></td>
        <td>Complemento da renovação no Evento 2 (<span class="math">40 / 386</span>).</td>
        <td class="num"><strong>10,36%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M15</strong></td>
        <td>Taxa de Retenção do Evento 1 no E2</td>
        <td><span class="math">T_ret_E1 = (S_ev / |E_1|) &times; 100</span></td>
        <td>Fração do público do Evento 1 que retornou no Evento 2 (<span class="math">40 / 742</span>).</td>
        <td class="num"><strong>5,39%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M16</strong></td>
        <td>Taxa de Recorrência Global</td>
        <td><span class="math">T_rec_glob = (S_ev / |U|) &times; 100</span></td>
        <td>Índice de Jaccard percentual sobre a comunidade única (<span class="math">40 / 1.088</span>).</td>
        <td class="num"><strong>3,68%</strong></td>
      </tr>
      <!-- BLOCO P3 -->
      <tr>
        <td class="num"><strong>M17</strong></td>
        <td>Estatística &chi;&sup2; e <em>V</em> de Cramér</td>
        <td><span class="math">&chi;&sup2; = &sum; (O_ij - E_ij)&sup2;/E_ij</span><br><span class="math">V = &radic;(&chi;&sup2; / [N &middot; min(r-1, c-1)])</span></td>
        <td>Associação entre Titulação (5 nívs.) e Função (4 nívs.) em <span class="math">N = 243</span> (<span class="math">gl = 12</span>).</td>
        <td class="num"><strong>&chi;&sup2; = 70,06<br>V = 0,3100</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M18</strong></td>
        <td>Inércia Explicada no Plano ACM</td>
        <td><span class="math">I_12 = [(&lambda;_1 + &lambda;_2) / &sum;&lambda;_k] &times; 100</span></td>
        <td>Soma dos 2 maiores autovalores (<span class="math">0,553 + 0,422 = 0,975</span>) dividida pela inércia total (<span class="math">3,667</span>).</td>
        <td class="num"><strong>26,59%</strong></td>
      </tr>
      <!-- BLOCO P4 -->
      <tr>
        <td class="num"><strong>M19</strong></td>
        <td>Concentração Geográfica no DF</td>
        <td><span class="math">P_DF = (N_DF / N_bruto) &times; 100</span></td>
        <td>Inscrições originárias do Distrito Federal sobre o total combinado (<span class="math">513 / 1.128</span>).</td>
        <td class="num"><strong>45,48%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M20</strong></td>
        <td>Participação da Esfera Federal</td>
        <td><span class="math">P_Fed = (N_Fed / N_bruto) &times; 100</span></td>
        <td>Inscrições vinculadas ao Poder Público Federal sobre o total (<span class="math">487 / 1.128</span>).</td>
        <td class="num"><strong>43,17%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M21</strong></td>
        <td>Prevalência Global da Saúde</td>
        <td><span class="math">P_Saude = (N_Saude / N_bruto) &times; 100</span></td>
        <td>Profissionais que responderam "Sim" para atuação em Saúde (<span class="math">557 / 1.128</span>).</td>
        <td class="num"><strong>49,38%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M22</strong></td>
        <td>Prevalência da Saúde por Esfera (e)</td>
        <td><span class="math">Prev(Saude | e) = (Saude_e / Total_e) &times; 100</span></td>
        <td>Condicional por esfera: Municipal (<span class="math">64/95</span>), Estadual (<span class="math">123/220</span>), Federal (<span class="math">210/487</span>).</td>
        <td class="num"><strong>Mun: 67,37%<br>Est: 55,91%<br>Fed: 43,12%</strong></td>
      </tr>
      <!-- BLOCO P5 E INSIGHTS -->
      <tr>
        <td class="num"><strong>M23</strong></td>
        <td>Padronização Z-Score (14 vars.)</td>
        <td><span class="math">z_ij = (x_ij - &mu;_j) / &sigma;_j</span></td>
        <td>Centragem na média amostral <span class="math">&mu;_j</span> e divisão pelo desvio-padrão populacional <span class="math">&sigma;_j</span> (<span class="math">N=245</span>).</td>
        <td class="num"><strong>&mu;=0, &sigma;=1</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M24</strong></td>
        <td>Proporção dos 3 Clusters K-Means</td>
        <td><span class="math">P_Ck = (|C_k| / 245) &times; 100</span></td>
        <td>Partição ótima em <span class="math">k=3</span>: C1 (<span class="math">32/245</span>), C2 (<span class="math">91/245</span>), C3 (<span class="math">122/245</span>).</td>
        <td class="num"><strong>C1: 13,06%<br>C2: 37,14%<br>C3: 49,80%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M25</strong></td>
        <td>Taxa de Interiorização Online (Fora DF)</td>
        <td><span class="math">T_on_fora = Online_fora / Declarados_fora</span></td>
        <td>No Evento 1, residentes fora do DF que declararam modalidade: <span class="math">291 / (291 + 44)</span> (ou <span class="math">68,1%</span> do total c/ missings).</td>
        <td class="num"><strong>86,87%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M26</strong></td>
        <td>Abismo da Comunicação Pública</td>
        <td><span class="math">&Delta;_com = P_decisores - P_sociedade</span></td>
        <td>Diferença entre quem divulga p/ decisores (<span class="math">180/245 = 73,47%</span>) e p/ público geral (<span class="math">81/245 = 33,06%</span>).</td>
        <td class="num"><strong>40,41 p.p.</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M27</strong></td>
        <td>Proporção Feminina (Eventos e Survey)</td>
        <td><span class="math">P_fem = Mulheres / Declarados_genero</span></td>
        <td>Evento 1 (<span class="math">447 / 742 = 60,24%</span>); Survey ativo (<span class="math">154 / 245 = 62,86%</span>); Cluster 1 ATS (<span class="math">24 / 32 = 75,00%</span>).</td>
        <td class="num"><strong>60,2% a 75,0%</strong></td>
      </tr>
      <tr>
        <td class="num"><strong>M28</strong></td>
        <td>Índice de Estratificação Racial</td>
        <td><span class="math">P(Raca_r | Cluster_k)</span></td>
        <td>Proporção racial intracluster: Brancos no C3 (<span class="math">87/122 = 71,31%</span>) vs. Pardos no C2 (<span class="math">31/91 = 34,07%</span>).</td>
        <td class="num"><strong>C3 Br: 71,3%<br>C2 Pd: 34,1%</strong></td>
      </tr>
    </tbody>
  </table>

  <!-- ===================================================================== -->
  <!-- PÁGINA 4: DETALHAMENTO DOS MÉTODOS P1 E P2 + FIGURA METODOLÓGICA 1    -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h2>5. Detalhamento Passo a Passo dos Métodos Estatísticos e Algorítmicos</h2>

  <h3>5.1. Método da Pergunta 1: Resolução Determinística de Entidades em Cascata (Record Linkage)</h3>
  <p>
    Para verificar se os respondentes do Survey (<span class="math">N = 521</span>) eram as mesmas pessoas que participaram do Evento 1 (<span class="math">N = 742</span>) e do Evento 2 (<span class="math">N = 386</span>), não era possível realizar um simples <code>JOIN</code> de banco de dados por chave única, pois: <strong>(a)</strong> 295 respondentes do survey permaneceram anônimos; <strong>(b)</strong> entre os 226 respondentes que se identificaram, alguns preencheram apenas o e-mail e o nome (deixando o CPF em branco); e <strong>(c)</strong> alguns profissionais inscreveram-se no evento com e-mail institucional (ex: <code>@saude.gov.br</code>) e responderam ao survey com e-mail pessoal (ex: <code>@gmail.com</code>).
  </p>
  <p>
    <strong>Como foi resolvido:</strong> Desenvolveu-se um algoritmo de <strong>Pareamento Determinístico Hierárquico de 3 Camadas</strong> usando conjuntos hash (<span class="math">O(1)</span> de complexidade de busca). Para cada indivíduo identificado <span class="math">i</span>, o pareamento é verdadeiro se ocorrer intersecção em pelo menos uma das três camadas:
  </p>

  <div class="formula-box">
    Match(i, Evento_k) = TRUE &nbsp; &hArr; &nbsp; [ CPFs(i) &cap; CPFs(E_k) &ne; &empty; ] &nbsp; &or; &nbsp; [ Emails(i) &cap; Emails(E_k) &ne; &empty; ] &nbsp; &or; &nbsp; [ Nomes(i) &cap; Nomes(E_k) &ne; &empty; ]
  </div>

  <div class="fig-box avoid-break">
    <img src="{b64_fig1}" alt="Cascata de Resolução de Entidades">
    <div class="fig-caption">
      <strong>Figura Metodológica 1:</strong> Auditoria de eficácia de cada camada do pareamento determinístico. Na Pergunta 1 (painel A), um cruzamento restrito ao CPF capturaria apenas 42 respostas; a adição da Camada 2 (E-mail) resgatou +10 respostas (16,7%) e a Camada 3 (Nome composto s/ conflito de CPF) resgatou +8 respostas (13,3%), totalizando 60 respostas (57 indivíduos únicos). Na Pergunta 2 (painel B), 100% (40 de 40) foram pareados diretamente na Camada 1 (CPF), e a trava anti-conflito de CPF bloqueou 2 falsos positivos nominais (<code>"Não se aplica"</code> e o pré-nome isolado <code>"Marta"</code>).
    </div>
  </div>

  <div class="callout callout-purple">
    <div class="callout-title">Auditoria de Inconsistências do Survey: Funil de Elegibilidade e Respostas Duplicadas (Pergunta 1)</div>
    Seja <span class="math">N_total = 521</span> o total de acessos ao survey, dividido em <span class="math">N_id = 226</span> respostas identificadas e <span class="math">N_sem_id = 295</span> registros sem identificação. A auditoria das colunas de filtro revelou duas descobertas fundamentais:<br>
    &bull; <strong>1. Decomposição dos 295 sem identificação:</strong> <strong>276 acessos</strong> foram encerrados nas perguntas-filtro iniciais (1 recusou o TCLE, 85 declararam <em>"Não atuo na área"</em> e 190 não possuíam publicação nos últimos 8 anos). Apenas <strong>19 respondentes (7,76% dos 245 elegíveis)</strong> concluíram o questionário de forma genuinamente anônima, elevando a taxa real de identificação entre os elegíveis para <strong>92,24% (226 de 245)</strong>.<br>
    &bull; <strong>2. Deduplicação de 8 respondentes que enviaram o Survey duas vezes:</strong> As 226 respostas identificadas correspondem a <strong>218 indivíduos únicos</strong> (8 profissionais submeteram o formulário em duplicidade). Calculando por respostas (<span class="math">N=226</span>), são <strong>60 em eventos (26,55%)</strong> e <strong>166 externos (73,45%)</strong>; calculando por indivíduos únicos (<span class="math">N=218</span>), são <strong>57 em eventos (26,15%)</strong> e <strong>161 externos (73,85%)</strong>.
  </div>

  <h3>5.2. Método da Pergunta 2: Teoria dos Conjuntos, Trava Anti-Conflito de CPF e Decomposição Longitudinal</h3>
  <p>
    Para mensurar a recorrência versus renovação entre o Evento 1 (<span class="math">E_1</span>, realizado primeiro, com foco em Políticas Informadas por Evidências) e o Evento 2 (<span class="math">E_2</span>, realizado em seguida, com foco em Práticas em Avaliação), modelou-se o sistema como uma trajetória discreta de conjuntos finitos. Aplicou-se uma <strong>trava de integridade documental</strong>: dois registros que possuam CPFs válidos e diferentes jamais podem ser pareados por nome ou e-mail, exigindo-se ainda nome composto (&ge; 2 palavras) e exclusão de placeholders como <code>"Não se aplica"</code>:
  </p>

  <div class="card-grid-2 avoid-break">
    <div class="card">
      <div class="card-title">1. Cardinalidades Primárias e Interseção Auditada</div>
      <ul style="font-size: 7.8pt; margin-bottom: 0;">
        <li>Conjunto Evento 1: <span class="math">|E_1| = 742</span> participantes (0 duplicatas internas).</li>
        <li>Conjunto Evento 2: <span class="math">|E_2| = 386</span> participantes (0 duplicatas internas).</li>
        <li>Interseção (Recorrentes em ambos): <span class="math">|S| = |E_1 &cap; E_2| = 40</span> (100% via CPF).</li>
        <li>Exclusivos do Evento 1: <span class="math">|E_1 \ E_2| = 742 - 40 = 702</span>.</li>
        <li>Exclusivos / Novos no Evento 2: <span class="math">|N_2| = |E_2 \ E_1| = 386 - 40 = 346</span>.</li>
        <li>União (Indivíduos Únicos): <span class="math">|U| = |E_1 &cup; E_2| = 702 + 346 + 40 = 1.088</span>.</li>
      </ul>
    </div>
    <div class="card">
      <div class="card-title">2. Quatro Taxas com Denominadores Distintos</div>
      <ul style="font-size: 7.8pt; margin-bottom: 0;">
        <li><strong>Taxa de Renovação do E2:</strong> <span class="math">|N_2| / |E_2| = 346 / 386 = 89,64%</span> (mede a capacidade do 2º evento de atrair público inédito).</li>
        <li><strong>Taxa de Recorrência no E2:</strong> <span class="math">|S| / |E_2| = 40 / 386 = 10,36%</span> (fração da plateia do E2 que veio do E1).</li>
        <li><strong>Taxa de Retenção do E1:</strong> <span class="math">|S| / |E_1| = 40 / 742 = 5,39%</span> (fração da plateia do E1 que retornou no E2).</li>
        <li><strong>Índice de Jaccard (Recorrência Global):</strong> <span class="math">J(E_1, E_2) = |E_1 &cap; E_2| / |E_1 &cup; E_2| = 40 / 1.088 = 3,68%</span>.</li>
      </ul>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- PÁGINA 5: MÉTODO DA PERGUNTA 3 (ACM E QUI-QUADRADO) + FIGURA 2        -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h3>5.3. Método da Pergunta 3: Testes &chi;&sup2;, V de Cramér e Análise de Correspondência Múltipla (ACM)</h3>
  <p>
    A Pergunta 3 investigou a relação estrutural entre três variáveis categóricas do Survey (<span class="math">N = 243</span> registros completos após saneamento): <strong>(1) Faixa de Tempo de Atuação em M&amp;A</strong> (<span class="math">K_1 = 5</span> categorias ordinais: Até 2 anos, 3 a 5 anos, 6 a 10 anos, 11 a 20 anos, Mais de 20 anos); <strong>(2) Grau de Titulação Acadêmica</strong> (<span class="math">K_2 = 5</span> categorias: Graduação/Médio, Especialização, Mestrado, Doutorado, Pós-doutorado); e <strong>(3) Função Principal Exercida</strong> (<span class="math">K_3 = 4</span> categorias: Pesquisador(a), Gestor(a), Técnico(a) em M&amp;A, Gerente).
  </p>

  <h4>Etapa A: Testes de Independência Bivariada Qui-Quadrado (&chi;&sup2;) e Magnitude de Efeito (V de Cramér)</h4>
  <p>
    Para cada par de variáveis categóricas, construiu-se a tabela de contingência de contagens observadas <span class="math">O_ij</span> e calcularam-se as frequências esperadas sob a hipótese nula de independência (<span class="math">E_ij = (R_i &times; C_j) / N</span>), a estatística <span class="math">&chi;&sup2;</span> de Pearson e o índice <span class="math">V</span> de Cramér (que normaliza o <span class="math">&chi;&sup2;</span> para o intervalo <span class="math">[0, 1]</span> independentemente do tamanho amostral e das dimensões da tabela):
  </p>

  <table>
    <thead>
      <tr>
        <th>Par de Variáveis Cruzadas</th>
        <th class="num">Dimensão (r &times; c)</th>
        <th class="num">Graus de Liberdade (gl)</th>
        <th class="num">Estatística &chi;&sup2;</th>
        <th class="num">Valor-p (p-value)</th>
        <th class="num">V de Cramér</th>
        <th>Decisão Estatística (&alpha; = 0,05)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Titulação Acadêmica &times; Função Principal</strong></td>
        <td class="num">5 &times; 4</td>
        <td class="num">12</td>
        <td class="num"><strong>70,06</strong></td>
        <td class="num"><strong>3,12 &times; 10<sup>-10</sup></strong></td>
        <td class="num"><strong>0,3100</strong></td>
        <td><strong>Altamente Significante</strong> (Forte associação estrutural)</td>
      </tr>
      <tr>
        <td><strong>Faixa de Tempo &times; Titulação Acadêmica</strong></td>
        <td class="num">5 &times; 5</td>
        <td class="num">16</td>
        <td class="num"><strong>46,02</strong></td>
        <td class="num"><strong>9,67 &times; 10<sup>-5</sup></strong></td>
        <td class="num"><strong>0,2176</strong></td>
        <td><strong>Altamente Significante</strong> (Progressão acadêmica temporal)</td>
      </tr>
      <tr>
        <td><strong>Faixa de Tempo &times; Função Principal</strong></td>
        <td class="num">5 &times; 4</td>
        <td class="num">12</td>
        <td class="num">17,86</td>
        <td class="num">0,1201</td>
        <td class="num">0,1565</td>
        <td>Não significante isoladamente (Efeito mediado pela titulação)</td>
      </tr>
    </tbody>
  </table>

  <h4>Etapa B: Formulação Algébrica da Análise de Correspondência Múltipla (ACM)</h4>
  <p>
    Seja <span class="math">Q = 3</span> o número de variáveis categóricas e <span class="math">K = K_1 + K_2 + K_3 = 5 + 5 + 4 = 14</span> o número total de categorias (modalidades). O algoritmo <code>prince.MCA</code> transforma a base <span class="math">N &times; Q</span> (<span class="math">243 &times; 3</span>) na <strong>Matriz Indicadora Disjuntiva Completa</strong> <span class="math">Z</span> de dimensão <span class="math">243 &times; 14</span> (codificação <em>One-Hot</em> binária <span class="math">0/1</span>), onde cada linha soma exatamente <span class="math">Q = 3</span>, e a soma total da matriz é <span class="math">N &middot; Q = 729</span>.
  </p>
  <p>
    Define-se a matriz de probabilidades relativas <span class="math">P = Z / (N &middot; Q)</span>, o vetor de massas das linhas <span class="math">r = P &middot; 1_K</span> (onde <span class="math">r_i = 1/N</span>), o vetor de massas das colunas <span class="math">c = P^T &middot; 1_N</span> e as matrizes diagonais <span class="math">D_r = diag(r)</span> e <span class="math">D_c = diag(c)</span>. A ACM executa a <strong>Decomposição em Valores Singulares (SVD)</strong> da matriz de resíduos padronizados <span class="math">S</span>:
  </p>

  <div class="formula-box">
    S = D_r<sup>-1/2</sup> (P - r c<sup>T</sup>) D_c<sup>-1/2</sup> = U &Delta; V<sup>T</sup> &nbsp;&nbsp;&rArr;&nbsp;&nbsp; Autovalores (Inércias): &lambda;_k = &delta;_k<sup>2</sup> &nbsp;&nbsp;|&nbsp;&nbsp; Coordenadas das Categorias: G = D_c<sup>-1/2</sup> V &Delta;
  </div>

  <p>
    O número total de dimensões fatoriais não-triviais é <span class="math">M = K - Q = 14 - 3 = 11</span>, e a inércia total teórica da nuvem é <span class="math">I_total = (K - Q) / Q = 11 / 3 = 3,6667</span>. Os dois primeiros eixos ortogonais (<span class="math">&lambda;_1 = 0,553</span> e <span class="math">&lambda;_2 = 0,422</span>) retêm <strong>26,59% da inércia total</strong>, sintetizando a estrutura latente em um mapa bidimensional:
  </p>

  <div class="fig-box avoid-break">
    <img src="{b64_fig2}" alt="Scree Plot ACM e Testes Qui-Quadrado">
    <div class="fig-caption">
      <strong>Figura Metodológica 2:</strong> No painel A, o Scree Plot exibe os 11 autovalores extraídos pela decomposição SVD da Matriz de Burt, destacando as Dimensões 1 (15,07%) e 2 (11,52%) utilizadas no mapa perceptual. No painel B, observa-se a magnitude da associação qui-quadrado e o índice V de Cramér para os três cruzamentos bivariados.
    </div>
  </div>

  <div class="avoid-break">
    <h4>Tabela Completa das Coordenadas Fatoriais Principais das 14 Categorias na ACM</h4>
    <table>
      <thead>
        <tr>
          <th>Variável Original</th>
          <th>Categoria / Modalidade</th>
          <th class="num">Coordenada Dim 1 (15,07%)</th>
          <th class="num">Coordenada Dim 2 (11,52%)</th>
          <th>Polo Estrutural e Interpretação Geométrica no Plano Cartesiano</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>Titulação</strong></td><td>Pós-doutorado</td><td class="num"><strong>-1,1683</strong></td><td class="num">+0,2388</td><td>Polo Acadêmico-Sênior Extremo (Esquerda)</td></tr>
        <tr><td><strong>Titulação</strong></td><td>Doutorado</td><td class="num"><strong>-0,4911</strong></td><td class="num">+0,4073</td><td>Polo Acadêmico-Sênior Consolidado (Esquerda)</td></tr>
        <tr><td><strong>Titulação</strong></td><td>Mestrado</td><td class="num"><strong>+0,6926</strong></td><td class="num">+0,5149</td><td>Polo Governamental-Executivo Qualificado (Direita Superior)</td></tr>
        <tr><td><strong>Titulação</strong></td><td>Graduação/Médio</td><td class="num"><strong>+0,7737</strong></td><td class="num">-1,2437</td><td>Polo Operacional de Entrada (Direita Inferior)</td></tr>
        <tr><td><strong>Titulação</strong></td><td>Especialização</td><td class="num"><strong>+1,1132</strong></td><td class="num">-1,3283</td><td>Polo Técnico-Burocrático Aplicado (Direita Inferior)</td></tr>
        <tr><td><strong>Função Principal</strong></td><td>Pesquisador(a)</td><td class="num"><strong>-0,7574</strong></td><td class="num">+0,1649</td><td>Associado diretamente a Doutorado e Pós-doutorado</td></tr>
        <tr><td><strong>Função Principal</strong></td><td>Técnico(a) em M&amp;A</td><td class="num"><strong>+0,3015</strong></td><td class="num">-0,9566</td><td>Associado à prática operacional e especialização</td></tr>
        <tr><td><strong>Função Principal</strong></td><td>Gestor(a)</td><td class="num"><strong>+0,6048</strong></td><td class="num">-0,1673</td><td>Associado à condução cotidiana de programas públicos</td></tr>
        <tr><td><strong>Função Principal</strong></td><td>Gerente</td><td class="num"><strong>+0,3786</strong></td><td class="num"><strong>+2,7502</strong></td><td>Isolado na Dimensão Vertical Superior (Chefia/Direção)</td></tr>
        <tr><td><strong>Faixa de Tempo</strong></td><td>5. Mais de 20 anos</td><td class="num"><strong>-0,8482</strong></td><td class="num">-1,1549</td><td>Alta senioridade histórica</td></tr>
        <tr><td><strong>Faixa de Tempo</strong></td><td>4. De 11 a 20 anos</td><td class="num"><strong>-0,7256</strong></td><td class="num">+0,2241</td><td>Senioridade madura fortemente alinhada a Doutores/Pesquisadores</td></tr>
        <tr><td><strong>Faixa de Tempo</strong></td><td>3. De 6 a 10 anos</td><td class="num">+0,1026</td><td class="num">+0,4613</td><td>Transição intermediária rumo à coordenação/mestrado</td></tr>
        <tr><td><strong>Faixa de Tempo</strong></td><td>2. De 3 a 5 anos</td><td class="num">+0,3779</td><td class="num">-0,2265</td><td>Consolidação técnica na gestão</td></tr>
        <tr><td><strong>Faixa de Tempo</strong></td><td>1. Até 2 anos</td><td class="num"><strong>+1,1213</strong></td><td class="num">-0,5354</td><td>Recém-ingressos no ecossistema governamental</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ===================================================================== -->
  <!-- PÁGINA 6: MÉTODO DA PERGUNTA 4 E INÍCIO DA PERGUNTA 5 (K-MEANS)       -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h3>5.4. Método da Pergunta 4: Geoprocessamento Tabular, Tokenização Multirresposta e Razão de Prevalência</h3>
  <p>
    A Pergunta 4 exigiu a integração espacial e institucional dos dois eventos (<span class="math">N = 1.128</span> inscrições combinadas) e a mineração das áreas temáticas de políticas públicas no Survey:
  </p>
  <ol>
    <li>
      <strong>Dicionário Heurístico de Padronização de UF (<code>norm_uf</code>):</strong>
      Mapeou entradas heterogêneas (como <code>"Brasília"</code>, <code>"Distrito Federal"</code>, <code>"DF"</code>, <code>"São Paulo - SP"</code>) para as 27 siglas oficiais da federação e agregou-as nas 5 macrorregiões do IBGE (Centro-Oeste: 560; Sudeste: 270; Nordeste: 138; Sul: 73; Norte: 67; Outros/Não Inf.: 20).
    </li>
    <li>
      <strong>Análise Condicional de Prevalência da Saúde por Esfera (<code>ct_esfera_saude</code>):</strong>
      Construiu-se a matriz de contingência entre <code>Esfera de atuação</code> e <code>É profissional da Área de Saúde?</code>. Para testar a hipótese de assimetria federativa, calculou-se a probabilidade condicional <span class="math">P(Saude = Sim | Esfera = e)</span> e a <strong>Razão de Prevalência (<span class="math">RP</span>)</strong> tendo a Esfera Federal como referência basal (<span class="math">43,12%</span>):
      <div class="formula-box">
        P(Saúde | Municipal) = 64 / 95 = 67,37% &nbsp; &rArr; &nbsp; RP_Mun/Fed = 67,37% / 43,12% = 1,56x (56% mais concentrada na Saúde)<br>
        P(Saúde | Estadual) &nbsp;= 123 / 220 = 55,91% &nbsp; &rArr; &nbsp; RP_Est/Fed = 55,91% / 43,12% = 1,30x (30% mais concentrada na Saúde)<br>
        P(Saúde | Federal) &nbsp;&nbsp;= 210 / 487 = 43,12% &nbsp; &rArr; &nbsp; Referência Basal (1,00x - Alta diversificação multissetorial)
      </div>
    </li>
    <li>
      <strong>Tokenização de Variáveis Multirresposta no Survey (<code>tematicas_counts</code>):</strong>
      No Survey, a questão sobre áreas temáticas permitia marcação múltipla separada por ponto-e-vírgula (ex: <code>"Saúde;Educação;Assistência social;"</code>). O algoritmo percorreu todas as respostas não nulas aplicando tokenização <span class="math">[p.strip() for p in item.split(';') if p.strip()]</span>, contabilizando a frequência marginal absoluta de cada política pública (Saúde: 134 menções; Educação: 115; Assistência Social: 60; Meio Ambiente: 51; Cultura: 25; Segurança: 22; Habitação: 19; Esporte: 14).
    </li>
  </ol>

  <h3>5.5. Método da Pergunta 5: Aprendizado Não Supervisionado via K-Means++ em Espaço 14-Dimensional</h3>
  <p>
    Para identificar os perfis reais de profissionais segundo suas atribuições cotidianas (<span class="math">N = 245</span> respondentes ativos em M&amp;A), aplicou-se o algoritmo de agrupamento <strong>K-Means com inicialização probabilística K-Means++</strong> (Arthur &amp; Vassilvitskii, 2007).
  </p>

  <h4>Etapa A: Engenharia de Features (Vetorização das 14 Variáveis Operacionais)</h4>
  <p>
    Cada respondente <span class="math">i &in; {{1, ..., 245}}</span> foi representado por um vetor <span class="math">x_i &in; &real;<sup>14</sup></span>. Treze variáveis categóricas/multirresposta foram convertidas em variáveis binárias indicadoras (<span class="math">0</span> ou <span class="math">1</span>) via busca de sub-strings normalizadas, e uma variável contínua (tamanho da equipe) foi winsorizada em <span class="math">20,0</span>.
  </p>

  <h4>Etapa B: Por que a Padronização Z-Score (StandardScaler) foi Indispensável?</h4>
  <p>
    O algoritmo K-Means minimiza a Soma dos Quadrados Intra-Cluster (<em>Within-Cluster Sum of Squares — WCSS</em>), baseada na distância euclidiana quadrática <span class="math">||z_i - &mu;_k||<sup>2</sup></span>. Nas variáveis brutas, a variável <code>tam_equipe</code> varia de <span class="math">1</span> a <span class="math">20</span> (variância <span class="math">&sigma;<sup>2</sup> = 22,09</span>), enquanto as 13 variáveis binárias variam apenas entre <span class="math">0</span> e <span class="math">1</span> (variância máxima <span class="math">&sigma;<sup>2</sup> &le; 0,25</span>). Sem padronização, <code>tam_equipe</code> representaria mais de <strong>87% de toda a distância euclidiana</strong>, reduzindo o agrupamento a uma mera divisão por tamanho de equipe. A transformação Z-Score equalizou todas as 14 dimensões para média <span class="math">0</span> e variância unitária <span class="math">1</span>:
  </p>

  <div class="formula-box">
    z_ij = (x_ij - &mu;_j) / &sigma;_j &nbsp;&nbsp;&nbsp;&rArr;&nbsp;&nbsp;&nbsp; Objetivo K-Means: &nbsp; argmin_C &sum;<sub>k=1</sub><sup>K</sup> &sum;<sub>z_i &in; C_k</sub> &sum;<sub>j=1</sub><sup>14</sup> (z_ij - c_kj)<sup>2</sup>
  </div>

  <h4>Etapa C: Critérios Matemáticos de Seleção do Número Ótimo de Clusters (k = 3)</h4>
  <p>
    O algoritmo foi executado para <span class="math">k &in; {{2, 3, 4, 5, 6}}</span> com <span class="math">25</span> reinicializações independentes (<code>n_init=25</code>). A escolha de <span class="math">k = 3</span> foi confirmada simultaneamente pela inflexão do WCSS e pelo <strong>Máximo Global do Coeficiente de Silhueta</strong> (<span class="math">S = 0,1235</span>):
  </p>

  <div class="fig-box avoid-break">
    <img src="{b64_fig3}" alt="Validação K-Means WCSS e Silhueta">
    <div class="fig-caption">
      <strong>Figura Metodológica 3:</strong> Curvas de validação matemática do modelo K-Means++. No painel A, a curva WCSS apresenta queda acentuada até k=3 (2.767,55). No painel B, o Coeficiente de Silhueta atinge seu pico máximo global exatamente em k=3 (0,1235), caindo abruptamente em k=4 (0,1109) e k=5 (0,1079), comprovando que 3 clusters é a partição natural dos dados.
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- PÁGINA 7: TABELA COMPLETA DAS 14 VARIÁVEIS DO K-MEANS E FIGURA 4      -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h4>Etapa D: Auditoria Estatística Completa das 14 Variáveis nos 3 Clusters (Médias, Z-Scores e ANOVA F-Test)</h4>
  <p>
    Para comprovar que os 3 clusters encontrados diferem significativamente nas dimensões avaliadas, aplicou-se o teste paramétrico de <strong>Análise de Variância Unidirecional (ANOVA F-Test de Fisher-Snedecor)</strong> para cada uma das 14 variáveis entre os grupos <span class="math">C_1, C_2, C_3</span>. A tabela abaixo exibe os parâmetros de padronização (<span class="math">&mu;_j, &sigma;_j</span>), as médias em escala original, as coordenadas exatas das centroides em Z-Score e o resultado do teste <span class="math">F</span>:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 19%;">Variável Operacional (Código)</th>
        <th class="num" style="width: 11%;">Parâmetros<br>(&mu; | &sigma;)</th>
        <th class="num" style="width: 16%;">Cluster 1: ATS<br>(N=32 | 13,1%)<br>Média | [Z-Score]</th>
        <th class="num" style="width: 17%;">Cluster 2: Ocasionais<br>(N=91 | 37,1%)<br>Média | [Z-Score]</th>
        <th class="num" style="width: 17%;">Cluster 3: Núcleo M&amp;A<br>(N=122 | 49,8%)<br>Média | [Z-Score]</th>
        <th class="num" style="width: 10%;">Estatística<br>ANOVA F</th>
        <th class="num" style="width: 10%;">Valor-p<br>(Significância)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Avaliação Tecnol. Saúde</strong> (<code>met_ats</code>)</td>
        <td class="num">0,139 | 0,346</td>
        <td class="num"><strong>100,0%</strong> | [+2,49]</td>
        <td class="num">2,2% | [-0,34]</td>
        <td class="num">0,0% | [-0,40]</td>
        <td class="num"><strong>1.690,35</strong></td>
        <td class="num"><strong>6,3 &times; 10<sup>-143</sup></strong></td>
      </tr>
      <tr>
        <td><strong>2. Projetos Ativos em M&amp;A</strong> (<code>proj_ativo</code>)</td>
        <td class="num">0,771 | 0,420</td>
        <td class="num">87,5% | [+0,25]</td>
        <td class="num">50,5% | [-0,63]</td>
        <td class="num"><strong>94,3%</strong> | [+0,41]</td>
        <td class="num"><strong>38,14</strong></td>
        <td class="num"><strong>4,0 &times; 10<sup>-15</sup></strong></td>
      </tr>
      <tr>
        <td><strong>3. Aplicação Questionários</strong> (<code>met_questionarios</code>)</td>
        <td class="num">0,518 | 0,500</td>
        <td class="num">62,5% | [+0,21]</td>
        <td class="num">20,9% | [-0,62]</td>
        <td class="num"><strong>72,1%</strong> | [+0,41]</td>
        <td class="num"><strong>36,28</strong></td>
        <td class="num"><strong>1,7 &times; 10<sup>-14</sup></strong></td>
      </tr>
      <tr>
        <td><strong>4. M&amp;A Atividade Principal</strong> (<code>ativid_principal</code>)</td>
        <td class="num">0,547 | 0,498</td>
        <td class="num">56,3% | [+0,03]</td>
        <td class="num">26,4% | [-0,57]</td>
        <td class="num"><strong>75,4%</strong> | [+0,42]</td>
        <td class="num"><strong>31,51</strong></td>
        <td class="num"><strong>6,9 &times; 10<sup>-13</sup></strong></td>
      </tr>
      <tr>
        <td><strong>5. Disseminação Decisores</strong> (<code>diss_decisores</code>)</td>
        <td class="num">0,735 | 0,442</td>
        <td class="num">78,1% | [+0,11]</td>
        <td class="num">49,5% | [-0,54]</td>
        <td class="num"><strong>90,2%</strong> | [+0,38]</td>
        <td class="num"><strong>27,03</strong></td>
        <td class="num"><strong>2,5 &times; 10<sup>-11</sup></strong></td>
      </tr>
      <tr>
        <td><strong>6. Métodos Estatísticos</strong> (<code>met_estatistica</code>)</td>
        <td class="num">0,473 | 0,499</td>
        <td class="num">62,5% | [+0,30]</td>
        <td class="num">19,8% | [-0,55]</td>
        <td class="num"><strong>63,9%</strong> | [+0,33]</td>
        <td class="num"><strong>26,60</strong></td>
        <td class="num"><strong>3,6 &times; 10<sup>-11</sup></strong></td>
      </tr>
      <tr>
        <td><strong>7. Uso de Indicadores</strong> (<code>met_indicadores</code>)</td>
        <td class="num">0,629 | 0,483</td>
        <td class="num">71,9% | [+0,19]</td>
        <td class="num">38,5% | [-0,50]</td>
        <td class="num"><strong>78,7%</strong> | [+0,33]</td>
        <td class="num"><strong>21,80</strong></td>
        <td class="num"><strong>2,0 &times; 10<sup>-9</sup></strong></td>
      </tr>
      <tr>
        <td><strong>8. Síntese de Evidências</strong> (<code>met_sintese</code>)</td>
        <td class="num">0,335 | 0,472</td>
        <td class="num"><strong>68,8%</strong> | [+0,75]</td>
        <td class="num">14,3% | [-0,41]</td>
        <td class="num">38,5% | [+0,11]</td>
        <td class="num"><strong>19,72</strong></td>
        <td class="num"><strong>1,2 &times; 10<sup>-8</sup></strong></td>
      </tr>
      <tr>
        <td><strong>9. Métodos Participativos</strong> (<code>met_participativa</code>)</td>
        <td class="num">0,388 | 0,487</td>
        <td class="num">43,8% | [+0,10]</td>
        <td class="num">16,5% | [-0,46]</td>
        <td class="num"><strong>54,1%</strong> | [+0,31]</td>
        <td class="num"><strong>17,82</strong></td>
        <td class="num"><strong>6,0 &times; 10<sup>-8</sup></strong></td>
      </tr>
      <tr>
        <td><strong>10. Parceria Internacional</strong> (<code>proj_internac</code>)</td>
        <td class="num">0,241 | 0,428</td>
        <td class="num">31,3% | [+0,17]</td>
        <td class="num">7,7% | [-0,38]</td>
        <td class="num"><strong>34,4%</strong> | [+0,24]</td>
        <td class="num"><strong>11,59</strong></td>
        <td class="num"><strong>1,6 &times; 10<sup>-5</sup></strong></td>
      </tr>
      <tr>
        <td><strong>11. Tamanho da Equipe</strong> (<code>tam_equipe</code>)</td>
        <td class="num">5,58 | 4,70</td>
        <td class="num"><strong>8,69 p.</strong> | [+0,66]</td>
        <td class="num">4,37 p. | [-0,26]</td>
        <td class="num">5,66 p. | [+0,02]</td>
        <td class="num"><strong>10,77</strong></td>
        <td class="num"><strong>3,3 &times; 10<sup>-5</sup></strong></td>
      </tr>
      <tr>
        <td><strong>12. Métodos Qualitativos</strong> (<code>met_qualitativa</code>)</td>
        <td class="num">0,543 | 0,498</td>
        <td class="num">56,3% | [+0,04]</td>
        <td class="num">38,5% | [-0,32]</td>
        <td class="num"><strong>65,6%</strong> | [+0,23]</td>
        <td class="num"><strong>8,17</strong></td>
        <td class="num"><strong>3,7 &times; 10<sup>-4</sup></strong></td>
      </tr>
      <tr>
        <td><strong>13. Disseminação Sociedade</strong> (<code>diss_geral</code>)</td>
        <td class="num">0,331 | 0,470</td>
        <td class="num">28,1% | [-0,10]</td>
        <td class="num">19,8% | [-0,28]</td>
        <td class="num"><strong>44,3%</strong> | [+0,24]</td>
        <td class="num"><strong>7,62</strong></td>
        <td class="num"><strong>6,2 &times; 10<sup>-4</sup></strong></td>
      </tr>
      <tr>
        <td><strong>14. Capacitação (Últ. 3 anos)</strong> (<code>fez_capacitacao</code>)</td>
        <td class="num">0,637 | 0,481</td>
        <td class="num"><strong>75,0%</strong> | [+0,24]</td>
        <td class="num">56,0% | [-0,16]</td>
        <td class="num">66,4% | [+0,06]</td>
        <td class="num">2,24</td>
        <td class="num">0,1090 (ns)</td>
      </tr>
    </tbody>
  </table>

  <div class="fig-box avoid-break">
    <img src="{b64_fig4}" alt="Centroides Z-Score e ANOVA F-Test">
    <div class="fig-caption">
      <strong>Figura Metodológica 4:</strong> No painel A, o perfil de linha das centroides em Z-Score evidencia a separação estrutural: o Cluster 2 situa-se sistematicamente abaixo da média (z &lt; 0 em todas as 14 variáveis), o Cluster 3 situa-se acima da média em todas as práticas multimetodológicas gerais, e o Cluster 1 destaca-se por picos extremos em ATS (+2,49), Síntese de Evidências (+0,75) e Tamanho de Equipe (+0,66). No painel B, o ranking ANOVA F confirma que 13 das 14 variáveis possuem significância estatística (p &lt; 0,001).
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- PÁGINA 8: MÉTODO DOS INSIGHTS APLICADOS E REPRODUTIBILIDADE           -->
  <!-- ===================================================================== -->
  <div class="page-break"></div>
  <h3>5.6. Método de Construção dos Insights Adicionais e Cruzamentos de Interseccionalidade</h3>
  <p>
    Após a modelagem das cinco perguntas principais, realizou-se o cruzamento das variáveis de saída (como o rótulo de Cluster <span class="math">C_k</span> atribuído pelo K-Means e a localização geográfica <span class="math">UF</span>) com variáveis sociodemográficas e operacionais suplementares das bases:
  </p>

  <ol>
    <li>
      <strong>Cálculo da Interiorização Digital no Evento 1 (Dupla Métrica com e sem Não-Declarados):</strong>
      Cruzou-se a variável geográfica <code>uf == 'DF'</code> vs. <code>uf != 'DF'</code> com a coluna <code>Você pretende acompanhar o evento de forma presencial ou online?</code> no Evento 1 (<span class="math">N = 742</span>). Entre os residentes fora do DF (<span class="math">N = 427</span>), <strong>291</strong> marcaram Online, <strong>44</strong> marcaram Presencial e <strong>92</strong> deixaram em branco (inscrições tardias/indefinidas). O pipeline reporta de forma transparente ambos os números:
      <div class="formula-box">
        Proporção Bruta (sobre todos os 427 de fora do DF): &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 291 / 427 = 68,15% Online | 44 / 427 = 10,30% Presencial<br>
        Proporção Válida (sobre os 335 que declararam formato): &nbsp; 291 / 335 = 86,87% Online | 44 / 335 = 13,13% Presencial
      </div>
      Já entre os residentes no Distrito Federal (<span class="math">N = 315</span>), 129 escolheram Presencial (<span class="math">40,95%</span> do total ou <span class="math">48,8%</span> dos válidos) e 113 escolheram Online (<span class="math">35,87%</span> do total ou <span class="math">51,2%</span> dos válidos), provando estatisticamente que a modalidade virtual é o principal vetor de equidade federativa.
    </li>
    <li>
      <strong>Estratificação Étnico-Racial e de Gênero por Cluster (Pós- Estratificação do K-Means):</strong>
      Uma vez atribuído o vetor de rótulos <code>sub_cluster['cluster']</code> (<span class="math">N = 245</span>), calculou-se a distribuição condicional de <code>Qual a sua identidade de gênero?</code> e <code>Como você se autodeclara em relação à sua raça e/ou etnia?</code> dentro de cada cluster <span class="math">k &in; {{0, 1, 2}}</span>:
      <ul>
        <li><strong>Cluster 1 (ATS, N=32):</strong> 75,0% mulheres (24/32); 65,6% brancos (21/32), 21,9% pardos (7/32) e 9,4% pretos (3/32).</li>
        <li><strong>Cluster 2 (Ocasionais, N=91):</strong> 58,2% mulheres (53/91); 59,3% brancos (54/91), <strong>34,1% pardos (31/91)</strong> e 4,4% pretos (4/91).</li>
        <li><strong>Cluster 3 (Núcleo M&amp;A, N=122):</strong> 63,1% mulheres (77/122); <strong>71,3% brancos (87/122)</strong>, 23,8% pardos (29/122) e 4,9% pretos (6/122).</li>
      </ul>
    </li>
    <li>
      <strong>Métrica do "Abismo da Comunicação Pública" e Canais Acadêmicos:</strong>
      Calculada pela comparação pareada das taxas de resposta positiva (<code>"Sim"</code>) nas quatro colunas de difusão do conhecimento dentro da amostra de avaliadores ativos (<span class="math">N = 245</span>):
      <ul>
        <li>Seminários e Sumários Executivos para Tomadores de Decisão: <span class="math">180 / 245 = 73,47%</span>;</li>
        <li>Apresentação de Trabalhos em Congressos e Eventos Científicos: <span class="math">106 / 245 = 43,27%</span>;</li>
        <li>Publicação de Artigos em Periódicos Científicos Revisados por Pares: <span class="math">95 / 245 = 38,78%</span>;</li>
        <li>Divulgação para Público Geral Não Especialista (Blogs, Redes Sociais, Imprensa): <span class="math">81 / 245 = 33,06%</span>.</li>
      </ul>
    </li>
  </ol>

  <h2>6. Governança de Código, Arquitetura de Scripts e Reprodutibilidade</h2>
  <p>
    Todo o trabalho foi encapsulado em sete scripts Python modulares e independentes, versionados no repositório Git oficial (<a href="https://github.com/glau234/dados_ma_denise.git">https://github.com/glau234/dados_ma_denise.git</a>):
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 26%;">Script Python</th>
        <th style="width: 30%;">Arquivo(s) de Saída Gerado(s)</th>
        <th style="width: 44%;">Responsabilidade Técnica no Pipeline</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>generate_analysis.py</code></td>
        <td><code>analise_dados_completa.json</code></td>
        <td>Núcleo científico: lê as 3 planilhas brutas, executa limpeza, pareamento em 3 camadas, ACM, K-Means++ e exporta todas as métricas em JSON.</td>
      </tr>
      <tr>
        <td><code>build_excel_summary.py</code></td>
        <td><code>Relatorio_Tabelas_Consolidadas_MA_2024.xlsx</code></td>
        <td>Gera a planilha consolidada de 9 abas formatada com <code>openpyxl</code> (KPIs, Q1, Q2, ACM, Regiões, Esferas, Clusters, Insights e Comentários).</td>
      </tr>
      <tr>
        <td><code>generate_pdf_report.py</code></td>
        <td><code>Relatorio_Completo_Monitoramento_Avaliacao_2024.pdf</code></td>
        <td>Gera os 5 gráficos analíticos via Matplotlib e compila o Relatório Técnico de Resultados (8 páginas) via Playwright Chromium.</td>
      </tr>
      <tr>
        <td><code>generate_methodology_pdf.py</code></td>
        <td><code>Relatorio_Metodologia_Ferramentas_Analise_2024.pdf</code></td>
        <td>Gera os 4 gráficos de validação metodológica e compila este Memorial Metodológico e Catálogo de 28 Métricas em PDF.</td>
      </tr>
      <tr>
        <td><code>generate_policy_brief.py</code></td>
        <td><code>Policy_Brief_Executivo_MA_2024.pdf</code></td>
        <td>Compila o sumário executivo de 2 páginas focado em recomendações práticas para gestores e dirigentes públicos.</td>
      </tr>
      <tr>
        <td><code>generate_manual_pdf.py</code></td>
        <td><code>Manual_Estrutura_Planilha_Excel_MA_2024.pdf</code></td>
        <td>Compila o manual técnico e dicionário de variáveis (3 páginas) explicando cada aba da planilha Excel consolidada.</td>
      </tr>
      <tr>
        <td><code>build_presentation.py</code> &amp;<br><code>build_html_dashboard.py</code></td>
        <td><code>Apresentacao_Executiva_..._2024.pptx</code><br><code>painel_analise_evidencias.html</code></td>
        <td>Constrói os 10 slides widescreen em PowerPoint e a aplicação web SPA interativa com 7 abas e 11 gráficos dinâmicos em Chart.js.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout callout-green avoid-break" style="margin-top: 14px;">
    <div class="callout-title">Certificação de Auditoria e Reprodutibilidade Determinística</div>
    Todos os resultados numéricos, testes de hipóteses (&chi;&sup2;, <em>V</em> de Cramér, ANOVA <em>F</em>), autovalores da ACM e centroides do K-Means++ apresentados neste relatório são 100% determinísticos e podem ser reexecutados a qualquer momento com o comando <code>python generate_analysis.py</code>, produzindo exatamente os mesmos valores até a quarta casa decimal.
  </div>

</body>
</html>
"""

# Salvar HTML temporário e compilar PDF via Playwright Chromium
html_temp_path = 'temp_relatorio_metodologia.html'
with open(html_temp_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

pdf_output_new = os.path.abspath('Relatorio_Completo_Metodologia_Metricas_e_Ferramentas_2024.pdf')
pdf_output_orig = os.path.abspath('Relatorio_Metodologia_Ferramentas_Analise_2024.pdf')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until='networkidle')
    pdf_bytes = page.pdf(
        format='A4',
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size: 7.5pt; color: #64748b; width: 100%; text-align: right; padding-right: 14mm; font-family: Helvetica, Arial, sans-serif;">Memorial Metodológico, Ferramentas e Catálogo de 28 Métricas • M&A 2024</div>',
        footer_template='<div style="font-size: 7.5pt; color: #64748b; width: 100%; text-align: center; font-family: Helvetica, Arial, sans-serif;">Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>',
        margin={
            'top': '16mm',
            'bottom': '18mm',
            'left': '14mm',
            'right': '14mm'
        }
    )
    browser.close()

with open(pdf_output_new, 'wb') as f:
    f.write(pdf_bytes)
print(f"Relatório Completo gerado com sucesso em: {pdf_output_new}")

try:
    with open(pdf_output_orig, 'wb') as f:
        f.write(pdf_bytes)
    print(f"Arquivo original também atualizado em: {pdf_output_orig}")
except PermissionError:
    print(f"Nota: {pdf_output_orig} está aberto em outro leitor PDF; a nova versão completa foi salva em {pdf_output_new}.")

if os.path.exists(html_temp_path):
    os.remove(html_temp_path)
