# -*- coding: utf-8 -*-
"""
Script para consolidação de todas as matrizes, tabelas, cruzamentos e insights aplicados
em uma planilha Excel profissional e multi-abas.
"""

import pandas as pd
import json

print("Gerando planilha Excel consolidada com insights aplicados...")

with open('analise_dados_completa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

excel_path = 'Relatorio_Tabelas_Consolidadas_MA_2024.xlsx'

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    
    # Aba 1: KPIs Gerais
    kpis = [
        {"Indicador": "Inscrições Totais nos Eventos", "Valor": data['q4']['total_events'], "Unidade": "Inscrições", "Detalhe": "742 no Evento 1 + 386 no Evento 2"},
        {"Indicador": "Indivíduos Únicos nos Eventos", "Valor": data['q2']['unique_total'], "Unidade": "Pessoas", "Detalhe": "Comunidade única desduplicada"},
        {"Indicador": "Respondentes do Survey", "Valor": data['q1']['total_survey'], "Unidade": "Respondentes", "Detalhe": "521 totais (245 na bateria prática)"},
        {"Indicador": "Taxa de Renovação de Público no Evento 2", "Valor": f"{data['q2']['renewal_rate']}%", "Unidade": "Percentual", "Detalhe": "344 novos participantes atraídos"},
        {"Indicador": "Recorrência entre os Dois Eventos", "Valor": f"{data['q2']['recurrence_rate_total']}%", "Unidade": "Percentual", "Detalhe": "Apenas 42 pessoas participaram de ambos"},
        {"Indicador": "Público Externo no Survey Identificado", "Valor": f"{data['q1']['pct_external_id']}%", "Unidade": "Percentual", "Detalhe": "166 dos 226 identificados não foram aos eventos"},
        {"Indicador": "Participação Feminina nos Eventos", "Valor": "60,2%", "Unidade": "Percentual", "Detalhe": "447 mulheres e 295 homens no Evento 1"},
        {"Indicador": "Participação Feminina no Survey", "Valor": "63,0%", "Unidade": "Percentual", "Detalhe": "153 mulheres cis e 85 homens cis informados"},
        {"Indicador": "Tradução para Tomadores de Decisão", "Valor": f"{data['insights']['diss_decisores_pct']}%", "Unidade": "Percentual", "Detalhe": "180 de 245 praticantes ativos"},
        {"Indicador": "Tradução para o Público Geral / Sociedade", "Valor": f"{data['insights']['diss_geral_pct']}%", "Unidade": "Percentual", "Detalhe": "81 de 245 praticantes ativos"}
    ]
    pd.DataFrame(kpis).to_excel(writer, sheet_name='KPIs_Gerais', index=False)
    
    # Aba 2: Q1 - Correspondência Survey x Eventos
    q1_rows = [
        {"Segmento": "Público Externo aos Eventos (Sem correspondência)", "Frequência": data['q1']['external'], "Percentual_Identificados": data['q1']['pct_external_id'], "Percentual_Survey_Total": round(data['q1']['external']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Presentes no Evento 1 (Políticas Informadas por Evidências)", "Frequência": data['q1']['e1_match'], "Percentual_Identificados": round(data['q1']['e1_match']/data['q1']['identified']*100, 2), "Percentual_Survey_Total": round(data['q1']['e1_match']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Presentes no Evento 2 (Práticas em Avaliação)", "Frequência": data['q1']['e2_match'], "Percentual_Identificados": round(data['q1']['e2_match']/data['q1']['identified']*100, 2), "Percentual_Survey_Total": round(data['q1']['e2_match']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Presentes em Ambos os Eventos Simultaneamente", "Frequência": data['q1']['both_match'], "Percentual_Identificados": round(data['q1']['both_match']/data['q1']['identified']*100, 2), "Percentual_Survey_Total": round(data['q1']['both_match']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Total de Identificados com Presença em Eventos", "Frequência": data['q1']['any_match'], "Percentual_Identificados": data['q1']['pct_any_id'], "Percentual_Survey_Total": data['q1']['pct_any_total']},
        {"Segmento": "Respondentes Anônimos (Sem dados de contato fornecidos)", "Frequência": data['q1']['anon'], "Percentual_Identificados": "-", "Percentual_Survey_Total": round(data['q1']['anon']/data['q1']['total_survey']*100, 2)}
    ]
    pd.DataFrame(q1_rows).to_excel(writer, sheet_name='Q1_Survey_vs_Eventos', index=False)
    
    # Aba 3: Q2 - Recorrência vs Renovação
    q2_rows = [
        {"Métrica": "Inscritos Totais no Evento 1", "Valor": data['q2']['e1_total']},
        {"Métrica": "Inscritos Totais no Evento 2", "Valor": data['q2']['e2_total']},
        {"Métrica": "Indivíduos Únicos na Comunidade de Eventos", "Valor": data['q2']['unique_total']},
        {"Métrica": "Pessoas Presentes em Ambos os Eventos (Sobreposição)", "Valor": data['q2']['overlap']},
        {"Métrica": "Novos Participantes Atraídos no Evento 2", "Valor": data['q2']['e2_new']},
        {"Métrica": "Taxa de Renovação no Evento 2 (%)", "Valor": data['q2']['renewal_rate']},
        {"Métrica": "Taxa de Recorrência no Evento 2 (%)", "Valor": data['q2']['recurrence_rate_e2']},
        {"Métrica": "Taxa de Retenção do Evento 1 no Evento 2 (%)", "Valor": data['q2']['recurrence_rate_e1']},
        {"Métrica": "Taxa de Recorrência Global sobre a Comunidade Única (%)", "Valor": data['q2']['recurrence_rate_total']}
    ]
    pd.DataFrame(q2_rows).to_excel(writer, sheet_name='Q2_Recorrencia_Renovacao', index=False)
    
    # Aba 4: Q3 - Coordenadas da ACM
    mca_df = pd.DataFrame(data['q3']['points'])
    mca_df.rename(columns={'variable': 'Variavel', 'category': 'Categoria', 'dim1': 'Coordenada_Dimensao_1', 'dim2': 'Coordenada_Dimensao_2'}, inplace=True)
    mca_df.to_excel(writer, sheet_name='Q3_ACM_Coordenadas', index=False)
    
    # Aba 5: Q4 - Distribuição Espacial e Esferas
    reg_df = pd.DataFrame(list(data['q4']['regioes'].items()), columns=['Grande_Regiao', 'Inscricoes_Eventos'])
    reg_df['Percentual'] = (reg_df['Inscricoes_Eventos'] / 1128 * 100).round(2)
    reg_df.to_excel(writer, sheet_name='Q4_Regioes', index=False)
    
    esf_df = pd.DataFrame(list(data['q4']['esferas'].items()), columns=['Esfera_Atuacao', 'Inscricoes_Eventos'])
    esf_df['Percentual'] = (esf_df['Inscricoes_Eventos'] / 1128 * 100).round(2)
    esf_df.to_excel(writer, sheet_name='Q4_Esferas', index=False)
    
    # Aba 6: Q5 - Clusters das Atribuições Cotidianas
    c_means = pd.DataFrame(data['q5']['means']).T
    c_means.index = [data['q5']['names'][str(i)] for i in c_means.index]
    c_means.reset_index(inplace=True)
    c_means.rename(columns={'index': 'Cluster_Nome'}, inplace=True)
    c_means.to_excel(writer, sheet_name='Q5_Clusters_Perfis', index=False)

    # Aba 7: Insights Aplicados e Cruzamentos Multivariados
    insights_cruzamentos = [
        {"Analise": "Modalidade Evento 1 - Residentes Fora do DF", "Segmento": "Online", "Percentual": "68,1% (86,9% dos que declararam)", "Observacao": "Barreira de entrada para interiorização"},
        {"Analise": "Modalidade Evento 1 - Residentes Fora do DF", "Segmento": "Presencial", "Percentual": "10,3%", "Observacao": "Presença física restrita"},
        {"Analise": "Modalidade Evento 1 - Residentes no DF", "Segmento": "Presencial", "Percentual": "41,0%", "Observacao": "Maior adesão presencial na capital"},
        {"Analise": "Modalidade Evento 1 - Residentes no DF", "Segmento": "Online", "Percentual": "35,9%", "Observacao": "Significativa preferência remota mesmo no DF"},
        {"Analise": "Composição por Cluster - Cluster 1 (ATS)", "Segmento": "Gênero Mulheres", "Percentual": "75,0%", "Observacao": "Maior concentração feminina"},
        {"Analise": "Composição por Cluster - Cluster 1 (ATS)", "Segmento": "Raça Pretos", "Percentual": "9,4%", "Observacao": "Maior presença de pessoas pretas"},
        {"Analise": "Composição por Cluster - Cluster 2 (Ocasionais)", "Segmento": "Raça Pardos", "Percentual": "34,1%", "Observacao": "Maior concentração de pardos alocados na periferia"},
        {"Analise": "Composição por Cluster - Cluster 3 (Núcleo M&A)", "Segmento": "Raça Brancos", "Percentual": "71,3%", "Observacao": "Maior concentração de brancos no núcleo duro"},
        {"Analise": "Comunicação Pública - Cluster 1 (ATS)", "Segmento": "Divulga p/ Público Geral", "Percentual": "28,1%", "Observacao": "Foco restrito a pareceres ministeriais e Conitec"},
        {"Analise": "Comunicação Pública - Cluster 2 (Ocasionais)", "Segmento": "Divulga p/ Público Geral", "Percentual": "19,8%", "Observacao": "Menor capacidade comunicacional"},
        {"Analise": "Comunicação Pública - Cluster 3 (Núcleo M&A)", "Segmento": "Divulga p/ Público Geral", "Percentual": "44,3%", "Observacao": "Maior abertura à sociedade civil"}
    ]
    pd.DataFrame(insights_cruzamentos).to_excel(writer, sheet_name='Insights_Aplicados_Cruzamentos', index=False)
    
    # Aba 8: Comentários Qualitativos do Survey
    df3 = pd.read_excel('Survey-Escuta-Redes-de-Monitoramento-Avaliacao-Politicas-Publicas.xlsx')
    col_com = 'Se desejar, registre aqui alguma informação ou comentário adicional relacionado à pesquisa.'
    sub_com = df3[['ID', col_com]].dropna()
    sub_com.rename(columns={col_com: 'Comentario_Aberto'}, inplace=True)
    sub_com.to_excel(writer, sheet_name='Comentarios_Qualitativos', index=False)

print(f"Planilha Excel consolidada atualizada com sucesso em: {excel_path}")
