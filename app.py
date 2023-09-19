import streamlit as st
from joblib import load
import pandas as pd

st.set_page_config(
    layout='wide',
    page_title='predicao-churn-novexus',
    page_icon=':chart_with_downwards_trend:'
)

st.image('https://raw.githubusercontent.com/FranciscoFoz/challenge-dados-alura-2-edicao/main/reports/figures/Identidade%20visual/Logo%20(2).png',
         width=700)
st.title('SIMULADOR DE CHURN:chart_with_downwards_trend:')

expander_pessoal = st.expander("Pessoal")
expander_servicos = st.expander("Serviços")
expander_contrato = st.expander("Contrato")

dict_respostas = {}
lista_campos = load('src/features/features.joblib')

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

-------------------------------------------------CORRIGIR ERRO-------------------------------------------------
with expander_pessoal:
    for campo in ['idoso', 'tem_conjuge', 'tem_dependentes']:
        dict_respostas[campo] = st.selectbox(perguntas[campo], ['Sim', 'Não'])

with expander_servicos:
    for campo in ['possui_servico_internet', 'possui_servico_seguranca_online', 'possui_servico_backup_online',
                  'possui_servico_protecao_dispositivo', 'possui_servico_suporte_tecnico', 'possui_TV_a_cabo',
                  'possui_TV_streaming']:
        dict_respostas[campo] = st.selectbox(perguntas[campo], lista_campos[campo])

with expander_contrato:
    for campo in ['meses_de_contrato', 'tipo_de_contrato', 'recebimento_de_fatura_online', 'forma_de_pagamento',
                  'fatura_mensal']:
        dict_respostas[campo] = st.selectbox(perguntas[campo], lista_campos[campo])

