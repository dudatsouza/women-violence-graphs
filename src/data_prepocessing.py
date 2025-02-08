import pandas as pd
from difflib import SequenceMatcher
import warnings
from itertools import combinations
import re

# Ignorar todos os warnings
warnings.filterwarnings("ignore")

# padronizar todos os dados do dataframe, removendo espaços extras, retirando os caracteres especiais e deixando tudo em caixa alta
def standardize_data(df):
    for column in df.columns:
        # Converte a coluna para string, substituindo valores nulos por uma string vazia
        df[column] = df[column].astype(str).fillna("")
        # Remove espaços extras, coloca em caixa alta e remove caracteres especiais
        df[column] = df[column].str.strip()
        df[column] = df[column].str.upper()
        df[column] = df[column].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df[column] = df[column].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex=True)
    return df

# remover coluna "Número REDS", "Qtde Envolvidos", "Ano Fato", "Mês Numérico Fato", "UF - Sigla", "Bairro Não Cadastrado", "Tentado/Consumado", "Grupo Tipo Envolvimento", "Sexo" e "Tentado/Consumado Nat Principal"
def remove_columns(df):
    df.drop(columns=["Número REDS", "Qtde Envolvidos", "Ano Fato", "Mês Numérico Fato", "UF - Sigla", "Grupo Tipo Envolvimento", "Sexo", "Tentado/Consumado Nat Principal"], inplace=True)
    return df

# adicionar coluna de id
def add_id_column(df):
    df["ID"] = range(1, len(df) + 1)

    # coloca a coluna id na primeira posição
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df

def identifica(df_nomes, threshold, df_crimes, df_localidade):
    for i, j in combinations(range(len(df_nomes)), 2):
        # Cidades comparadas
        cidade1 = df_nomes['Município'].iloc[i]
        cidade2 = df_nomes['Município'].iloc[j]
        
        # Verifica a similaridade entre as cidades
        if similaridade_entre_cidades(cidade1, cidade2) > threshold and \
           similaridade_entre_cidades(cidade1, cidade2) < 1:
            # Checa se a cidade já está em ambos os dataframes
            if (cidade1 in df_crimes['Município'].values and cidade1 in df_localidade['Município'].values) or \
               (cidade2 in df_crimes['Município'].values and cidade2 in df_localidade['Município'].values):
                continue
            else:
                # Define o nome padrão como o menor em termos de comprimento
                nome_padrao = min(cidade1, cidade2, key=len)
                
                # Atualiza os nomes nos dataframes
                for df in [df_crimes, df_localidade]:
                    df.loc[df['Município'] == cidade1, 'Município'] = nome_padrao
                    df.loc[df['Município'] == cidade2, 'Município'] = nome_padrao
    return df_crimes, df_localidade

def merge(df_crimes, df_localidade, threshold=0.86):
    # Merge inicial
    df_merged = pd.merge(df_crimes, df_localidade, on='Município', how='outer', indicator=True)

    # Identifica as cidades sem correspondência
    cidades_sem_latlong = df_merged[df_merged['_merge'] != 'both']['Município'].dropna().unique()
    
    # Cria um DataFrame com as cidades faltantes
    df_faltantes = pd.DataFrame({'Município': cidades_sem_latlong})
    
    # Trata as cidades faltantes usando a função identifica
    df_crimes, df_localidade = identifica(df_faltantes, threshold, df_crimes, df_localidade)

    # Reexecuta o merge após a padronização
    df_merged_final = pd.merge(df_crimes, df_localidade, on='Município', how='outer')

    # ordena o dataframe de acordo com a coluna "Data Fato"
    df_merged_final.sort_values(by='Data Fato', ascending=True, inplace=True)   

    return df_merged_final

def similaridade_entre_cidades(municipio1, municipio2):
    similaridade = SequenceMatcher(None, municipio1, municipio2).ratio()

    return similaridade

# Função que remove acentos e caracteres especiais
def limpar_nomes_colunas(nome):
    # Substituir acentos manualmente
    nome = re.sub(r'[áàâãä]', 'a', nome, flags=re.IGNORECASE)
    nome = re.sub(r'[éèêë]', 'e', nome, flags=re.IGNORECASE)
    nome = re.sub(r'[íìîï]', 'i', nome, flags=re.IGNORECASE)
    nome = re.sub(r'[óòôõö]', 'o', nome, flags=re.IGNORECASE)
    nome = re.sub(r'[úùûü]', 'u', nome, flags=re.IGNORECASE)
    nome = re.sub(r'[ç]', 'c', nome, flags=re.IGNORECASE)
    # Remove caracteres especiais
    nome = re.sub(r'[^a-zA-Z0-9 ]', ' ', nome)
    # Remove espaços extras
    nome = re.sub(r'\s+', ' ', nome).strip()
    return nome

