import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from joblib import dump, load
import pickle


def carregar_dados(dados):
    
    df = pd.read_json(dados)
    
    return df

def normalizar_dataframe(df):
    
    customer = pd.json_normalize(df['customer'])
    phone = pd.json_normalize(df['phone'])
    internet = pd.json_normalize(df['internet'])
    account = pd.json_normalize(df['account'])

    df_minimo = df[['customerID','Churn']]

    df_normalizado = pd.concat([df_minimo,customer,phone,internet,account],axis=1)
    
    return df_normalizado

def limpar_valores(df):
    
    df['Charges.Total'] = df['Charges.Total'].replace(' ','0')
    df['Charges.Total'] = df['Charges.Total'].astype('float')

    #Excluindo linhas onde o churn é nulo, pois não será possível "classficar" o cliente
    df['Churn'].replace('',None,inplace=True)
    df.dropna(inplace=True)
    
    df_total_gasto_0 = df.query('`Charges.Total` == 0')
    df = df.drop(labels=df_total_gasto_0.index)
    
    return df

def renomear_colunas(df):
    
    df.columns = ['customerID', 'churn', 'genero', 'idoso', 'tem_conjuge',
                  'tem_dependentes','meses_de_contrato', 'possui_servico_telefone', 
                  'possui_multiplas_linhas','possui_servico_internet',
                  'possui_servico_seguranca_online', 'possui_servico_backup_online',
                  'possui_servico_protecao_dispositivo','possui_servico_suporte_tecnico',
                  'possui_TV_a_cabo', 'possui_TV_streaming', 'tipo_de_contrato',
                  'recebimento_de_fatura_online','forma_de_pagamento', 
                  'fatura_mensal','total_gasto']
    
    return df

def padronizar_dados(df):

    df['idoso'] = df['idoso'].replace({0:'No',1:'Yes'}) #Padronizando formato de leitura inicial

    #Tradução dos dados para melhor visualização
    df.replace({'No':'Não',
                'Yes':'Sim',
                'Fiber optic':'Fibra óptica',
                'One year':'Um ano',
                'Month-to-month':'Mês-a-mês',
                'Two year':'Dois anos',
                'Mailed check':'Cheque enviado',
                'Electronic check':'Cheque eletrônico',
                'No phone service':'Sem serviço de telefone',
                'No internet service':'Sem serviço de internet',
                'Credit card (automatic)':'Cartão de crédito (automático)',
                'Bank transfer (automatic)':'Transferência Bancária (Automática)',
                'Female':'Feminino',
                'Male':'Masculino'},inplace=True)
    
    return df

def normalizar_dados(df):

    df = df.drop(columns='customerID').copy()

    variaveis_numericas = df[['meses_de_contrato','fatura_mensal','total_gasto']]

    variaveis_binarias = df[['churn','idoso','tem_conjuge','tem_dependentes','possui_servico_telefone']].replace({'Não':0,'Sim':1})

    variaveis_multiplas = df[['genero','possui_multiplas_linhas','possui_servico_internet','possui_servico_seguranca_online',
                            'possui_servico_backup_online','possui_servico_protecao_dispositivo','possui_servico_suporte_tecnico',
                            'possui_TV_a_cabo','possui_TV_streaming','tipo_de_contrato','forma_de_pagamento']]

    variaveis_multiplas_normalizadas = pd.get_dummies(variaveis_multiplas,dtype=int)

    df_final = pd.concat([variaveis_binarias,variaveis_numericas,variaveis_multiplas_normalizadas],axis=1)
    
    return df_final

def excluir_colunas(df): 

    df.drop(columns=[
        'possui_servico_telefone','genero_Feminino', 'genero_Masculino',
        'possui_multiplas_linhas_Não',
        'possui_multiplas_linhas_Sem serviço de telefone',
        'possui_multiplas_linhas_Sim',
        'total_gasto'],
        inplace=True)
    
    return df

def pipeline_transformacao(dados):
    
    pipeline = (
        carregar_dados(dados)
        .pipe(normalizar_dataframe)
        .pipe(limpar_valores)
        .pipe(renomear_colunas)
        .pipe(padronizar_dados)
        .pipe(normalizar_dados)
        .pipe(excluir_colunas)
    )
    
    return pipeline



def treinar_e_avaliar_modelo(df, modelo):
    
    X = df.drop(columns=['churn'], axis = 1)
    y = df['churn']
        
    modelo.fit(X,y)
    y_pred = modelo.predict(X)
    auc_test = roc_auc_score(y, y_pred)
    
    print("\nAUC:", auc_test.round(3))
    print("\nClassification Report:")
    print(classification_report(y, y_pred))
    
    return modelo

def treinar_modelo(df, modelo):
    
    X = df.drop(columns=['churn'], axis = 1)
    y = df['churn']
        
    modelo.fit(X,y)
    
    return modelo

def salvar_modelo(modelo, nome_arquivo):
    
    caminho = f'/home/franciscofoz/Documents/GitHub/challenge-dados-alura-2-edicao/Models/{nome_arquivo}.pkl'
    
    with open(caminho, 'wb') as arquivo_modelo:
        pickle.dump(modelo, arquivo_modelo)
    








dados = 'https://challenge-data-science-3ed.s3.amazonaws.com/Telco-Customer-Churn.json'

melhor_modelo = load('/home/franciscofoz/Documents/GitHub/challenge-dados-alura-2-edicao/Notebooks/modelo_churn_novexus_1.joblib')

df = pipeline_transformacao(dados)

# APENAS VERIFICAÇÃO DO TREINO FINAL
#treinar_e_avaliar_modelo(df,melhor_modelo)


modelo = treinar_modelo(df,melhor_modelo)


salvar_modelo(modelo, 'melhor_modelo')


            


