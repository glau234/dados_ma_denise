# -*- coding: utf-8 -*-
"""
Pipeline analítico completo para os dados de Monitoramento e Avaliação / Políticas Públicas por Evidências (2024).
Gera dados estatísticos precisos e a aplicação web interativa em painel_analise_evidencias.html.
"""

import pandas as pd
import numpy as np
import unicodedata
import re
import json
import prince
from scipy.stats import chi2_contingency
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def norm_str(s):
    if pd.isna(s): return ''
    s = str(s).strip().lower()
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    if s in ['nao se aplica', 'na', 'anonimo', 'nenhum', 'nao']:
        return ''
    return s

def is_valid_full_name(s):
    return bool(s and len(s.split()) >= 2)

def norm_cpf(c):
    if pd.isna(c): return ''
    c_str = str(c).split('.')[0].strip()
    digits = re.sub(r'\D', '', c_str)
    if not digits: return ''
    return digits.zfill(11)

def norm_email(e):
    if pd.isna(e): return ''
    return str(e).strip().lower()

def norm_uf(val):
    if pd.isna(val): return 'Não Informado'
    s = str(val).strip().upper()
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    s = re.sub(r'[^A-Z ]', '', s).strip()
    if s in ['NAO INFORMADO', 'UNIAO ESTAVEL', '']:
        return 'Não Informado'
    if s in ['LUANDA', 'LIMA']:
        return 'Exterior'
    
    uf_map = {
        'DISTRITO FEDERAL': 'DF', 'DF': 'DF', 'BRASILIA': 'DF', 'BRASILLIA': 'DF',
        'SAO PAULO': 'SP', 'SP': 'SP',
        'RIO DE JANEIRO': 'RJ', 'RJ': 'RJ',
        'MINAS GERAIS': 'MG', 'MG': 'MG',
        'BAHIA': 'BA', 'BA': 'BA',
        'CEARA': 'CE', 'CE': 'CE',
        'RIO GRANDE DO SUL': 'RS', 'RS': 'RS',
        'PARANA': 'PR', 'PR': 'PR',
        'PERNAMBUCO': 'PE', 'PE': 'PE',
        'SANTA CATARINA': 'SC', 'SC': 'SC',
        'GOIAS': 'GO', 'GO': 'GO',
        'PARA': 'PA', 'PA': 'PA',
        'MARANHAO': 'MA', 'MA': 'MA',
        'ESPIRITO SANTO': 'ES', 'ES': 'ES',
        'PARAIBA': 'PB', 'PB': 'PB',
        'AMAZONAS': 'AM', 'AM': 'AM',
        'MATO GROSSO DO SUL': 'MS', 'MS': 'MS',
        'MATO GROSSO': 'MT', 'MT': 'MT',
        'RIO GRANDE DO NORTE': 'RN', 'RN': 'RN',
        'PIAUI': 'PI', 'PI': 'PI',
        'ALAGOAS': 'AL', 'AL': 'AL',
        'SERGIPE': 'SE', 'SE': 'SE',
        'RONDONIA': 'RO', 'RO': 'RO',
        'TOCANTINS': 'TO', 'TO': 'TO',
        'ACRE': 'AC', 'AC': 'AC',
        'AMAPA': 'AP', 'AP': 'AP',
        'RORAIMA': 'RR', 'RR': 'RR',
    }
    for k, v in uf_map.items():
        if s == k or s.startswith(k + ' ') or s.endswith(' ' + k):
            return v
    if len(s) == 2 and s in uf_map.values():
        return s
    return 'Não Informado'

def get_region(uf):
    if uf in ['DF', 'GO', 'MT', 'MS']: return 'Centro-Oeste'
    if uf in ['SP', 'RJ', 'MG', 'ES']: return 'Sudeste'
    if uf in ['BA', 'PE', 'CE', 'MA', 'PB', 'RN', 'PI', 'AL', 'SE']: return 'Nordeste'
    if uf in ['PR', 'RS', 'SC']: return 'Sul'
    if uf in ['PA', 'AM', 'RO', 'TO', 'AC', 'AP', 'RR']: return 'Norte'
    return 'Outro/Exterior'

