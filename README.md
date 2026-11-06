# Redes de Monitoramento, Avaliação e Evidências em Políticas Públicas (2024)

Repositório com a análise estatística, econométrica e qualitativa integrada dos dados de participantes de eventos e respondentes do survey nacional de escuta no campo de Monitoramento e Avaliação (M&A) e Políticas Públicas Informadas por Evidências (PIE) no Brasil.

---

## 📋 Bases de Dados Analisadas
1. **`Inscritos-Politicas-Publicas-Informadas-por-Evidencias-2024.xlsx`** — 742 inscritos no evento nacional de Políticas por Evidências.
2. **`Inscritos-Praticas-em-Avaliacao-e-Evidencias-para-Politicas-Publicas-2024.xlsx`** — 386 inscritos no evento de Práticas em Avaliação.
3. **`Survey-Escuta-Redes-de-Monitoramento-Avaliacao-Politicas-Publicas.xlsx`** — 521 respondentes do questionário nacional de escuta de M&A (245 com prática profunda analisados).

---

## 🎯 Síntese das 5 Perguntas de Pesquisa

1. **Os respondentes do survey são os mesmos que participaram dos eventos?**
   * **Não.** 73,5% dos respondentes identificados do survey (166 pessoas) são externos aos eventos de 2024. Apenas 26,5% (60 pessoas) participaram de pelo menos um evento. O survey funcionou como um canal aberto de escuta setorial muito mais amplo.

2. **Existe uma recorrência da participação nos dois eventos ou renovação de profissionais?**
   * **Forte renovação e atração de novos profissionais.** No Evento 2, **89,1% eram novos participantes** (344 de 386). A sobreposição direta entre ambos os eventos foi de apenas 42 pessoas (taxa de recorrência de **3,87%** sobre a comunidade única de 1.086 indivíduos).

3. **Qual a relação entre tempo de atuação, titulação e formação profissional (ACM)?**
   * A Análise de Correspondência Múltipla (ACM, $\chi^2 = 70,06, p < 0,001$) explicou 26,6% da inércia bidimensional, dividindo o campo entre o **Polo Acadêmico-Sênior** (Doutores e Pós-doutores, >10 a 20 anos de experiência, pesquisadores) e o **Polo Governamental-Operacional** (Especialistas e Mestres, até 5 anos, atuando na gestão pública e na ponta). A gerência atua isolada no topo vertical (+2,75).

4. **Qual a distribuição espacial, esfera de atuação e área setorial de política pública?**
   * **Geografia:** Concentração no Distrito Federal (45,4%) e Centro-Oeste (49,6%), seguidos por Sudeste (23,9% - SP e RJ) e Nordeste (12,2% - BA e CE).
   * **Esfera:** Federal (43,2%), Estadual (19,5%), Academia/Outros (18,4%) e Municipal (8,4%).
   * **O Padrão da Saúde:** Metade dos inscritos (49,4%) é da Saúde. Nos municípios, **67,4% são da Saúde**; nos estados, **55,9%**; enquanto no nível federal a atuação divide-se amplamente com Educação, Assistência Social e Planejamento.

5. **Qual a relação dos perfis profissionais segundo suas atribuições cotidianas (Clusters)?**
   * O modelo K-Means padronizado em 14 variáveis operacionais revelou 3 grupos:
     * **Cluster 1 (13,1%):** *Especialistas em ATS e Síntese de Evidências* (100% ATS, 69% síntese, equipes de 8,7 pessoas);
     * **Cluster 2 (37,1%):** *Avaliadores Ocasionais / Prática Periférica* (M&A secundário para 74%, menor complexidade metodológica);
     * **Cluster 3 (49,8%):** *Núcleo Multimetodológico Ativo* (75% dedicação principal, 94% projetos ativos, múltiplos métodos quali-quanti, 90% dialogam com governantes).

---

## 💡 Insights Adicionais Aplicados
* **Liderança Feminina:** Mais de 60% dos participantes dos eventos e 63% no survey são mulheres. No Cluster 1 (ATS e Síntese), **75,0% são mulheres**.
* **Equidade Étnico-Racial:** O núcleo duro de M&A (Cluster 3) concentra 71,3% de pessoas brancas, enquanto profissionais pardos concentram-se no Cluster 2 (34,1% - prática secundária). Entre doutores e pós-doutores, >73% são brancos.
* **O "Abismo da Comunicação Pública":** 73,5% divulgam para tomadores de decisão governamentais, mas apenas **33,1% comunicam para o público geral**.
* **Interiorização Federativa:** Fora do DF, **86,9% dos participantes optaram pelo formato Online**, provando que o modelo híbrido é indispensável para a rede nacional.

---

## 📁 Estrutura de Arquivos e Entregáveis

| Arquivo | Descrição |
| :--- | :--- |
| **`Relatorio_Completo_Monitoramento_Avaliacao_2024.pdf`** | Relatório Técnico Oficial diagramado (8 páginas) com tabelas, testes $\chi^2$ e gráficos vetoriais. |
| **`Relatorio_Metodologia_Ferramentas_Analise_2024.pdf`** | Relatório Técnico de Metodologia e Ferramentas (10 páginas) descrevendo todo o ecossistema computacional, fórmulas e algoritmos. |
| **`Policy_Brief_Executivo_MA_2024.pdf`** | Policy Brief condensado de 2 páginas voltado para tomadores de decisão e dirigentes. |
| **`Manual_Estrutura_Planilha_Excel_MA_2024.pdf`** | Manual do Usuário e Dicionário de Dados (3 páginas) da planilha Excel consolidada. |
| **`Relatorio_Tabelas_Consolidadas_MA_2024.xlsx`** | Planilha Excel profissional estilizada com 9 abas (KPIs, Q1, Q2, ACM, Espacial, Clusters, Cruzamentos e Qualitativo). |
| **`Apresentacao_Executiva_Monitoramento_Avaliacao_2024.pptx`** | Apresentação em PowerPoint (10 slides widescreen) pronta para exibição executiva. |
| **`painel_analise_evidencias.html`** | Painel interativo para visualização em navegador com Tailwind CSS e Chart.js. |
| **`analise_dados_completa.json`** | Base de dados estruturada em JSON com todas as métricas agregadas da pesquisa. |

---

## 🛠️ Scripts de Análise (Python)
* `generate_analysis.py`: Processamento dos dados brutos, testes estatísticos, pareamento, ACM (prince) e clusterização (K-Means).
* `generate_pdf_report.py`: Geração do relatório técnico oficial de 8 páginas via Playwright Chromium e Matplotlib.
* `generate_methodology_pdf.py`: Geração do relatório técnico de metodologia e ferramentas (10 páginas).
* `generate_policy_brief.py`: Geração do Policy Brief executivo de 2 páginas.
* `generate_manual_pdf.py`: Geração do manual da planilha em PDF.
* `build_excel_summary.py`: Montagem da planilha consolidada multi-abas e estilização visual corporativa.
* `build_presentation.py`: Construção automática dos slides PowerPoint (.pptx).
* `build_html_dashboard.py`: Atualização do painel web interativo.