def remover_dados_irelevantes(df):
    # se na coluna "Bairro" tiver "INVALIDO", deverá verificar se na coluna "Bairro Nao Cadastrado" tem algum valor diferente, se tiver, substituir o valor da coluna "Bairro" pelo valor da coluna "Bairro Nao Cadastrado" caso não tenha, essa linha deverá ser removida
    df.loc[(df["Bairro"] == "INVALIDO") & (df["Bairro Nao Cadastrado"] != "NAN"), "Bairro"] = df["Bairro Nao Cadastrado"]
    df = df.drop(df[(df["Bairro"] == "INVALIDO") & (df["Bairro Nao Cadastrado"] == "NAN")].index)

    df.loc[(df["Bairro Envolvido"] == "INVALIDO") & (df["Bairro Envolvido Nao Cadastrado"] != "NAN"), "Bairro Envolvido"] = df["Bairro Envolvido Nao Cadastrado"]
    df = df.drop(df[(df["Bairro Envolvido"] == "INVALIDO") & (df["Bairro Envolvido Nao Cadastrado"] == "NAN")].index)

    # retirar coluna "Bairro Nao Cadastrado" e "Bairro Envolvido Nao Cadastrado"
    df.drop(columns=["Bairro Nao Cadastrado", "Bairro Envolvido Nao Cadastrado"], inplace=True)

    # se tiver em qualquer uma das colunas a o valor "IGNORADO", "INVALIDO", "IGNORADA", "PREENCHIMENTO OPCIONAL", "SEM INFORMACAO" essa linha deverá ser removida
    valores = ["IGNORADO", "INVALIDO", "IGNORADA", "PREENCHIMENTO OPCIONAL", "SEM INFORMACAO", "INEXISTENTE"]
    for col in df.columns:
        for valor in valores:
            df = df.drop(df[df[col] == valor].index)

    # retiras as linhas q possuem valores nulos
    df = df.dropna()

    return df


if __name__ == '__main__':
    # carregar os dados
    df_crimes = pd.read_csv("./datasets/violencias/crimes.csv", 
                delimiter=',', # Especifica o delimitador correto
                encoding='utf-8', # Especifica a codificação correta
                engine='python' # Especifica o engine correto
                )
    df_localidade = pd.read_csv("./datasets/localidade/localidade.csv",
                delimiter=',', # Especifica o delimitador correto
                encoding='utf-8',  # Especifica a codificação correta
                engine='python' # Especifica o engine correto
                )
    
    # remover colunas
    df_crimes = remove_columns(df_crimes)
    print("Colunas removidas com sucesso!")
    
    # Aplicando a limpeza apenas na primeira linha
    df_crimes.columns = [limpar_nomes_colunas(col) for col in df_crimes.columns]

    # padronizar os dados das colunas "Desc Longa Local Imediato", "Bairro", "Descricao Grupo Natureza", "Descricao Subclasse Natureza", "Causa Presumida", "Descricao Meio Utilizado", "Raca Cor", "Escolaridade", "Relacao Vitima Autor", "Bairro Envolvido", "Bairro Envolvido Nao Cadastrado", "Municipio Envolvido", "Descricao Subclasse Nat Principal"
    df_temp = df_crimes[["Desc Longa Local Imediato", "Bairro", "Descricao Grupo Natureza", "Descricao Subclasse Natureza", "Causa Presumida", "Descricao Meio Utilizado", "Raca Cor", "Escolaridade", "Relacao Vitima Autor", "Bairro Envolvido", "Bairro Envolvido Nao Cadastrado", "Municipio Envolvido", "Descricao Subclasse Nat Principal"]].copy()
    df_temp = standardize_data(df_temp)
    df_crimes[["Desc Longa Local Imediato", "Bairro", "Descricao Grupo Natureza", "Descricao Subclasse Natureza", "Causa Presumida", "Descricao Meio Utilizado", "Raca Cor", "Escolaridade", "Relacao Vitima Autor", "Bairro Envolvido", "Bairro Envolvido Nao Cadastrado", "Municipio Envolvido", "Descricao Subclasse Nat Principal"]] = df_temp[["Desc Longa Local Imediato", "Bairro", "Descricao Grupo Natureza", "Descricao Subclasse Natureza", "Causa Presumida", "Descricao Meio Utilizado", "Raca Cor", "Escolaridade", "Relacao Vitima Autor", "Bairro Envolvido", "Bairro Envolvido Nao Cadastrado", "Municipio Envolvido", "Descricao Subclasse Nat Principal"]]

    df_temp = df_localidade[["Município"]].copy()
    df_temp = standardize_data(df_temp)
    df_localidade["Município"] = df_temp["Município"]
    print("Apenas a coluna 'Município' foi padronizada!")    

    # mudar o nomes da coluna Municipio para Município
    df_crimes.rename(columns={"Municipio": "Município"}, inplace=True)

    # merge dos dataframes
    df_merged = merge(df_crimes, df_localidade)
    print("Dataframes unidos com sucesso!")

    # remover dados irrelevantes
    df_merged = remover_dados_irelevantes(df_merged)
    print("Dados irrelevantes removidos com sucesso!")

    # adicionar coluna de id
    df_merged = add_id_column(df_merged)
    print("Coluna de id adicionada com sucesso!")

    # criar arquivo dados.csv
    df_merged.to_csv("./datasets/dados_pre.csv", index=False)
    print("Arquivo dados_pre.csv criado com sucesso!")

   