# -*- coding: utf-8 -*-
"""
Script para conversão do Manual do Usuário e Dicionário de Dados
da Planilha Excel Consolidada em documento PDF diagramado oficialmente.
"""

import os
from playwright.sync_api import sync_playwright

print("Iniciando geração do Manual da Planilha em PDF...")

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Manual do Usuário e Dicionário de Dados: Planilha Excel Consolidada</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 16mm 16mm 18mm 16mm;
      @bottom-right {
        content: "Página " counter(page) " de " counter(pages);
        font-size: 8pt;
        color: #64748b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }
      @bottom-left {
        content: "MANUAL DA PLANILHA • RELATÓRIO CONSOLIDADO M&A 2024";
        font-size: 8pt;
        color: #64748b;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }
    }
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      font-size: 8.5pt;
      line-height: 1.45;
      color: #1e293b;
      margin: 0;
      padding: 0;
    }
    .cover-banner {
      background: linear-gradient(135deg, #0c182b 0%, #1e3a8a 60%, #1e1b4b 100%);
      color: #ffffff;
      padding: 18px 22px;
      border-radius: 6px;
      margin-bottom: 14px;
      border-bottom: 3px solid #00875f;
    }
    .badge {
      display: inline-block;
      background-color: #00875f;
      color: #ffffff;
      font-size: 7pt;
      font-weight: bold;
      padding: 2px 7px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 5px;
    }
    h1 {
      font-size: 15pt;
      font-weight: 800;
      margin: 0 0 4px 0;
      color: #ffffff;
      line-height: 1.25;
    }
    .subtitle {
      font-size: 9pt;
      color: #cbd5e1;
      margin: 0;
    }
    .meta-grid {
      display: table;
      width: 100%;
      margin-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.2);
      padding-top: 8px;
    }
    .meta-col {
      display: table-cell;
      font-size: 7.5pt;
      color: #94a3b8;
    }
    .meta-col strong {
      color: #ffffff;
      display: block;
      font-size: 8pt;
    }
    h2 {
      font-size: 11pt;
      font-weight: 700;
      color: #0c182b;
      border-bottom: 1.5px solid #00875f;
      padding-bottom: 3px;
      margin-top: 16px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }
    h3 {
      font-size: 9.5pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-top: 12px;
      margin-bottom: 4px;
      page-break-after: avoid;
    }
    p {
      margin-top: 0;
      margin-bottom: 6px;
      text-align: justify;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 7.5pt;
      margin: 6px 0 10px 0;
      page-break-inside: avoid;
    }
    th {
      background-color: #0c182b;
      color: #ffffff;
      font-weight: 700;
      padding: 5px 7px;
      text-align: left;
      border: 1px solid #0c182b;
    }
    td {
      padding: 4px 7px;
      border: 1px solid #cbd5e1;
    }
    tr:nth-child(even) {
      background-color: #f8fafc;
    }
    .alert-box {
      background-color: #f0fdf4;
      border-left: 3.5px solid #16a34a;
      padding: 6px 10px;
      font-size: 8pt;
      color: #166534;
      margin: 8px 0;
      border-radius: 0 4px 4px 0;
    }
    .alert-info {
      background-color: #eff6ff;
      border-left: 3.5px solid #2563eb;
      color: #1e40af;
      padding: 6px 10px;
      font-size: 8pt;
      margin: 8px 0;
      border-radius: 0 4px 4px 0;
    }
    .sheet-card {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 8px 12px;
      margin-bottom: 10px;
      page-break-inside: avoid;
    }
    .sheet-title {
      font-size: 9pt;
      font-weight: 700;
      color: #0c182b;
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
    }
    .page-break {
      page-break-after: always;
    }
    code {
      background-color: #e2e8f0;
      padding: 1px 4px;
      border-radius: 3px;
      font-size: 7.5pt;
      font-family: monospace;
      color: #0f172a;
    }
  </style>
