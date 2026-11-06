# -*- coding: utf-8 -*-
"""
Script para geração de um Policy Brief Executivo de 2 Páginas em PDF.
Formato condensado, direto e de alto impacto visual para ministros, secretários e diretores.
"""

import os
import json
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from playwright.sync_api import sync_playwright

print("Iniciando geração do Policy Brief Executivo de 2 Páginas...")

# Carregar dados
with open('analise_dados_completa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Gerar mini-gráficos otimizados para o Policy Brief
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = True

def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=220, bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{b64}"

# Figura 1: Miniatura Renovação E2 e ACM Dimensão 1
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 2.6))
# Donut Renovação
ax1.pie([data['q2']['e2_new'], data['q2']['overlap']],
        labels=['Novos\n(89,6%)', 'Recorrentes\n(10,4%)'],
        colors=['#10b981', '#f59e0b'], autopct='%1.1f%%', startangle=140,
        textprops={'fontsize': 7.5}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.2})
ax1.set_title('Renovação no Evento 2 (N=386)', fontsize=8.5, fontweight='bold')

# Barras Clusters
c_names = ['ATS/Saúde', 'Ocasionais', 'Núcleo M&A']
c_sizes = [32, 91, 122]
bars = ax2.bar(c_names, c_sizes, color=['#3b82f6', '#94a3b8', '#10b981'], edgecolor='black', linewidth=0.5)
ax2.set_title('Os 3 Perfis Operacionais (N=245)', fontsize=8.5, fontweight='bold')
ax2.tick_params(axis='x', labelsize=7.5)
for b in bars:
    h = b.get_height()
    pct = h / 245 * 100
    ax2.annotate(f"{pct:.1f}%", (b.get_x() + b.get_width()/2, h + 3), ha='center', fontsize=7.5, fontweight='bold')
ax2.set_ylim(0, 145)

b64_pb1 = fig_to_b64(fig1)

# Figura 2: Esfera x Saúde e Abismo da Comunicação
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 2.6))
# Esfera x Saúde
esferas = ['Federal', 'Estadual', 'Municipal']
s_sim = [43.1, 55.9, 67.4]
ax1.barh(esferas, s_sim, color='#0284c7', edgecolor='black', linewidth=0.5)
ax1.set_title('% Atuam na Saúde por Esfera', fontsize=8.5, fontweight='bold')
ax1.set_xlim(0, 85)
ax1.tick_params(axis='y', labelsize=7.5)
for i, v in enumerate(s_sim):
    ax1.annotate(f"{v:.1f}%", (v + 2, i), va='center', fontsize=7.5, fontweight='bold')

# Comunicação
ax2.bar(['Decisores\n(Governo)', 'Sociedade\n(Público)'], [73.5, 33.1], color=['#2563eb', '#e11d48'], edgecolor='black', linewidth=0.5)
ax2.set_title("O 'Abismo da Comunicação' (%)", fontsize=8.5, fontweight='bold')
ax2.set_ylim(0, 95)
ax2.tick_params(axis='x', labelsize=7.5)
for i, v in enumerate([73.5, 33.1]):
    ax2.annotate(f"{v:.1f}%", (i, v + 3), ha='center', fontsize=7.5, fontweight='bold')

b64_pb2 = fig_to_b64(fig2)