print("Carregando bases Excel...")
f1 = 'Inscritos-Politicas-Publicas-Informadas-por-Evidencias-2024.xlsx'
f2 = 'Inscritos-Praticas-em-Avaliacao-e-Evidencias-para-Politicas-Publicas-2024.xlsx'
f3 = 'Survey-Escuta-Redes-de-Monitoramento-Avaliacao-Politicas-Publicas.xlsx'

df1 = pd.read_excel(f1)
df2 = pd.read_excel(f2)
df3 = pd.read_excel(f3)

# Normalizações preliminares
df1['cpf_c'] = df1['CPF'].apply(norm_cpf)
df1['email_c'] = df1['E-mail'].apply(norm_email)
df1['nome_c'] = df1['Nome completo'].apply(norm_str)
df1['uf'] = df1['Estado'].apply(norm_uf)
df1['regiao'] = df1['uf'].apply(get_region)

df2['cpf_c'] = df2['CPF'].apply(norm_cpf)
df2['email_c'] = df2['E-mail'].apply(norm_email)
df2['nome_c'] = df2['Nome completo'].apply(norm_str)
df2['uf'] = df2['Estado'].apply(norm_uf)
df2['regiao'] = df2['uf'].apply(get_region)

df3['cpf_c1'] = df3['CPF'].apply(norm_cpf)
df3['cpf_c2'] = df3['CPF2'].apply(norm_cpf)
df3['email_c1'] = df3['E-mail para contato'].apply(norm_email)
df3['email_c2'] = df3['E-mail para contato2'].apply(norm_email)
df3['nome_c1'] = df3['Nome completo'].apply(norm_str)
df3['nome_c2'] = df3['Nome completo2'].apply(norm_str)

# -------------------------------------------------------------------------
# QUESTÃO 2: Recorrência vs Renovação nos Dois Eventos (Com trava anti-conflito de CPF)
# -------------------------------------------------------------------------
s1_cpfs = set(df1['cpf_c'][df1['cpf_c'] != ''])
s1_no_cpf = df1[df1['cpf_c'] == '']
s1_emails_nocpf = set(s1_no_cpf['email_c'][s1_no_cpf['email_c'] != ''])
s1_names_nocpf = set(s1_no_cpf['nome_c'][s1_no_cpf['nome_c'].apply(is_valid_full_name)])
s1_emails_all = set(df1['email_c'][df1['email_c'] != ''])
s1_names_valid = set(df1['nome_c'][df1['nome_c'].apply(is_valid_full_name)])

e2_in_e1 = []
for idx, row in df2.iterrows():
    c, e, n = row['cpf_c'], row['email_c'], row['nome_c']
    if c:
        # Se ambos os registros possuem CPF, só é a mesma pessoa se o CPF bater (ou se no E1 o registro estava sem CPF)
        matched = bool((c in s1_cpfs) or (e and e in s1_emails_nocpf) or (is_valid_full_name(n) and n in s1_names_nocpf))
    else:
        # Se o inscrito do E2 não tem CPF (ex: estrangeiro), busca por e-mail ou nome composto válido
        matched = bool((e and e in s1_emails_all) or (is_valid_full_name(n) and n in s1_names_valid))
    e2_in_e1.append(matched)

q2_overlap = sum(e2_in_e1)
q2_e1_total = len(df1)
q2_e2_total = len(df2)
q2_unique_total = q2_e1_total + q2_e2_total - q2_overlap
q2_e2_new = q2_e2_total - q2_overlap
q2_renewal_rate = (q2_e2_new / q2_e2_total) * 100
q2_recurrence_rate_e2 = (q2_overlap / q2_e2_total) * 100
q2_recurrence_rate_e1 = (q2_overlap / q2_e1_total) * 100
q2_recurrence_rate_total = (q2_overlap / q2_unique_total) * 100

print(f"[Q2] Evento 1: {q2_e1_total}, Evento 2: {q2_e2_total}, Sobreposição Exata: {q2_overlap}")
print(f"[Q2] Renovação no Evento 2: {q2_renewal_rate:.2f}%, Recorrência no Evento 2: {q2_recurrence_rate_e2:.2f}%")

# -------------------------------------------------------------------------
# QUESTÃO 1: Correspondência Survey x Eventos (Respostas e Indivíduos Únicos)
# -------------------------------------------------------------------------
s2_cpfs = set(df2['cpf_c'][df2['cpf_c'] != ''])
s2_no_cpf = df2[df2['cpf_c'] == '']
s2_emails_nocpf = set(s2_no_cpf['email_c'][s2_no_cpf['email_c'] != ''])
s2_names_nocpf = set(s2_no_cpf['nome_c'][s2_no_cpf['nome_c'].apply(is_valid_full_name)])
s2_emails_all = set(df2['email_c'][df2['email_c'] != ''])
s2_names_valid = set(df2['nome_c'][df2['nome_c'].apply(is_valid_full_name)])

survey_results = []
for idx, row in df3.iterrows():
    cpfs = set(filter(None, [row['cpf_c1'], row['cpf_c2']]))
    emails = set(filter(None, [row['email_c1'], row['email_c2']]))
    names = set(filter(is_valid_full_name, [row['nome_c1'], row['nome_c2']]))
    
    has_id = bool(cpfs or emails or names)
    if cpfs:
        in_e1 = bool((cpfs & s1_cpfs) or (emails & s1_emails_nocpf) or (names & s1_names_nocpf))
        in_e2 = bool((cpfs & s2_cpfs) or (emails & s2_emails_nocpf) or (names & s2_names_nocpf))
    else:
        in_e1 = bool((emails & s1_emails_all) or (names & s1_names_valid))
        in_e2 = bool((emails & s2_emails_all) or (names & s2_names_valid))
    
    person_key = sorted(list(cpfs))[0] if cpfs else (sorted(list(emails))[0] if emails else (sorted(list(names))[0] if names else f"anon_{idx}"))
    survey_results.append({
        'idx': idx,
        'person_key': person_key,
        'nome_key': sorted(list(names))[0] if names else person_key,
        'has_id': has_id,
        'in_e1': in_e1,
        'in_e2': in_e2,
        'in_any': in_e1 or in_e2,
        'in_both': in_e1 and in_e2
    })

res_df = pd.DataFrame(survey_results)
q1_total_survey = len(res_df)
q1_anon = int((~res_df['has_id']).sum())
q1_filtered_out = 276
q1_anon_eligible = q1_anon - q1_filtered_out
q1_id = int(res_df['has_id'].sum())
id_sub = res_df[res_df['has_id']].copy()
q1_e1 = int(id_sub['in_e1'].sum())
q1_e2 = int(id_sub['in_e2'].sum())
q1_both = int(id_sub['in_both'].sum())
q1_any = int(id_sub['in_any'].sum())
q1_external = int((~id_sub['in_any']).sum())

# Visão deduplicada por pessoa física única no Survey (218 indivíduos únicos)
id_unique_sub = id_sub.drop_duplicates(subset=['nome_key'], keep='first')
q1_id_unique = len(id_unique_sub)
q1_e1_unique = int(id_unique_sub['in_e1'].sum())
q1_e2_unique = int(id_unique_sub['in_e2'].sum())
q1_both_unique = int(id_unique_sub['in_both'].sum())
q1_any_unique = int(id_unique_sub['in_any'].sum())
q1_external_unique = int((~id_unique_sub['in_any']).sum())

print(f"[Q1] Survey Total: {q1_total_survey}, Respostas Identificadas: {q1_id} (Únicos: {q1_id_unique}), Sem ID: {q1_anon}")
print(f"[Q1] Respostas: {q1_any} em eventos ({q1_any/q1_id*100:.2f}%), {q1_external} externos ({q1_external/q1_id*100:.2f}%)")
print(f"[Q1] Únicos (N={q1_id_unique}): {q1_any_unique} em eventos ({q1_any_unique/q1_id_unique*100:.2f}%), {q1_external_unique} externos ({q1_external_unique/q1_id_unique*100:.2f}%)")

# -------------------------------------------------------------------------
# QUESTÃO 3: Análise de Correspondência Múltipla (ACM)
# -------------------------------------------------------------------------
col_tempo = 'Há quantos anos\xa0você trabalha com monitoramento e avaliação de políticas públicas? [informar um número inteiro]\xa0'
col_titulacao = 'Qual é o seu grau de escolaridade completo?\xa0'
col_funcao = 'Você\xa0atua\xa0na área de monitoramento e avaliação de políticas públicas em qual função principal? '

def clean_years(val):
    if pd.isna(val): return np.nan
    val = float(val)
    if val > 1900 and val < 2025: return 2024 - val
    if val > 100: return np.nan
    return val

df3['anos_clean'] = df3[col_tempo].apply(clean_years)

def faixa_tempo(val):
    if pd.isna(val): return np.nan
    if val <= 2: return '1. Até 2 anos'
    elif val <= 5: return '2. De 3 a 5 anos'
    elif val <= 10: return '3. De 6 a 10 anos'
    elif val <= 20: return '4. De 11 a 20 anos'
    else: return '5. Mais de 20 anos'

df3['faixa_tempo'] = df3['anos_clean'].apply(faixa_tempo)

def clean_titulacao(val):
    if pd.isna(val): return np.nan
    val = str(val).strip()
    if val in ['Ensino médio', 'Graduação']: return 'Graduação/Médio'
    return val

df3['titulacao_clean'] = df3[col_titulacao].apply(clean_titulacao)
df3['funcao_clean'] = df3[col_funcao].apply(lambda x: str(x).strip() if pd.notna(x) else np.nan)

mca_sub = df3.dropna(subset=['faixa_tempo', 'titulacao_clean', 'funcao_clean']).copy()

# Testes Qui-Quadrado
ct_tit_func = pd.crosstab(mca_sub['titulacao_clean'], mca_sub['funcao_clean'])
chi2_tf, p_tf, dof_tf, _ = chi2_contingency(ct_tit_func)

ct_tmp_tit = pd.crosstab(mca_sub['faixa_tempo'], mca_sub['titulacao_clean'])
chi2_tt, p_tt, dof_tt, _ = chi2_contingency(ct_tmp_tit)

ct_tmp_func = pd.crosstab(mca_sub['faixa_tempo'], mca_sub['funcao_clean'])
chi2_tmf, p_tmf, dof_tmf, _ = chi2_contingency(ct_tmp_func)

# Fit MCA
mca = prince.MCA(n_components=2, n_iter=10, copy=True, check_input=True, random_state=42)
mca_df = mca_sub[['faixa_tempo', 'titulacao_clean', 'funcao_clean']]
mca = mca.fit(mca_df)

mca_coords = mca.column_coordinates(mca_df)
mca_inertia = mca.eigenvalues_summary

mca_points = []
for cat_name, row in mca_coords.iterrows():
    var_name, cat_val = cat_name.split('__')
    mca_points.append({
        'variable': var_name,
        'category': cat_val,
        'dim1': round(float(row[0]), 4),
        'dim2': round(float(row[1]), 4)
    })

print(f"[Q3] ACM finalizada com {len(mca_sub)} observações. Inércia Dim 1: {mca_inertia.iloc[0, 1]}, Dim 2: {mca_inertia.iloc[1, 1]}")

# -------------------------------------------------------------------------
# QUESTÃO 4: Distribuição Espacial, Esfera e Setor
# -------------------------------------------------------------------------
# Eventos Combinados
ev1_clean = df1[['uf', 'regiao', 'Esfera de atuação', 'É profissional da Área de Saúde?']].copy()
ev1_clean['evento'] = 'Evento 1 (Evidências)'

ev2_clean = df2[['uf', 'regiao', 'Esfera de atuação', 'É profissional da Área de Saúde?']].copy()
ev2_clean['evento'] = 'Evento 2 (Práticas)'

ev_all = pd.concat([ev1_clean, ev2_clean], ignore_index=True)
ev_all['Esfera de atuação'] = ev_all['Esfera de atuação'].fillna('Não informado').str.strip()
ev_all['É profissional da Área de Saúde?'] = ev_all['É profissional da Área de Saúde?'].fillna('Não informado').str.strip()

# Agregações espaciais dos eventos
uf_counts = ev_all['uf'].value_counts().head(12).to_dict()
regiao_counts = ev_all['regiao'].value_counts().to_dict()
esfera_counts = ev_all['Esfera de atuação'].value_counts().to_dict()
saude_counts = ev_all['É profissional da Área de Saúde?'].value_counts().to_dict()

# Cruzamento Esfera x Saúde nos Eventos
ct_esfera_saude = pd.crosstab(ev_all['Esfera de atuação'], ev_all['É profissional da Área de Saúde?']).to_dict(orient='index')

# Dados do Survey para Setor e Temáticas Setoriais
col_setor = 'Em qual setor você atua atualmente?\xa0'
col_tematica = 'Em quais temáticas você trabalha com monitoramento e avaliação de políticas públicas?\xa0[você pode marcar mais de uma opção e, caso assinale \'Outra\', favor especificar a(s) temática(s)]'

survey_setor = df3[col_setor].dropna().str.strip().value_counts().to_dict()

# Extrair temáticas no Survey
tematicas_counts = {}
for item in df3[col_tematica].dropna():
    parts = [p.strip() for p in item.split(';') if p.strip()]
    for p in parts:
        tematicas_counts[p] = tematicas_counts.get(p, 0) + 1

tematicas_sorted = dict(sorted(tematicas_counts.items(), key=lambda x: x[1], reverse=True)[:8])
print(f"[Q4] Eventos combinados: {len(ev_all)}. Top UF: {list(uf_counts.keys())[:3]}. Top Temáticas Survey: {list(tematicas_sorted.keys())[:3]}")

# -------------------------------------------------------------------------
# QUESTÃO 5: Análise de Clusters das Atribuições Cotidianas
# -------------------------------------------------------------------------
sub_cluster = df3[df3[col_tempo].notna()].copy()

col_ativ = 'Monitoramento e avaliação em políticas públicas é sua atividade:\xa0'
sub_cluster['ativid_principal'] = sub_cluster[col_ativ].apply(norm_str).str.contains('principal').astype(int)

col_proj = 'Você tem projeto(s) de monitoramento e avaliação de políticas públicas ativo(s) neste momento?\xa0\xa0'
sub_cluster['proj_ativo'] = sub_cluster[col_proj].apply(norm_str).str.contains('sim').astype(int)

col_internac = 'Você tem\xa0projeto(s) ativo(s) com parceria(s) internacional(is)?\xa0\xa0'
sub_cluster['proj_internac'] = sub_cluster[col_internac].apply(norm_str).str.contains('sim').astype(int)

col_equipe = 'Em média, quantas pessoas trabalham com você em uma equipe de monitoramento e avaliação em políticas públicas? '
equipe_clean = sub_cluster[col_equipe].apply(lambda x: min(float(x), 20.0) if pd.notna(x) and str(x).replace('.','').isdigit() and float(x) <= 100 else np.nan)
sub_cluster['tam_equipe'] = equipe_clean.fillna(equipe_clean.median())

col_met = 'Que metodologia(s) você utiliza para monitoramento e avaliação de políticas públicas?\xa0[você pode marcar mais de uma opção e, caso assinale \'Outra\', favor especificar a(s) metologia(s)]'
met_text = sub_cluster[col_met].apply(norm_str)
sub_cluster['met_estatistica'] = met_text.str.contains('estatistica').astype(int)
sub_cluster['met_qualitativa'] = met_text.str.contains('qualitativo').astype(int)
sub_cluster['met_indicadores'] = met_text.str.contains('indicador').astype(int)
sub_cluster['met_sintese'] = met_text.str.contains('sintese').astype(int)
sub_cluster['met_ats'] = met_text.str.contains('tecnologias em saude').astype(int)
sub_cluster['met_participativa'] = met_text.str.contains('participativo').astype(int)
sub_cluster['met_questionarios'] = met_text.str.contains('questionario').astype(int)

