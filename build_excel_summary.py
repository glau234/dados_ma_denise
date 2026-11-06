# -*- coding: utf-8 -*-
"""
Script para consolidação de todas as matrizes, tabelas, cruzamentos e insights aplicados
em uma planilha Excel profissional e multi-abas com estilização corporativa Navy.
"""

import pandas as pd
import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

print("Gerando planilha Excel consolidada com dados auditados e insights aplicados...")

with open('analise_dados_completa.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

excel_path = 'Relatorio_Tabelas_Consolidadas_MA_2024.xlsx'

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    
    # Aba 1: KPIs Gerais
    kpis = [
        {"Indicador": "Inscrições Totais nos Eventos", "Valor": data['q4']['total_events'], "Unidade": "Inscrições", "Detalhe": "742 no Evento 1 + 386 no Evento 2"},
        {"Indicador": "Indivíduos Únicos nos Eventos", "Valor": data['q2']['unique_total'], "Unidade": "Pessoas", "Detalhe": "Comunidade única desduplicada (742 + 386 - 40)"},
        {"Indicador": "Respondentes do Survey", "Valor": data['q1']['total_survey'], "Unidade": "Respostas", "Detalhe": "521 acessos totais (245 responderam à bateria completa)"},
        {"Indicador": "Indivíduos Únicos Identificados no Survey", "Valor": data['q1']['identified_unique'], "Unidade": "Pessoas", "Detalhe": "226 respostas identificadas (8 pessoas enviaram 2 vezes)"},
        {"Indicador": "Taxa de Renovação de Público no Evento 2", "Valor": f"{data['q2']['renewal_rate']}%", "Unidade": "Percentual", "Detalhe": f"{data['q2']['e2_new']} novos participantes atraídos no Evento 2"},
        {"Indicador": "Recorrência entre os Dois Eventos", "Valor": f"{data['q2']['recurrence_rate_total']}%", "Unidade": "Percentual", "Detalhe": f"Exatamente {data['q2']['overlap']} pessoas participaram de ambos (por CPF)"},
        {"Indicador": "Público Externo no Survey Identificado", "Valor": f"{data['q1']['pct_external_id']}%", "Unidade": "Percentual", "Detalhe": f"166 respostas (161 pessoas únicas = {data['q1']['pct_external_unique']}%) fora dos eventos"},
        {"Indicador": "Participação Feminina nos Eventos", "Valor": "60,2%", "Unidade": "Percentual", "Detalhe": "447 mulheres e 295 homens no Evento 1"},
        {"Indicador": "Participação Feminina no Survey", "Valor": "62,9%", "Unidade": "Percentual", "Detalhe": "154 mulheres cis entre os 245 praticantes ativos"},
        {"Indicador": "Tradução para Tomadores de Decisão", "Valor": f"{data['insights']['diss_decisores_pct']}%", "Unidade": "Percentual", "Detalhe": "180 de 245 praticantes ativos"},
        {"Indicador": "Tradução para o Público Geral / Sociedade", "Valor": f"{data['insights']['diss_geral_pct']}%", "Unidade": "Percentual", "Detalhe": "81 de 245 praticantes ativos"}
    ]
    pd.DataFrame(kpis).to_excel(writer, sheet_name='KPIs_Gerais', index=False)
    
    # Aba 2: Q1 - Correspondência Survey x Eventos
    q1_rows = [
        {"Segmento": "Público Externo aos Eventos (Respostas Identificadas)", "Frequência": data['q1']['external'], "Percentual_Identificados": data['q1']['pct_external_id'], "Percentual_Survey_Total": round(data['q1']['external']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Presentes no Evento 1 (Políticas Informadas por Evidências)", "Frequência": data['q1']['e1_match'], "Percentual_Identificados": round(data['q1']['e1_match']/data['q1']['identified']*100, 2), "Percentual_Survey_Total": round(data['q1']['e1_match']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Presentes no Evento 2 (Práticas em Avaliação)", "Frequência": data['q1']['e2_match'], "Percentual_Identificados": round(data['q1']['e2_match']/data['q1']['identified']*100, 2), "Percentual_Survey_Total": round(data['q1']['e2_match']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Presentes em Ambos os Eventos Simultaneamente", "Frequência": data['q1']['both_match'], "Percentual_Identificados": round(data['q1']['both_match']/data['q1']['identified']*100, 2), "Percentual_Survey_Total": round(data['q1']['both_match']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Total de Respostas Identificadas com Presença em Eventos", "Frequência": data['q1']['any_match'], "Percentual_Identificados": data['q1']['pct_any_id'], "Percentual_Survey_Total": data['q1']['pct_any_total']},
        {"Segmento": "Total de Indivíduos Únicos Identificados (Desduplicando 8 duplos)", "Frequência": data['q1']['identified_unique'], "Percentual_Identificados": 100.0, "Percentual_Survey_Total": round(data['q1']['identified_unique']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Indivíduos Únicos Identificados Presentes em Eventos", "Frequência": data['q1']['any_match_unique'], "Percentual_Identificados": data['q1']['pct_any_unique'], "Percentual_Survey_Total": round(data['q1']['any_match_unique']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Indivíduos Únicos Identificados Externos aos Eventos", "Frequência": data['q1']['external_unique'], "Percentual_Identificados": data['q1']['pct_external_unique'], "Percentual_Survey_Total": round(data['q1']['external_unique']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Respondentes Elegíveis Anônimos (Concluíram sem informar nome)", "Frequência": data['q1']['anon_eligible'], "Percentual_Identificados": "-", "Percentual_Survey_Total": round(data['q1']['anon_eligible']/data['q1']['total_survey']*100, 2)},
        {"Segmento": "Encerrados nas Perguntas Filtro (Não atuam / Sem publicação 8 anos)", "Frequência": data['q1']['filtered_out'], "Percentual_Identificados": "-", "Percentual_Survey_Total": round(data['q1']['filtered_out']/data['q1']['total_survey']*100, 2)}
    ]
    pd.DataFrame(q1_rows).to_excel(writer, sheet_name='Q1_Survey_vs_Eventos', index=False)
    
    # Aba 3: Q2 - Recorrência vs Renovação
    q2_rows = [
        {"Métrica": "Inscritos Totais no Evento 1", "Valor": data['q2']['e1_total']},
        {"Métrica": "Inscritos Totais no Evento 2", "Valor": data['q2']['e2_total']},
        {"Métrica": "Indivíduos Únicos na Comunidade de Eventos", "Valor": data['q2']['unique_total']},
        {"Métrica": "Pessoas Presentes em Ambos os Eventos (Sobreposição Exata por CPF)", "Valor": data['q2']['overlap']},
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
        {"Analise": "Modalidade Evento 1 - Residentes Fora do DF", "Segmento": "Presencial", "Percentual": "10,3% (13,1% dos que declararam)", "Observacao": "Presença física restrita"},
        {"Analise": "Modalidade Evento 1 - Residentes no DF", "Segmento": "Presencial", "Percentual": "41,0% (48,8% dos que declararam)", "Observacao": "Maior adesão presencial na capital"},
        {"Analise": "Modalidade Evento 1 - Residentes no DF", "Segmento": "Online", "Percentual": "35,9% (51,2% dos que declararam)", "Observacao": "Significativa preferência remota mesmo no DF"},
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

# Aplicar estilização corporativa Navy via openpyxl
wb = load_workbook(excel_path)
header_fill = PatternFill(start_color="0C182B", end_color="0C182B", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
cell_font = Font(name="Calibri", size=10, color="1E293B")
thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    ws.views.sheetView[0].showGridLines = True
    for col_idx in range(1, ws.max_column + 1):
        col_letter = get_column_letter(col_idx)
        max_len = 0
        for row_idx in range(1, ws.max_row + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            val_str = str(cell.value or '')
            max_len = max(max_len, min(len(val_str), 65))
            cell.border = thin_border
            if row_idx == 1:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            else:
                cell.fill = zebra_fill if row_idx % 2 == 0 else white_fill
                cell.font = cell_font
                if isinstance(cell.value, (int, float)):
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.column_dimensions[col_letter].width = max(max_len + 5, 14)
    ws.row_dimensions[1].height = 26

wb.save(excel_path)
print(f"Planilha Excel consolidada atualizada e estilizada com sucesso em: {excel_path}")
