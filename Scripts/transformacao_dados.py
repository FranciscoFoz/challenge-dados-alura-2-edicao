import pandas as pd

class TransformacaoDados:
    def carregar_dados(self, dados):
        self.df = pd.read_json(dados)
    
    def normalizar_dataframe(self):
        customer = pd.json_normalize(self.df['customer'])
        phone = pd.json_normalize(self.df['phone'])
        internet = pd.json_normalize(self.df['internet'])
        account = pd.json_normalize(self.df['account'])

        df_minimo = self.df[['customerID','Churn']]

        self.df_normalizado = pd.concat([df_minimo, customer, phone, internet, account], axis=1)
    
    def limpar_valores(self):
        self.df_normalizado['Charges.Total'] = self.df_normalizado['Charges.Total'].replace(' ', '0')
        self.df_normalizado['Charges.Total'] = self.df_normalizado['Charges.Total'].astype('float')

        # Excluindo linhas onde o churn é nulo, pois não será possível "classificar" o cliente
        self.df_normalizado['Churn'].replace('', None, inplace=True)
        self.df_normalizado.dropna(inplace=True)

        df_total_gasto_0 = self.df_normalizado.query('`Charges.Total` == 0')
        self.df_normalizado = self.df_normalizado.drop(labels=df_total_gasto_0.index)
    
    def renomear_colunas(self):
        self.df_normalizado.columns = ['customerID', 'churn', 'genero', 'idoso', 'tem_conjuge',
                  'tem_dependentes','meses_de_contrato', 'possui_servico_telefone', 
                  'possui_multiplas_linhas','possui_servico_internet',
                  'possui_servico_seguranca_online', 'possui_servico_backup_online',
                  'possui_servico_protecao_dispositivo','possui_servico_suporte_tecnico',
                  'possui_TV_a_cabo', 'possui_TV_streaming', 'tipo_de_contrato',
                  'recebimento_de_fatura_online','forma_de_pagamento', 
                  'fatura_mensal','total_gasto']
    
    def padronizar_dados(self):
        self.df_normalizado['idoso'] = self.df_normalizado['idoso'].replace({0:'No',1:'Yes'})

        # Tradução dos dados para melhor visualização
        self.df_normalizado.replace({'No':'Não',
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
                'Male':'Masculino'}, inplace=True)
    
    def normalizar_dados(self):
        self.df_normalizado = self.df_normalizado.drop(columns='customerID').copy()

        variaveis_numericas = self.df_normalizado[['meses_de_contrato','fatura_mensal','total_gasto']]

        variaveis_binarias = self.df_normalizado[['churn','idoso','tem_conjuge','tem_dependentes','possui_servico_telefone']].replace({'Não':0,'Sim':1})

        variaveis_multiplas = self.df_normalizado[['genero','possui_multiplas_linhas','possui_servico_internet','possui_servico_seguranca_online',
                            'possui_servico_backup_online','possui_servico_protecao_dispositivo','possui_servico_suporte_tecnico',
                            'possui_TV_a_cabo','possui_TV_streaming','tipo_de_contrato','forma_de_pagamento']]

        variaveis_multiplas_normalizadas = pd.get_dummies(variaveis_multiplas, dtype=int)

        self.df_final = pd.concat([variaveis_binarias, variaveis_numericas, variaveis_multiplas_normalizadas], axis=1)
    
    def excluir_colunas(self):
        self.df_final.drop(columns=[
            'possui_servico_telefone','genero_Feminino', 'genero_Masculino',
            'possui_multiplas_linhas_Não',
            'possui_multiplas_linhas_Sem serviço de telefone',
            'possui_multiplas_linhas_Sim',
            'total_gasto'],
            inplace=True)
    
    def pipeline_transformacao(self, dados):
        self.carregar_dados(dados)
        self.normalizar_dataframe()
        self.limpar_valores()
        self.renomear_colunas()
        self.padronizar_dados()
        self.normalizar_dados()
        self.excluir_colunas()