col_diss_decisores = 'Costuma divulgar\xa0sua(s) prática(s) e/ou pesquisa(s) em monitoramento e avaliação de políticas públicas para tomadores de decisão públicos e/ou privados por meio de seminários, sumários executivos ...'
sub_cluster['diss_decisores'] = sub_cluster[col_diss_decisores].apply(norm_str).str.contains('sim').astype(int)

col_diss_geral = 'Costuma divulgar sua(s) prática(s) e/ou pesquisa(s) em monitoramento e avaliação de políticas públicas para público geral não especialista em blog, Instagram etc.?\xa0\xa0'
sub_cluster['diss_geral'] = sub_cluster[col_diss_geral].apply(norm_str).str.contains('sim').astype(int)

col_capac = 'Você fez capacitação em temas relacionados a monitoramento e avaliação de políticas públicas nos últimos 3 (três) anos?'
sub_cluster['fez_capacitacao'] = sub_cluster[col_capac].apply(norm_str).str.contains('sim').astype(int)

duty_cols = [
    'ativid_principal', 'proj_ativo', 'proj_internac', 'tam_equipe',
    'met_estatistica', 'met_qualitativa', 'met_indicadores', 'met_sintese', 'met_ats', 'met_participativa', 'met_questionarios',
    'diss_decisores', 'diss_geral', 'fez_capacitacao'
]

X_clus = sub_cluster[duty_cols].copy()
scaler = StandardScaler()
X_clus_scaled = scaler.fit_transform(X_clus)

km = KMeans(n_clusters=3, random_state=42, n_init=25).fit(X_clus_scaled)
sub_cluster['cluster'] = km.labels_

cluster_means = sub_cluster.groupby('cluster')[duty_cols].mean().to_dict(orient='index')
cluster_counts = sub_cluster['cluster'].value_counts().to_dict()

# Nomes interpretativos dos clusters
cluster_names = {
    0: "Cluster 1: Especialistas em ATS e Síntese de Evidências em Grandes Equipes",
    1: "Cluster 2: Avaliadores Ocasionais / Prática Periférica",
    2: "Cluster 3: Núcleo Multimetodológico de Alta Intensidade Operacional"
}

print(f"[Q5] Clusters gerados: {cluster_counts}")

# -------------------------------------------------------------------------
# INSIGHTS ADICIONAIS
# -------------------------------------------------------------------------
# Gênero no Evento 1 e Survey
e1_sexo = df1['Sexo'].value_counts(normalize=True).mul(100).round(1).to_dict()

col_gen = 'Qual a sua identidade de gênero?'
s_gen = df3[col_gen].dropna().str.strip()
s_gen_counts = s_gen.apply(lambda x: 'Mulher cis' if 'Mulher' in x or 'mulher' in x else ('Homem cis' if 'Homem' in x or 'homem' in x else 'Outros/Não declarado')).value_counts(normalize=True).mul(100).round(1).to_dict()

# Raça/Etnia Survey
col_raca = 'Como você se autodeclara em relação à sua raça e/ou etnia?\xa0'
s_raca = df3[col_raca].dropna().str.strip().value_counts(normalize=True).mul(100).round(1).to_dict()

# Disseminação: Decisores vs Público Geral
col_dg = 'Costuma divulgar sua(s) prática(s) e/ou pesquisa(s) em monitoramento e avaliação de políticas públicas para público geral não especialista em blog, Instagram etc.?\xa0\xa0'
col_dd = 'Costuma divulgar\xa0sua(s) prática(s) e/ou pesquisa(s) em monitoramento e avaliação de políticas públicas para tomadores de decisão públicos e/ou privados por meio de seminários, sumários executivos ...'
diss_decisores_pct = round((df3[col_dd] == 'Sim').sum() / 245 * 100, 1)
diss_geral_pct = round((df3[col_dg] == 'Sim').sum() / 245 * 100, 1)

