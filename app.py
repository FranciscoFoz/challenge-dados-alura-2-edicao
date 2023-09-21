import streamlit as st
from joblib import load
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

pd.options.display.max_columns = 999



def processar_dados(dict_respostas):

    features = load('src/features/features.joblib')
    
    respostas = pd.DataFrame([dict_respostas])

    respostas = respostas.replace({'Não': 0, 'Sim': 1})
    variaveis_numericas = respostas[['meses_de_contrato', 'fatura_mensal']]
    variaveis_binarias = respostas[['idoso', 'tem_conjuge', 'tem_dependentes']]
    variaveis_multiplas = respostas[['possui_servico_internet', 'possui_servico_seguranca_online',
                                    'possui_servico_backup_online', 'possui_servico_protecao_dispositivo',
                                    'possui_servico_suporte_tecnico', 'possui_TV_a_cabo',
                                    'possui_TV_streaming', 'tipo_de_contrato', 'forma_de_pagamento']]
    variaveis_multiplas_normalizadas = pd.get_dummies(variaveis_multiplas, dtype=int)
    
    df_processado = pd.concat([variaveis_binarias, variaveis_numericas, variaveis_multiplas_normalizadas], axis=1) 

    df_final = df_processado.reindex(columns=features, fill_value=0)
    
    return df_final


def prever_resultado(df):
    modelo = load('models/melhor_modelo.pkl')

    resultado = modelo.predict(df)[0]
    
    prob_churn = (modelo.predict_proba(df)[0][1] * 100).round(2)
    
    return resultado,prob_churn







st.set_page_config(
    layout='wide',
    page_title='predicao-churn-novexus',
    page_icon=':chart_with_downwards_trend:'
)

st.image('https://raw.githubusercontent.com/FranciscoFoz/challenge-dados-alura-2-edicao/main/reports/figures/Identidade%20visual/Logo%20(2).png',
         width=700)
st.title('SIMULADOR DE CHURN:chart_with_downwards_trend:')

# PAINÉL DE INSERÇÕES
expander_pessoal = st.expander("Pessoal")
expander_servicos = st.expander("Serviços")
expander_contrato = st.expander("Contrato")

dict_respostas = {}
lista_campos = load('src/features/lista_campos.pkl')


perguntas = {
    'idoso': 'O cliente é idoso?',
    'tem_conjuge': 'O cliente tem cônjuge ?',
    'tem_dependentes': 'O cliente tem dependentes ?',
    'possui_servico_internet': 'O cliente possui serviço de internet?',
    'possui_servico_seguranca_online': 'O cliente possui serviço de segurança online?',
    'possui_servico_backup_online': 'O cliente possui serviço de backup online?',
    'possui_servico_protecao_dispositivo': 'O cliente possui serviço de proteção do dispositivo?',
    'possui_servico_suporte_tecnico': 'O cliente possui serviço de suporte técnico?',
    'possui_TV_a_cabo': 'O cliente possui TV a cabo?',
    'possui_TV_streaming': 'O cliente possui TV streaming?',
    'meses_de_contrato': 'Quantos meses de contrato o cliente possui?',
    'tipo_de_contrato': 'Qual o tipo de contrato do cliente?',
    'recebimento_de_fatura_online': 'O cliente optou por receber a fatura online?',
    'forma_de_pagamento': 'Qual a forma de pagamento do cliente?',
    'fatura_mensal': 'Qual o valor médio da fatura mensal do cliente?',
}

with expander_pessoal:
    for campo in ['idoso', 'tem_conjuge', 'tem_dependentes']:
        dict_respostas[campo] = st.selectbox(perguntas[campo], ['Sim', 'Não'])

with expander_servicos:
    for campo in ['possui_servico_internet', 'possui_servico_seguranca_online', 'possui_servico_backup_online',
                  'possui_servico_protecao_dispositivo', 'possui_servico_suporte_tecnico', 'possui_TV_a_cabo',
                  'possui_TV_streaming']:
        dict_respostas[campo] = st.selectbox(perguntas[campo], lista_campos[campo])

with expander_contrato:
    for campo in ['tipo_de_contrato', 'recebimento_de_fatura_online', 'forma_de_pagamento']:
        dict_respostas[campo] = st.selectbox(perguntas[campo], lista_campos[campo])

    dict_respostas['meses_de_contrato'] = st.slider(perguntas['meses_de_contrato'],
                                                    help='Pode-se mover a barra usando as setas do teclado',
                                                    min_value=0, max_value=360, step=1)
    dict_respostas['fatura_mensal'] = st.slider(perguntas['fatura_mensal'],
                                                help='Pode-se mover a barra usando as setas do teclado',
                                                min_value=0, max_value=200, step=1)
    

if st.button("Avaliar"):
    df_processado = processar_dados(dict_respostas)
    resultado, prob_churn = prever_resultado(df_processado)

    if resultado > 0:
        st.write('O cliente deixará a empresa.')
        st.write(f'Probabilidade de churn: {prob_churn}% .')
    else:
        st.write('O cliente NÃO deixará a empresa.')
        st.write(f'Probabilidade de churn: {prob_churn}% .')


