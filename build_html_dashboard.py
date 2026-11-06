# -*- coding: utf-8 -*-
import json

with open('analise_dados_completa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel Analítico: Avaliação e Evidências em Políticas Públicas (2024)</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
    }}
    .tab-btn.active {{
      border-color: #2563eb;
      color: #1d4ed8;
      background-color: #eff6ff;
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- Header Superior -->
  <header class="bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-950 text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="bg-blue-500 text-white text-xs font-bold px-2.5 py-0.5 rounded-full tracking-wider uppercase">Relatório Oficial de Pesquisa</span>
            <span class="text-blue-200 text-xs">Ano Base: 2024</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight mt-1 text-white">
            Redes de Monitoramento, Avaliação e Evidências em Políticas Públicas
          </h1>
          <p class="text-sm text-slate-300">
            Análise integrada entre inscritos em eventos de evidências e o survey nacional de escuta
          </p>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="window.print()" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700 transition shadow-sm">
            🖨️ Imprimir / Salvar PDF
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- Métricas Rápidas (Cards de Destaque) -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-2 pt-6 w-full">
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 hover:shadow transition">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Inscrições em Eventos</div>
        <div class="text-2xl font-bold text-slate-900 mt-1">1.128</div>
        <div class="text-xs text-blue-600 mt-0.5 font-medium">1.086 indivíduos únicos</div>
      </div>
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 hover:shadow transition">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Respondentes Survey</div>
        <div class="text-2xl font-bold text-blue-700 mt-1">521</div>
        <div class="text-xs text-slate-500 mt-0.5">245 com prática profunda</div>
      </div>
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 hover:shadow transition">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Taxa de Renovação</div>
        <div class="text-2xl font-bold text-emerald-600 mt-1">89,1%</div>
        <div class="text-xs text-emerald-700 mt-0.5 font-medium">Novos no 2º evento</div>
      </div>
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 hover:shadow transition">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Recorrência nos Eventos</div>
        <div class="text-2xl font-bold text-amber-600 mt-1">3,87%</div>
        <div class="text-xs text-amber-700 mt-0.5">Apenas 42 pessoas em ambos</div>
      </div>
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 hover:shadow transition">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Maioria Feminina</div>
        <div class="text-2xl font-bold text-indigo-600 mt-1">60,2%</div>
        <div class="text-xs text-slate-500 mt-0.5">63,0% no Survey</div>
      </div>
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200/80 hover:shadow transition">
        <div class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Comunicação Decisores</div>
        <div class="text-2xl font-bold text-purple-600 mt-1">73,5%</div>
        <div class="text-xs text-rose-500 mt-0.5 font-medium">33,1% p/ público geral</div>
      </div>
    </div>
  </div>

  <!-- Navegação por Abas -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 w-full">
    <div class="flex overflow-x-auto border-b border-slate-200 gap-1 bg-white p-1 rounded-xl shadow-sm border">
      <button onclick="switchTab('tab-visao-geral')" id="btn-tab-visao-geral" class="tab-btn active px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        📊 Visão Geral Executiva
      </button>
      <button onclick="switchTab('tab-q1')" id="btn-tab-q1" class="tab-btn px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        🔍 P1: Survey x Eventos
      </button>
      <button onclick="switchTab('tab-q2')" id="btn-tab-q2" class="tab-btn px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        🔄 P2: Recorrência vs Renovação
      </button>
      <button onclick="switchTab('tab-q3')" id="btn-tab-q3" class="tab-btn px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        🎓 P3: Análise de Correspondência (ACM)
      </button>
      <button onclick="switchTab('tab-q4')" id="btn-tab-q4" class="tab-btn px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        🗺️ P4: Distribuição Espacial e Setorial
      </button>
      <button onclick="switchTab('tab-q5')" id="btn-tab-q5" class="tab-btn px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        👥 P5: Análise de Clusters
      </button>
      <button onclick="switchTab('tab-insights')" id="btn-tab-insights" class="tab-btn px-4 py-2.5 text-xs sm:text-sm font-semibold rounded-lg border-b-2 border-transparent transition whitespace-nowrap">
        💡 Insights Extras para Validação
      </button>
    </div>
  </div>

  <!-- Conteúdo das Abas -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">

    <!-- ABA 0: VISÃO GERAL EXECUTIVA -->
    <section id="tab-visao-geral" class="tab-content space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <h2 class="text-xl font-bold text-slate-900 border-b pb-4 mb-4 flex items-center gap-2">
          <span>📋</span> Sumário Executivo das 5 Perguntas de Pesquisa
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="border-l-4 border-blue-500 pl-4 space-y-1">
            <span class="text-xs font-bold uppercase text-blue-600 tracking-wider">Pergunta 1</span>
            <h3 class="font-bold text-slate-800">Os respondentes do survey são os mesmos dos eventos?</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              <strong>Não.</strong> O survey alcançou uma comunidade substancialmente externa aos eventos. Dos 226 respondentes identificados, <strong>73,5% (166 pessoas)</strong> não participaram de nenhum dos eventos, enquanto <strong>26,5% (60 pessoas)</strong> estiveram em pelo menos um evento. Além disso, 295 participantes responderam de forma estritamente anônima.
            </p>
          </div>
          <div class="border-l-4 border-emerald-500 pl-4 space-y-1">
            <span class="text-xs font-bold uppercase text-emerald-600 tracking-wider">Pergunta 2</span>
            <h3 class="font-bold text-slate-800">Recorrência ou Renovação de profissionais?</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              <strong>Alta renovação e atração de novos profissionais.</strong> No segundo evento, <strong>89,1% dos participantes eram estreantes</strong> (344 de 386). A taxa de sobreposição direta entre ambos os eventos foi de apenas <strong>3,87%</strong> do universo total de 1.086 indivíduos únicos (42 pessoas).
            </p>
          </div>
          <div class="border-l-4 border-purple-500 pl-4 space-y-1">
            <span class="text-xs font-bold uppercase text-purple-600 tracking-wider">Pergunta 3</span>
            <h3 class="font-bold text-slate-800">Relação Tempo, Titulação e Formação (ACM)</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              A Análise de Correspondência Múltipla revelou dois polos contrastantes: o <strong>Polo Acadêmico-Sênior</strong> (Doutores e Pós-doutores, >10 a 20 anos de experiência, atuando como Pesquisadores) vs o <strong>Polo de Gestão/Prática Aplicada</strong> (Especialistas e Mestres, tempo de atuação mais recente de até 5 anos, na gestão e ponta). Associação altamente significante (p &lt; 0,001).
            </p>
          </div>
          <div class="border-l-4 border-amber-500 pl-4 space-y-1">
            <span class="text-xs font-bold uppercase text-amber-600 tracking-wider">Pergunta 4</span>
            <h3 class="font-bold text-slate-800">Distribuição Espacial, Esfera e Área Setorial</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Forte concentração geográfica no <strong>Distrito Federal (~45%)</strong> e na esfera <strong>Federal (43,2%)</strong>, seguida do Sudeste (23,9%) e Nordeste (12,2%). Na distribuição setorial, quase metade é da <strong>Saúde (49,4%)</strong>, havendo nítida correlação: esferas municipais e estaduais são majoritariamente da Saúde (67% e 56%), enquanto a esfera federal abriga maior diversidade de políticas públicas.
            </p>
          </div>
          <div class="border-l-4 border-rose-500 pl-4 space-y-1 md:col-span-2">
            <span class="text-xs font-bold uppercase text-rose-600 tracking-wider">Pergunta 5</span>
            <h3 class="font-bold text-slate-800">Perfis Profissionais segundo Atribuições Cotidianas (Clusters)</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              O modelo de clustering identificou 3 perfis funcionais bem estruturados no campo de M&A:
              <br>• <strong>Cluster 1 (13,1%):</strong> <em>Especialistas em ATS e Síntese de Evidências</em> (100% atuam com ATS, 69% com síntese, grandes equipes de 8,7 pessoas);
              <br>• <strong>Cluster 2 (37,1%):</strong> <em>Avaliadores Ocasionais / Prática Periférica</em> (M&A como atividade secundária, menor complexidade metodológica e pouca disseminação);
              <br>• <strong>Cluster 3 (49,8%):</strong> <em>Núcleo Multimetodológico de Alta Intensidade</em> (75% dedicação principal, 94% projetos ativos, múltiplos métodos estatísticos e participativos, 90% divulgam para decisores).
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ABA 1: PERGUNTA 1 -->
    <section id="tab-q1" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div class="flex flex-col md:flex-row md:items-center justify-between border-b pb-4 mb-6 gap-2">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Pergunta 1: As pessoas que responderam ao survey são as mesmas dos eventos?</h2>
            <p class="text-sm text-slate-500">Cruzamento determinístico por CPF, E-mail normalizado e Nome completo</p>
          </div>
          <span class="inline-block bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full font-semibold">
            N = 521 Survey | 1.128 Inscrições em Eventos
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-5 space-y-4">
            <div class="bg-slate-50 rounded-xl p-5 border border-slate-200 space-y-3">
              <h3 class="font-bold text-slate-800 text-sm uppercase tracking-wider">Estrutura de Identificação da Amostra</h3>
              <div class="flex justify-between items-center text-sm border-b pb-2">
                <span class="text-slate-600">Total de Respondentes no Survey:</span>
                <span class="font-bold text-slate-900">{data['q1']['total_survey']} (100%)</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b pb-2">
                <span class="text-slate-600">Respostas Anônimas (sem identificação):</span>
                <span class="font-bold text-slate-500">{data['q1']['anon']} (56,6%)</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-slate-600">Respondentes Identificados (contatos válidos):</span>
                <span class="font-bold text-blue-600">{data['q1']['identified']} (43,4%)</span>
              </div>
            </div>

            <div class="bg-blue-50/70 rounded-xl p-5 border border-blue-200 space-y-3">
              <h3 class="font-bold text-blue-900 text-sm uppercase tracking-wider">Cruzamento dos 226 Identificados</h3>
              <div class="flex justify-between items-center text-sm border-b border-blue-200/60 pb-2">
                <span class="text-slate-700">Presentes no Evento 1 (Evidências):</span>
                <span class="font-bold text-slate-900">{data['q1']['e1_match']} (20,8%)</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b border-blue-200/60 pb-2">
                <span class="text-slate-700">Presentes no Evento 2 (Práticas):</span>
                <span class="font-bold text-slate-900">{data['q1']['e2_match']} (7,5%)</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b border-blue-200/60 pb-2">
                <span class="text-slate-700">Presentes em AMBOS os eventos:</span>
                <span class="font-bold text-slate-900">{data['q1']['both_match']} (1,8%)</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b border-blue-200/60 pb-2">
                <span class="text-slate-900 font-semibold">Total com Presença em Evento(s):</span>
                <span class="font-bold text-emerald-700">{data['q1']['any_match']} (26,5%)</span>
              </div>
              <div class="flex justify-between items-center text-sm pt-1">
                <span class="text-slate-900 font-semibold">Público EXTERNO aos Eventos:</span>
                <span class="font-bold text-rose-600">{data['q1']['external']} (73,5%)</span>
              </div>
            </div>
          </div>

          <div class="lg:col-span-7 bg-white p-4 rounded-xl border border-slate-100 shadow-inner">
            <h4 class="text-sm font-semibold text-slate-700 mb-3 text-center">Distribuição de Correspondência do Público do Survey</h4>
            <div class="h-72">
              <canvas id="chartQ1"></canvas>
            </div>
            <p class="text-xs text-slate-500 text-center mt-3">
              💡 <strong>Conclusão Central:</strong> As pessoas do survey <strong>não são as mesmas</strong> dos eventos em sua maioria. O survey funcionou como um canal aberto de escuta setorial mais amplo, mobilizando 166 profissionais não participantes dos eventos.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ABA 2: PERGUNTA 2 -->
    <section id="tab-q2" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div class="flex flex-col md:flex-row md:items-center justify-between border-b pb-4 mb-6 gap-2">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Pergunta 2: Recorrência ou Renovação de Profissionais nos Eventos?</h2>
            <p class="text-sm text-slate-500">Comparação longitudinal de participação entre o Evento 1 e o Evento 2 (2024)</p>
          </div>
          <span class="inline-block bg-emerald-100 text-emerald-800 text-xs px-3 py-1 rounded-full font-semibold">
            1.086 Indivíduos Únicos
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-6 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                <div class="text-xs text-slate-500 font-bold uppercase">Evento 1 (Evidências)</div>
                <div class="text-2xl font-extrabold text-slate-900 mt-1">{data['q2']['e1_total']}</div>
                <div class="text-xs text-slate-500 mt-1">Inscritos Totais</div>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                <div class="text-xs text-slate-500 font-bold uppercase">Evento 2 (Práticas)</div>
                <div class="text-2xl font-extrabold text-slate-900 mt-1">{data['q2']['e2_total']}</div>
                <div class="text-xs text-slate-500 mt-1">Inscritos Totais</div>
              </div>
            </div>

            <div class="bg-emerald-50/70 rounded-xl p-5 border border-emerald-200 space-y-3">
              <h3 class="font-bold text-emerald-950 text-sm uppercase tracking-wider">Indicadores de Fidelidade e Atração</h3>
              <div class="flex justify-between items-center text-sm border-b border-emerald-200/60 pb-2">
                <span class="text-slate-700">Pessoas presentes em AMBOS os eventos:</span>
                <span class="font-bold text-slate-900">{data['q2']['overlap']} indivíduos</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b border-emerald-200/60 pb-2">
                <span class="text-slate-700">Taxa de Recorrência no Evento 2:</span>
                <span class="font-bold text-amber-700">{data['q2']['recurrence_rate_e2']}%</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b border-emerald-200/60 pb-2">
                <span class="text-slate-700">Taxa de Renovação no Evento 2:</span>
                <span class="font-bold text-emerald-700 text-base">{data['q2']['renewal_rate']}%</span>
              </div>
              <div class="flex justify-between items-center text-sm border-b border-emerald-200/60 pb-2">
                <span class="text-slate-700">Retenção do Evento 1 no Evento 2:</span>
                <span class="font-bold text-slate-900">{data['q2']['recurrence_rate_e1']}% (42 de 742)</span>
              </div>
              <div class="flex justify-between items-center text-sm pt-1">
                <span class="text-slate-700 font-medium">Recorrência sobre a Comunidade Total:</span>
                <span class="font-bold text-slate-900">{data['q2']['recurrence_rate_total']}% (42 de 1.086)</span>
              </div>
            </div>
          </div>

          <div class="lg:col-span-6 bg-white p-4 rounded-xl border border-slate-100 shadow-inner">
            <h4 class="text-sm font-semibold text-slate-700 mb-3 text-center">Composição do Público no Evento 2 (Práticas em Avaliação)</h4>
            <div class="h-72">
              <canvas id="chartQ2"></canvas>
            </div>
            <p class="text-xs text-slate-500 text-center mt-3">
              💡 <strong>Diagnóstico:</strong> Há uma <strong>expressiva capacidade de atração de novos profissionais</strong> (renovação de ~90%), indicando que a temática prática alcançou novos públicos e setores que não haviam aderido ao evento anterior.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ABA 3: PERGUNTA 3 -->
    <section id="tab-q3" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div class="flex flex-col md:flex-row md:items-center justify-between border-b pb-4 mb-6 gap-2">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Pergunta 3: Relação Tempo de Atuação, Titulação e Formação</h2>
            <p class="text-sm text-slate-500">Análise de Correspondência Múltipla (ACM / MCA) e Testes de Associação Qui-Quadrado</p>
          </div>
          <span class="inline-block bg-purple-100 text-purple-800 text-xs px-3 py-1 rounded-full font-semibold">
            Inércia Total Explicada: {data['q3']['inertia_cum']}% (2D)
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <div class="lg:col-span-7 bg-white p-4 rounded-xl border border-slate-100 shadow-inner">
            <h4 class="text-sm font-semibold text-slate-700 mb-2 text-center">Mapa Perceptual 2D: Coordenadas das Categorias</h4>
            <div class="h-96">
              <canvas id="chartMCA"></canvas>
            </div>
            <div class="flex justify-center gap-4 text-xs mt-3">
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-600 inline-block"></span> Tempo de Atuação</span>
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-purple-600 inline-block"></span> Titulação Acadêmica</span>
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-500 inline-block"></span> Função Profissional</span>
            </div>
          </div>

          <div class="lg:col-span-5 space-y-4">
            <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
              <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Testes de Independência Qui-Quadrado (χ²)</h3>
              <div class="text-xs space-y-2">
                <div class="p-2.5 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-800">Titulação x Função Profissional</div>
                  <div class="text-slate-600">χ² = {data['q3']['chi2_tit_func']['chi2']} | p-valor = {data['q3']['chi2_tit_func']['p']} | gl = {data['q3']['chi2_tit_func']['dof']}</div>
                  <div class="text-emerald-700 font-semibold mt-0.5">Altamente significante (p &lt; 0,001)</div>
                </div>
                <div class="p-2.5 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-800">Tempo de Atuação x Titulação</div>
                  <div class="text-slate-600">χ² = {data['q3']['chi2_tmp_tit']['chi2']} | p-valor = {data['q3']['chi2_tmp_tit']['p']} | gl = {data['q3']['chi2_tmp_tit']['dof']}</div>
                  <div class="text-emerald-700 font-semibold mt-0.5">Altamente significante (p &lt; 0,001)</div>
                </div>
                <div class="p-2.5 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-800">Tempo de Atuação x Função</div>
                  <div class="text-slate-600">χ² = {data['q3']['chi2_tmp_func']['chi2']} | p-valor = {data['q3']['chi2_tmp_func']['p']} | gl = {data['q3']['chi2_tmp_func']['dof']}</div>
                  <div class="text-slate-500 font-medium mt-0.5">Sem significância isolada (p = 0,12)</div>
                </div>
              </div>
            </div>

            <div class="bg-purple-50/70 p-4 rounded-xl border border-purple-200 text-xs text-slate-700 leading-relaxed space-y-2">
              <h4 class="font-bold text-purple-950 uppercase tracking-wider text-xs">Interpretação dos Eixos:</h4>
              <p>
                <strong>Dimensão 1 (15,07% da inércia):</strong> Oposição entre o <em>Polo Acadêmico-Sênior</em> (Doutorado, Pós-doutorado, >10 anos, Pesquisador no lado negativo) e o <em>Polo Gestão/Prática Operacional</em> (Especialização, Graduação, até 5 anos de carreira, na Gestão e Prática no lado positivo).
              </p>
              <p>
                <strong>Dimensão 2 (11,52% da inércia):</strong> Diferencia os <em>Gerentes e Líderes de Equipe</em> (no topo do eixo vertical) em relação aos técnicos executores e à base operacional.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ABA 4: PERGUNTA 4 -->
    <section id="tab-q4" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div class="flex flex-col md:flex-row md:items-center justify-between border-b pb-4 mb-6 gap-2">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Pergunta 4: Distribuição Espacial, Esfera e Área Setorial</h2>
            <p class="text-sm text-slate-500">Mapeamento federativo, esferas de governo e áreas setoriais de políticas públicas</p>
          </div>
          <span class="inline-block bg-amber-100 text-amber-800 text-xs px-3 py-1 rounded-full font-semibold">
            1.128 Inscrições em Eventos
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <h4 class="text-xs font-bold uppercase text-slate-600 mb-3 text-center">Distribuição por Grande Região</h4>
            <div class="h-56">
              <canvas id="chartRegioes"></canvas>
            </div>
          </div>
          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <h4 class="text-xs font-bold uppercase text-slate-600 mb-3 text-center">Esfera de Atuação Declarada</h4>
            <div class="h-56">
              <canvas id="chartEsferas"></canvas>
            </div>
          </div>
          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <h4 class="text-xs font-bold uppercase text-slate-600 mb-3 text-center">Proporção Saúde vs Não-Saúde</h4>
            <div class="h-56">
              <canvas id="chartSaude"></canvas>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white p-5 rounded-xl border border-slate-200">
            <h4 class="font-bold text-slate-900 text-sm mb-3">Top Unidades Federativas de Origem (Eventos)</h4>
            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left text-slate-600">
                <thead class="bg-slate-100 uppercase text-slate-700">
                  <tr>
                    <th class="p-2">UF</th>
                    <th class="p-2">Inscrições</th>
                    <th class="p-2">% do Total</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  {"".join([f"<tr><td class='p-2 font-bold text-slate-800'>{uf}</td><td class='p-2'>{cnt}</td><td class='p-2'>{cnt/1128*100:.1f}%</td></tr>" for uf, cnt in list(data['q4']['uf_top'].items())[:8]])}
                </tbody>
              </table>
            </div>
          </div>

          <div class="bg-white p-5 rounded-xl border border-slate-200">
            <h4 class="font-bold text-slate-900 text-sm mb-3">Áreas Setoriais Temáticas no Survey</h4>
            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left text-slate-600">
                <thead class="bg-slate-100 uppercase text-slate-700">
                  <tr>
                    <th class="p-2">Temática de Política Pública</th>
                    <th class="p-2">Menções</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  {"".join([f"<tr><td class='p-2 font-semibold text-slate-800'>{tem}</td><td class='p-2 font-bold text-blue-600'>{cnt}</td></tr>" for tem, cnt in data['q4']['survey_tematicas'].items()])}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ABA 5: PERGUNTA 5 -->
    <section id="tab-q5" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div class="flex flex-col md:flex-row md:items-center justify-between border-b pb-4 mb-6 gap-2">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Pergunta 5: Perfis Profissionais segundo Atribuições Cotidianas</h2>
            <p class="text-sm text-slate-500">Análise de Clusters (K-Means) com 14 variáveis operacionais e rotinas de trabalho</p>
          </div>
          <span class="inline-block bg-rose-100 text-rose-800 text-xs px-3 py-1 rounded-full font-semibold">
            3 Clusters Bem Definidos (N = 245)
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-6">
          <div class="lg:col-span-7 bg-white p-4 rounded-xl border border-slate-100 shadow-inner">
            <h4 class="text-sm font-semibold text-slate-700 mb-3 text-center">Comparativo de Métodos e Práticas nos 3 Clusters</h4>
            <div class="h-80">
              <canvas id="chartClusters"></canvas>
            </div>
          </div>

          <div class="lg:col-span-5 space-y-3">
            <div class="p-4 rounded-xl border border-blue-200 bg-blue-50/60">
              <div class="flex items-center justify-between">
                <span class="font-bold text-blue-900 text-sm">Cluster 1: Especialistas em ATS e Síntese</span>
                <span class="text-xs bg-blue-200 text-blue-800 font-bold px-2 py-0.5 rounded">{data['q5']['counts']['0']} profissionais (13,1%)</span>
              </div>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                <strong>100%</strong> usam Avaliação de Tecnologias em Saúde (ATS); <strong>69%</strong> usam síntese de evidências; atuam em grandes equipes (média <strong>8,7 pessoas</strong>); alta internacionalização (31%) e foco na decisão pública (78%).
              </p>
            </div>

            <div class="p-4 rounded-xl border border-slate-300 bg-slate-50">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-900 text-sm">Cluster 2: Avaliadores Ocasionais</span>
                <span class="text-xs bg-slate-200 text-slate-700 font-bold px-2 py-0.5 rounded">{data['q5']['counts']['1']} profissionais (37,1%)</span>
              </div>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                M&A é atividade <strong>secundária</strong> para 74%; equipes menores (4,4 pessoas); baixo uso de métodos complexos (20% estatística, 38% indicadores); baixa disseminação para decisores (49%).
              </p>
            </div>

            <div class="p-4 rounded-xl border border-emerald-300 bg-emerald-50/60">
              <div class="flex items-center justify-between">
                <span class="font-bold text-emerald-950 text-sm">Cluster 3: Núcleo Multimetodológico</span>
                <span class="text-xs bg-emerald-200 text-emerald-800 font-bold px-2 py-0.5 rounded">{data['q5']['counts']['2']} profissionais (49,8%)</span>
              </div>
              <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                M&A como atividade <strong>principal (75%)</strong>; <strong>94% com projetos ativos</strong>; amplo domínio multimetodológico (79% indicadores, 72% questionários, 66% qualitativo, 64% estatística); <strong>90% comunicam com decisores</strong>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ABA 6: INSIGHTS ADICIONAIS -->
    <section id="tab-insights" class="tab-content hidden space-y-6">
      <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm border border-slate-200">
        <div class="flex flex-col md:flex-row md:items-center justify-between border-b pb-4 mb-6 gap-2">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Insights Adicionais Relevantes (Para Validação)</h2>
            <p class="text-sm text-slate-500">Achados suplementares de demografia, diversidade, formatos e disseminação</p>
          </div>
          <span class="inline-block bg-indigo-100 text-indigo-800 text-xs px-3 py-1 rounded-full font-semibold">
            Subsídios para Gestão
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Card 1: Gênero -->
          <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
            <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
              <span>👩‍💼</span> Predomínio Feminino no Campo
            </h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Tanto no Evento 1 (<strong>{data['insights']['sexo_e1'].get('Feminino', 60.2)}%</strong>) quanto no Survey (<strong>{data['insights']['genero_survey'].get('Mulher cis', 63.0)}%</strong>), as mulheres constituem a expressiva maioria dos profissionais de M&A e políticas informadas por evidências no Brasil.
            </p>
            <div class="text-xs font-semibold text-indigo-700 bg-indigo-50 p-2.5 rounded border border-indigo-200">
              Taxa Feminina: ~60% a 63%
            </div>
          </div>

          <!-- Card 2: Raça/Etnia -->
          <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
            <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
              <span>🏛️</span> Sub-representação Racial
            </h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              No Survey, <strong>{data['insights']['raca_survey'].get('Branca', 66.5)}%</strong> autodeclaram-se brancos, <strong>{data['insights']['raca_survey'].get('Parda', 24.9)}%</strong> pardos e apenas <strong>{data['insights']['raca_survey'].get('Preta', 5.7)}%</strong> pretos. Em posições com doutorado e pós-doutorado, a proporção de brancos ultrapassa 73%.
            </p>
            <div class="text-xs font-semibold text-amber-800 bg-amber-50 p-2.5 rounded border border-amber-200">
              Brancos: 66,5% | Pardos e Pretos: 30,6%
            </div>
          </div>

          <!-- Card 3: Abismo de Comunicação -->
          <div class="bg-slate-50 p-5 rounded-xl border border-slate-200 space-y-3">
            <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
              <span>📢</span> O "Abismo da Comunicação Pública"
            </h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Enquanto <strong>{data['insights']['diss_decisores_pct']}%</strong> dos profissionais divulgam ativamente suas pesquisas para tomadores de decisão (sumários executivos e seminários), apenas <strong>{data['insights']['diss_geral_pct']}%</strong> comunicam para o público geral (redes, blogs, imprensa).
            </p>
            <div class="text-xs font-semibold text-rose-800 bg-rose-50 p-2.5 rounded border border-rose-200">
              Gargalo na tradução de conhecimento p/ sociedade
            </div>
          </div>
        </div>

        <div class="bg-blue-50/70 p-5 rounded-xl border border-blue-200 text-xs text-slate-700 leading-relaxed space-y-2 mt-4">
          <h4 class="font-bold text-blue-900 uppercase tracking-wider text-xs">Outros Destaques Observados:</h4>
          <ul class="list-disc list-inside space-y-1">
            <li><strong>Preferência pela Modalidade Online:</strong> No Evento 1, mais de 53,6% dos inscritos optaram explicitamente pelo acompanhamento online, frente a apenas 24,1% presencial (relação de mais de 2 para 1), reforçando o alcance nacional e custo-efetividade do modelo híbrido.</li>
            <li><strong>Estabilidade Institucional dos Especialistas:</strong> 73,5% dos respondentes ativos são servidores públicos estatutários ou empregados públicos estáveis, e 71,0% não mudaram de instituição nos últimos 5 anos.</li>
            <li><strong>Capacitação Contínua:</strong> 63,7% realizaram capacitação recente em M&A nos últimos 3 anos, com predominância esmagadora do formato autoinstrucional / EAD assíncrono (>65%).</li>
          </ul>
        </div>
      </div>
    </section>

  </main>

  <footer class="bg-slate-900 text-slate-400 py-6 text-xs text-center border-t border-slate-800 mt-12">
    <div class="max-w-7xl mx-auto px-4">
      Painel Gerado para Análise de Dados de Monitoramento, Avaliação e Evidências • Ano 2024 • Antigravity AI
    </div>
  </footer>

  <!-- Scripts Interativos e Gráficos -->
  <script>
    // Gerenciador de Abas
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      const target = document.getElementById(tabId);
      if(target) target.classList.remove('hidden');
      
      const btn = document.getElementById('btn-' + tabId);
      if(btn) btn.classList.add('active');
    }}

    // Dados embutidos
    const rawData = {json.dumps(data)};

    // Chart Q1
    new Chart(document.getElementById('chartQ1'), {{
      type: 'doughnut',
      data: {{
        labels: ['Externos ao Evento (73,5%)', 'Presentes em Eventos (26,5%)'],
        datasets: [{{
          data: [rawData.q1.external, rawData.q1.any_match],
          backgroundColor: ['#f43f5e', '#10b981'],
          borderWidth: 2
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ position: 'bottom' }}
        }}
      }}
    }});

    // Chart Q2
    new Chart(document.getElementById('chartQ2'), {{
      type: 'doughnut',
      data: {{
        labels: ['Novos Profissionais (89,1%)', 'Participantes Recorrentes (10,9%)'],
        datasets: [{{
          data: [rawData.q2.e2_new, rawData.q2.overlap],
          backgroundColor: ['#059669', '#d97706'],
          borderWidth: 2
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ position: 'bottom' }}
        }}
      }}
    }});

    // Chart MCA Scatter
    const mcaPoints = rawData.q3.points.map(p => ({{
      x: p.dim1,
      y: p.dim2,
      label: p.category,
      variable: p.variable
    }}));

    const colorMap = {{
      'faixa_tempo': '#2563eb',
      'titulacao_clean': '#9333ea',
      'funcao_clean': '#f59e0b'
    }};

    new Chart(document.getElementById('chartMCA'), {{
      type: 'scatter',
      data: {{
        datasets: [
          {{
            label: 'Tempo de Atuação',
            data: mcaPoints.filter(p => p.variable === 'faixa_tempo'),
            backgroundColor: '#2563eb',
            pointRadius: 7
          }},
          {{
            label: 'Titulação Acadêmica',
            data: mcaPoints.filter(p => p.variable === 'titulacao_clean'),
            backgroundColor: '#9333ea',
            pointRadius: 7
          }},
          {{
            label: 'Função Profissional',
            data: mcaPoints.filter(p => p.variable === 'funcao_clean'),
            backgroundColor: '#f59e0b',
            pointRadius: 7
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
          x: {{
            title: {{ display: true, text: 'Dimensão 1 (15,07% Inércia) - Acadêmico/Pesquisa (-) vs Prática/Gestão (+)' }},
            grid: {{ color: '#e2e8f0' }}
          }},
          y: {{
            title: {{ display: true, text: 'Dimensão 2 (11,52% Inércia) - Liderança/Gerência (+) vs Base Técnica (-)' }},
            grid: {{ color: '#e2e8f0' }}
          }}
        }},
        plugins: {{
          tooltip: {{
            callbacks: {{
              label: function(ctx) {{
                return ctx.raw.label + ' (' + ctx.parsed.x.toFixed(2) + ', ' + ctx.parsed.y.toFixed(2) + ')';
              }}
            }}
          }}
        }}
      }}
    }});

    // Chart Regioes
    new Chart(document.getElementById('chartRegioes'), {{
      type: 'bar',
      data: {{
        labels: Object.keys(rawData.q4.regioes),
        datasets: [{{
          label: 'Inscrições',
          data: Object.values(rawData.q4.regioes),
          backgroundColor: '#3b82f6',
          borderRadius: 6
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }}
      }}
    }});

    // Chart Esferas
    new Chart(document.getElementById('chartEsferas'), {{
      type: 'pie',
      data: {{
        labels: Object.keys(rawData.q4.esferas),
        datasets: [{{
          data: Object.values(rawData.q4.esferas),
          backgroundColor: ['#1d4ed8', '#0284c7', '#0d9488', '#16a34a', '#ca8a04', '#dc2626', '#64748b']
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'right' }} }}
      }}
    }});

    // Chart Saude
    new Chart(document.getElementById('chartSaude'), {{
      type: 'doughnut',
      data: {{
        labels: ['Saúde (49,4%)', 'Outras Políticas Públicas (50,6%)'],
        datasets: [{{
          data: [rawData.q4.saude['Sim'] || 557, rawData.q4.saude['Nao'] || 571],
          backgroundColor: ['#0284c7', '#64748b']
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'bottom' }} }}
      }}
    }});

    // Chart Clusters
    const clusterLabels = ['Estatística', 'Qualitativo', 'Indicadores', 'Síntese', 'ATS', 'Participativo', 'Questionários', 'Decisores'];
    const c0 = rawData.q5.means['0'];
    const c1 = rawData.q5.means['1'];
    const c2 = rawData.q5.means['2'];

    new Chart(document.getElementById('chartClusters'), {{
      type: 'bar',
      data: {{
        labels: clusterLabels,
        datasets: [
          {{
            label: 'Cluster 1: ATS e Síntese',
            data: [c0.met_estatistica, c0.met_qualitativa, c0.met_indicadores, c0.met_sintese, c0.met_ats, c0.met_participativa, c0.met_questionarios, c0.diss_decisores],
            backgroundColor: '#3b82f6'
          }},
          {{
            label: 'Cluster 2: Ocasionais',
            data: [c1.met_estatistica, c1.met_qualitativa, c1.met_indicadores, c1.met_sintese, c1.met_ats, c1.met_participativa, c1.met_questionarios, c1.diss_decisores],
            backgroundColor: '#94a3b8'
          }},
          {{
            label: 'Cluster 3: Núcleo Multimetodológico',
            data: [c2.met_estatistica, c2.met_qualitativa, c2.met_indicadores, c2.met_sintese, c2.met_ats, c2.met_participativa, c2.met_questionarios, c2.diss_decisores],
            backgroundColor: '#10b981'
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
          y: {{
            beginAtZero: true,
            max: 1,
            ticks: {{
              callback: function(val) {{ return (val * 100) + '%'; }}
            }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""

with open('painel_analise_evidencias.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Painel interativo HTML gerado com sucesso em d:\\dados_ma_denise\\painel_analise_evidencias.html")

