import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from joblib import dump, load
import pickle

from transformacao_dados import TransformacaoDados

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


dados = 'https://challenge-data-science-3ed.s3.amazonaws.com/Telco-Customer-Churn.json'

melhor_modelo = load('/home/franciscofoz/Documents/GitHub/challenge-dados-alura-2-edicao/Notebooks/modelo_churn_novexus_1.joblib')

transformador = TransformacaoDados()
df = transformador.pipeline_transformacao(dados)

treinar_e_avaliar_modelo(df,melhor_modelo)



            


