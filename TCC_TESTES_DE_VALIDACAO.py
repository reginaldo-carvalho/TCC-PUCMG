#!/usr/bin/env python
# coding: utf-8

# # Testes de Validação
# 
# ### Aqui serão apresentados os testes da solução desenvolvida, confrontando os dados apresentados no dashboard com consultas independentes realizadas na base de dados de origem.

# # Imports:

# In[1]:


# Importando bibliotecas necessárias
import os
import pandas as pd


# # Configuração:

# In[2]:


# Diretório onde os arquivos CSV estão armazenados
diretorio = 'C:/Users/user/OneDrive/Documentos/Pós Graduação/TCC2/Base de dados'


# In[3]:


# Lista para armazenar todos os DataFrames carregados dos arquivos CSV
dataframes = []


# # Pré tratamento dos Dados:

# In[4]:


# Loop através dos arquivos no diretório
for filename in os.listdir(diretorio):
    if filename.endswith('.csv'):
        # Caminho completo do arquivo
        filepath = os.path.join(diretorio, filename)
        
        # Carregando o arquivo CSV em um DataFrame
        df = pd.read_csv(filepath, delimiter=';', header=0)
        
        # Removendo as colunas especificadas
        colunas_para_remover = ["Região", "Cidade", "Como Comprou Contratou", "Respondida", "Segmento de Mercado", "Área"]
        df = df.drop(colunas_para_remover, axis=1)
        
        # Filtrando as linhas com 'Uber' na coluna 'Nome Fantasia'
        df = df.loc[df['Nome Fantasia'] == 'Uber']
        
        # Filtrando as linhas com 'Avaliação Reclamação' diferente de 'Não Avaliada'
        df = df.loc[df['Avaliação Reclamação'] != 'Não Avaliada']
        
        # Removendo linhas que contenham algum valor em branco em qualquer coluna
        df = df.dropna(how='any')
        
        # Adicionando o DataFrame à lista
        dataframes.append(df)


# In[12]:


dados_completos.columns


# # Teste 1
# ### Total de reclamações // card

# In[5]:


# Concatenando todos os DataFrames em um único DataFrame
dados_completos = pd.concat(dataframes, ignore_index=True)

# Contagem do total de reclamações
total_reclamacoes = dados_completos.shape[0]

# Exibindo o resultado
print(f"O total de reclamações no conjunto de dados é: {total_reclamacoes}")


# # Teste 2
# ### Total de reclamações por período // card, segmentação de dados

# In[11]:


# Convertendo a coluna 'Data Finalização' para o formato de data
dados_completos['Data Finalização'] = pd.to_datetime(dados_completos['Data Finalização'], format='%d/%m/%Y', errors='coerce')

# Filtrando apenas os registros do primeiro semestre de 2023
dados_primeiro_semestre_2023 = dados_completos[(dados_completos['Data Finalização'].dt.year == 2023) & 
                                               (dados_completos['Data Finalização'].dt.month <= 6)]

# Contagem do total de reclamações no primeiro semestre de 2023
total_reclamacoes_primeiro_semestre_2023 = dados_primeiro_semestre_2023.shape[0]

# Exibindo o resultado
print(f"O total de reclamações no primeiro semestre de 2023 é: {total_reclamacoes_primeiro_semestre_2023}")


# # Teste 3
# ### Nota média // velocímetro
# 

# In[13]:


# Calculando a média dos valores da coluna 'Nota do Consumidor'
nota_media = dados_completos['Nota do Consumidor'].mean()

# Exibindo o resultado formatado como '0,00'
print(f"A nota média dos consumidores em toda a base de dados é: {nota_media:.2f}")


# # Teste 4
# ### Tempo médio de resposta // velocímetro
# 

# In[14]:


# Calculando a média dos valores da coluna 'Tempo Resposta'
tempo_medio_resposta = dados_completos['Tempo Resposta'].mean()

# Exibindo o resultado formatado como '0,00'
print(f"O tempo médio de resposta é: {tempo_medio_resposta:.2f} dias")


# # Teste 5
# ### Reclamações com contato prévio // Treemap
# 

# In[15]:


# Contando o total de registros do período, segmentado por 'Procurou Empresa'
contagem_por_procurou_empresa = dados_completos.groupby('Procurou Empresa').size()

# Exibindo o resultado
print(contagem_por_procurou_empresa)


# # Teste 6
# ### Top n reclamações por grupo problema // barras empilhadas
# 

# In[16]:


# Contando o total de registros, segmentado por 'Grupo Problema' e exibindo os três maiores
contagem_por_grupo_problema = dados_completos.groupby('Grupo Problema').size().nlargest(3)

# Exibindo o resultado
print(contagem_por_grupo_problema)


# # Teste 7
# ### Total de reclamações segmentada por avaliação e ano // gráfico de área
# 

# In[17]:


# Convertendo a coluna 'Data Finalização' para o formato de data
dados_completos['Data Finalização'] = pd.to_datetime(dados_completos['Data Finalização'], errors='coerce')

# Criando uma nova coluna para armazenar o ano da data de finalização
dados_completos['Ano'] = dados_completos['Data Finalização'].dt.year