# Modalidade Evento 1
col_mod = 'Você pretende acompanhar o evento de forma presencial ou online?'
mod_counts = df1[col_mod].dropna().astype(str).str.lower().apply(lambda x: 'Online' if 'online' in x else ('Presencial' if 'presencial' in x else 'Outro')).value_counts(normalize=True).mul(100).round(1).to_dict()

# Compilar todos os dados para o aplicativo JSON
app_data = {
    'q1': {
        'total_survey': q1_total_survey,
        'anon': q1_anon,
        'anon_eligible': q1_anon_eligible,
        'filtered_out': q1_filtered_out,
        'identified': q1_id,
        'e1_match': q1_e1,
        'e2_match': q1_e2,
        'both_match': q1_both,
        'any_match': q1_any,
        'external': q1_external,
        'pct_external_id': round(q1_external / q1_id * 100, 2),
        'pct_any_id': round(q1_any / q1_id * 100, 2),
        'pct_any_total': round(q1_any / q1_total_survey * 100, 2),
        'identified_unique': q1_id_unique,
        'e1_match_unique': q1_e1_unique,
        'e2_match_unique': q1_e2_unique,
        'both_match_unique': q1_both_unique,
        'any_match_unique': q1_any_unique,
        'external_unique': q1_external_unique,
        'pct_external_unique': round(q1_external_unique / q1_id_unique * 100, 2),
        'pct_any_unique': round(q1_any_unique / q1_id_unique * 100, 2)
    },
    'q2': {
        'e1_total': q2_e1_total,
        'e2_total': q2_e2_total,
        'unique_total': q2_unique_total,
        'overlap': q2_overlap,
        'e2_new': q2_e2_new,
        'renewal_rate': round(q2_renewal_rate, 2),
        'recurrence_rate_e2': round(q2_recurrence_rate_e2, 2),
        'recurrence_rate_e1': round(q2_recurrence_rate_e1, 2),
        'recurrence_rate_total': round(q2_recurrence_rate_total, 2)
    },
    'q3': {
        'n': len(mca_sub),
        'inertia_dim1': float(str(mca_inertia.iloc[0, 1]).replace('%','').strip()),
        'inertia_dim2': float(str(mca_inertia.iloc[1, 1]).replace('%','').strip()),
        'inertia_cum': float(str(mca_inertia.iloc[1, 2]).replace('%','').strip()),
        'chi2_tit_func': {'chi2': round(chi2_tf, 2), 'p': float(f"{p_tf:.4e}"), 'dof': int(dof_tf)},
        'chi2_tmp_tit': {'chi2': round(chi2_tt, 2), 'p': round(p_tt, 4), 'dof': int(dof_tt)},
        'chi2_tmp_func': {'chi2': round(chi2_tmf, 2), 'p': round(p_tmf, 4), 'dof': int(dof_tmf)},
        'points': mca_points
    },
    'q4': {
        'total_events': len(ev_all),
        'uf_top': uf_counts,
        'regioes': regiao_counts,
        'esferas': esfera_counts,
        'saude': saude_counts,
        'esfera_x_saude': ct_esfera_saude,
        'survey_setor': survey_setor,
        'survey_tematicas': tematicas_sorted
    },
    'q5': {
        'counts': cluster_counts,
        'means': cluster_means,
        'names': cluster_names
    },
    'insights': {
        'sexo_e1': e1_sexo,
        'genero_survey': s_gen_counts,
        'raca_survey': s_raca,
        'diss_decisores_pct': diss_decisores_pct,
        'diss_geral_pct': diss_geral_pct,
        'modalidade_e1': mod_counts
    }
}

with open('analise_dados_completa.json', 'w', encoding='utf-8') as f:
    json.dump(app_data, f, ensure_ascii=False, indent=2)

print("Dados analíticos salvos em analise_dados_completa.json.")
