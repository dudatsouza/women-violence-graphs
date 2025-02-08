import pandas as pd
import warnings

# Ignorar todos os warnings
warnings.filterwarnings("ignore")


def cutting_data(df, cidade):
    """
    Filtra o DataFrame para a cidade desejada e remove colunas indesejadas.
    """
    # Filtra a cidade específica
    df = df[df["Município"] == cidade]

    # Remove colunas que não serão utilizadas
    colunas_remover = [
        "Município", "Desc Longa Local Imediato", "Descricao Grupo Natureza", "Causa Presumida",
        "Relacao Vitima Autor", "Bairro Envolvido", "Municipio Envolvido", "UF Envolvido Sigla",
        "Descricao Subclasse Nat Principal", "Latitude", "Longitude"
    ]
    df = df.drop(columns=colunas_remover)

    return df


def arrumar_bairros_divinopolis(df):
    """
    Padroniza e corrige os nomes dos bairros no DataFrame.
    """
    if "Bairro" not in df.columns:
        print("Erro: Coluna 'Bairro' não encontrada no DataFrame.")
        return df

    def limpar_bairro(bairro):
        if pd.isna(bairro):
            return bairro
        bairro = str(bairro).strip()

        # Lista de palavras a serem removidas
        substituicoes = [
            "RESIDENCIAL ", "CONJUNTO HABITACIONAL ", "CONJUNTO ", "PROLONGAMENTO ", "BALNEARIO "
        ]
        for palavra in substituicoes:
            bairro = bairro.replace(palavra, "")
        
        # Remove " II" e " I" do final do nome, se existirem
        if bairro.endswith(" II"):
            bairro = bairro[:-3]
        elif bairro.endswith(" I"):
            bairro = bairro[:-2]

        return bairro

    df["Bairro"] = df["Bairro"].apply(limpar_bairro)

    # Correções específicas para padronização dos nomes
    correcoes = {
        "XAVANTES": "XAVANTE",
        "santa lucia": "SANTA LUCIA",
        "FREI GALVÃO": "SAO FREI GALVAO",
        "MANOEL VALINHOS": "MANOEL VALINHAS",
        "CIDADE INDUSTRIAL CORONEL JOVELINO RABELO": "DISTRITO INDUSTRIAL CEL JOVELINO RABELO",
        "LAGO DAS ROSEIRAS": "VILA ROSEIRAS",
        "Frei galvao": "SAO FREI GALVAO",
        "JARDIM DONA QUITA": "DONA QUITA",
        "SÃO FREI GALVÃO": "SAO FREI GALVAO",
        "CHACARAS XAVANTE": "XAVANTE",
        "DONA MARIA ELISA": "SANTA TEREZA",
        "JOAO PAULO": "JOAO PAULO II",
        "DOM PEDRO": "DOM PEDRO II"
    }
    df["Bairro"] = df["Bairro"].replace(correcoes)

    # Remove linhas com valores vazios ou NaN na coluna 'Bairro'
    df = df.dropna(subset=["Bairro"])
    df = df[df["Bairro"].str.strip() != ""]

    return df