# HTML do Policy Brief (2 Páginas A4 Exatas)
html_pb = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Policy Brief: O Ecossistema de Monitoramento, Avaliação e Evidências no Brasil (2024)</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 14mm 14mm 14mm 14mm;
      @bottom-right {{
        content: "Página " counter(page) " de 2";
        font-size: 7.5pt;
        color: #64748b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }}
      @bottom-left {{
        content: "POLICY BRIEF • NOTA TÉCNICA ESTRATÉGICA • M&A E EVIDÊNCIAS 2024";
        font-size: 7.5pt;
        color: #64748b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }}
    }}
    body {{
      font-family: 'Helvetica Neue', Arial, sans-serif;
      font-size: 8.5pt;
      line-height: 1.4;
      color: #1e293b;
      margin: 0;
      padding: 0;
    }}
    .header-banner {{
      background: linear-gradient(135deg, #0c182b 0%, #1e3a8a 60%, #1e1b4b 100%);
      color: white;
      padding: 14px 18px;
      border-radius: 6px;
      border-bottom: 3px solid #00875f;
      margin-bottom: 12px;
    }}
    .badge {{
      display: inline-block;
      background-color: #00875f;
      color: white;
      font-size: 6.5pt;
      font-weight: bold;
      padding: 1.5px 6px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }}
    h1 {{
      font-size: 14pt;
      font-weight: 800;
      margin: 0 0 4px 0;
      color: white;
      line-height: 1.2;
    }}
    .sub {{
      font-size: 8pt;
      color: #cbd5e1;
      margin: 0;
    }}
    .kpi-strip {{
      display: table;
      width: 100%;
      margin-bottom: 10px;
    }}
    .kpi-box {{
      display: table-cell;
      width: 25%;
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 6px 8px;
      text-align: center;
      border-radius: 4px;
    }}
    .kpi-lbl {{
      font-size: 6.5pt;
      color: #64748b;
      font-weight: bold;
      text-transform: uppercase;
    }}
    .kpi-val {{
      font-size: 11pt;
      font-weight: 800;
      margin-top: 1px;
    }}
    h2 {{
      font-size: 10pt;
      font-weight: 700;
      color: #0c182b;
      border-bottom: 1.5px solid #00875f;
      padding-bottom: 2px;
      margin-top: 10px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }}
    .callout {{
      background-color: #f0fdf4;
      border-left: 3px solid #16a34a;
      padding: 6px 10px;
      font-size: 8pt;
      color: #166534;
      margin: 8px 0;
      border-radius: 0 4px 4px 0;
    }}
    .callout-warn {{
      background-color: #fffbeb;
      border-left: 3px solid #f59e0b;
      color: #92400e;
    }}
    .grid-2 {{
      display: table;
      width: 100%;
      margin: 6px 0;
    }}
    .col-2 {{
      display: table-cell;
      width: 50%;
      vertical-align: top;
      padding-right: 8px;
    }}
    .col-2:last-child {{
      padding-right: 0;
      padding-left: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 7.5pt;
      margin: 6px 0;
    }}
    th {{
      background-color: #0c182b;
      color: white;
      font-weight: 700;
      padding: 4px 6px;
      text-align: left;
    }}
    td {{
      padding: 3.5px 6px;
      border: 1px solid #cbd5e1;
    }}
    tr:nth-child(even) {{
      background-color: #f8fafc;
    }}
    .page-break {{
      page-break-after: always;
    }}
    .chart-box {{
      text-align: center;
      margin: 6px 0;
    }}
    .chart-box img {{
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
    }}
    ol {{
      margin: 4px 0 0 16px;
      padding: 0;
    }}
    li {{
      margin-bottom: 5px;
    }}
  </style>
</head>
<body>

  <!-- PÁGINA 1 -->
  <div class="header-banner">
    <div class="badge">Sumário Executivo para Decisores Governamentais</div>
    <h1>O Ecossistema de Monitoramento, Avaliação e Evidências no Brasil</h1>
    <div class="sub">Diagnóstico Empírico de 1.128 Inscrições em Eventos e do Survey Nacional de 521 Especialistas (2024)</div>
  </div>

  <div class="kpi-strip">
    <div class="kpi-box" style="margin-right: 4px;">
      <div class="kpi-lbl">Comunidade M&A Única</div>
      <div class="kpi-val" style="color: #2563eb;">1.088 Pessoas</div>
    </div>
    <div class="kpi-box" style="margin-right: 4px;">
      <div class="kpi-lbl">Taxa de Renovação E2</div>
      <div class="kpi-val" style="color: #10b981;">89,6% Novos</div>
    </div>
    <div class="kpi-box" style="margin-right: 4px;">
      <div class="kpi-lbl">Presença Feminina</div>
      <div class="kpi-val" style="color: #7c3aed;">60,2% a 63%</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-lbl">Tradução Decisores</div>
      <div class="kpi-val" style="color: #0284c7;">73,5% Ativa</div>
    </div>
  </div>

  <h2>1. Contexto e Mensagens-Chave em 1 Minuto</h2>
  <div class="callout">
    <strong>Síntese Estratégica:</strong>
    A rede brasileira de políticas públicas informadas por evidências e M&A não constitui uma corporação fechada, mas um campo em franca expansão. O segundo evento nacional de 2024 atraiu <strong>89,6% de novos profissionais</strong>, e o survey setorial alcançou <strong>73,5% de profissionais externos</strong> aos eventos. Contudo, há gargalos críticos: forte polarização entre o meio acadêmico e a gestão, exclusão de estados fora de Brasília caso os eventos sejam exclusivamente presenciais, sub-representação racial nas posições de doutorado (>73% brancos) e um grave <em>abismo de comunicação pública</em> (apenas 33% comunicam com o cidadão).
  </div>

  <h2>2. Dinâmica de Participação: Renovação vs. Recorrência (P1 e P2)</h2>
  <p>
    O cruzamento nominativo e por CPF comprovou que o survey funcionou como um canal aberto de ausculta e não apenas como lista de presença dos eventos: dos 226 respondentes identificados, <strong>73,5% (166 pessoas) não participaram de nenhum dos eventos</strong>, e apenas 26,5% estiveram presentes. Além disso, entre os dois eventos nacionais (Evento 1 com 742 inscritos e Evento 2 com 386 inscritos), a sobreposição foi de apenas <strong>40 indivíduos (3,68% da comunidade total)</strong>, demonstrando que o recorte prático do segundo encontro atraiu um contingente técnico inteiramente novo de avaliadores.
  </p>

  <div class="chart-box">
    <img src="{b64_pb1}" alt="Renovação e Clusters">
  </div>

  <h2>3. A Clivagem Estrutural: Pesquisa Acadêmica vs. Gestão Governamental (P3)</h2>
  <p>
    A Análise de Correspondência Múltipla (ACM, $\chi^2 = 70,06, p < 0,001$) demonstrou que a governança de evidências no Brasil opera sob dois polos institucionais afastados:
    <br>• <strong>Polo Acadêmico-Sênior:</strong> Doutores e pós-doutores (95,8% atuam como pesquisadores), com mais de 10 a 20 anos de carreira, concentrados em universidades e institutos de pesquisa;
    <br>• <strong>Polo Governamental-Operacional:</strong> Especialistas e mestres com até 5 anos de atuação, alocados na gestão pública direta e em hospitais. A alta liderança gerencial (+2,75) atua isolada no topo, demandando pontes permanentes de transferência tecnológica entre os dois mundos.
  </p>

  <div class="page-break"></div>

  <!-- PÁGINA 2 -->
  <h2>4. O Papel do SUS e a Descentralização Federativa (P4 e P5)</h2>
  <div class="grid-2">
    <div class="col-2">
      <p>
        <strong>A Saúde como Motor Federativo:</strong> A área da Saúde responde por metade dos avaliadores do país (49,4%), mas sua presença varia bruscamente segundo a esfera: é hegemônica nos municípios (<strong>67,4%</strong>) e estados (<strong>55,9%</strong>), enquanto no nível federal a atuação divide-se com Educação, Assistência Social e Planejamento.
      </p>
      <p>
        <strong>Três Perfis Operacionais de Trabalho (Clusters):</strong>
        <br>• <em>Cluster 1 (13,1%):</em> Especialistas em Avaliação de Tecnologias em Saúde (ATS - 100%) e Síntese (69%) em grandes equipes (8,7 pessoas);
        <br>• <em>Cluster 2 (37,1%):</em> Avaliadores ocasionais que realizam M&A como tarefa secundária e pouco complexa;
        <br>• <em>Cluster 3 (49,8%):</em> Núcleo multimetodológico ativo (75% atividade principal, 94% projetos ativos e 90% diálogo com decisores).
      </p>
    </div>
    <div class="col-2">
      <div class="chart-box" style="margin-top: 0;">
        <img src="{b64_pb2}" alt="Esfera x Saúde e Comunicação">
      </div>
    </div>
  </div>

  <h2>5. Diagnóstico de Diversidade e o "Abismo da Comunicação" (Insights Validados)</h2>
  <div class="callout-warn">
    <strong>Alertas Críticos de Gestão Pública:</strong>
    <ul style="margin: 2px 0 0 14px; padding: 0;">
      <li><strong>Adesão ao Online nos Estados:</strong> Entre os participantes residentes fora do DF, <strong>86,9% dos que declararam opção escolheram a modalidade remota</strong>. Eventos estritamente presenciais em Brasília excluem 9 em cada 10 avaliadores do país.</li>
      <li><strong>Equidade Étnico-Racial:</strong> Profissionais negros somam 30,6% (24,9% pardos e 5,7% pretos), mas no estrato com doutorado e pós-doutorado, <strong>mais de 73% são pessoas brancas</strong>. Profissionais pardos encontram-se represados no Cluster 2 (34,1% - práticas periféricas).</li>
      <li><strong>Insulamento Comunicacional:</strong> Enquanto 73,5% divulgam ativamente relatórios para governantes, <strong>apenas 33,1% comunicam para o público geral</strong>. As evidências científicas não chegam à população.</li>
    </ul>
  </div>

  <h2>6. Agenda Estratégica: 4 Diretrizes Prioritárias para Gestão de Políticas Públicas</h2>
  <ol>
    <li>
      <strong>Programa de Transição e Capacitação de Avaliadores Ocasionais (Cluster 2 → Cluster 3):</strong>
      Capacitar os 37,1% de técnicos que realizam avaliação de forma esporádica em técnicas práticas de formulação de indicadores, ciência de dados e métodos mistos, integrando-os às câmaras setoriais ministeriais.
    </li>
    <li>
      <strong>Ações Afirmativas e Bolsas de Liderança em M&A para Servidores Negros:</strong>
      Instituir trilhas afirmativas em cursos de especialização e mestrado profissional (ENAP/Fiocruz/Ipea) voltadas a avaliadores negros, superando o afunilamento racial na alta governança do Estado.
    </li>
    <li>
      <strong>Instituição Obrigatória do "Sumário Leigo para o Cidadão" (Knowledge Translation):</strong>
      Tornar requisito contratual em todos os Termos de Execução Descentralizada (TEDs) e editais públicos a entrega de sínteses em linguagem acessível e infográficos voltados à sociedade civil e controle social.
    </li>
    <li>
      <strong>Protocolo Híbrido Permanente para Eventos Nacionais de Evidências:</strong>
      Garantir transmissão e interação síncrona online de alta qualidade em todos os fóruns sediados em Brasília para manter a adesão dos estados do Norte, Nordeste e Sul, onde 87% dependem do formato remoto.
    </li>
  </ol>

</body>
</html>
"""

# Salvar HTML do Policy Brief
with open('policy_brief_temp.html', 'w', encoding='utf-8') as f:
    f.write(html_pb)

# Gerar PDF via Playwright
pdf_pb_path = os.path.abspath('Policy_Brief_Executivo_MA_2024.pdf')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_pb, wait_until='networkidle')
    page.pdf(
        path=pdf_pb_path,
        format='A4',
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size: 7pt; color: #94a3b8; width: 100%; text-align: right; padding-right: 14mm; font-family: Helvetica, Arial, sans-serif;">POLICY BRIEF EXECUTIVO • M&A E EVIDÊNCIAS 2024</div>',
        footer_template='<div style="font-size: 7pt; color: #94a3b8; width: 100%; text-align: center; font-family: Helvetica, Arial, sans-serif;">Página <span class="pageNumber"></span> de 2</div>',
        margin={
            'top': '14mm',
            'bottom': '14mm',
            'left': '14mm',
            'right': '14mm'
        }
    )
    browser.close()

# Remover temporário HTML
if os.path.exists('policy_brief_temp.html'):
    os.remove('policy_brief_temp.html')

print(f"Policy Brief Executivo de 2 Páginas gerado com sucesso em: {pdf_pb_path}")

