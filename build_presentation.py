# -*- coding: utf-8 -*-
"""
Script para geração automática da Apresentação Executiva em PowerPoint (.pptx).
Estrutura 10 slides institucionais com design profissional, tabelas, tópicos executivos
e gráficos de alta resolução embutidos.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

print("Iniciando geração da Apresentação Executiva (.pptx)...")

# 1. Carregar dados consolidados
with open('analise_dados_completa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Configurar diretório temporário para figuras
img_dir = os.path.abspath('img_slides')
os.makedirs(img_dir, exist_ok=True)

# -------------------------------------------------------------
# GERAR IMAGENS DE ALTA RESOLUÇÃO PARA OS SLIDES
# -------------------------------------------------------------
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = True

# Imagem 1: Q1 e Q2
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.2))
ax1.pie([data['q1']['external'], data['q1']['any_match']],
        labels=['Externos aos Eventos\n(166 pessoas - 73,5%)', 'Participantes de Eventos\n(60 pessoas - 26,5%)'],
        colors=['#e11d48', '#10b981'], autopct='%1.1f%%', startangle=140,
        textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
ax1.set_title('P1: Correspondência Survey x Eventos\n(Respondentes Identificados N=226)', fontsize=10.5, fontweight='bold', pad=8)

ax2.pie([data['q2']['e2_new'], data['q2']['overlap']],
        labels=['Novos Profissionais\n(344 pessoas - 89,1%)', 'Recorrentes do E1\n(42 pessoas - 10,9%)'],
        colors=['#2563eb', '#f59e0b'], autopct='%1.1f%%', startangle=140,
        textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
ax2.set_title('P2: Renovação no Evento 2 (Práticas)\n(Inscritos Totais N=386)', fontsize=10.5, fontweight='bold', pad=8)
path_fig1 = os.path.join(img_dir, 'fig1_q1_q2.png')
fig1.savefig(path_fig1, dpi=200, bbox_inches='tight')
plt.close(fig1)

# Imagem 2: Q3 Mapa ACM
fig2, ax = plt.subplots(figsize=(8.5, 5.2))
points = data['q3']['points']
var_colors = {'faixa_tempo': '#2563eb', 'titulacao_clean': '#9333ea', 'funcao_clean': '#d97706'}
var_markers = {'faixa_tempo': 'o', 'titulacao_clean': 's', 'funcao_clean': '^'}
var_labels = {'faixa_tempo': 'Tempo de Atuação', 'titulacao_clean': 'Titulação Acadêmica', 'funcao_clean': 'Função Profissional'}

ax.axhline(0, color='#94a3b8', linestyle='--', linewidth=0.8, alpha=0.7)
ax.axvline(0, color='#94a3b8', linestyle='--', linewidth=0.8, alpha=0.7)
seen = set()
for p in points:
    v, cat, x, y = p['variable'], p['category'], p['dim1'], p['dim2']
    lbl = var_labels[v] if v not in seen else ""
    seen.add(v)
    ax.scatter(x, y, color=var_colors[v], marker=var_markers[v], s=110, edgecolors='black', linewidth=0.7, label=lbl, zorder=5)
    off_x, off_y = (0.04, 0.04)
    if 'gerente' in cat.lower(): off_y = -0.16
    elif 'pós-doutorado' in cat.lower(): off_x = -0.28
    ax.annotate(cat, (x + off_x, y + off_y), fontsize=8, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#cbd5e1", alpha=0.85), zorder=6)

ax.set_xlabel(f"Dimensão 1 ({data['q3']['inertia_dim1']}%) ← Acadêmico/Pesquisa vs Prática/Gestão →", fontsize=9, fontweight='bold')
ax.set_ylabel(f"Dimensão 2 ({data['q3']['inertia_dim2']}%) ← Técnico vs Liderança/Gerência →", fontsize=9, fontweight='bold')
ax.set_title("P3: Mapa Perceptual da Análise de Correspondência Múltipla (ACM)", fontsize=10.5, fontweight='bold', pad=10)
ax.grid(True, linestyle=':', alpha=0.4)
ax.legend(loc='lower left', fontsize=8, facecolor='white', framealpha=0.9)
path_fig2 = os.path.join(img_dir, 'fig2_mca.png')
fig2.savefig(path_fig2, dpi=200, bbox_inches='tight')
plt.close(fig2)

# Imagem 3: Q4 Distribuição Espacial e Setorial
fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.2))
regs = list(data['q4']['regioes'].keys())
vals_reg = list(data['q4']['regioes'].values())
bars1 = ax1.bar(regs, vals_reg, color=['#1d4ed8', '#0284c7', '#0d9488', '#ca8a04', '#e11d48', '#64748b'], edgecolor='black', linewidth=0.6)
ax1.set_title('Inscritos por Grande Região (N=1.128)', fontsize=10, fontweight='bold')
ax1.tick_params(axis='x', rotation=25, labelsize=8)
for b in bars1:
    h = b.get_height()
    ax1.annotate(f"{h / 1128 * 100:.1f}%", (b.get_x() + b.get_width()/2, h + 8), ha='center', fontsize=7.5, fontweight='bold')

esferas = ['Públ. Federal', 'Públ. Estadual', 'Públ. Municipal', 'Outros/Acad.']
s_sim = [210, 123, 64, 73]
s_nao = [277, 97, 31, 134]
y_p = np.arange(len(esferas))
w = 0.35
ax2.barh(y_p - w/2, s_sim, w, label='Saúde (SUS)', color='#0284c7', edgecolor='black', linewidth=0.5)
ax2.barh(y_p + w/2, s_nao, w, label='Outras Políticas', color='#64748b', edgecolor='black', linewidth=0.5)
ax2.set_yticks(y_p)
ax2.set_yticklabels(esferas, fontsize=8.5)
ax2.invert_yaxis()
ax2.set_title('P4: Esfera x Área da Saúde', fontsize=10, fontweight='bold')
ax2.legend(loc='lower right', fontsize=8)
path_fig3 = os.path.join(img_dir, 'fig3_spatial.png')
fig3.savefig(path_fig3, dpi=200, bbox_inches='tight')
plt.close(fig3)

# Imagem 4: Q5 Clusters
fig4, ax = plt.subplots(figsize=(9, 4.4))
met_names = ['Estatística', 'Qualitativo', 'Indicadores', 'Síntese', 'ATS', 'Participativo', 'Questionários', 'Decisores']
keys = ['met_estatistica', 'met_qualitativa', 'met_indicadores', 'met_sintese', 'met_ats', 'met_participativa', 'met_questionarios', 'diss_decisores']
c0 = [data['q5']['means']['0'][k] * 100 for k in keys]
c1 = [data['q5']['means']['1'][k] * 100 for k in keys]
c2 = [data['q5']['means']['2'][k] * 100 for k in keys]
xi = np.arange(len(met_names))
bw = 0.26
ax.bar(xi - bw, c0, bw, label='Cluster 1: ATS e Síntese (13,1%)', color='#3b82f6', edgecolor='black', linewidth=0.5)
ax.bar(xi, c1, bw, label='Cluster 2: Ocasionais (37,1%)', color='#94a3b8', edgecolor='black', linewidth=0.5)
ax.bar(xi + bw, c2, bw, label='Cluster 3: Núcleo M&A (49,8%)', color='#10b981', edgecolor='black', linewidth=0.5)
ax.set_xticks(xi)
ax.set_xticklabels(met_names, fontsize=8.5)
ax.set_ylabel('% Adoção Cotidiana', fontsize=8.5)
ax.set_title('P5: Perfis dos Clusters de Atribuições Cotidianas (K-Means, N=245)', fontsize=10.5, fontweight='bold', pad=10)
ax.set_ylim(0, 115)
ax.legend(loc='upper right', fontsize=8, facecolor='white', framealpha=0.9)
path_fig4 = os.path.join(img_dir, 'fig4_clusters.png')
fig4.savefig(path_fig4, dpi=200, bbox_inches='tight')
plt.close(fig4)

# Imagem 5: Insights
fig5, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3.4))
ax1.pie([60.2, 39.8], labels=['Feminino\n(60,2%)', 'Masculino\n(39,8%)'], colors=['#8b5cf6', '#38bdf8'], autopct='%1.1f%%', textprops={'fontsize': 8})
ax1.set_title("Liderança Feminina\n(Evento 1)", fontsize=9.5, fontweight='bold')
ax2.bar(['Branca', 'Parda', 'Preta', 'Outros'], [66.5, 24.9, 5.7, 2.9], color=['#f59e0b', '#d97706', '#78350f', '#94a3b8'], edgecolor='black', linewidth=0.5)
ax2.set_title("Composição Racial\n(Survey M&A)", fontsize=9.5, fontweight='bold')
ax2.tick_params(axis='x', labelsize=7.5)
ax3.bar(['Decisores\n(Governo)', 'Sociedade\n(Público)'], [73.5, 33.1], color=['#2563eb', '#e11d48'], edgecolor='black', linewidth=0.5)
ax3.set_title("O 'Abismo da Comunicação'\n(Difusão de M&A)", fontsize=9.5, fontweight='bold')
ax3.tick_params(axis='x', labelsize=8)
path_fig5 = os.path.join(img_dir, 'fig5_insights.png')
fig5.savefig(path_fig5, dpi=200, bbox_inches='tight')
plt.close(fig5)

print("Gráficos salvos com sucesso no disco.")

# -------------------------------------------------------------
# MONTAGEM DA APRESENTAÇÃO POWERPOINT (16:9 WIDESCREEN)
# -------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Paleta Corporativa Oficial
NAVY = RGBColor(12, 24, 43)        # #0c182b
EMERALD = RGBColor(0, 135, 95)     # #00875f
BLUE = RGBColor(37, 99, 235)       # #2563eb
GRAY_BG = RGBColor(248, 250, 252)  # #f8fafc
TEXT_DARK = RGBColor(30, 41, 59)   # #1e293b
WHITE = RGBColor(255, 255, 255)

def apply_slide_header(slide, title_text, category="PESQUISA DE EVIDÊNCIAS E M&A 2024"):
    # Barra superior decorativa
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = EMERALD
    top_bar.line.fill.background()
    
    # Caixa de título
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(1.1))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY
    p_title.space_before = Pt(3)

blank_layout = prs.slide_layouts[6]

# =============================================================
# SLIDE 1: CAPA INSTITUCIONAL
# =============================================================
slide1 = prs.slides.add_slide(blank_layout)

bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.fill.background()

stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.2), Inches(13.333), Inches(0.3))
stripe.fill.solid()
stripe.fill.fore_color.rgb = EMERALD
stripe.line.fill.background()

tb_capa = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(4.0))
tf_capa = tb_capa.text_frame
tf_capa.word_wrap = True

p_badge = tf_capa.paragraphs[0]
p_badge.text = "RELATÓRIO EXECUTIVO DE PESQUISA • ANO BASE 2024"
p_badge.font.size = Pt(11)
p_badge.font.bold = True
p_badge.font.color.rgb = RGBColor(56, 189, 248)

p_h1 = tf_capa.add_paragraph()
p_h1.text = "Redes de Monitoramento, Avaliação e Evidências em Políticas Públicas"
p_h1.font.size = Pt(34)
p_h1.font.bold = True
p_h1.font.color.rgb = WHITE
p_h1.space_before = Pt(12)

p_sub = tf_capa.add_paragraph()
p_sub.text = "Análise Integrada entre Participantes de Eventos e o Survey Nacional de Escuta"
p_sub.font.size = Pt(17)
p_sub.font.color.rgb = RGBColor(203, 213, 225)
p_sub.space_before = Pt(10)

p_meta = tf_capa.add_paragraph()
p_meta.text = "Bases Analisadas: 1.128 Inscrições em Eventos (1.086 Indivíduos Únicos) | 521 Respondentes do Survey Nacional"
p_meta.font.size = Pt(11)
p_meta.font.color.rgb = RGBColor(148, 163, 184)
p_meta.space_before = Pt(24)

# =============================================================
# SLIDE 2: PAINEL DE INDICADORES-CHAVE (KPIS)
# =============================================================
slide2 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide2, "Painel de Indicadores Globais da Pesquisa", "Visão Geral Executiva")

kpi_data = [
    ("1.128", "Inscrições nos Eventos", "1.086 indivíduos únicos desduplicados", BLUE),
    ("521", "Respondentes do Survey", "245 profissionais com prática profunda", NAVY),
    ("89,1%", "Taxa de Renovação", "Novos profissionais no Evento 2 (Práticas)", EMERALD),
    ("3,87%", "Recorrência Geral", "Apenas 42 pessoas em ambos os eventos", RGBColor(217, 119, 6)),
    ("60,2%", "Maioria Feminina", "63,0% no survey de escuta nacional", RGBColor(124, 58, 237)),
    ("73,5%", "Tradução p/ Decisores", "33,1% divulgam p/ sociedade em geral", RGBColor(225, 29, 72))
]

for idx, (val, tit, sub, cor) in enumerate(kpi_data):
    row = idx // 3
    col = idx % 3
    left = Inches(0.8 + col * 3.95)
    top = Inches(1.8 + row * 2.5)
    
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.75), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = GRAY_BG
    card.line.color.rgb = RGBColor(226, 232, 240)
    card.line.width = Pt(1)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)
    
    p_t = tf.paragraphs[0]
    p_t.text = tit.upper()
    p_t.font.size = Pt(9.5)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(100, 116, 139)
    
    p_v = tf.add_paragraph()
    p_v.text = val
    p_v.font.size = Pt(32)
    p_v.font.bold = True
    p_v.font.color.rgb = cor
    p_v.space_before = Pt(4)
    
    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(9)
    p_s.font.color.rgb = TEXT_DARK
    p_s.space_before = Pt(4)

# =============================================================
# SLIDE 3: PERGUNTA 1 (SURVEY X EVENTOS)
# =============================================================
slide3 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide3, "Pergunta 1: Os Respondentes do Survey são os Mesmos dos Eventos?", "Pareamento de Bases")

tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(5.5), Inches(5.2))
tf3 = tb3.text_frame
tf3.word_wrap = True

p1 = tf3.paragraphs[0]
p1.text = "DIAGNÓSTICO: NÃO SÃO AS MESMAS PESSOAS"
p1.font.size = Pt(13)
p1.font.bold = True
p1.font.color.rgb = RGBColor(225, 29, 72)

bullet_points_s3 = [
    "O survey alcançou uma comunidade substancialmente externa aos eventos, atuando como um canal aberto de escuta setorial.",
    "Dos 521 respondentes, 295 (56,6%) responderam anonimamente e 226 (43,4%) forneceram contatos voluntários para entrevistas.",
    "Entre os 226 identificados, 73,45% (166 pessoas) não constam em nenhum dos eventos.",
    "Apenas 26,55% (60 pessoas) participaram de pelo menos um evento (47 no Evento 1, 17 no Evento 2 e 4 em ambos).",
    "Em relação ao universo total de inscritos nos eventos (1.086 indivíduos), apenas ~5,5% responderam ao survey identificado."
]
for pt in bullet_points_s3:
    p = tf3.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)

slide3.shapes.add_picture(path_fig1, Inches(6.5), Inches(1.8), width=Inches(6.0))

# =============================================================
# SLIDE 4: PERGUNTA 2 (RECORRÊNCIA VS RENOVAÇÃO)
# =============================================================
slide4 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide4, "Pergunta 2: Recorrência ou Renovação de Profissionais nos Eventos?", "Dinâmica Longitudinal")

tb4 = slide4.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
tf4 = tb4.text_frame
tf4.word_wrap = True

p1 = tf4.paragraphs[0]
p1.text = "DIAGNÓSTICO: FORTE RENOVAÇÃO E BAIXA RECORRÊNCIA"
p1.font.size = Pt(13)
p1.font.bold = True
p1.font.color.rgb = EMERALD

bullet_points_s4 = [
    "Taxa de Renovação no Evento 2: 89,12% dos participantes eram estreantes que não haviam se inscrito no primeiro evento (344 de 386).",
    "Taxa de Recorrência no Evento 2: Apenas 10,88% (42 indivíduos) foram participantes do primeiro evento.",
    "Taxa de Retenção do Evento 1 no Evento 2: Apenas 5,66% dos 742 inscritos do Evento 1 migraram para o segundo evento.",
    "Comunidade Única Consolidada: Somando os dois encontros, alcançou-se 1.086 profissionais únicos no país.",
    "Conclusão: O recorte aplicado de 'Práticas em Avaliação' do segundo evento mobilizou com sucesso um novo público técnico."
]
for pt in bullet_points_s4:
    p = tf4.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)

# Inserir tabela de transição no Slide 4
rows, cols = 4, 3
left_t, top_t, w_t, h_t = Inches(6.6), Inches(2.0), Inches(5.9), Inches(3.8)
tbl_s4 = slide4.shapes.add_table(rows, cols, left_t, top_t, w_t, h_t).table
tbl_s4.columns[0].width = Inches(2.7)
tbl_s4.columns[1].width = Inches(1.5)
tbl_s4.columns[2].width = Inches(1.7)

headers = ["Métrica de Participação", "Quantidade", "Taxa (%)"]
for i, h in enumerate(headers):
    cell = tbl_s4.cell(0, i)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    for p in cell.text_frame.paragraphs:
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

data_t4 = [
    ["Novos Inscritos Atraídos (E2)", "344", "89,12%"],
    ["Recorrentes em Ambos os Eventos", "42", "10,88%"],
    ["Comunidade de Indivíduos Únicos", "1.086", "100,00%"]
]
for r_idx, row_vals in enumerate(data_t4, 1):
    for c_idx, val in enumerate(row_vals):
        cell = tbl_s4.cell(r_idx, c_idx)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = GRAY_BG if r_idx % 2 == 0 else WHITE
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

# =============================================================
# SLIDE 5: PERGUNTA 3 (ANÁLISE DE CORRESPONDÊNCIA - ACM)
# =============================================================
slide5 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide5, "Pergunta 3: Análise de Correspondência Múltipla (ACM)", "Tempo x Titulação x Função")

slide5.shapes.add_picture(path_fig2, Inches(0.8), Inches(1.7), width=Inches(6.6))

tb5 = slide5.shapes.add_textbox(Inches(7.6), Inches(1.7), Inches(4.9), Inches(5.2))
tf5 = tb5.text_frame
tf5.word_wrap = True

p1 = tf5.paragraphs[0]
p1.text = "ESTRUTURA FATORIAL BIDIMENSIONAL (26,6% INÉRCIA)"
p1.font.size = Pt(11.5)
p1.font.bold = True
p1.font.color.rgb = RGBColor(147, 51, 234)

bullet_points_s5 = [
    "Testes Qui-Quadrado (χ²): Associação altamente significante entre Titulação e Função (p = 3,12e-10) e entre Tempo e Titulação (p = 0,0001).",
    "Dimensão 1 (Eixo Horizontal - 15,07%): Divide o Polo Acadêmico-Sênior (Doutores, Pós-doutores, >10 a 20 anos, Pesquisadores) do Polo Governamental-Operacional (Especialistas, Mestres, até 5 anos, na Gestão e Prática).",
    "Dimensão 2 (Eixo Vertical - 11,52%): Isola no topo a Liderança e Gerência Estratégica (+2,75), diferenciando gerentes com mestrado e 6-10 anos dos analistas executores de ponta.",
    "95,8% dos pós-doutores atuam como pesquisadores, enquanto 61,5% dos especialistas estão alocados na gestão governamental direta."
]
for pt in bullet_points_s5:
    p = tf5.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)

# =============================================================
# SLIDE 6: PERGUNTA 4 (DISTRIBUIÇÃO ESPACIAL E SETORIAL)
# =============================================================
slide6 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide6, "Pergunta 4: Distribuição Espacial, Esfera e Área Setorial", "Geografia e SUS")

slide6.shapes.add_picture(path_fig3, Inches(0.8), Inches(1.7), width=Inches(6.4))

tb6 = slide6.shapes.add_textbox(Inches(7.4), Inches(1.7), Inches(5.1), Inches(5.2))
tf6 = tb6.text_frame
tf6.word_wrap = True

p1 = tf6.paragraphs[0]
p1.text = "PADRÃO FEDERATIVO E DOMINÂNCIA DA SAÚDE"
p1.font.size = Pt(12)
p1.font.bold = True
p1.font.color.rgb = RGBColor(2, 132, 199)

bullet_points_s6 = [
    "Concentração Centro-Oeste e DF: O DF lidera com 45,4% dos participantes dos eventos devido à sede ministerial. Sudeste responde por 23,9% (SP e RJ) e Nordeste por 12,2% (BA e CE).",
    "Equilíbrio Geral: 49,38% dos inscritos são da Saúde e 50,62% de outras políticas públicas (Educação, Assistência Social, Planejamento e Meio Ambiente).",
    "A Saúde nos Níveis Federativos: Há forte correlação: na esfera municipal, 67,4% são da Saúde (hospitais e atenção básica); na estadual, 55,9% são da Saúde; enquanto na federal, a maioria (56,9%) opera em outras políticas públicas.",
    "No survey, as áreas setoriais mais citadas foram Saúde (46,9%), Educação (29,8%) e Assistência Social (12,7%)."
]
for pt in bullet_points_s6:
    p = tf6.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)

# =============================================================
# SLIDE 7: PERGUNTA 5 (CLUSTERS DE ATRIBUIÇÕES COTIDIANAS)
# =============================================================
slide7 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide7, "Pergunta 5: Perfis segundo Atribuições Cotidianas (Clusters)", "Segmentação Operacional")

slide7.shapes.add_picture(path_fig4, Inches(0.8), Inches(1.7), width=Inches(6.5))

tb7 = slide7.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(5.0), Inches(5.2))
tf7 = tb7.text_frame
tf7.word_wrap = True

p1 = tf7.paragraphs[0]
p1.text = "TRÊS PERFIS PROFISSIONAIS BEM ESTRUTURADOS"
p1.font.size = Pt(11.5)
p1.font.bold = True
p1.font.color.rgb = RGBColor(16, 185, 129)

clusters_desc = [
    ("Cluster 1: Especialistas em ATS (13,1%):", "100% aplicam Avaliação de Tecnologias em Saúde; 68,8% usam síntese de evidências; atuam em grandes equipes (média 8,7 pessoas); 78% comunicam com decisores."),
    ("Cluster 2: Avaliadores Ocasionais (37,1%):", "M&A é atividade secundária (73,6%); menor complexidade metodológica (20% usam estatística e 38% indicadores); equipes de 4,4 pessoas; pouca visibilidade governamental."),
    ("Cluster 3: Núcleo Multimetodológico (49,8%):", "Motor do campo de M&A. Atividade principal (75,4%); 94,3% projetos ativos; domínio de métodos quantitativos (64%), qualitativos (66%) e indicadores (79%); 90,2% dialogam com decisores.")
]
for tit_c, desc_c in clusters_desc:
    p_t = tf7.add_paragraph()
    p_t.text = tit_c
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_t.space_before = Pt(8)
    
    p_d = tf7.add_paragraph()
    p_d.text = desc_c
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_DARK

# =============================================================
# SLIDE 8: ECOSSISTEMA, CANAIS & CAPACITAÇÃO
# =============================================================
slide8 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide8, "Ecossistema Institucional, Veículos e Demandas de Capacitação", "Articulação e Competências")

tb8_l = slide8.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
tf8_l = tb8_l.text_frame
tf8_l.word_wrap = True

p_i = tf8_l.paragraphs[0]
p_i.text = "INSTITUIÇÕES ÂNCORAS DO ECOSSISTEMA"
p_i.font.size = Pt(11.5)
p_i.font.bold = True
p_i.font.color.rgb = BLUE

inst_list = [
    "Ministério da Saúde (MS): 71 menções diretas (indução de políticas informadas por evidências e Conitec).",
    "Fundação Oswaldo Cruz (Fiocruz): 41 menções (referência científica e formação em saúde coletiva).",
    "Embrapa: 17 menções (avaliação de impactos agroambientais ex-ante e ex-post).",
    "IPEA & ENAP: 15 e 8 menções (desenho institucional, impacto e capacitação de carreiras de Estado).",
    "Secretarias Estaduais (SES-DF: 11 menções) e Universidades (UnB: 11 menções, USP: 8 menções)."
]
for item in inst_list:
    p = tf8_l.add_paragraph()
    p.text = "• " + item
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(6)

tb8_r = slide8.shapes.add_textbox(Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
tf8_r = tb8_r.text_frame
tf8_r.word_wrap = True

p_c = tf8_r.paragraphs[0]
p_c.text = "CANAIS E DEMANDAS DE CAPACITAÇÃO"
p_c.font.size = Pt(11.5)
p_c.font.bold = True
p_c.font.color.rgb = RGBColor(147, 51, 234)

cap_list = [
    "Canais para Decisores Governamentais: Relatórios técnicos (42,4%), seminários internos (41,3%), reuniões estratégicas (25,0%) e sumários executivos (15,2%).",
    "Canais para a Sociedade Geral: Instagram (45,7%) e LinkedIn (39,1%), porém com adesão de apenas 33% dos avaliadores.",
    "Formato de Capacitação Predominante: 63,7% realizaram cursos nos últimos 3 anos, massivamente em modalidade autoinstrucional / EAD assíncrona (>65%).",
    "Temas Mais Demandados: Avaliação de Impacto Contrafactual, Ciência de Dados em Políticas Públicas, Construção de Indicadores e Teoria da Mudança / Modelos Lógicos."
]
for item in cap_list:
    p = tf8_r.add_paragraph()
    p.text = "• " + item
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(6)

# =============================================================
# SLIDE 9: INSIGHTS ADICIONAIS APLICADOS
# =============================================================
slide9 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide9, "Insights Adicionais Aplicados: Diversidade e Comunicação", "Validação e Cruzamentos")

slide9.shapes.add_picture(path_fig5, Inches(0.8), Inches(1.7), width=Inches(6.6))

tb9 = slide9.shapes.add_textbox(Inches(7.6), Inches(1.7), Inches(4.9), Inches(5.2))
tf9 = tb9.text_frame
tf9.word_wrap = True

p1 = tf9.paragraphs[0]
p1.text = "CRUZAMENTOS MULTIVARIADOS VALIDADOS"
p1.font.size = Pt(11.5)
p1.font.bold = True
p1.font.color.rgb = RGBColor(225, 29, 72)

insights_bullets = [
    "Protagonismo Feminino nos Clusters: 75,0% dos especialistas do Cluster 1 (ATS e Síntese) e 63,1% do Cluster 3 (Núcleo M&A) são mulheres.",
    "Gargalo de Equidade Étnico-Racial: 71,3% do Cluster 3 (núcleo de maior liderança) é branco. Profissionais pardos concentram-se no Cluster 2 (34,1% - prática periférica). Doutorado/Pós-doutorado tem >73% de pessoas brancas.",
    "Adesão ao Online nos Estados: Entre os participantes de fora do DF, 86,9% optaram pelo modelo online, provando que o formato híbrido é o pilar da descentralização federativa.",
    "O 'Abismo da Comunicação': 73,5% divulgam para decisores governamentais, mas só 33,1% comunicam para o cidadão comum."
]
for pt in insights_bullets:
    p = tf9.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)

# =============================================================
# SLIDE 10: DIRETRIZES E PLANO ESTRATÉGICO
# =============================================================
slide10 = prs.slides.add_slide(blank_layout)
apply_slide_header(slide10, "Plano de Diretrizes Estratégicas para a Rede Nacional de M&A", "Recomendações Práticas")

acoes = [
    ("1. Trilha de Transição de Avaliadores Ocasionais (Cluster 2 → Cluster 3)",
     "Estruturar programas de mentoria e oficinas práticas em formulação de indicadores e análise quantitativa voltadas aos 37,1% de técnicos que realizam avaliação de modo acessório, integrando-os aos projetos ativos dos ministérios."),
    ("2. Ações Afirmativas de Equidade Racial na Alta Liderança de M&A",
     "Instituir cotas e bolsas de pós-graduação e formação executiva em ciência de dados e avaliação de impacto voltadas para servidores negros, visando reverter a assimetria racial no topo da carreira (>73% de brancos em doutorado)."),
    ("3. Instituição do 'Sumário Leigo Obrigatório' (Knowledge Translation)",
     "Superar o abismo da comunicação tornando obrigatória a publicação de sínteses em linguagem acessível e infográficos em todas as avaliações financiadas por fundos públicos (TEDs e editais), aproximando o cidadão das evidências."),
    ("4. Política Híbrida Permanente em Fóruns Nacionais de Evidências",
     "Garantir transmissão e participação síncrona online estruturada em todos os fóruns nacionais para assegurar a permanência e participação contínua dos estados fora de Brasília, onde 86,9% dependem da modalidade remota.")
]

for idx, (tit_a, desc_a) in enumerate(acoes):
    top_pos = Inches(1.8 + idx * 1.3)
    box_a = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.15))
    box_a.fill.solid()
    box_a.fill.fore_color.rgb = GRAY_BG
    box_a.line.color.rgb = RGBColor(226, 232, 240)
    
    tf = box_a.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.15)
    
    p_t = tf.paragraphs[0]
    p_t.text = tit_a
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = BLUE
    
    p_d = tf.add_paragraph()
    p_d.text = desc_a
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(3)

# Salvar apresentação PowerPoint
pptx_output_path = os.path.abspath('Apresentacao_Executiva_Monitoramento_Avaliacao_2024.pptx')
prs.save(pptx_output_path)

print(f"Apresentação PowerPoint gerada com sucesso em: {pptx_output_path}")