def classificar_casos(df):
    """
    Classifica os casos com base em pontuações definidas a partir de três colunas.
    """
    # Pesos para "Descricao Subclasse Natureza"
    peso_natureza = {
        "AMEACA": 1, "FURTO": 1, "VIAS DE FATO   AGRESSAO": 3, "ESTELIONATO": 1,
        "LESAO CORPORAL": 4, "ESTUPRO DE VULNERAVEL": 5, "VIOLENCIA PSICOLOGICA": 1,
        "DIFAMACAO": 1, "ROUBO": 3, "APROPRIACAO INDEBITA DE COISA ALHEIA MOVEL": 1,
        "CALUNIA": 1, "DANO": 2, "IMPORTUNACAO SEXUAL": 3, "ESTUPRO": 5, "INJURIA": 1,
        "ATO OBSCENO": 1, "APROPRIACAO DE COISA HAVIDA POR ERRO  COISA ACHADA": 1,
        "INJURIA RACIAL": 2, "INVASAO DE DISPOSITIVO INFORMATICO": 1, "ASSEDIO SEXUAL": 3,
        "PERSEGUICAO": 2, "VIOLACAO DE DOMICILIO": 3, "OUTRAS INFRACOES CONTRA O PATRIMONIO": 2,
        "OUTRAS INFRACOES CONTRA DIGNIDADE SEXUAL E A FAMIL": 4,
        "RACISMO   PRATICA INDUZ INCITA PRECONCEITO COR DIV": 2, "MAUS TRATOS": 4,
        "OUTROS INFRACOES C  A PESSOA": 2, "APROPRIA DESV BEM PROVENTO PENSAO REND IDOSO": 2,
        "ABANDONO DE INCAPAZ": 3, "RACISMO   IMPEDE CASAMENTO CONVIVENCIA FAMILIAR SO": 2,
        "EXTORSAO": 3, "RECEPTACAO": 2, "DIVULGACAO CENA ESTUPRO E IMAGEM NUDEZ  SEXO OU PO": 2,
        "PERIGO PARA A VIDA OU SAUDE DE OUTREM": 4, "SEQUESTRO E CARCERE PRIVADO": 5,
        "ESBULHO POSSESSORIO": 2, "CONSTRANGIMENTO ILEGAL": 2,
        "ZOMBA PERTUBA CERIMONIA SIMILAR INDIGENA": 1, "NEGAR SALDAR DESPESA": 1,
        "TORTURA": 5, "REGISTRO NAO AUTORIZADO DA INTIMIDADE SEXUAL": 4,
        "OUTRA INFRACAO REFERENTE A SUB  ENTORPECENTE": 4,
        "OUTRAS INFRACOES DEMAIS LEIS ESPECIAIS": 2, "CONSTRANGE VEXAME MENOR DE IDADE SOB GUARDA": 3,
        "FAVORECIMENTO DA PROSTITUICAO": 4, "OMISSAO DE SOCORRO": 5,
        "FOTOG  PUBLICA CENA DE SEXO PORNO C MENOR ID": 3
    }

    # Pesos para "Descricao Meio Utilizado"
    peso_meio = {
        "FALA": 1, "ESCALADA": 1, "AGRESSAO FISICA SEM EMPREGO DE INSTRUMENTOS": 3,
        "MEIO ELETRONICO  INTERNET OU SMS": 1, "OUTROS MEIOS  DESCREVER EM CAMPO ESPECIFICO": 2,
        "ARROMBAMENTO ROMPIMENTO DE OBSTACULO": 3, "FRAUDE": 1, "ABUSO DE CONFIANCA": 1,
        "RADIODIFUSAO  TELEVISAO  RADIO  SIMILARES": 1, "EMPREGO DE CHAVE FALSA   MICHA   GAZUA": 3,
        "MEIO DESCONHECIDO": 2, "INST CONTUNDENTE CORTANTE PERFURANTE  ARMA BR": 5,
        "ARMAS DE FOGO": 5, "SEM EMPREGO DE INSTRUMENTOS": 1, "MEDIANTE FRAUDE": 1,
        "AGRESSAO FISICA COM EMPREGO DE INSTRUMENTOS": 4,
        "ATO DE SUFOCAR  ENFORCAR  ESTRANGULAR OU ESGA": 5,
        "CONHECIMENTO TECNICO ESPECIFICO": 1, "ESCRITA FISICA": 1, "VIOLENCIA OU VIAS DE FATO": 4,
        "VIOLENCIA OU GRAVE AMEACA": 5, "VEICULO": 4, "SEM USO DE VIOLENCIA OU GRAVE AMEACA": 1,
        "SUBST QUIMICA BIOLOGICA ENTORPECENTE ENVENENA": 5,
        "OFERECIMENTO DE VANTAGEM A VITIMA": 1, "AMEACA": 2, "IMOBILIZACAO DA VITIMA": 4,
        "AQUISICAO  ONEROSA OU GRATUITA  PRODUTO DE CR": 2,
        "ARROMBAMENTO ROMPIMENTO DE OBSTACULO C EXPLOS": 4, "USO DE SINAIS  GESTOS OU IMAGENS": 1,
        "TRAFICAR DROGAS": 4, "COACAO": 3, "SIMULACRO DE ARMA DE FOGO": 3,
        "RECEBIMENTO  A QUALQUER TITULO  DE PROD  DE C": 2, "QUEDA": 3
    }

    # Pesos para "Tentado Consumado"
    peso_tentado_consumado = {
        "TENTADO": 0,
        "CONSUMADO": 2
    }

    def calcular_pontuacao(row):
        descricao_natureza = str(row["Descricao Subclasse Natureza"]).upper().strip()
        descricao_meio = str(row["Descricao Meio Utilizado"]).upper().strip()
        tentado_consumado = str(row["Tentado Consumado"]).upper().strip()

        pontos_natureza = peso_natureza.get(descricao_natureza, 0)
        pontos_meio = peso_meio.get(descricao_meio, 0)
        pontos_tentado_consumado = peso_tentado_consumado.get(tentado_consumado, 0)

        pontuacao_total = pontos_natureza + pontos_meio + pontos_tentado_consumado

        if pontuacao_total >= 11:
            return "ALTO RISCO DE FATALIDADE"
        elif pontuacao_total >= 5:
            return "POSSIVEL FATAL"
        else:
            return "NAO FATAL"

    df["Classificacao"] = df.apply(calcular_pontuacao, axis=1)
    return df


def possible_bairros(df_bairros, df, df_edges):
    """
    Indexa os bairros a partir dos dados de bairros e atualiza os DataFrames dos casos e das arestas.
    """
    # Obter os bairros únicos das colunas 'bairro' e 'bairro_divisa'
    bairros_1 = set(df_bairros["bairro"].unique())
    bairros_2 = set(df_bairros["bairro_divisa"].unique())
    possiveis_bairros = list(bairros_1.union(bairros_2))

    # Cria um DataFrame com os bairros e atribui IDs
    df_bairros_possiveis = pd.DataFrame({"ID": range(len(possiveis_bairros)), "Bairro": possiveis_bairros})
    df_bairros_possiveis = df_bairros_possiveis.sort_values(by="Bairro").reset_index(drop=True)
    df_bairros_possiveis["ID"] = df_bairros_possiveis.index.astype(int)

    # Mapeia cada bairro ao seu ID
    bairro_to_id = df_bairros_possiveis.set_index("Bairro")["ID"].to_dict()

    # Atualiza o DataFrame de casos: substitui o nome do bairro pelo seu ID
    for bairro in df["Bairro"].unique():
        if bairro not in bairro_to_id:
            print(f"Bairro não encontrado: {bairro}")
    df["Bairro"] = df["Bairro"].map(bairro_to_id).fillna(-1).astype(int)

    # Atualiza o DataFrame de arestas com os IDs dos bairros
    df_edges["bairro"] = df_bairros["bairro"].map(bairro_to_id).fillna(-1).astype(int)
    df_edges["bairro_divisa"] = df_bairros["bairro_divisa"].map(bairro_to_id).fillna(-1).astype(int)

    return df_bairros_possiveis, df, df_edges

def calcular_casos_total(df_nodes, df_aux):
    """
    Calcula o número total de casos para um bairro.
    """
    for i in range(len(df_aux)):
        n_casos_total = 0
        for j in range(len(df_nodes)):
            if df_nodes.at[j, "Tipo"] == 1:
                id_caso = df_nodes.at[j, "ID"]
                bairro = df_nodes.at[j, "Bairro"]
                if bairro == df_aux.at[i, "ID"]:
                    n_casos_total += 1
        df_aux.at[i, "N de casos Total"] = n_casos_total

    df_aux["N de casos Total"] = df_aux["N de casos Total"].fillna(0).astype(int)
        
    return df_aux
        
def calcular_casos_fatais(df_nodes, df_aux):
    """
    Calcula o número de casos fatais para um bairro.
    """
    n_casos_fatais = 0
    for i in range(len(df_aux)):
        n_casos_total = 0
        for j in range(len(df_nodes)):
            if df_nodes.at[j, "Tipo"] == 1:
                id_caso = df_nodes.at[j, "ID"]
                bairro = df_nodes.at[j, "Bairro"]
                if bairro == df_aux.at[i, "ID"] and df_nodes.at[j, "Classificacao"] == "ALTO RISCO DE FATALIDADE":
                    n_casos_total += 1
        df_aux.at[i, "N de casos Fatais"] = n_casos_total

    df_aux["N de casos Fatais"] = df_aux["N de casos Fatais"].fillna(0).astype(int)

    return df_aux
        

def calcular_bairros_divisa(df_bairros, df_aux):
    """
    Calcula o número de bairros divisa para um bairro.
    """
    for i in range(len(df_aux)):
        n_bairros_divisa = 0
        for j in range(len(df_bairros)):
            bairro = df_bairros.at[j, "bairro"]
            bairro_divisa = df_bairros.at[j, "bairro_divisa"]
            if bairro == df_aux.at[i, "Bairro"]:
                n_bairros_divisa += 1
            if bairro_divisa == df_aux.at[i, "Bairro"]:
                n_bairros_divisa += 1
            if bairro == df_aux.at[i, "Bairro"] and bairro_divisa == df_aux.at[i, "Bairro"]:
                n_bairros_divisa = 0                
        df_aux.at[i, "N de bairros Divisa"] = n_bairros_divisa

    df_aux["N de bairros Divisa"] = df_aux["N de bairros Divisa"].fillna(0).astype(int)

    return df_aux

def add_possible_bairros(df_nodes, df_aux, df_bairros):
    """
    Cria um DataFrame com os bairros possíveis e os integra com os casos existentes.
    """

    df_nodes["Tipo"] = 1
    df_aux["Classificacao"] = "Bairro"
    df_aux["Tipo"] = 2
    # Cria DataFrame para os bairros com a mesma estrutura dos nós de casos
    df_aux = calcular_casos_total(df_nodes, df_aux)
    df_aux = calcular_casos_fatais(df_nodes, df_aux)
    df_aux = calcular_bairros_divisa(df_bairros, df_aux)
    # Substituir valores NaN por -1 e converter para inteiro
    df_aux["ID"] = df_aux["ID"].fillna(-1).astype(int)
    # Filtrar apenas os bairros encontrados
    df_aux = df_aux[df_aux["ID"] != -1].reset_index(drop=True)

    # Mensagem de aviso (opcional)
    if any(df_aux["ID"] == -1):
        print("Bairros não encontrados e removidos.")

    # Salva os nós referentes aos bairros
    df_aux.to_csv("./datasets/nodes_bairros.csv", index=False)

    # Define o tipo para os nós de casos e salva separadamente

    df_nodes["N de casos Total"] = None
    df_nodes["N de casos Fatais"] = None
    df_nodes["N de bairros Divisa"] = None
    df_nodes.to_csv("./datasets/nodes_casos.csv", index=False)

    df_aux2 = pd.DataFrame(columns=df_nodes.columns)
    df_aux2["ID"] = df_aux["ID"]
    df_aux2["Bairro"] = df_aux["Bairro"]
    df_aux2["Classificacao"] = df_aux["Classificacao"]
    df_aux2["Tipo"] = df_aux["Tipo"]
    df_aux2["N de casos Total"] = df_aux["N de casos Total"]
    df_aux2["N de casos Fatais"] = df_aux["N de casos Fatais"]
    df_aux2["N de bairros Divisa"] = df_aux["N de bairros Divisa"]

    # Concatena os DataFrames para formar o conjunto final de nós
    df_nodes = pd.concat([df_aux2, df_nodes], ignore_index=True)

    return df_nodes

def nodes(df):
    """
    Processa o DataFrame removendo colunas desnecessárias e criando um identificador único.
    """
    colunas_remover = [
        "Data Fato", "Descricao Subclasse Natureza",
        "Tentado Consumado", "Descricao Meio Utilizado"
    ]
    df = df.drop(columns=colunas_remover)
    df.reset_index(drop=True, inplace=True)
    df["ID"] = df.index
    return df


def edges(df_edges, df_nodes):
    """
    Cria e atualiza os DataFrames de arestas para representar as conexões entre bairros e casos.
    """
    # Define o peso para as arestas entre bairros
    df_edges["Weight"] = 2
    df_edges = df_edges.rename(columns={"bairro": "Source", "bairro_divisa": "Target"})
    df_edges.to_csv("./datasets/edges_bairros.csv", index=False)

    # Cria arestas entre casos e bairros
    df_aux = pd.DataFrame(columns=["Source", "Target", "Weight"])
    for i in range(len(df_nodes)):
        if df_nodes.at[i, "Tipo"] == 1:  # Casos são Tipo 1
            id_caso = df_nodes.at[i, "ID"]
            bairro = df_nodes.at[i, "Bairro"]
            
            linha = {"Source": bairro, "Target": id_caso, "Weight": 1}
            df_aux = pd.concat([df_aux, pd.DataFrame([linha])], ignore_index=True)
            df_edges = pd.concat([df_edges, pd.DataFrame([linha])], ignore_index=True)

    df_aux.to_csv("./datasets/edges_casos.csv", index=False)
    return df_edges


def main():
    # Carregar os dados
    df = pd.read_csv("./datasets/dados_pre.csv", delimiter=',', encoding='utf-8', engine='python')

    # Filtrar e cortar os dados para a cidade DIVINOPOLIS
    df = cutting_data(df, "DIVINOPOLIS")
    print("Dados cortados com sucesso!")

    # Arrumar e padronizar os nomes dos bairros
    df = arrumar_bairros_divinopolis(df)
    print("Bairros arrumados com sucesso!")

    # Reiniciar os índices e criar coluna de ID
    df.reset_index(drop=True, inplace=True)
    df["ID"] = df.index

    # Salvar dados processados
    df.to_csv("./datasets/dados_divinopolis.csv", index=False)
    print("Arquivo dados_divinopolis.csv criado com sucesso!")

    # Carregar arquivo com os bairros
    df_bairros = pd.read_csv("./datasets/localidade/bairros_divinopolis.csv", delimiter=';', encoding='utf-8', engine='python')
    print("Arquivo bairros_divinopolis.csv lido com sucesso!")

    # Inicializa DataFrame de arestas (vazio)
    df_edges = pd.DataFrame(columns=["bairro", "bairro_divisa"])

    # Indexar e mapear os possíveis bairros
    df_aux, df_nodes, df_edges = possible_bairros(df_bairros, df, df_edges)
    print("Possíveis bairros indexados com sucesso!")

    # Classificar os casos de acordo com a pontuação
    df_nodes = classificar_casos(df_nodes)
    print("Casos definidos com sucesso!")

    # Salvar os possíveis bairros indexados
    df_aux.to_csv("./datasets/bairros_possiveis.csv", index=False)

    # Adicionar os possíveis bairros aos nós e salvar separadamente
    df_nodes = add_possible_bairros(df_nodes, df_aux, df_bairros)
    print("Possíveis bairros adicionados com sucesso!")

    # Processar e salvar os nós finais
    df_nodes = nodes(df_nodes)
    df_nodes.to_csv("./datasets/nodes.csv", index=False)
    print("Arquivo nodes.csv criado com sucesso!")

    # Processar e salvar as arestas finais
    df_edges = edges(df_edges, df_nodes)
    df_edges.to_csv("./datasets/edges.csv", index=False)
    print("Arquivo edges.csv criado com sucesso!")


if __name__ == '__main__':
    main()