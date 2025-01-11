import pandas as pd
from difflib import SequenceMatcher
import warnings
import os

# Ignorar todos os warnings
warnings.filterwarnings("ignore")

def converter_xlsx_para_csv(caminho_xlsx, caminho_csv):
    """
    Converte um arquivo Excel (.xlsx) para CSV.
    
    Parâmetros:
    - caminho_xlsx: Caminho do arquivo Excel de entrada.
    - caminho_csv: Caminho onde o arquivo CSV será salvo.
    """
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(caminho_xlsx)
        
        # Salva como CSV
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        
        print(f"     - Arquivo CSV salvo em: {caminho_csv}")
    except Exception as e:
        print(f"     - Erro ao converter arquivo: {e}")


# juntar dados dos arquivos de violencia 
# arquivos para serem juntados: /datasets/feminicidio_2018.csv, /datasets/feminicidio_2019.csv, /datasets/feminicidio_2020.csv, /datasets/feminicidio_2021.csv, violencia_domestica_2014.csv, violencia_domestica_2015.csv, violencia_domestica_2016.csv, violencia_domestica_2017.csv, violencia_domestica_2018.csv, violencia_domestica_2019.csv, violencia_domestica_2020.csv, violencia_domestica_2021.csv
#depois apagar a primeira coluna, mudar a celula "municipio_fato" para "Município", mudar a celula "data_fato" para "Data", mudar a celula "mes" para "Mês", mudar a celula "ano" para "Ano", mudar a celula "risp" para "RISP", mudar a celula "rmbh" para "RMBH", mudar celula de "tentado_consumado" para "Tentado/Consumado", mudar celula de "qtde_vitimas" para "Número de Vítimas", mudar celula de "natureza_delito" para "Natureza do Delito"
# depois organizar os dados de acordo com a Data, extá no formato 2018-01-01
def junta_dados_violencia():
    df = pd.DataFrame()
    for i in range(2018, 2022):
        try:
            temp_df = pd.read_csv(
                f'datasets/violencias/planilhas_separadas/feminicidio_{i}.csv', 
                delimiter=';',  # Especifica o delimitador correto
                encoding='utf-8', 
                engine='python',
                on_bad_lines='skip'  # Ignora linhas problemáticas
            )
            df = pd.concat([df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Erro ao carregar feminicidio_{i}.csv: {e}")

    for i in range(2014, 2022):
        try:
            temp_df = pd.read_csv(
                f'datasets/violencias/planilhas_separadas/violencia_domestica_{i}.csv', 
                delimiter=';', 
                encoding='utf-8', 
                engine='python',
                on_bad_lines='skip'
            )
            df = pd.concat([df, temp_df], ignore_index=True)
        except Exception as e:
            print(f"Erro ao carregar violencia_domestica_{i}.csv: {e}")
    
    # Apaga a primeira coluna, "municipio_cod"
    df = df.drop(columns=['municipio_cod'], errors='ignore')

    # Renomeia as colunas
    df = df.rename(columns={
        'municipio_fato': 'Município', 
        'data_fato': 'Data', 
        'mes': 'Mês', 
        'ano': 'Ano', 
        'risp': 'RISP', 
        'rmbh': 'RMBH', 
        'tentado_consumado': 'Tentado/Consumado', 
        'qtde_vitimas': 'Número de Vítimas', 
        'natureza_delito': 'Natureza do Delito'
    })

    # Organiza os dados pela Data
    # Converte a coluna "Data" para o formato datetime
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d', errors='coerce')

    # Organiza os dados pela coluna "Data"
    df = df.sort_values(by='Data', ascending=True)
    return df


# contar numero de violencia por municipio em cada ano, pegar do campo "Número de Vítimas"
def contar_violencia_por_municipio(df):
    df = df.groupby(['Município', 'Ano', 'RISP', 'RMBH']).agg({'Número de Vítimas': 'sum'}).reset_index()
    return df

# tirar dados irrelevantes do arquivo do pib
# colunas para serem tiradas: "Código da Grande Região", "Nome da Grande Região", "Código da Unidade da Federação", "Nome da Unidade da Federação", "Código do Município", "Região Metropolitana", "Código da Mesorregião", "Nome da Mesorregião", "Código da Microrregião", "Nome da Microrregião", "Código da Região Geográfica Imediata", "Nome da Região Geográfica Imediata", "Município da Região Geográfica Imediata", "Código da Região Geográfica Intermediária", "Nome da Região Geográfica Intermediária", "Município da Região Geográfica Intermediária", "Código Concentração Urbana", "Nome Concentração Urbana", "Tipo Concentração Urbana", "Código Arranjo Populacional", "Nome Arranjo Populacional", "Hierarquia Urbana", "Hierarquia Urbana (principais categorias)", "Código da Região Rural", "Nome da Região Rural", "Região rural (segundo classificação do núcleo)", "Amazônia Legal", "Semiárido", "Cidade-Região de São Paulo"
# deixar apenas linhas onde o campo "Ano" seja 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021
# deixar apenas linhas onde o campo "Sigla da Unidade da Federação" seja "MG"
# apagar coluna "Sigla da Unidade da Federação"
# mudar celula "Nome do Município" para "Município"
def organiza_pib():
    colunas_retirar = [
        "Código da Grande Região", "Nome da Grande Região", "Código da Unidade da Federação", 
        "Nome da Unidade da Federação", "Código do Município", "Região Metropolitana", 
        "Código da Mesorregião", "Nome da Mesorregião", "Código da Microrregião", 
        "Nome da Microrregião", "Código da Região Geográfica Imediata", 
        "Nome da Região Geográfica Imediata", "Município da Região Geográfica Imediata", 
        "Código da Região Geográfica Intermediária", "Nome da Região Geográfica Intermediária", 
        "Município da Região Geográfica Intermediária", "Código Concentração Urbana", 
        "Nome Concentração Urbana", "Tipo Concentração Urbana", "Código Arranjo Populacional", 
        "Nome Arranjo Populacional", "Hierarquia Urbana", "Hierarquia Urbana (principais categorias)", 
        "Código da Região Rural", "Nome da Região Rural", 
        "Região rural (segundo classificação do núcleo)", "Amazônia Legal", "Semiárido", 
        "Cidade-Região de São Paulo", "Valor adicionado bruto da Agropecuária, \na preços correntes\n(R$ 1.000)","Valor adicionado bruto da Indústria,\na preços correntes\n(R$ 1.000)","Valor adicionado bruto dos Serviços,\na preços correntes \n- exceto Administração, defesa, educação e saúde públicas e seguridade social\n(R$ 1.000)","Valor adicionado bruto da Administração, defesa, educação e saúde públicas e seguridade social, \na preços correntes\n(R$ 1.000)","Valor adicionado bruto total, \na preços correntes\n(R$ 1.000)","Impostos, líquidos de subsídios, sobre produtos, \na preços correntes\n(R$ 1.000)","Produto Interno Bruto, \na preços correntes\n(R$ 1.000)", "Atividade com maior valor adicionado bruto", "Atividade com segundo maior valor adicionado bruto", "Atividade com terceiro maior valor adicionado bruto"
    ]
    df = pd.read_csv('datasets/pib/PIB dos Municípios - base de dados 2010-2021.csv', encoding='utf-8', engine='python')
    df = df.drop(columns=colunas_retirar, errors='ignore')
    df = df[df['Ano'].isin([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])]
    df = df[df['Sigla da Unidade da Federação'] == 'MG']
    df = df.drop(columns=['Sigla da Unidade da Federação'], errors='ignore')
    df = df.rename(columns={'Nome do Município': 'Município'})
    df = df.rename(columns={'Produto Interno Bruto per capita, \na preços correntes\n(R$ 1,00)' : 'PIB per capita'})

    # trocar a coluna de ano e municipio de lugar, para ficar igual aos outros datasets
    cols = list(df.columns)
    cols.remove('Ano')
    cols.remove('Município')
    cols = ['Município', 'Ano'] + cols
    df = df[cols]

    return df


# tirar as duas primeira linhas, dividir o campo "Município" para "Municipio" e "UF", depois excuir as duas primeiras colunas, depois exluir a celula "Ano" que está ao lado do campo "UF" após a divisão
# no campo "Município" os dados estão com o UF na frente entre parenteses, ex: "Alta Floresta D'Oeste (RO)". Será necessário dividir o campo em dois, um com o nome do município e outro com a UF
# deixar apenas os "UF" que sejam "MG"
# Apagar coluna "UF"
def organiza_populacao():
    # Lê o arquivo ignorando as duas primeiras linhas
    df = pd.read_csv(
        'datasets/populacao/tabela6579.csv',
        encoding='utf-8',
        engine='python',
        skiprows=2  # Ignora as duas primeiras linhas
    )

    # Renomeia as colunas
    df.columns = ['Município', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
    
    # remover abaixo da linha 1
    df = df.drop([0, 1])

    # Divide a coluna "Município" em "Município" e "UF"
    df[['Município', 'UF']] = df['Município'].str.split(r' \(', expand=True)
    df['UF'] = df['UF'].str.replace(')', '', regex=False)  # Remove o parêntese de fechamento

    # Transforma os dados para long format (um ano por linha)
    df = df.melt(
        id_vars=['Município', 'UF'],
        value_vars=['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021'],
        var_name='Ano',
        value_name='População'
    )

    # Remove linhas onde "Município" ou "UF" estão vazios
    df = df.dropna(subset=['Município', 'UF'])

    # Converte a coluna "Ano" para número inteiro
    df['Ano'] = df['Ano'].astype(int)

    # Converte a coluna "População" para número inteiro
    df['População'] = df['População'].astype(int)

    # Filtra apenas os dados de Minas Gerais
    df = df[df['UF'] == 'MG']
    
    # Remove a coluna "UF"
    df = df.drop(columns=['UF'], errors='ignore')

    return df

# Junta os dados de população, violência e PIB
# Municipio, Ano, População, RISP, RMBH, Número de Vítimas, ...(PIB)
def organiza_dados(df_violencia, df_pib, df_populacao):
    # Passo 1: Certificar-se de que as colunas relevantes estão padronizadas
    df_violencia['Município'] = df_violencia['Município'].str.strip()  # Remove espaços extras
    df_pib['Município'] = df_pib['Município'].str.strip()
    df_populacao['Município'] = df_populacao['Município'].str.strip()

    # colocar todos os campos "Município" em maiusculo, tirar os acentos e tirar caracteres especiais
    df_violencia['Município'] = df_violencia['Município'].str.upper()
    df_pib['Município'] = df_pib['Município'].str.upper()
    df_populacao['Município'] = df_populacao['Município'].str.upper()

    df_violencia['Município'] = df_violencia['Município'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df_pib['Município'] = df_pib['Município'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df_populacao['Município'] = df_populacao['Município'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    df_violencia['Município'] = df_violencia['Município'].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex=True)
    df_pib['Município'] = df_pib['Município'].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex=True)
    df_populacao['Município'] = df_populacao['Município'].str.replace(r'[^a-zA-Z0-9 ]', ' ', regex=True)


    # Passo 2: Unir os DataFrames
    # Merge inicial: População e Violência
    df_merged = pd.merge(
        df_populacao, 
        df_violencia, 
        on=['Município', 'Ano'], 
        how='outer'
    )

    # Merge secundário: Dados do PIB
    df_merged = pd.merge(
        df_merged, 
        df_pib, 
        on=['Município', 'Ano'], 
        how='outer'
    )

    # Passo 3: Ordenar por Município e Ano
    df_merged = df_merged.sort_values(by=['Município', 'Ano']).reset_index(drop=True)

    return df_merged

# se o campo "População" estiver vazio, significa que esá endo divergencia no nome da cidade. É necessário padronizar o nome da cidade, para isso, pegar o nome da cidade que está no campo "Município" e procurar no campo um nome parecido, se encontrar, substituir o nome da cidade no campo "Município" pelo nome encontrado e mesclar os dados
def padronizar_cidades(df, coluna_municipio):
    """
    Padroniza os nomes dos municípios com base em similaridade.
    
    Parâmetros:
    - df: DataFrame com os dados
    - coluna_municipio: Nome da coluna que contém os municípios
    
    Retorna:
    - DataFrame com os municípios padronizados e mesclados
    """
    # Lista de municípios únicos
    municipios_unicos = list(df[coluna_municipio].dropna().unique())
    
    # Mapeamento de nomes para padronizar
    mapeamento = {}
    
    for i, municipio1 in enumerate(municipios_unicos):
        for municipio2 in municipios_unicos[i+1:]:
            # Calcular a similaridade entre os dois nomes
            similaridade = SequenceMatcher(None, municipio1, municipio2).ratio()
            
            threshold = 0.85;       
            # Se a similaridade for alta, consideramos como o mesmo município
            if similaridade > threshold:
                # se nao tiver dados a coluna de populacao ou RISP
                if (df[df[coluna_municipio] == municipio1]['População'].isnull().all() and df[df[coluna_municipio] == municipio2]['RISP'].isnull().all()) or (df[df[coluna_municipio] == municipio1]['RISP'].isnull().all() and df[df[coluna_municipio] == municipio2]['População'].isnull().all()):
                    # Nome padrão será o menor ou primeiro na ordem alfabética
                    nome_padrao = min(municipio1, municipio2, key=len)
                    mapeamento[municipio1] = nome_padrao
                    mapeamento[municipio2] = nome_padrao
    
    # Aplicar o mapeamento para padronizar os nomes, ou seja, substituir os nomes similares pelo nome padrão
    df[coluna_municipio] = df[coluna_municipio].replace(mapeamento)
    
    # Remover espaços extras nos nomes finais
    df[coluna_municipio] = df[coluna_municipio].str.strip()

    # mesclar os dados, se existir uma cidade com o mesmo nome e o mesmo ano, mesclar os dados
    def mesclar_linhas(grupo):
        # Mesclar valores em cada coluna
        resultado = {}
        for col in grupo.columns:
            if col == coluna_municipio or col == 'Ano':
                resultado[col] = grupo[col].iloc[0]  # Mantém o valor original
            elif grupo[col].dtype == 'object':  # Para strings, concatena valores únicos
                resultado[col] = '; '.join(grupo[col].dropna().unique())
            else:  # Para numéricos, mantém o primeiro valor não nulo
                resultado[col] = grupo[col].dropna().iloc[0] if not grupo[col].dropna().empty else None
        return pd.Series(resultado)

    # Agrupar pelos municípios padronizados e ano, aplicando a mesclagem
    df_mesclado = df.groupby([coluna_municipio, 'Ano']).apply(mesclar_linhas).reset_index(drop=True)

    return df_mesclado


def indice_violencia_populacao(df):
    # criar nova coluna "Índice de Violência" ao lado da coluna "Número de Vítimas", que é a divisão do campo "Número de Vítimas" pelo campo "População"
    df['Índice de Violência'] = (df['Número de Vítimas'] / df['População']) * 10000

    cols = list(df.columns)
    cols.remove('Município')
    cols.remove('Ano')
    cols.remove('População')
    cols.remove('RISP')
    cols.remove('RMBH')
    cols.remove('Número de Vítimas')
    cols.remove('Índice de Violência')
    cols = ['Município', 'Ano', 'População', 'Número de Vítimas', 'Índice de Violência', 'RISP', 'RMBH'] + cols
    df = df[cols]
    return df

if __name__ == '__main__':
    print("Iniciando a pré-processamento dos dados...")
    print("\nDADOS DE VIOLÊNCIA DOMÉSTICA E FEMINICÍDIO:")
    print(" - Dados de violência doméstica e feminicídio, pegados do site do governo de Minas Gerais: https://github.com/transparencia-mg/violencia-contra-mulher/tree/main/dataset/data e colocados em datasets/violencias/planilhas_separadas")
    # Junta os dados de violência e salva como CSV
    df = junta_dados_violencia()
    df.to_csv('datasets/violencias/violencia_mg_2014_2021.csv', index=False)
    print("     - Arquivo violencia_mg_2014_2021.csv criado com sucesso!")

    # Conta a violência por município
    df_violencia = contar_violencia_por_municipio(df)
    df_violencia.to_csv('datasets/violencias/violencia_mg_municipio_2014_2021.csv', index=False)
    print("     - Arquivo violencia_mg_municipio_2014_2021.csv criado com sucesso!")


    print("\nDADOS DE PIB: ")
    print(" - Dados de PIB, pegados do site do IBGE: https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?=&t=downloads e colocados em datasets/pib")
    # Organiza os dados do PIB
    converter_xlsx_para_csv('datasets/pib/PIB dos Municípios - base de dados 2010-2021.xlsx', 'datasets/pib/PIB dos Municípios - base de dados 2010-2021.csv')
    df_pib = organiza_pib()
    df_pib.to_csv('datasets/pib/pib_mg_2014_2021.csv', index=False)
    print("     - Arquivo pib_mg_2014_2021.csv criado com sucesso!")


    print("\nDADOS DE POPULAÇÃO: ")
    print(" - Dados de população, pegados do site do IBGE: https://sidra.ibge.gov.br/tabela/6579 e colocados em datasets/populacao")
    print(" - No site, deve ter a configuração dos anos de 2014 a 2021, e na Unidade Territorial apenas os Municipíos, depois na opção de download, escolher a opção de XLSX, apenas Exibir nomes de territóro.")
    # Organiza os dados da população
    converter_xlsx_para_csv('datasets/populacao/tabela6579.xlsx', 'datasets/populacao/tabela6579.csv')
    df_populacao = organiza_populacao()
    df_populacao.to_csv('datasets/populacao/populacao_mg_2014_2021.csv', index=False)
    print("     - Arquivo populacao_mg_2014_2021.csv criado com sucesso!")


    print("\nMESCLANDO OS DADOS: ")
    print(" - Mesclando os dados de violência, PIB e população")
    # Junta os dados finais
    df_final = organiza_dados(df_violencia, df_pib, df_populacao)
    df_final.to_csv('datasets/dados_violencia_populacao_pib.csv', index=False)
    print("     - Arquivo dados_violencia_populacao_pib.csv criado com sucesso!")

    print(" - Padronizando os nomes dos municípios, removendo nomes duplicados e mesclando os dados")
    # Padroniza os nomes dos municípios
    df_final = padronizar_cidades(df_final, 'Município')
    df_final.to_csv('datasets/dados_violencia_populacao_pib.csv', index=False)
    print("     - Arquivo dados_violencia_populacao_pib.csv atualizado com sucesso!")

    print("\nCALCULANDO O ÍNDICE DE VIOLÊNCIA: ")
    print(" - Calculando o índice de violência")
    # Calcula o índice de violência
    df_final = indice_violencia_populacao(df_final)
    df_final.to_csv('datasets/dados_violencia_populacao_pib.csv', index=False)
    os.rename('datasets/dados_violencia_populacao_pib.csv', 'datasets/dados_violencia_populacao_indice_pib_2014_2021.csv')
    print("     - Arquivo dados_violencia_populacao_indice_pib_2014_2021.csv criado com sucesso!")