</head>
<body>

  <!-- BANNER -->
  <div class="cover-banner">
    <div class="badge">Documentação Técnica e Dicionário de Dados</div>
    <h1>Manual Operacional da Planilha Excel Consolidada</h1>
    <div class="subtitle">Guia de Estrutura, Variáveis, Fórmulas e Interpretação das Abas Analíticas (Ano Base 2024)</div>
    <div class="meta-grid">
      <div class="meta-col">
        <strong>Arquivo Consolidado:</strong> Relatorio_Tabelas_Consolidadas_MA_2024.xlsx
      </div>
      <div class="meta-col">
        <strong>Total de Abas Estruturadas:</strong> 9 abas (8 seções temáticas)
      </div>
      <div class="meta-col">
        <strong>Formatação e Estilo:</strong> Dark Navy (#0C182B) + Borda Fina + Zebra
      </div>
    </div>
  </div>

  <h2>1. Visão Geral e Finalidade da Planilha</h2>
  <p>
    A planilha <code>Relatorio_Tabelas_Consolidadas_MA_2024.xlsx</code> é a base unificada de dados quantitativos, matrizes fatoriais da Análise de Correspondência Múltipla (ACM), modelos de agrupamento em clusters (K-Means) e cruzamentos demográfico-institucionais gerados a partir do processamento de <strong>1.128 inscrições em eventos</strong> e <strong>521 respostas ao survey nacional de escuta</strong>.
  </p>
  <div class="alert-box">
    <strong>Objetivo do Manual:</strong> Orientar gestores, pesquisadores e analistas sobre como extrair dados, compreender as fórmulas subjacentes, replicar gráficos no Excel e fundamentar relatórios, notas técnicas e apresentações executivas.
  </div>

  <h2>2. Dicionário Detalhado das 9 Abas</h2>

  <!-- ABA 1 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 1: <code>KPIs_Gerais</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Painel de Controle e Indicadores de Topo</span>
    </div>
    <p><strong>Finalidade:</strong> Resumo executivo com os 10 indicadores globais da pesquisa para alimentação de cards de apresentações e notas para dirigentes.</p>
    <table>
      <thead>
        <tr>
          <th>Coluna</th>
          <th>Tipo</th>
          <th>Descrição Semântica e Regra de Cálculo</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><code>Indicador</code></td><td>Texto</td><td>Nome formal da métrica de gestão apurada.</td></tr>
        <tr><td><code>Valor</code></td><td>Numérico/%</td><td>Valor absoluto ou percentual consolidado.</td></tr>
        <tr><td><code>Unidade</code></td><td>Texto</td><td>Inscrições, Pessoas, Respondentes ou Percentual.</td></tr>
        <tr><td><code>Detalhe</code></td><td>Texto</td><td>Nota metodológica com numerador, denominador e contexto.</td></tr>
      </tbody>
    </table>
    <div class="alert-info">
      <strong>Exemplo de Aplicação:</strong> Utilize para montar a capa ou primeiro slide de reuniões: "Comunidade de 1.086 indivíduos únicos, renovação de 89,1% no Evento 2 e 60,2% de liderança feminina".
    </div>
  </div>

  <!-- ABA 2 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 2: <code>Q1_Survey_vs_Eventos</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Pareamento Determinístico (Pergunta 1)</span>
    </div>
    <p><strong>Pergunta Respondida:</strong> <em>1 — As pessoas que responderam ao survey são as mesmas que participaram dos eventos?</em></p>
    <table>
      <thead>
        <tr>
          <th>Coluna</th>
          <th>Tipo</th>
          <th>Descrição Semântica e Regra de Cálculo</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><code>Segmento</code></td><td>Texto</td><td>Classificação após cruzamento multinível (CPF limpo, e-mail padronizado e nome completo).</td></tr>
        <tr><td><code>Frequência</code></td><td>Inteiro</td><td>Contagem absoluta de indivíduos.</td></tr>
        <tr><td><code>Percentual_Identificados</code></td><td>%</td><td>Proporção sobre os respondentes identificados (N = 226).</td></tr>
        <tr><td><code>Percentual_Survey_Total</code></td><td>%</td><td>Proporção sobre o total da amostra do survey (N = 521).</td></tr>
      </tbody>
    </table>
    <p><strong>Métrica Central:</strong> <strong>73,45% (166 pessoas)</strong> dos identificados são externos aos eventos. Comprova que o survey atingiu uma comunidade setorial ampliada e não apenas a lista de participantes dos eventos.</p>
  </div>

  <div class="page-break"></div>

  <!-- ABA 3 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 3: <code>Q2_Recorrencia_Renovacao</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Matriz de Fidelidade e Transição (Pergunta 2)</span>
    </div>
    <p><strong>Pergunta Respondida:</strong> <em>2 — Existe recorrência da participação das pessoas nos dois eventos ou renovação e atração de novos profissionais?</em></p>
    <table>
      <thead>
        <tr>
          <th>Métrica</th>
          <th>Valor</th>
          <th>Fórmula / Regra de Negócio</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Taxa de Renovação no Evento 2 (%)</td><td><strong>89,12%</strong></td><td>(344 novos inscritos no E2 / 386 inscritos totais no E2) * 100</td></tr>
        <tr><td>Taxa de Recorrência no Evento 2 (%)</td><td>10,88%</td><td>(42 pessoas que vieram do E1 / 386 inscritos totais no E2) * 100</td></tr>
        <tr><td>Retenção do Evento 1 no Evento 2 (%)</td><td>5,66%</td><td>(42 pessoas / 742 inscritos totais no E1) * 100</td></tr>
        <tr><td>Taxa de Recorrência Global (%)</td><td>3,87%</td><td>(42 sobrepostos / 1.086 indivíduos únicos da comunidade) * 100</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ABA 4 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 4: <code>Q3_ACM_Coordenadas</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Coordenadas da Análise de Correspondência (Pergunta 3)</span>
    </div>
    <p><strong>Pergunta Respondida:</strong> <em>3 — Qual a relação entre tempo de atuação profissional, titulação e formação profissional?</em></p>
    <table>
      <thead>
        <tr>
          <th>Coluna</th>
          <th>Tipo</th>
          <th>Descrição Semântica</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><code>Variavel</code></td><td>Texto</td><td>Nome da variável (faixa_tempo, titulacao_clean, funcao_clean).</td></tr>
        <tr><td><code>Categoria</code></td><td>Texto</td><td>Rótulo da categoria (ex: Doutorado, Na gestão, Mais de 20 anos).</td></tr>
        <tr><td><code>Coordenada_Dimensao_1</code></td><td>Decimal</td><td>Posição no Eixo Horizontal (15,07% da inércia explicada).</td></tr>
        <tr><td><code>Coordenada_Dimensao_2</code></td><td>Decimal</td><td>Posição no Eixo Vertical (11,52% da inércia explicada).</td></tr>
      </tbody>
    </table>
    <p><strong>Como Criar o Mapa Perceptual no Excel:</strong> Selecione as duas colunas de coordenadas e insira um gráfico de <em>Dispersão XY</em>. O quadrante esquerdo negativo representa o Polo Acadêmico-Sênior (Doutores e Pesquisadores); o quadrante direito positivo representa a Gestão Pública Operacional.</p>
  </div>

  <!-- ABAS 5 E 6 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Abas 5 e 6: <code>Q4_Regioes</code> e <code>Q4_Esferas</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Distribuição Federativa e Esferas de Atuação (Pergunta 4)</span>
    </div>
    <p><strong>Pergunta Respondida:</strong> <em>4 — Qual a distribuição espacial entre UF, esfera de atuação e área setorial da política pública?</em></p>
    <table>
      <thead>
        <tr>
          <th>Grande Região</th>
          <th>Inscrições</th>
          <th>% Total</th>
          <th>Esfera de Atuação</th>
          <th>Inscrições</th>
          <th>% Total</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Centro-Oeste (DF lidera com 45,4%)</td><td>559</td><td>49,56%</td><td>Público Federal</td><td>487</td><td>43,17%</td></tr>
        <tr><td>Sudeste (SP 11,0%, RJ 8,0%)</td><td>269</td><td>23,85%</td><td>Público Estadual</td><td>220</td><td>19,50%</td></tr>
        <tr><td>Nordeste (BA e CE)</td><td>138</td><td>12,23%</td><td>Outros / Academia</td><td>207</td><td>18,35%</td></tr>
        <tr><td>Sul (PR, RS, SC)</td><td>73</td><td>6,47%</td><td>Público Municipal</td><td>95</td><td>8,42%</td></tr>
        <tr><td>Norte (AM e PA)</td><td>65</td><td>5,76%</td><td>Privado e Autônomo</td><td>115</td><td>10,20%</td></tr>
      </tbody>
    </table>
    <div class="alert-info">
      <strong>O Padrão da Saúde:</strong> Nos municípios, <strong>67,4% são da Saúde</strong> (hospitais e postos); nos estados, <strong>55,9%</strong>; e na União, 43,1% (com 56,9% em Educação, Planejamento e Meio Ambiente).
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ABA 7 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 7: <code>Q5_Clusters_Perfis</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Perfis Operacionais segundo Atribuições Cotidianas (Pergunta 5)</span>
    </div>
    <p><strong>Pergunta Respondida:</strong> <em>5 — Qual a relação dos perfis profissionais segundo suas atribuições cotidianas?</em></p>
    <p>Apresenta as médias das 14 rotinas de trabalho dos 3 grupos identificados pelo algoritmo K-Means (N = 245):</p>
    <table>
      <thead>
        <tr>
          <th>Atribuição Cotidiana</th>
          <th>Cluster 1: ATS e Síntese (13,1%)</th>
          <th>Cluster 2: Ocasionais (37,1%)</th>
          <th>Cluster 3: Núcleo M&A (49,8%)</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>M&A é Atividade Principal</td><td>56,2%</td><td>26,4%</td><td><strong>75,4%</strong></td></tr>
        <tr><td>Projetos Ativos no Momento</td><td>87,5%</td><td>50,5%</td><td><strong>94,3%</strong></td></tr>
        <tr><td>Tamanho Médio da Equipe</td><td><strong>8,7 pessoas</strong></td><td>4,4 pessoas</td><td>5,7 pessoas</td></tr>
        <tr><td>Uso de Análise Estatística</td><td>62,5%</td><td>19,8%</td><td><strong>63,9%</strong></td></tr>
        <tr><td>Uso de Métodos Qualitativos</td><td>56,2%</td><td>38,5%</td><td><strong>65,6%</strong></td></tr>
        <tr><td>Desenvolvimento de Indicadores</td><td>71,9%</td><td>38,5%</td><td><strong>78,7%</strong></td></tr>
        <tr><td>Síntese de Evidências (Revisões)</td><td><strong>68,8%</strong></td><td>14,3%</td><td>38,5%</td></tr>
        <tr><td>Avaliação de Tecnologias em Saúde (ATS)</td><td><strong>100,0%</strong></td><td>2,2%</td><td>0,0%</td></tr>
        <tr><td>Disseminação para Tomadores de Decisão</td><td>78,1%</td><td>49,5%</td><td><strong>90,2%</strong></td></tr>
        <tr><td>Disseminação para o Público Geral</td><td>28,1%</td><td>19,8%</td><td><strong>44,3%</strong></td></tr>
      </tbody>
    </table>
  </div>

  <!-- ABA 8 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 8: <code>Insights_Aplicados_Cruzamentos</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Cruzamentos Multivariados Validados e Aplicados</span>
    </div>
    <p><strong>Finalidade:</strong> Reunir as tabulações que articulam demografia (gênero e raça), formato remoto e canais de disseminação com os clusters e regiões.</p>
    <table>
      <thead>
        <tr>
          <th>Análise</th>
          <th>Segmento</th>
          <th>Percentual</th>
          <th>Observação Estratégica</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Interiorização Federativa (Fora do DF)</td><td>Online</td><td><strong>86,9%</strong></td><td>Apenas 10,3% presencial. O modelo híbrido é barreira de inclusão.</td></tr>
        <tr><td>Gênero no Cluster 1 (ATS e Síntese)</td><td>Mulheres</td><td><strong>75,0%</strong></td><td>Dominância feminina expressiva na alta avaliação em saúde.</td></tr>
        <tr><td>Raça no Cluster 3 (Núcleo Duro M&A)</td><td>Brancos</td><td><strong>71,3%</strong></td><td>Maior concentração de pessoas brancas no núcleo de liderança.</td></tr>
        <tr><td>Raça no Cluster 2 (Ocasionais)</td><td>Pardos</td><td><strong>34,1%</strong></td><td>Concentração de pardos alocados na prática secundária/periférica.</td></tr>
        <tr><td>Comunicação Pública no Cluster 1</td><td>Público Geral</td><td>28,1%</td><td>Insulamento tecnocrático em notas da Conitec e Ministério da Saúde.</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ABA 9 -->
  <div class="sheet-card">
    <div class="sheet-title">
      <span>Aba 9: <code>Comentarios_Qualitativos</code></span>
      <span style="color: #2563eb; font-size: 8pt;">Base Textual dos 68 Comentários Abertos</span>
    </div>
    <p><strong>Finalidade:</strong> Fornecer a íntegra dos depoimentos livres registrados ao final do survey para análise de conteúdo qualitativa. Organiza-se em duas colunas: <code>ID</code> (identificador do formulário) e <code>Comentario_Aberto</code> (texto transcrito na íntegra sem cortes).</p>
  </div>

  <h2>3. Orientações Práticas para Gestores e Analistas</h2>
  <ol style="margin-left: 18px; padding: 0;">
    <li><strong>Criação de Relatórios Rápidos:</strong> Copie as tabelas das abas <code>KPIs_Gerais</code> e <code>Insights_Aplicados_Cruzamentos</code> diretamente para relatórios no Word ou apresentações no PowerPoint — as tabelas já possuem formatação compatível e nomes padronizados.</li>
    <li><strong>Elaboração de Termos de Referência (TRs):</strong> Utilize os centróides da aba <code>Q5_Clusters_Perfis</code> para definir perfis de equipe em contratações de consultorias ou cooperações com organismos internacionais (ex: diferenciar especialistas em ATS de avaliadores de indicadores).</li>
    <li><strong>Planejamento de Eventos e Trilhas:</strong> Os dados das abas <code>Q2_Recorrencia_Renovacao</code> e <code>Insights_Aplicados_Cruzamentos</code> comprovam a necessidade técnica de oferecer transmissão online para atingir mais de 86% do público fora de Brasília.</li>
  </ol>

</body>
</html>
"""

# Converter para PDF via Playwright
pdf_output_path = os.path.abspath('Manual_Estrutura_Planilha_Excel_MA_2024.pdf')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until='networkidle')
    page.pdf(
        path=pdf_output_path,
        format='A4',
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size: 7pt; color: #94a3b8; width: 100%; text-align: right; padding-right: 16mm; font-family: Helvetica, Arial, sans-serif;">Manual Operacional • Planilha Consolidada M&A 2024</div>',
        footer_template='<div style="font-size: 7pt; color: #94a3b8; width: 100%; text-align: center; font-family: Helvetica, Arial, sans-serif;">Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>',
        margin={
            'top': '16mm',
            'bottom': '18mm',
            'left': '16mm',
            'right': '16mm'
        }
    )
    browser.close()

print(f"Manual em PDF gerado com sucesso em: {pdf_output_path}")