# Contando o total de registros, segmentado por 'Avaliação Reclamação' e agrupado por ano
contagem_por_avaliacao_ano = dados_completos.groupby(['Avaliação Reclamação', 'Ano']).size()

# Exibindo o resultado
print(contagem_por_avaliacao_ano)


# # Teste 8
# ### Índice resolvidas // gráfico de pizza
# 

# In[18]:


# Calculando a porcentagem do total de registros por 'Avaliação Reclamação'
porcentagem_por_avaliacao = (dados_completos['Avaliação Reclamação'].value_counts(normalize=True) * 100).round(2)

# Exibindo o resultado
print(porcentagem_por_avaliacao)


# # Teste 9
# ### Nota média por assunto // treemap
# 

# In[20]:


# Calculando a média da nota do consumidor por assunto
media_por_assunto = dados_completos.groupby('Assunto')['Nota do Consumidor'].mean()

# Exibindo o resultado formatado com duas casas decimais
print(media_por_assunto.round(2))


# # Teste 10
# ### Total de reclamações 30 dias // card
# 

# In[30]:


# Calculando a data correspondente aos últimos 30 dias a partir da data mais recente
data_mais_recente = pd.to_datetime(dados_completos['Data Finalização']).max()
data_limite = data_mais_recente - pd.DateOffset(days=30)

# Filtrando os registros dos últimos 30 dias
dados_ultimos_30_dias = dados_completos[dados_completos['Data Finalização'] >= data_limite]

# Calculando a contagem total de registros
contagem_total_registros = len(dados_ultimos_30_dias)

# Exibindo o resultado
print(f"Total de registros nos últimos 30 dias: {contagem_total_registros}")


# # Teste 11
# ### Nota média 30 dias // kpi
# 

# In[37]:


# Calculando a data correspondente aos últimos 30 dias a partir da data mais recente
data_mais_recente = pd.to_datetime(dados_completos['Data Finalização']).max()
data_limite = data_mais_recente - pd.DateOffset(days=30)

# Filtrando os registros dos últimos 30 dias
dados_ultimos_30_dias = dados_completos[dados_completos['Data Finalização'] >= data_limite]

# Calculando a nota média dos últimos 30 dias
nota_media_ultimos_30_dias = dados_ultimos_30_dias['Nota do Consumidor'].mean()

# Exibindo o resultado
print(f"Nota média nos últimos 30 dias: {nota_media_ultimos_30_dias:.2f}")



# # Teste 12
# ### Tempo médio 30 dias // kpi
# 

# In[38]:


# Calculando a data correspondente aos últimos 30 dias a partir da data mais recente
data_mais_recente = pd.to_datetime(dados_completos['Data Finalização']).max()
data_limite = data_mais_recente - pd.DateOffset(days=30)

# Filtrando os registros dos últimos 30 dias
dados_ultimos_30_dias = dados_completos[dados_completos['Data Finalização'] >= data_limite]

# Calculando o tempo médio dos últimos 30 dias
tempo_medio_ultimos_30_dias = dados_ultimos_30_dias['Tempo Resposta'].mean()

# Exibindo o resultado
print(f"Tempo médio de resposta nos últimos 30 dias: {tempo_medio_ultimos_30_dias:.2f} dias")


# # Teste 13
# ### Avaliação da reclamação 30 dias // rosca

# In[39]:


# Calculando a data correspondente aos últimos 30 dias a partir da data mais recente
data_mais_recente = pd.to_datetime(dados_completos['Data Finalização']).max()
data_limite = data_mais_recente - pd.DateOffset(days=30)

# Filtrando os registros dos últimos 30 dias
dados_ultimos_30_dias = dados_completos[dados_completos['Data Finalização'] >= data_limite]

# Contando os registros dos últimos 30 dias, segmentados pela avaliação da reclamação
contagem_por_avaliacao = dados_ultimos_30_dias['Avaliação Reclamação'].value_counts()

# Exibindo os resultados no formato 000 (00,00%)
for avaliacao, contagem in contagem_por_avaliacao.items():
    percentual = (contagem / dados_ultimos_30_dias.shape[0]) * 100
    print(f"{avaliacao}: {contagem:03d} ({percentual:.2f}%)")


# # Teste 14
# ### Avaliação por faixa etária 30 dias // colunas empilhadas

# In[47]:


# Calculando a data mais recente
data_mais_recente = dados_completos['Data Finalização'].max()

# Calculando a data correspondente aos últimos 30 dias a partir da data mais recente
data_limite = data_mais_recente - pd.DateOffset(days=30)

# Filtrando os registros dos últimos 30 dias
dados_ultimos_30_dias = dados_completos[dados_completos['Data Finalização'] >= data_limite]

# Agrupando por faixa etária e contando os registros
contagem_por_faixa_etaria = dados_ultimos_30_dias.groupby('Faixa Etária').size()

# Exibindo o resultado
print(contagem_por_faixa_etaria)
print(f"Total de registros: {dados_ultimos_30_dias.shape[0]}")


# In[ ]:




