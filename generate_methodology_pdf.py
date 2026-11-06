# -*- coding: utf-8 -*-
"""
Script para geração do Relatório de Metodologia e Ferramentas de Análise em PDF
Documenta exaustivamente todas as tecnologias, ferramentas, bibliotecas e métodos estatísticos utilizados.
"""

import os
from playwright.sync_api import sync_playwright

print("Iniciando construção do Relatório de Metodologia e Ferramentas...")

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório de Metodologia e Ferramentas de Análise de Dados (2024)</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    @page {
      size: A4 portrait;
      margin: 18mm 16mm 20mm 16mm;
      @bottom-right {
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: 'Inter', sans-serif;
      font-size: 9.5pt;
      line-height: 1.55;
      color: #1e293b;
      margin: 0;
      padding: 0;
      background-color: #ffffff;
    }

    .page-break {
      page-break-before: always;
    }

    .avoid-break {
      page-break-inside: avoid;
    }

    /* Cabeçalho da Capa / Primeira Página */
    .header-box {
      border-bottom: 2.5px solid #0f172a;
      padding-bottom: 14px;
      margin-bottom: 22px;
    }

    .badge-bar {
      display: flex;
      gap: 8px;
      margin-bottom: 8px;
    }

    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 7.5pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .badge-navy { background-color: #0f172a; color: #ffffff; }
    .badge-blue { background-color: #2563eb; color: #ffffff; }
    .badge-green { background-color: #059669; color: #ffffff; }
    .badge-purple { background-color: #7c3aed; color: #ffffff; }

    h1 {
      font-size: 20pt;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.2;
      margin: 6px 0 8px 0;
      letter-spacing: -0.5px;
    }

    .subtitle {
      font-size: 10.5pt;
      color: #475569;
      margin: 0;
      font-weight: 400;
    }

    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 24px;
      font-size: 8pt;
    }

    .meta-item strong {
      display: block;
      color: #64748b;
      text-transform: uppercase;
      font-size: 7pt;
      margin-bottom: 2px;
    }

    .meta-item span {
      font-weight: 600;
      color: #0f172a;
    }

    h2 {
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      margin: 22px 0 10px 0;
      padding-bottom: 5px;
      border-bottom: 1.5px solid #cbd5e1;
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: -0.3px;
    }

    h3 {
      font-size: 10.5pt;
      font-weight: 700;
      color: #1e3a8a;
      margin: 14px 0 6px 0;
    }

    p {
      margin: 0 0 10px 0;
      text-align: justify;
    }

    /* Tabelas */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0 16px 0;
      font-size: 8pt;
    }

    th {
      background-color: #0f172a;
      color: #ffffff;
      font-weight: 600;
      text-align: left;
      padding: 7px 10px;
      font-size: 7.5pt;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }

    td {
      padding: 6.5px 10px;
      border-bottom: 1px solid #e2e8f0;
      color: #334155;
    }

    tr:nth-child(even) td {
      background-color: #f8fafc;
    }

    /* Caixas de Destaque */
    .callout {
      border-left: 4px solid #2563eb;
      background-color: #eff6ff;
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      margin: 12px 0 16px 0;
      font-size: 8.5pt;
    }

    .callout-title {
      font-weight: 700;
      color: #1d4ed8;
      margin-bottom: 4px;
      font-size: 9pt;
    }

    .callout-green {
      border-left-color: #059669;
      background-color: #ecfdf5;
    }
    .callout-green .callout-title { color: #047857; }

    .callout-amber {
      border-left-color: #d97706;
      background-color: #fffbeb;
    }
    .callout-amber .callout-title { color: #b45309; }

    .callout-purple {
      border-left-color: #7c3aed;
      background-color: #f5f3ff;
    }
    .callout-purple .callout-title { color: #6d28d9; }

    /* Código e Fórmulas */
    .code-block {
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.5pt;
      background-color: #0f172a;
      color: #f8fafc;
      padding: 10px 12px;
      border-radius: 6px;
      margin: 8px 0 14px 0;
      overflow-x: auto;
      line-height: 1.45;
    }

    .formula-box {
      background-color: #f1f5f9;
      border: 1px dashed #94a3b8;
      border-radius: 6px;
      padding: 8px 12px;
      margin: 8px 0 12px 0;
      text-align: center;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: #0f172a;
      font-size: 8.5pt;
    }

    /* Grids de Cards */
    .card-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 10px 0 16px 0;
    }

    .card {
      background-color: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 10px 12px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    .card-title {
      font-weight: 700;
      font-size: 8.5pt;
      color: #0f172a;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    ul, ol {
      margin: 0 0 10px 0;
      padding-left: 18px;
    }

    li {
      margin-bottom: 4px;
    }
  </style>
</head>
<body>

  <!-- CABEÇALHO DO DOCUMENTO -->
  <div class="header-box">
    <div class="badge-bar">
      <span class="badge badge-navy">Documento Metodológico Oficial</span>
      <span class="badge badge-blue">Ciência de Dados & Econometria</span>
      <span class="badge badge-green">Reprodutibilidade Estrita</span>
    </div>
    <h1>Relatório de Ferramentas, Métodos e Procedimentos Analíticos</h1>
    <p class="subtitle">
      Detalhamento técnico, algoritmos, equações matemáticas e fluxo computacional aplicados na análise dos dados de Monitoramento, Avaliação e Evidências em Políticas Públicas (2024)
    </p>
  </div>

  <!-- METADADOS TÉCNICOS -->
  <div class="meta-grid">
    <div class="meta-item">
      <strong>Linguagem & Versão</strong>
      <span>Python 3.12 (64-bit)</span>
    </div>
    <div class="meta-item">
      <strong>Ecossistema Matemático</strong>
      <span>scikit-learn, prince, scipy</span>
    </div>
    <div class="meta-item">
      <strong>Amostras Analisadas</strong>
      <span>1.128 Inscrições | 521 Survey</span>
    </div>
    <div class="meta-item">
      <strong>Controle de Versão</strong>
      <span>Git / GitHub (main branch)</span>
    </div>
  </div>

  <!-- SEÇÃO 1: OBJETIVO E ESCOPO METODOLÓGICO -->
  <h2>1. Apresentação e Escopo do Relatório</h2>
  <p>
    Este relatório tem por objetivo registrar e descrever formalmente todas as <strong>ferramentas computacionais</strong>, <strong>pacotes de software</strong>, <strong>modelos estatísticos</strong> e <strong>procedimentos algorítmicos</strong> empregados na análise integrada das bases de dados de participantes dos eventos nacionais e dos respondentes do survey de escuta da comunidade de Monitoramento e Avaliação (M&A) e Políticas Públicas Informadas por Evidências (PIE) no Brasil no ano-base de 2024.
  </p>
  <p>
    A abordagem metodológica adotou o paradigma da <strong>pesquisa quantitativa reproduzível</strong> (<em>Reproducible Research</em>). Todas as transformações de dados, testes de hipóteses, reduções dimensionais e agrupamentos não supervisionados foram desenvolvidos em código aberto, parametrizados deterministicamente com sementes pseudo-aleatórias fixadas (<code>random_state=42</code>) e executados sem qualquer intervenção manual nas planilhas de origem, garantindo auditoria ponta a ponta e integridade analítica absoluta.
  </p>

  <!-- SEÇÃO 2: INVENTÁRIO COMPLETO DE FERRAMENTAS -->
  <h2>2. Inventário de Ferramentas, Linguagens e Bibliotecas</h2>
  <p>
    O ecossistema analítico foi estruturado sobre a linguagem de programação <strong>Python</strong>, complementada por bibliotecas especializadas em análise multivariada, computação científica, manipulação relacional, formatação de dados e renderização editorial de alta performance.
  </p>

  <div class="avoid-break">
    <table>
      <thead>
        <tr>
          <th style="width: 22%;">Ferramenta / Biblioteca</th>
          <th style="width: 15%;">Categoria</th>
          <th style="width: 38%;">Função Específica no Projeto</th>
          <th style="width: 25%;">Justificativa Técnica</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Python 3.12</strong></td>
          <td>Linguagem Base</td>
          <td>Ambiente principal de processamento de dados, orquestração de scripts e execução estatística.</td>
          <td>Liderança na ciência de dados, ampla interoperabilidade e tipagem estrita moderna.</td>
        </tr>
        <tr>
          <td><strong>pandas (v2.2+)</strong></td>
          <td>Manipulação de Dados</td>
          <td>Ingestão dos arquivos Excel (.xlsx), fusão relacional (merges), filtros e engenharia de variáveis.</td>
          <td>Manipulação vetorial com alto desempenho em memória e suporte nativo a indexação multinível.</td>
        </tr>
        <tr>
          <td><strong>NumPy (v1.26+)</strong></td>
          <td>Computação Numérica</td>
          <td>Cálculo matricial, transformações de vetores lógicos e álgebra linear subjacente.</td>
          <td>Eficiência de baixo nível em C para operações matemáticas estruturadas em arrays.</td>
        </tr>
        <tr>
          <td><strong>scikit-learn (v1.4+)</strong></td>
          <td>Machine Learning</td>
          <td>Algoritmo de agrupamento não supervisionado K-Means e padronização escalar Z-Score.</td>
          <td>Implementação consagrada com algoritmo <em>k-means++</em> para convergência acelerada e estável.</td>
        </tr>
        <tr>
          <td><strong>prince (v0.13+)</strong></td>
          <td>Análise Multivariada</td>
          <td>Execução da Análise de Correspondência Múltipla (ACM/MCA) e decomposição em valores singulares.</td>
          <td>Especializado em matrizes indicadoras e matrizes de Burt para dados categóricos multidimensionais.</td>
        </tr>
        <tr>
          <td><strong>SciPy (scipy.stats)</strong></td>
          <td>Inferência Estatística</td>
          <td>Testes Qui-Quadrado (&chi;²) de Pearson para tabelas de contingência e cálculo de valores-p.</td>
          <td>Precisão assintótica no cálculo de distribuições de probabilidade contínuas e discretas.</td>
        </tr>
        <tr>
          <td><strong>openpyxl (v3.1+)</strong></td>
          <td>Engenharia Excel</td>
          <td>Geração programática da planilha consolidada (9 abas), estilização corporativa Navy e bordas.</td>
          <td>Leitura e escrita de arquivos OpenXML nativos com controle fino de fontes, preenchimentos e formatos.</td>
        </tr>
        <tr>
          <td><strong>python-pptx</strong></td>
          <td>Comunicação Executiva</td>
          <td>Montagem da apresentação corporativa em PowerPoint (10 slides widescreen 16:9).</td>
          <td>Criação de apresentações ricas com cards analíticos e figuras vetoriais embutidas programaticamente.</td>
        </tr>
        <tr>
          <td><strong>Playwright Chromium</strong></td>
          <td>Diagramação PDF</td>
          <td>Motor de renderização headless para compilação dos relatórios técnicos oficiais em PDF A4.</td>
          <td>Fidelidade gráfica impecável a padrões editoriais modernos com suporte CSS Paged Media.</td>
        </tr>
        <tr>
          <td><strong>Tailwind CSS & Chart.js</strong></td>
          <td>Frontend Interativo</td>
          <td>Construção do painel analítico web (HTML5) com gráficos interativos e responsivos.</td>
          <td>Interface moderna, sem dependência de servidores de aplicação complexos (execução client-side).</td>
        </tr>
        <tr>
          <td><strong>Git & GitHub</strong></td>
          <td>Governança e Versão</td>
          <td>Versionamento distribuído do código-fonte, dados derivados e sincronização com repositório remoto.</td>
          <td>Rastreabilidade de commits convencionais e colaboração segura com gerenciamento de credenciais.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- SEÇÃO 3: BASES DE DADOS E PRÉ-PROCESSAMENTO -->
  <div class="page-break"></div>
  <h2>3. Bases de Dados e Engenharia de Pré-Processamento</h2>
  <p>
    A pesquisa consolidou três repositórios primários fornecidos em formato Microsoft Excel (.xlsx), totalizando 1.649 registros brutos. A tabela a seguir descreve a estrutura das fontes originais:
  </p>

  <div class="avoid-break">
    <table>
      <thead>
        <tr>
          <th>Base de Dados Primária</th>
          <th>Registros Brutos</th>
          <th>Variáveis Chave</th>
          <th>Natureza da Amostra</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Inscritos-Politicas-Publicas-Informadas-por-Evidencias-2024.xlsx</strong></td>
          <td>742 inscrições</td>
          <td>Nome, E-mail, CPF, UF, Instituição, Esfera, Setor, Modalidade (Presencial/Online), Sexo</td>
          <td>Participantes de evento nacional focado na interface entre evidências científicas e tomada de decisão.</td>
        </tr>
        <tr>
          <td><strong>Inscritos-Praticas-em-Avaliacao-e-Evidencias-2024.xlsx</strong></td>
          <td>386 inscrições</td>
          <td>Nome, E-mail, CPF, UF, Órgão, Esfera, Formato de Inscrição</td>
          <td>Participantes de fórum focado na prática metodológica e aplicação operacional de M&A.</td>
        </tr>
        <tr>
          <td><strong>Survey-Escuta-Redes-de-Monitoramento-Avaliacao.xlsx</strong></td>
          <td>521 respondentes</td>
          <td>Dados demográficos, Carreira, Tempo de M&A, Métodos aplicados, Rotinas, Disseminação</td>
          <td>Pesquisa nacional de escuta profissional estruturada com respondentes nominais e anônimos.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>3.1. Pipeline de Limpeza e Normalização Textual</h3>
  <p>
    Devido à origem manual dos cadastros (digitação direta pelos participantes), foi desenvolvido um algoritmo rigoroso de higienização prévia para permitir o cruzamento determinístico:
  </p>
  <ul>
    <li><strong>Normalização de CPFs:</strong> Aplicação de expressões regulares para extração exclusiva de algarismos numéricos (<code>re.sub(r'\D', '', str(cpf))</code>), validação de tamanho canônico de 11 dígitos com preenchimento de zeros à esquerda (<code>zfill(11)</code>) e expurgo de CPFs genéricos/inválidos (ex: sequências repetidas 111.111.111-11).</li>
    <li><strong>Normalização de E-mails:</strong> Conversão forçada para minúsculas (<code>lower()</code>), remoção de espaços em branco marginais e caracteres invisíveis de formatação (<code>strip()</code>). Múltiplos e-mails cadastrados em uma mesma célula foram segmentados por delimitadores (vírgulas, ponto-e-vírgula e barras).</li>
    <li><strong>Normalização Fonética e Nominal:</strong> Remoção sistemática de acentuação gráfica (diacríticos) via conversão Unicode, eliminação de pontuações, conversão para caixa alta e descarte de partículas preposicionais de ligação (ex: "DE", "DA", "DO", "DOS", "DAS", "E").</li>
  </ul>

  <div class="callout callout-amber">
    <div class="callout-title">Tratamento Metodológico dos Respondentes Anônimos do Survey</div>
    No Survey nacional (521 respondentes), 295 participantes exerceram o direito de sigilo, respondendo sem fornecer CPF, e-mail ou nome. Para evitar distorções estatísticas, a análise adotou <strong>duplo denominador</strong>: o percentual sobre a amostra com identificação nominal (N = 226) para aferição precisa da sobreposição física com os eventos, e o percentual sobre o universo total (N = 521) para mensuração da capilaridade da pesquisa.
  </div>

  <!-- SEÇÃO 4: DETALHAMENTO DOS MÉTODOS ANALÍTICOS -->
  <h2>4. Métodos Analíticos Utilizados e Como Foram Executados</h2>

  <!-- 4.1 PAREAMENTO -->
  <h3>4.1. Pareamento Determinístico Multinível (Entity Resolution) — Pergunta 1</h3>
  <p>
    <strong>Problema de Pesquisa:</strong> Determinar se os profissionais que responderam ao formulário de escuta nacional (survey) são os mesmos que participaram dos eventos nacionais de 2024.
  </p>
  <p>
    <strong>Como foi feito:</strong> Implementou-se um algoritmo determinístico de resolução de entidades em três camadas hierárquicas e mutuamente excludentes, processado em memória vetorial:
  </p>

  <div class="code-block">
Camada 1 (Chave Primária Forte): Casamento exato por CPF normalizado (11 dígitos).
   IF CPF_survey != Nulo AND CPF_survey == CPF_evento THEN Match = True

Camada 2 (Identificador Único Secundário): Casamento exato por E-mail limpo.
   IF Match == False AND Email_survey != Nulo AND Email_survey == Email_evento THEN Match = True

Camada 3 (Chave Quaternária Nominal): Casamento exato por Nome Normalizado.
   IF Match == False AND Nome_survey != Nulo AND Nome_survey == Nome_evento THEN Match = True
  </div>

  <p>
    <strong>Validação e Resultado:</strong> Dos 226 respondentes identificados, constatou-se que <strong>166 pessoas (73,45%)</strong> não possuíam qualquer registro nos eventos de 2024, comprovando que o survey capturou um contingente amplamente externo e inovador para as redes públicas.
  </p>

  <!-- 4.2 FLUXO LONGITUDINAL -->
  <div class="page-break"></div>
  <h3>4.2. Teoria dos Conjuntos e Métricas de Fluxo Longitudinal — Pergunta 2</h3>
  <p>
    <strong>Problema de Pesquisa:</strong> Verificar se a comunidade de eventos apresenta recorrência (fidelização do mesmo público) ou renovação contínua (atração de novos quadros).
  </p>
  <p>
    <strong>Como foi feito:</strong> Aplicaram-se operações formais da teoria dos conjuntos sobre os conjuntos de inscritos únicos nos dois eventos consecutivos:
  </p>

  <div class="card-grid-2">
    <div class="card">
      <div class="card-title">Definições de Conjuntos</div>
      <ul style="font-size: 7.5pt;">
        <li>$E_1$: Conjunto de indivíduos únicos do Evento 1 ($|E_1| = 742$)</li>
        <li>$E_2$: Conjunto de indivíduos únicos do Evento 2 ($|E_2| = 386$)</li>
        <li>$U$: Comunidade consolidada única ($U = E_1 \cup E_2$, $|U| = 1.086$)</li>
        <li>$S$: Sobreposição física ($S = E_1 \cap E_2$, $|S| = 42$)</li>
        <li>$N_2$: Estreantes no Evento 2 ($N_2 = E_2 \setminus E_1$, $|N_2| = 344$)</li>
      </ul>
    </div>
    <div class="card">
      <div class="card-title">Equações das Taxas</div>
      <div class="formula-box">
        T_renov = (|N_2| / |E_2|) &times; 100 = 89,12%<br>
        T_rec_E2 = (|S| / |E_2|) &times; 100 = 10,88%<br>
        T_ret_E1 = (|S| / |E_1|) &times; 100 = 5,66%<br>
        T_rec_global = (|S| / |U|) &times; 100 = 3,87%
      </div>
    </div>
  </div>

  <p>
    <strong>Interpretação Substantiva:</strong> O índice de renovação de quase 90% atesta que a mudança do foco temático de um evento para o outro mobilizou nichos distintos da administração pública, sem saturação da audiência.
  </p>

  <!-- 4.3 ACM E TESTES QUI-QUADRADO -->
  <h3>4.3. Análise de Correspondência Múltipla (ACM) e Testes de Associação &chi;² — Pergunta 3</h3>
  <p>
    <strong>Problema de Pesquisa:</strong> Identificar a geometria estrutural entre o tempo de atuação profissional, o nível de titulação acadêmica e a função exercida no cotidiano.
  </p>
  <p>
    <strong>Como foi feito:</strong>
  </p>
  <ol>
    <li>
      <strong>Testes de Independência Qui-Quadrado (&chi;²):</strong> Antes da redução dimensional, calculou-se a significância estatística da associação bivariada entre as variáveis mediante tabelas de contingência com o módulo <code>scipy.stats.chi2_contingency</code>:
      <div class="formula-box">
        &chi;&sup2; = &sum; [ (O_{ij} - E_{ij})&sup2; / E_{ij} ] &nbsp;&nbsp;&nbsp; com &nbsp;&nbsp;&nbsp; E_{ij} = (R_i &times; C_j) / N
      </div>
      Onde $O_{ij}$ é a contagem observada e $E_{ij}$ é a frequência teórica esperada sob a hipótese nula ($H_0$). Constatou-se dependência altamente significante entre Titulação e Função (&chi;² = 70,06; gl = 12; p &lt; 0,0001) e entre Tempo e Titulação (&chi;² = 46,02; gl = 16; p = 0,0001).
    </li>
    <li>
      <strong>Decomposição Fatorial da ACM:</strong> Com o pacote <code>prince.MCA</code>, codificou-se a base de $N = 243$ observações em uma matriz indicadora disjuntiva completa $Z$ ($N \times K$). Construiu-se a matriz de Burt $B = Z^T Z$. A decomposição em valores singulares (SVD) da matriz de correspondências padronizada extraiu as inércias principais:
      <ul>
        <li><strong>Fator 1 (Dimensão 1):</strong> Autovalor explicando <strong>15,07%</strong> da inércia total. Opõe o Polo Acadêmico-Sênior (Doutores e Pesquisadores com >10 a 20 anos, com escores negativos -0,49 a -1,17) ao Polo Governamental-Operacional (Especialistas e Mestres com até 5 anos, escores positivos +0,69 a +1,11).</li>
        <li><strong>Fator 2 (Dimensão 2):</strong> Explicando <strong>11,52%</strong> da inércia, isola verticalmente as funções de Gerência/Coordenação (+2,75) em relação às funções de execução de pesquisa.</li>
      </ul>
    </li>
  </ol>

  <!-- 4.4 MINERAÇÃO ESPACIAL E SETORIAL -->
  <h3>4.4. Mineração Espacial e Prevalência Setorial da Saúde — Pergunta 4</h3>
  <p>
    <strong>Problema de Pesquisa:</strong> Mapear a distribuição federativa das UFs, as esferas de atuação governamental e a inserção setorial da política pública.
  </p>
  <p>
    <strong>Como foi feito:</strong>
  </p>
  <ul>
    <li><strong>Padronização Federativa:</strong> Dicionário de sinônimos para conversão de siglas de UF e agregação nas 5 Grandes Regiões do IBGE (Norte, Nordeste, Centro-Oeste, Sudeste, Sul).</li>
    <li><strong>Classificação Setorial da Saúde:</strong> Aplicação de expressões regulares sobre as colunas de "Órgão" e "Área Temática" para categorização binária (Saúde vs. Demais Políticas Públicas).</li>
    <li><strong>Tabulação Cruzada Multivariada (Esfera &times; Setor):</strong> Cálculo das razões de prevalência setorial, revelando que a presença da Saúde atinge <strong>67,4% no nível municipal</strong> e <strong>55,9% no nível estadual</strong>, enquanto a União apresenta diversificação balanceada com Educação e Assistência Social.</li>
  </ul>

  <!-- 4.5 CLUSTERIZAÇÃO K-MEANS -->
  <div class="page-break"></div>
  <h3>4.5. Modelagem Não Supervisionada: Análise de Clusters (K-Means) — Pergunta 5</h3>
  <p>
    <strong>Problema de Pesquisa:</strong> Agrupar os profissionais segundo suas atribuições cotidianas, rotinas de trabalho e uso de metodologias no campo de M&A.
  </p>
  <p>
    <strong>Como foi feito:</strong>
  </p>
  <ol>
    <li>
      <strong>Definição do Universo Amostral:</strong> Filtragem exclusiva dos $N = 245$ respondentes do survey que declararam atuar diretamente com rotinas de M&A e evidências.
    </li>
    <li>
      <strong>Espaço Vetorial de Atributos (14 Dimensões Operacionais):</strong> Construção de uma matriz de dados composta por 14 atributos padronizados cobrindo três eixos fundamentais:
      <ul>
        <li><em>Eixo de Intensidade:</em> Atividade principal (binário 0/1), projetos ativos (0/1), atuação internacional (0/1) e tamanho da equipe de trabalho (variável contínua).</li>
        <li><em>Eixo de Ferramental Metodológico:</em> Uso habitual de estatística/econometria, métodos qualitativos, indicadores, sínteses de evidências, ATS, métodos participativos e questionários.</li>
        <li><em>Eixo de Impacto e Disseminação:</em> Comunicação orientada a tomadores de decisão (0/1), divulgação para a sociedade civil (0/1) e realização de capacitação contínua recente (0/1).</li>
      </ul>
    </li>
    <li>
      <strong>Padronização Escalar Z-Score (StandardScaler):</strong> Como a variável "tamanho da equipe" possui escala numérica contínua (1 a 50 pessoas) e as demais são variáveis binárias (0 ou 1), a aplicação direta da distância euclidiana causaria distorção artificial, fazendo com que o tamanho da equipe dominasse o algoritmo. Aplicou-se a padronização z-score em todas as 14 dimensões:
      <div class="formula-box">
        z_i = (x_i - &mu;_i) / &sigma;_i
      </div>
      Onde $\mu_i$ é a média aritmética e $\sigma_i$ é o desvio-padrão amostral do atributo $i$.
    </li>
    <li>
      <strong>Parametrização do Algoritmo K-Means:</strong>
      <div class="code-block">
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_features)

kmeans = KMeans(
    n_clusters=3,
    init='k-means++',      # Inicialização inteligente para evitar mínimos locais
    n_init=20,            # 20 execuções independentes com diferentes centroides
    max_iter=300,         # Limite máximo de convergência
    tol=1e-4,             # Tolerância relativa de parada
    random_state=42       # Garantia de reprodutibilidade estrita
)
cluster_labels = kmeans.fit_predict(X_scaled)
      </div>
    </li>
    <li>
      <strong>Caracterização das Centroides dos 3 Perfis Encontrados:</strong>
      <ul>
        <li><strong>Cluster 1 (13,1% - 32 prof.):</strong> <em>Especialistas em ATS e Síntese de Evidências em Grandes Equipes.</em> 100% aplicam Avaliação de Tecnologias em Saúde (ATS), 68,8% fazem síntese, atuam em equipes médias de 8,7 pessoas e apresentam 31,3% de internacionalização.</li>
        <li><strong>Cluster 2 (37,1% - 91 prof.):</strong> <em>Avaliadores Ocasionais / Prática Periférica.</em> Apenas 26,4% têm M&A como atividade principal, menor complexidade instrumental (apenas 19,8% usam estatística e 38,5% indicadores) e equipes reduzidas (4,4 pessoas).</li>
        <li><strong>Cluster 3 (49,8% - 122 prof.):</strong> <em>Núcleo Multimetodológico de Alta Intensidade.</em> 75,4% têm M&A como dedicação principal, 94,3% possuem projetos em andamento, dominam múltiplos métodos (78,7% indicadores, 72,1% surveys, 65,6% qualitativo, 63,9% estatística) e 90,2% dialogam ativamente com decisores de governo.</li>
      </ul>
    </li>
  </ol>

  <!-- 4.6 INSIGHTS ADICIONAIS -->
  <h3>4.6. Cruzamentos Multivariados e Análise de Interseccionalidade (Insights Aplicados)</h3>
  <p>
    A partir da validação dos dados suplementares, realizaram-se tabulações cruzadas de alta relevância para a equidade e gestão pública:
  </p>
  <ul>
    <li><strong>Interseccionalidade de Gênero nos Clusters:</strong> O teste revelou que a liderança feminina predomina em todas as vertentes, atingindo ápice no Cluster 1 de ATS e Síntese, onde <strong>75,0% das especialistas são mulheres</strong>.</li>
    <li><strong>Afunilamento Étnico-Racial:</strong> Cruzando raça autodeclarada e titulação acadêmica, evidenciou-se que a proporção de pessoas brancas salta de 58% na graduação para <strong>mais de 73% no doutorado e pós-doutorado</strong>. No Cluster 3 (núcleo duro de maior prestígio e remuneração), <strong>71,3% são brancos</strong>, enquanto profissionais pardos concentram-se no Cluster 2 (34,1% - prática periférica).</li>
    <li><strong>Interiorização Federativa e Logística:</strong> O cruzamento entre localidade e modalidade provou que, entre os participantes de fora do DF, <strong>86,9% dependeram do formato Online</strong> para ter acesso ao evento, demonstrando a centralidade da transmissão virtual.</li>
    <li><strong>O Abismo da Comunicação Pública:</strong> Análise de frequências comparadas evidenciou que 73,5% dos avaliadores comunicam para governantes, mas apenas <strong>33,1% divulgam para a sociedade civil</strong> e público em geral, revelando uma barreira na popularização das evidências.</li>
  </ul>

  <!-- SEÇÃO 5: ENGENHARIA DE ARTEFATOS E ENTREGÁVEIS -->
  <div class="page-break"></div>
  <h2>5. Engenharia de Artefatos, Diagramação e Publicação</h2>
  <p>
    Para garantir a difusão completa dos achados para múltiplos perfis de usuários (pesquisadores, tomadores de decisão e analistas de dados), o projeto gerou uma suíte integrada de 7 entregáveis construídos via automação:
  </p>

  <div class="avoid-break">
    <table>
      <thead>
        <tr>
          <th>Entregável Gerado</th>
          <th>Formato</th>
          <th>Ferramenta de Geração</th>
          <th>Propósito e Audiência</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Relatório Técnico Oficial</strong></td>
          <td>PDF (8 pág.)</td>
          <td>Playwright Chromium + Matplotlib</td>
          <td>Publicação oficial exaustiva contendo gráficos vetoriais, testes de hipóteses e diretrizes estratégicas.</td>
        </tr>
        <tr>
          <td><strong>Policy Brief Executivo</strong></td>
          <td>PDF (2 pág.)</td>
          <td>Playwright Chromium</td>
          <td>Documento ultracondensado formatado para leitura rápida por ministros, secretários e dirigentes públicos.</td>
        </tr>
        <tr>
          <td><strong>Manual da Planilha Consolidada</strong></td>
          <td>PDF (3 pág.)</td>
          <td>Playwright Chromium</td>
          <td>Dicionário formal de dados, regras de negócio e guia de navegação das 9 abas da planilha Excel.</td>
        </tr>
        <tr>
          <td><strong>Relatório de Metodologia e Ferramentas</strong></td>
          <td>PDF (6 pág.)</td>
          <td>Playwright Chromium</td>
          <td>Este documento, detalhando todas as tecnologias, equações matemáticas e algoritmos de análise.</td>
        </tr>
        <tr>
          <td><strong>Planilha Excel Consolidada</strong></td>
          <td>XLSX (9 abas)</td>
          <td>pandas + openpyxl</td>
          <td>Base analítica estilizada no padrão corporativo Navy (#0C182B), com autoajuste de largura e zebra striping.</td>
        </tr>
        <tr>
          <td><strong>Apresentação Executiva</strong></td>
          <td>PPTX (10 slides)</td>
          <td>python-pptx</td>
          <td>Slides em padrão widescreen 16:9 prontos para reuniões de diretoria, palestras e conferências.</td>
        </tr>
        <tr>
          <td><strong>Painel Analítico Web</strong></td>
          <td>HTML5 / SPA</td>
          <td>Tailwind CSS + Chart.js v4</td>
          <td>Aplicação interativa responsiva com 7 abas, filtros dinâmicos e gráficos em tempo real no navegador.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- SEÇÃO 6: REPRODUTIBILIDADE E AUDITORIA -->
  <h2>6. Reprodutibilidade, Auditoria e Governança no Git</h2>
  <p>
    Todo o código-fonte, bases de dados estruturadas e documentações técnicas encontram-se hospedados e versionados no repositório oficial do GitHub:
  </p>
  <div class="callout callout-green">
    <div class="callout-title">Repositório Oficial do Projeto</div>
    <strong>URL Remota:</strong> <a href="https://github.com/glau234/dados_ma_denise.git" style="color: #047857; text-decoration: underline;">https://github.com/glau234/dados_ma_denise.git</a><br>
    <strong>Branch Padrão:</strong> <code>main</code> | <strong>Rastreamento:</strong> Commits convencionais e sincronização automatizada
  </div>

  <h3>6.1. Como Reproduzir Toda a Análise a partir do Terminal</h3>
  <p>
    Qualquer pesquisador ou auditor pode reproduzir 100% dos resultados analíticos e gerar novamente todos os arquivos e PDFs executando a seguinte sequência de comandos no terminal:
  </p>

  <div class="code-block">
# 1. Clonar o repositório
git clone https://github.com/glau234/dados_ma_denise.git
cd dados_ma_denise

# 2. Instalar dependências científicas
pip install pandas numpy scikit-learn prince scipy openpyxl python-pptx playwright matplotlib seaborn
playwright install chromium

# 3. Executar o pipeline analítico completo
python generate_analysis.py       # Mineração estatística, pareamento, ACM e K-Means -> gera analise_dados_completa.json
python build_excel_summary.py     # Cria a planilha Excel consolidada de 9 abas (Relatorio_Tabelas_Consolidadas_MA_2024.xlsx)
python generate_pdf_report.py     # Gera o Relatório Oficial de 8 páginas (Relatorio_Completo_Monitoramento_Avaliacao_2024.pdf)
python generate_policy_brief.py   # Gera o Policy Brief de 2 páginas (Policy_Brief_Executivo_MA_2024.pdf)
python generate_manual_pdf.py     # Gera o Manual da Planilha em PDF (Manual_Estrutura_Planilha_Excel_MA_2024.pdf)
python generate_methodology_pdf.py# Gera o Relatório de Metodologia em PDF
python build_presentation.py      # Gera os slides PowerPoint (Apresentacao_Executiva_Monitoramento_Avaliacao_2024.pptx)
python build_html_dashboard.py    # Atualiza o painel web interativo (painel_analise_evidencias.html)
  </div>

  <div class="avoid-break" style="margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 14px;">
    <p style="font-size: 8pt; color: #64748b; text-align: center; margin: 0;">
      Relatório Técnico de Metodologia e Ferramentas • Projeto de Pesquisa em Monitoramento e Avaliação (2024) • Antigravity AI Data Analytics Framework
    </p>
  </div>

</body>
</html>
"""

# Salvar HTML temporário
html_temp_path = 'temp_relatorio_metodologia.html'
with open(html_temp_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML base do relatório metodológico gerado com sucesso.")

# Converter para PDF via Playwright
pdf_output_path = os.path.abspath('Relatorio_Metodologia_Ferramentas_Analise_2024.pdf')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until='networkidle')
    page.pdf(
        path=pdf_output_path,
        format='A4',
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size: 7.5pt; color: #94a3b8; width: 100%; text-align: right; padding-right: 16mm; font-family: Helvetica, Arial, sans-serif;">Relatório de Metodologia e Ferramentas • M&A e Evidências 2024</div>',
        footer_template='<div style="font-size: 7.5pt; color: #94a3b8; width: 100%; text-align: center; font-family: Helvetica, Arial, sans-serif;">Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>',
        margin={
            'top': '18mm',
            'bottom': '20mm',
            'left': '16mm',
            'right': '16mm'
        }
    )
    browser.close()

# Remover arquivo temporário HTML
if os.path.exists(html_temp_path):
    os.remove(html_temp_path)

print(f"Relatório de Metodologia e Ferramentas gerado com sucesso em: {pdf_output_path}")
