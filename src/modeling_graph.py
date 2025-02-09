import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import community.community_louvain as community_louvain
from networkx.algorithms.community import girvan_newman
from fa2_modified import ForceAtlas2 
import matplotlib
from scipy.stats import pearsonr
import sys
import os
import igraph as ig
from leidenalg import find_partition, ModularityVertexPartition
from networkx.algorithms.community import asyn_lpa_communities  
import seaborn as sns
import warnings
import statsmodels.api as sm

warnings.simplefilter(action='ignore', category=FutureWarning)

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def grafico_bairro_casos(df_bairros, n):
    # Ordenar por número de casos
    df_bairros = df_bairros.sort_values(by="N de casos Total", ascending=False)

    # Criar o gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.bar(df_bairros["Bairro"][:n], df_bairros["N de casos Total"][:n], color="skyblue")
    plt.xticks(rotation=90, fontsize=9)  # Ajuste o tamanho do label do eixo X
    plt.xlabel("Bairros", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Número de Casos", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Distribuição de Casos por Bairro (Top " + str(n) + ")", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/gerais/grafico_bairro_casos_" + str(n) + ".png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_idade_casos(df_nodes):
    # plotar aas idades de cada caso de acordo com o seu respectivo bairro
    plt.figure(figsize=(10,7))
    plt.scatter(df_nodes["ID"], df_nodes["Idade Aparente"], color="skyblue", alpha=0.7)
    plt.ylim(0, None)  # Define o limite inferior como 0 e mantém o superior automático

    plt.xlabel("ID", fontsize=14)
    plt.ylabel("Idade Aparente", fontsize=14)

    plt.title("Idade Aparente por Caso", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)

    file_path = "datasets/output/graphs/gerais/grafico_idade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_distribuicao_idade(df_divinopolis):
    
    # Converter a coluna de idade para numérica (caso haja valores não numéricos)
    df_divinopolis["Idade Aparente"] = pd.to_numeric(df_divinopolis["Idade Aparente"], errors="coerce")
    
    # Remover valores nulos
    df_divinopolis = df_divinopolis.dropna(subset=["Idade Aparente"])

    # Criar o histograma
    plt.figure(figsize=(10, 5))
    sns.histplot(df_divinopolis["Idade Aparente"], bins=20, kde=True, color="blue", edgecolor="black", alpha=0.5)

    # Adicionar título e rótulos
    plt.title("Distribuição da Idade das Vítimas em Divinópolis")
    plt.xlabel("Idade")
    plt.ylabel("Número de Casos")

    # Salvar o gráfico
    file_path = "datasets/output/graphs/gerais/grafico_distribuicao_idade.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_cor_casos(df_nodes):
    df_nodes = df_nodes[df_nodes["Tipo"] == 1]
    # plotar aas cores de cada caso de acordo com o seu respectivo bairro
    plt.figure(figsize=(10,7))
    plt.bar(df_nodes["Raca Cor"], df_nodes["Bairro"], color="skyblue", alpha=0.7)

    plt.xlabel("Raca Cor", fontsize=14)
    plt.ylabel("Bairro", fontsize=14)

    plt.title("Raca Cor por Caso", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)

    file_path = "datasets/output/graphs/gerais/grafico_cor_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_distribuicao_cor(df_divinopolis):
    # Contar a frequência de cada categoria de raça/cor
    raca_cor_counts = df_divinopolis["Raca Cor"].value_counts()

    # Criar o gráfico de barras
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=raca_cor_counts.index,
        y=raca_cor_counts.values,
        palette="Blues_r"  # Cores azuis semelhantes ao gráfico original
    )

    # Adicionar título e rótulos
    plt.title("Distribuição por Raça/Cor das Vítimas em Divinópolis")
    plt.xlabel("Raça/Cor")
    plt.ylabel("Número de Casos")

    # Ajustar a rotação dos rótulos no eixo X para melhor visualização
    plt.xticks(rotation=30, ha="right")

    # Salvar o gráfico
    file_path = "datasets/output/graphs/gerais/grafico_distribuicao_cor.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_escolaridade_casos(df_nodes):
    df_nodes = df_nodes[df_nodes["Tipo"] == 1]
    # plotar aas escolaridades de cada caso de acordo com o seu respectivo bairro
    plt.figure(figsize=(10,7))
    plt.bar(df_nodes["Bairro"], df_nodes["Escolaridade"], color="skyblue", alpha=0.7)

    plt.xlabel("Bairro", fontsize=14)
    plt.ylabel("Escolaridade", fontsize=14)

    plt.title("Escolaridade por Caso", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)

    file_path = "datasets/output/graphs/gerais/grafico_escolaridade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_distribuicao_escolaridade(df_divinopolis):
    # Contar a frequência de cada categoria de escolaridade
    escolaridade_counts = df_divinopolis["Escolaridade"].value_counts()

    # Criar o gráfico de barras
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=escolaridade_counts.index,
        y=escolaridade_counts.values,
        palette="Purples_r"  # Cores roxas semelhantes ao gráfico original
    )

    # Adicionar título e rótulos
    plt.title("Distribuição por Escolaridade das Vítimas em Divinópolis")
    plt.xlabel("Escolaridade")
    plt.ylabel("Número de Casos")

    # Ajustar a rotação dos rótulos no eixo X para melhor visualização
    plt.xticks(rotation=45, ha="right")

    # salvar o gráfico
    file_path = "datasets/output/graphs/gerais/grafico_distribuicao_escolaridade.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_classificacao_casos(df_nodes):
    df_nodes = df_nodes[df_nodes["Tipo"] == 1]
    # plotar aas classificacoes de cada caso de acordo com o seu respectivo bairro
    plt.figure(figsize=(10,7))
    plt.bar(df_nodes["Bairro"], df_nodes["Classificacao"], color="skyblue", alpha=0.7)

    plt.xlabel("Bairro", fontsize=14)
    plt.ylabel("Classificacao", fontsize=14)

    plt.title("Classificacao por Caso", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)

    file_path = "datasets/output/graphs/gerais/grafico_classificacao_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_media_idade_casos(df_idade, df_bairros, color_map):
    df_idade = df_idade.reset_index(drop=True)
    df_bairros = df_bairros.reset_index(drop=True)

    # Criar o mapeamento de cores usando a comunidade detectada no grafo
    comunidades_unicas = df_bairros["Comunidade"].unique()
    mapa_cores = {comunidade: color_map.get(comunidade, "gray") for comunidade in comunidades_unicas}

    # 📌 Criar gráfico da média de idade e número de casos (SEM REGRESSÃO)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_bairros["Comunidade"] == comunidade
        plt.scatter(
            df_bairros.loc[mask, "N de casos Total"],
            df_idade.loc[mask, "Media Idade"],
            color=mapa_cores[comunidade],  
            alpha=0.7,
            label=comunidade
        )

    plt.ylim(0, None)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Média de Idade", fontsize=14)
    plt.title("Relação entre Média de Idade e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/media/grafico_media_idade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

    # 📌 Criar gráfico do desvio padrão e número de casos (COM LOWESS)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_bairros["Comunidade"] == comunidade
        plt.scatter(
            df_bairros.loc[mask, "N de casos Total"],
            df_idade.loc[mask, "Desvio Padrao Idade"],
            color=mapa_cores[comunidade],  
            alpha=0.7,
            label=comunidade
        )

    # 🔹 Conversão para números antes da regressão
    x = pd.to_numeric(df_bairros["N de casos Total"], errors="coerce")
    y = pd.to_numeric(df_idade["Desvio Padrao Idade"], errors="coerce")

    # Remover valores NaN para evitar erros
    mask = ~x.isna() & ~y.isna()
    x = x[mask]
    y = y[mask]

    # 🔹 Ajuste com LOWESS (regressão suavizada)
    lowess_results = sm.nonparametric.lowess(y, x, frac=0.3)  # "frac" controla a suavização
    x_smooth, y_smooth = zip(*lowess_results)

    # 🔹 Adicionar curva LOWESS
    plt.plot(x_smooth, y_smooth, color="black", linestyle="--", linewidth=2, label="LOWESS")

    plt.ylim(0, None)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Desvio Padrão de Idade", fontsize=14)
    plt.title("Relação entre Desvio Padrão de Idade e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/desvio-padrao/grafico_desvio_padrao_idade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_media_cor_casos(df_cor, df_nodes, color_map):
    df_cor = df_cor.reset_index(drop=True)
    df_nodes = df_nodes.reset_index(drop=True)

    comunidades_unicas = df_nodes["Comunidade"].unique()
    mapa_cores = {comunidade: color_map.get(comunidade, "gray") for comunidade in comunidades_unicas}

    # 📌 Criar gráfico da média de cor e número de casos (SEM REGRESSÃO)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_nodes["Comunidade"] == comunidade
        plt.scatter(
            df_nodes.loc[mask, "N de casos Total"],
            df_cor.loc[mask, "Cor Predominante"],
            color=mapa_cores[comunidade],
            alpha=0.7,
            label=comunidade
        )

    plt.ylim(0, 1)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Cor Predominante", fontsize=14)
    plt.title("Relação entre Cor Predominante e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/media/grafico_media_cor_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

    # 📌 Criar gráfico do desvio padrão e número de casos (COM LOWESS)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_nodes["Comunidade"] == comunidade
        plt.scatter(
            df_nodes.loc[mask, "N de casos Total"],
            df_cor.loc[mask, "Desvio Padrao Cor"],
            color=mapa_cores[comunidade],
            alpha=0.7,
            label=comunidade
        )

    # 🔹 Conversão para números antes da regressão
    x = pd.to_numeric(df_nodes["N de casos Total"], errors="coerce")
    y = pd.to_numeric(df_cor["Desvio Padrao Cor"], errors="coerce")

    # Remover valores NaN para evitar erros
    mask = ~x.isna() & ~y.isna()
    x = x[mask]
    y = y[mask]

    # 🔹 Ajuste com LOWESS (regressão suavizada)
    lowess_results = sm.nonparametric.lowess(y, x, frac=0.3)  # "frac" controla a suavização
    x_smooth, y_smooth = zip(*lowess_results)

    # 🔹 Adicionar curva LOWESS
    plt.plot(x_smooth, y_smooth, color="black", linestyle="--", linewidth=2, label="LOWESS")

    plt.ylim(0, 1)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Desvio Padrão de Cor", fontsize=14)
    plt.title("Relação entre Desvio Padrão de Cor e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/desvio-padrao/grafico_desvio_padrao_cor_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_media_escolaridade_casos(df_escolaridade, df_nodes, color_map):
    df_escolaridade = df_escolaridade.reset_index(drop=True)
    df_nodes = df_nodes.reset_index(drop=True)

    comunidades_unicas = df_nodes["Comunidade"].unique()
    mapa_cores = {comunidade: color_map.get(comunidade, "gray") for comunidade in comunidades_unicas}

    # 📌 Criar gráfico da média de escolaridade e número de casos (SEM REGRESSÃO)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_nodes["Comunidade"] == comunidade
        plt.scatter(
            df_nodes.loc[mask, "N de casos Total"],
            df_escolaridade.loc[mask, "Escolaridade Predominante"],
            color=mapa_cores[comunidade],
            alpha=0.7,
            label=comunidade
        )

    plt.ylim(0, 1)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Escolaridade Predominante", fontsize=14)
    plt.title("Relação entre Escolaridade Predominante e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/media/grafico_media_escolaridade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

    # 📌 Criar gráfico do desvio padrão de escolaridade e número de casos (COM LOWESS)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_nodes["Comunidade"] == comunidade
        plt.scatter(
            df_nodes.loc[mask, "N de casos Total"],
            df_escolaridade.loc[mask, "Desvio Padrao Escolaridade"],
            color=mapa_cores[comunidade],
            alpha=0.7,
            label=comunidade
        )

    # 🔹 Conversão para números antes da regressão
    x = pd.to_numeric(df_nodes["N de casos Total"], errors="coerce")
    y = pd.to_numeric(df_escolaridade["Desvio Padrao Escolaridade"], errors="coerce")

    # Remover valores NaN para evitar erros
    mask = ~x.isna() & ~y.isna()
    x = x[mask]
    y = y[mask]

    # 🔹 Ajuste com LOWESS (regressão suavizada)
    lowess_results = sm.nonparametric.lowess(y, x, frac=0.3)  # "frac" controla a suavização
    x_smooth, y_smooth = zip(*lowess_results)

    # 🔹 Adicionar curva LOWESS
    plt.plot(x_smooth, y_smooth, color="black", linestyle="--", linewidth=2, label="LOWESS")

    plt.ylim(0, 1)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Desvio Padrão de Escolaridade", fontsize=14)
    plt.title("Relação entre Desvio Padrão de Escolaridade e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/desvio-padrao/grafico_desvio_padrao_escolaridade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_media_classificacao_casos(df_classificacao, df_nodes, color_map):
    df_classificacao = df_classificacao.reset_index(drop=True)
    df_nodes = df_nodes.reset_index(drop=True)

    comunidades_unicas = df_nodes["Comunidade"].unique()
    mapa_cores = {comunidade: color_map.get(comunidade, "gray") for comunidade in comunidades_unicas}

    # 📌 Criar gráfico da média de classificação e número de casos (SEM REGRESSÃO)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_nodes["Comunidade"] == comunidade
        plt.scatter(
            df_nodes.loc[mask, "N de casos Total"],
            df_classificacao.loc[mask, "Classificacao Predominante"],
            color=mapa_cores[comunidade],
            alpha=0.7,
            label=comunidade
        )

    plt.ylim(0, 1)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Classificação Predominante", fontsize=14)
    plt.title("Relação entre Classificação Predominante e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/media/grafico_media_classificacao_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

    # 📌 Criar gráfico do desvio padrão de classificação e número de casos (COM LOWESS)
    plt.figure(figsize=(10,7))

    for comunidade in comunidades_unicas:
        mask = df_nodes["Comunidade"] == comunidade
        plt.scatter(
            df_nodes.loc[mask, "N de casos Total"],
            df_classificacao.loc[mask, "Desvio Padrao Classificacao"],
            color=mapa_cores[comunidade],
            alpha=0.7,
            label=comunidade
        )

    # 🔹 Conversão para números antes da regressão
    x = pd.to_numeric(df_nodes["N de casos Total"], errors="coerce")
    y = pd.to_numeric(df_classificacao["Desvio Padrao Classificacao"], errors="coerce")

    # Remover valores NaN para evitar erros
    mask = ~x.isna() & ~y.isna()
    x = x[mask]
    y = y[mask]

    # 🔹 Ajuste com LOWESS (regressão suavizada)
    lowess_results = sm.nonparametric.lowess(y, x, frac=0.3)  # "frac" controla a suavização
    x_smooth, y_smooth = zip(*lowess_results)

    # 🔹 Adicionar curva LOWESS
    plt.plot(x_smooth, y_smooth, color="black", linestyle="--", linewidth=2, label="LOWESS")

    plt.ylim(0, 1)
    plt.xlabel("N de casos Total", fontsize=14)
    plt.ylabel("Desvio Padrão de Classificação", fontsize=14)
    plt.title("Relação entre Desvio Padrão de Classificação e Número de Casos", fontsize=16)
    plt.grid(linestyle="--", alpha=0.7)
    plt.legend(title="Comunidade")

    file_path = "datasets/output/graphs/desvio-padrao/grafico_desvio_padrao_classificacao_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Gráfico salvo em", file_path)

def betweenness_centrality(df_nodes, df_edges):
    # 📌 2. Criar o Grafo
    G = nx.Graph()

    # Adicionar nós (bairros e casos)
    for _, row in df_nodes.iterrows():
        G.add_node(row["ID"], tipo=row["Tipo"])  # Tipo 2 = Bairro, Tipo 1 = Caso

    # Adicionar arestas com pesos
    for _, row in df_edges.iterrows():
        G.add_edge(row["Source"], row["Target"], weight=row["Weight"])

    # 📌 3. Calcular a Centralidade Betweenness para os bairros
    betweenness = nx.betweenness_centrality(G, weight="weight")

    # Criar um DataFrame com os resultados apenas para bairros (Tipo 2)
    bairros_betweenness = pd.DataFrame([
        {"ID": node, "Bairro": df_nodes.loc[df_nodes["ID"] == node, "Bairro"].values[0], 
        "Betweenness": betweenness[node]}
        for node in G.nodes if G.nodes[node]["tipo"] == 2
    ])

    # 📌 4. Salvar ou visualizar os resultados
    file_path = "datasets/output/dados/betweenness/bairros_betweenness.csv"
    bairros_betweenness.to_csv(file_path, index=False)
    print("Centralidade Betweenness salva em", file_path)

def grafico_betweenness(df_bairros, n):
    # Ordenar por número de casos
    df_bairros = df_bairros.sort_values(by="Betweenness", ascending=False)

    # Criar o gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.bar(df_bairros["Bairro"][:n], df_bairros["Betweenness"][:n], color="skyblue")
    plt.xticks(rotation=90, fontsize=9)  # Ajuste o tamanho do label do eixo X
    plt.xlabel("Bairros", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Betweenness", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Centralidade Betweenness por Bairro (Top " + str(n) + ")", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/betweenness/grafico_betweenness_" + str(n) + ".png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_betweenness_casos(df_betweenness, df_bairros):
    # 📌 2. Unir os DataFrames de Betweenness e Número de Casos
    df_betweenness = df_betweenness.merge(df_bairros, how="left", left_on="ID", right_on="ID")

    # 📌 3. Criar o gráfico de dispersão
    plt.figure(figsize=(8, 8))
    plt.scatter(df_betweenness["Betweenness"], df_betweenness["N de casos Total"], color="skyblue", alpha=0.7)
    plt.xlabel("Betweenness", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Número de Casos", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Betweenness vs. Número de Casos por Bairro", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/betweenness/grafico_betweenness_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def closeness_centrality(df_nodes, df_edges):
    # 📌 2. Criar o Grafo
    G = nx.Graph()

    # Adicionar nós (bairros e casos)
    for _, row in df_nodes.iterrows():
        G.add_node(row["ID"], tipo=row["Tipo"])  # Tipo 2 = Bairro, Tipo 1 = Caso

    # Adicionar arestas com pesos
    for _, row in df_edges.iterrows():
        G.add_edge(row["Source"], row["Target"], weight=row["Weight"])

    # 📌 3. Calcular a Centralidade Closeness para os bairros
    closeness = nx.closeness_centrality(G, distance="weight")

    # Criar um DataFrame com os resultados apenas para bairros (Tipo 2)
    bairros_closeness = pd.DataFrame([
        {"ID": node, "Bairro": df_nodes.loc[df_nodes["ID"] == node, "Bairro"].values[0], 
        "Closeness": closeness[node]}
        for node in G.nodes if G.nodes[node]["tipo"] == 2
    ])

    # 📌 4. Salvar ou visualizar os resultados
    file_path = "datasets/output/dados/closeness/bairros_closeness.csv"
    bairros_closeness.to_csv(file_path, index=False)
    print("Centralidade Closeness salva em", file_path)

def grafico_closeness(df_bairros, n):
    # Ordenar por número de casos
    df_bairros = df_bairros.sort_values(by="Closeness", ascending=False)

    # Criar o gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.bar(df_bairros["Bairro"][:n], df_bairros["Closeness"][:n], color="skyblue")
    plt.xticks(rotation=90, fontsize=9)  # Ajuste o tamanho do label do eixo X
    plt.xlabel("Bairros", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Closeness", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Centralidade Closeness por Bairro (Top " + str(n) + ")", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/closeness/grafico_closeness_" + str(n) + ".png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_closeness_casos(df_closeness, df_bairros):
    # 📌 2. Unir os DataFrames de Closeness e Número de Casos
    df_closeness = df_closeness.merge(df_bairros, how="left", left_on="ID", right_on="ID")

    # 📌 3. Criar o gráfico de dispersão
    plt.figure(figsize=(8, 8))
    plt.scatter(df_closeness["Closeness"], df_closeness["N de casos Total"], color="skyblue", alpha=0.7)
    plt.xlabel("Closeness", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Número de Casos", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Closeness vs. Número de Casos por Bairro", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/closeness/grafico_closeness_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def calcular_morans_i(df_nodes, df_edges):
    # 📌 2. Criar o Grafo de bairros
    G = nx.Graph()

    # Adicionar nós (apenas bairros)
    for _, row in df_nodes.iterrows():
        if row["Tipo"] == 2:  # Tipo 2 = Bairro
            G.add_node(row["ID"], casos=row["N de casos Total"])

    # Adicionar arestas (apenas conexões entre bairros, peso 2)
    for _, row in df_edges.iterrows():
        if row["Weight"] == 2:
            G.add_edge(row["Source"], row["Target"])

    # 📌 3. Criar a matriz de adjacência normalizada
    matriz_adj = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))  # Matriz de vizinhança
    matriz_pesos = matriz_adj / matriz_adj.sum(axis=1, keepdims=True)  # Normaliza pelos vizinhos

    # 📌 4. Criar vetor de casos de violência
    casos = np.array([G.nodes[n]["casos"] for n in sorted(G.nodes())])

    # 📌 5. Calcular Moran's I
    N = len(casos)
    media_casos = np.mean(casos)

    numerador = 0
    for i in range(N):
        for j in range(N):
            numerador += matriz_pesos[i, j] * (casos[i] - media_casos) * (casos[j] - media_casos)

    denominador = np.sum((casos - media_casos) ** 2)

    morans_i = (N / matriz_pesos.sum()) * (numerador / denominador)

    print(f"Moran’s I calculado: {morans_i:.4f}")
    
    if morans_i > 0.6:
        print("Autocorrelação espacial positiva e significativa.")
    elif morans_i > 0 and morans_i < 0.6:
        print("Autocorrelação espacial positiva, mas não significativa.")
    elif morans_i < 0:
        print("Autocorrelação espacial negativa, ou seja os bairros com mais casos estão rodeados por bairros com menos casos.")

def calcular_pagerank(df_nodes, df_edges, damping=0.85, max_iter=100, tol=1e-6):
    # 📌 2. Criar o Grafo de bairros
    G = nx.Graph()

    # Adicionar nós (somente bairros)
    for _, row in df_nodes.iterrows():
        if row["Tipo"] == 2:  # Tipo 2 = Bairro
            G.add_node(row["ID"], bairro=row["Bairro"])

    # Adicionar arestas (somente conexões entre bairros, peso 2)
    for _, row in df_edges.iterrows():
        if row["Weight"] == 2:
            G.add_edge(row["Source"], row["Target"])

    # 📌 3. Calcular PageRank
    pagerank = nx.pagerank(G, alpha=damping, max_iter=max_iter, tol=tol)

    # Criar um DataFrame com os resultados
    pagerank_df = pd.DataFrame([
        {"ID": node, "Bairro": G.nodes[node]["bairro"], "PageRank": pagerank[node]}
        for node in G.nodes
    ]).sort_values(by="PageRank", ascending=False)

    # 📌 4. Salvar os resultados
    file_path = "datasets/output/dados/pagerank/bairros_pagerank.csv"
    pagerank_df.to_csv(file_path, index=False)
    print(f"PageRank calculado e salvo em: {file_path}")

def grafico_pagerank(df_pagerank, n):
    # Ordenar por PageRank
    df_pagerank = df_pagerank.sort_values(by="PageRank", ascending=False)

    # Criar o gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.bar(df_pagerank["Bairro"][:n], df_pagerank["PageRank"][:n], color="skyblue")
    plt.xticks(rotation=90, fontsize=9)  # Ajuste o tamanho do label do eixo X
    plt.xlabel("Bairros", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("PageRank", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("PageRank por Bairro (Top " + str(n) + ")", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/pagerank/grafico_pagerank_" + str(n) + ".png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_pagerank_casos(df_pagerank, df_bairros):
    # 📌 2. Unir os DataFrames de PageRank e Número de Casos
    df_pagerank = df_pagerank.merge(df_bairros, how="left", left_on="ID", right_on="ID")

    # 📌 3. Criar o gráfico de dispersão
    plt.figure(figsize=(8, 8))
    plt.scatter(df_pagerank["PageRank"], df_pagerank["N de casos Total"], color="skyblue", alpha=0.7)
    plt.xlabel("PageRank", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Número de Casos", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("PageRank vs. Número de Casos por Bairro", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/pagerank/grafico_pagerank_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def pearson_correlation_coefficient(df_nodes, df_edges):
    # 📌 1. Criar o Grafo
    G = nx.Graph()

    # Adicionar nós (bairros apenas)
    for _, row in df_nodes.iterrows():
        if row["Tipo"] == 2:  # Apenas bairros
            G.add_node(row["ID"], tipo="bairro", casos=row["N de casos Total"])

    # Adicionar arestas (somente entre bairros - peso 2)
    for _, row in df_edges.iterrows():
        if row["Weight"] == 2:
            G.add_edge(row["Source"], row["Target"], weight=row["Weight"])

    # 📌 2. Criar um dicionário para armazenar a média de casos dos vizinhos
    media_casos_vizinhos = {}
    desvio_casos_vizinhos = {}

    for bairro in G.nodes:
        vizinhos = [n for n in G.neighbors(bairro) if G.nodes[n]["tipo"] == "bairro"]
        if vizinhos:
            casos_vizinhos = [G.nodes[v]["casos"] for v in vizinhos]
            media_casos_vizinhos[bairro] = np.mean(casos_vizinhos)
            desvio_casos_vizinhos[bairro] = np.std(casos_vizinhos)  # Desvio padrão dos vizinhos
        else:
            media_casos_vizinhos[bairro] = 0
            desvio_casos_vizinhos[bairro] = 0

    # Criar um DataFrame com os resultados individuais por bairro
    bairros_df = pd.DataFrame([
        {"ID": bairro, 
         "Bairro": df_nodes.loc[df_nodes["ID"] == bairro, "Bairro"].values[0],
         "Casos": G.nodes[bairro]["casos"], 
         "Media Casos Vizinhos": media_casos_vizinhos[bairro],
         "Desvio Casos Vizinhos": desvio_casos_vizinhos[bairro],
         "Diferenca Percentual": ((G.nodes[bairro]["casos"] - media_casos_vizinhos[bairro]) / 
                                  (media_casos_vizinhos[bairro] + 1e-6)) * 100  # Evitar divisão por zero
        }
        for bairro in G.nodes
    ])

    # 📌 3. Salvar os resultados em um arquivo CSV
    file_path = "datasets/output/dados/assortatividade/bairros_assortatividade.csv"
    bairros_df.to_csv(file_path, index=False)
    print("Assortatividade salva em", file_path)

def grafico_assortatividade(df_bairros, n):
    # Ordenar por diferença percentual
    df_bairros = df_bairros.sort_values(by="Diferenca Percentual", ascending=False)

    # Criar o gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.bar(df_bairros["Bairro"][:n], df_bairros["Diferenca Percentual"][:n], color="skyblue")
    plt.xticks(rotation=90, fontsize=9)  # Ajuste o tamanho do label do eixo X
    plt.xlabel("Bairros", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Diferença Percentual", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Assortatividade por Bairro (Top " + str(n) + ")", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/assortatividade/grafico_assortatividade_" + str(n) + ".png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def grafico_assortatividade_casos(df_assortatividade):
    # 📌 3. Criar o gráfico de dispersão
    plt.figure(figsize=(8, 8))
    plt.scatter(df_assortatividade["Media Casos Vizinhos"], df_assortatividade["Casos"], color="skyblue", alpha=0.7)
    plt.xlabel("Média de Casos dos Vizinhos", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Número de Casos", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Assortatividade: Casos vs. Média de Casos dos Vizinhos por Bairro", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/assortatividade/grafico_assortatividade_casos.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def calcular_pvalor_assortatividade(df_assortatividade):
    """
    Lê a correlação de Pearson já calculada e salva no arquivo bairros_assortatividade.csv,
    e testa a significância estatística (p-valor).
    
    Parâmetros:
    - df_assortatividade: DataFrame contendo os valores já calculados.

    Retorno:
    - Correlação de Pearson e p-valor.
    """
    # 📌 1. Obter os valores já calculados
    casos_bairros = df_assortatividade["Casos"].values
    media_casos_vizinhos = df_assortatividade["Media Casos Vizinhos"].values

    # 📌 2. Calcular a correlação de Pearson e o p-valor
    correlacao, p_valor = pearsonr(casos_bairros, media_casos_vizinhos)
    
    return correlacao, p_valor

def teste_permutacao_assortatividade(df_assortatividade, n_permutacoes=1000):
    """
    Testa se a correlação observada entre os casos nos bairros e seus vizinhos é estatisticamente significativa
    usando um teste de permutação.

    Parâmetros:
    - df_assortatividade: DataFrame contendo os valores já calculados.
    - n_permutacoes: número de permutações para o teste.

    Retorno:
    - p-valor da permutação.
    """
    # 📌 1. Obter a correlação real já calculada
    correlacao_real, _ = calcular_pvalor_assortatividade(df_assortatividade)

    # 📌 2. Teste de Permutação
    permutacoes = []
    
    for _ in range(n_permutacoes):
        # Embaralhar os valores dos casos entr  e os bairros
        casos_embaralhados = np.random.permutation(df_assortatividade["Casos"].values)

        # Calcular a correlação de Pearson na permutação
        permutacao_corr, _ = pearsonr(casos_embaralhados, df_assortatividade["Media Casos Vizinhos"].values)
        permutacoes.append(permutacao_corr)

    # 📌 3. Calcular p-valor da permutação
    p_valor_perm = np.sum(np.abs(permutacoes) >= np.abs(correlacao_real)) / n_permutacoes

    print(f"P-valor do teste de permutação: {p_valor_perm:.4f}")

    # 📌 4. Interpretar o resultado
    if p_valor_perm < 0.05:
        print("A correlação é estatisticamente significativa com o teste de permutação (p < 0.05).")
    else:
        print("A correlação NÃO é estatisticamente significativa com o teste de permutação (p >= 0.05).")

def detectar_comunidades(df_nodes, df_edges):
    # 📌 1. Criar o Grafo
    G = nx.Graph()

    # Adicionar nós (bairros apenas)
    for _, row in df_nodes.iterrows():
        if row["Tipo"] == 2:  # Apenas bairros
            G.add_node(row["ID"], tipo="bairro", bairro=row["Bairro"])

    # Adicionar arestas (somente entre bairros - peso 2)
    for _, row in df_edges.iterrows():
        if row["Weight"] == 2:
            G.add_edge(row["Source"], row["Target"], weight=row["Weight"])

    # 📌 2. Aplicar diferentes métodos de detecção de comunidade

    ## 2.1 Girvan-Newman (Baseado em remoção de arestas)
    comp_gn = girvan_newman(G)  # Agora chamando do lugar correto
    first_level_gn = next(comp_gn, None)
    if first_level_gn:
        communities_gn = {node: i for i, community in enumerate(first_level_gn) for node in community}
    else:
        communities_gn = {}


    ## 2.2 Louvain (Baseado em otimização da modularidade)
    partition_louvain = community_louvain.best_partition(G)
    
    ## 2.3 Label Propagation (Baseado em propagação de rótulos)
    communities_lp = {node: i for i, community in enumerate(asyn_lpa_communities(G)) for node in community}

    ## 2.4 Leiden (Baseado em modularidade, similar ao Louvain, mas mais eficiente)
    # Converter NetworkX para iGraph (Leiden precisa dessa estrutura)
    # Criar um dicionário para mapear IDs originais para índices do iGraph
    # Criar uma lista de arestas e nós para o iGraph
    nodes_list = list(G.nodes)
    edges_list = list(G.edges)

    # Criar um grafo iGraph com os mesmos nós e arestas do NetworkX
    ig_G = ig.Graph(edges_list, directed=False)

    # Criar um dicionário para mapear índices do iGraph para IDs originais do NetworkX
    node_mapping = {i: nodes_list[i] for i in range(len(nodes_list))}

    # Aplicar Leiden
    partition_leiden = find_partition(ig_G, ModularityVertexPartition)

    # Converter as comunidades do Leiden de volta para os IDs originais
    communities_leiden = {node_mapping[node]: i for i, community in enumerate(partition_leiden) for node in community}



    # 📌 3. Criar um DataFrame com as Comunidades detectadas
    comunidades_df = pd.DataFrame([
        {"ID": bairro,
         "Bairro": G.nodes[bairro]["bairro"],
         "Comunidade Girvan-Newman": communities_gn.get(bairro, -1),
         "Comunidade Louvain": partition_louvain.get(bairro, -1),
         "Comunidade Label Propagation": communities_lp.get(bairro, -1),
         "Comunidade Leiden": communities_leiden.get(bairro, -1)}
        for bairro in G.nodes
    ])

    # 📌 4. Salvar os resultados em um arquivo CSV
    file_path = "datasets/output/dados/comunidades/bairros_comunidades.csv"
    comunidades_df.to_csv(file_path, index=False)
    print("Comunidades salvas em", file_path)

def grafo_por_comunidade(df_nodes, df_edges, df_communities, name):
    # 📌 2. Criar o Grafo Geral
    G = nx.Graph()

    # Criar um dicionário para armazenar o número de casos de cada bairro
    casos_por_bairro = {row["ID"]: row["N de casos Total"] for _, row in df_nodes.iterrows() if row["Tipo"] == 2}

    # Normalizar o tamanho dos nós (evita valores muito grandes ou pequenos)
    min_size = 50   # Tamanho mínimo do nó
    max_size = 2000  # Tamanho máximo do nó

    if casos_por_bairro:
        max_casos = max(casos_por_bairro.values())
        min_casos = min(casos_por_bairro.values())

        # Ajustar tamanho proporcional (evitar divisão por zero)
        tamanho_nos = {
            node: min_size + ((casos - min_casos) / (max_casos - min_casos + 1e-6)) * (max_size - min_size)
            for node, casos in casos_por_bairro.items()
        }
    else:
        tamanho_nos = {node: min_size for node in G.nodes()}  # Caso não haja dados

    # Adicionar nós ao grafo
    for _, row in df_nodes.iterrows():
        if row["Tipo"] == 2:  # Apenas bairros
            G.add_node(row["ID"], bairro=row["Bairro"])

    # Adicionar arestas (somente entre bairros - peso 2)
    for _, row in df_edges.iterrows():
        if row["Weight"] == 2:
            G.add_edge(row["Source"], row["Target"])

    # 📌 3. Mapear comunidades Girvan-Newman
    comunidade_map = dict(zip(df_communities["ID"], df_communities["Comunidade"]))

    # 📌 4. Criar subgrafos por comunidade
    unique_communities = set(comunidade_map.values())
    color_map = {
        community: matplotlib.colormaps.get_cmap("tab10")(i / len(unique_communities)) 
        for i, community in enumerate(unique_communities)
    }

    # Criar um dicionário {ID: Nome do Bairro}
    label_map = {row["ID"]: row["Bairro"] for _, row in df_nodes.iterrows() if row["Tipo"] == 2}

    # 📌 3.1 Remover comunidades isoladas com poucos nós
    min_nos_por_comunidade = 10  # Defina um valor adequado
    contagem_por_comunidade = {}

    # Contar quantos nós existem em cada comunidade
    for node in list(G.nodes):
        comunidade = comunidade_map.get(node, -1)
        if comunidade != -1:
            contagem_por_comunidade[comunidade] = contagem_por_comunidade.get(comunidade, 0) + 1

    # Filtrar comunidades com poucos nós
    comunidades_validas = {com for com, count in contagem_por_comunidade.items() if count >= min_nos_por_comunidade}

    # 📌 3.2 Atualizar comunidade_map removendo referências a comunidades inválidas
    comunidade_map_filtrado = {node: com for node, com in comunidade_map.items() if com in comunidades_validas}

    # 📌 Remover nós que pertencem a comunidades inválidas
    for node in list(G.nodes):
        if node not in comunidade_map_filtrado:
            G.remove_node(node)

    # 📌 4. Criar subgrafos por comunidade (apenas as válidas)
    unique_communities = set(comunidade_map_filtrado.values())

    # Criar o color_map apenas para comunidades válidas
    color_map = {
        community: matplotlib.colormaps.get_cmap("tab10")(i / len(unique_communities)) 
        for i, community in enumerate(unique_communities)
    }

    # colocar -1 para os bairros que as suas comunidades foram tiradas, em df_communities
    for _, row in df_communities.iterrows():
        if row["Comunidade"] not in comunidades_validas:
            df_communities.at[_, "Comunidade"] = -1

    # 📌 6. Aplicar ForceAtlas2 no Grafo Geral
    forceatlas2_global = ForceAtlas2(
        outboundAttractionDistribution=True,
        jitterTolerance=20.0,  # Deixa os nós mais espalhados
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        scalingRatio=50.0,  # Aumenta a separação dos nós
        strongGravityMode=False,
        gravity=1  # Reduz a gravidade para deixar o layout mais disperso
    )

    # Gerar posições globais usando ForceAtlas2
    with HiddenPrints():
        pos_global = forceatlas2_global.forceatlas2_networkx_layout(G, iterations=3000)

    # Criar cores para os nós globais e definir tamanho proporcional ao número de casos
    node_colors_global = [color_map[comunidade_map_filtrado[node]] for node in G.nodes if node in comunidade_map_filtrado]
    node_sizes_global = [tamanho_nos.get(node, min_size) for node in G.nodes]

    # 📌 7. Plotar o Grafo Geral
    # Criar um dicionário {ID: Nome do Bairro}

    plt.figure(figsize=(10, 7))

    # Desenhar os nós e arestas
    nx.draw(G, pos_global, with_labels=False, node_size=node_sizes_global, node_color=node_colors_global, edge_color="gray", alpha=0.8)

    # 🔹 Exibir nomes dos bairros nos nós
    nx.draw_networkx_labels(G, pos_global, labels={node: label_map.get(node, "Desconhecido") for node in G.nodes}, font_size=4)

    # Configuração do gráfico
    plt.title("ForceAtlas2 - Grafo Geral de Comunidades - " + name)
    file_path = "datasets/output/graphs/comunidades/" + name + "/grafo_geral_" + name + ".png"

    # Salvar a imagem sem espaços desnecessários
    plt.savefig(file_path, format="png", dpi=300, bbox_inches="tight")

    print("📌 Grafo Geral de Comunidades salvo em", file_path)
    plt.close()

    return color_map, df_communities

def grafico_comunidade(df_communities, df_aux, name, coluna):
    # 📌 2. Unir os DataFrames de Comunidade e Número de Casos
    df_communities = df_communities.merge(df_aux, how="left", left_on="ID", right_on="ID")

    # 📌 3. Criar o gráfico de dispersão
    plt.figure(figsize=(10, 7))
    # plt.scatter(valor_comunidade, somas, color="skyblue", alpha=0.7)
    plt.scatter(df_communities["Comunidade"], df_aux[coluna], color="skyblue", alpha=0.7)
    name1 = "Comunidade " + name
    plt.xlabel(name1, fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel(coluna, fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title(name1 + " vs. " + coluna, fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/comunidades/" + name + "/grafico_" + name1 + "_" + coluna + ".png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()
    print("Gráfico salvo em", file_path)

def normalizar_bairros(df_bairros):
    # Tirar bairros estremos, ou com 0 casos ou com muito altos, ou seja muito maior do q a maioria
    # 📌 1. Normalizar os dados
    df_bairros = df_bairros[(df_bairros["N de casos Total"] > 0)]

    media = df_bairros["N de casos Total"].mean()

    maximo = df_bairros["N de casos Total"].max()

    df_bairros = df_bairros[(df_bairros["N de casos Total"] < 5 * media)]

    # 📌 2. Salvar 
    file_path = "datasets/output/dados/bairros_normalizados.csv"
    df_bairros.to_csv(file_path, index=False)
    print("Bairros normalizados salvos em", file_path)

    return df_bairros

def media_idade(df_nodes, df_aux):
    """
    Calcula a média e o desvio padrão da idade para cada bairro, garantindo que os IDs sejam inteiros e comparáveis.
    """

    # Remover valores NaN antes de converter para inteiro
    df_nodes = df_nodes.dropna(subset=["Bairro"]).reset_index(drop=True)
    df_aux = df_aux.dropna(subset=["ID"]).reset_index(drop=True)

    # Converter apenas os bairros onde Tipo == 1 para inteiros, garantindo que não haja espaços
    df_nodes.loc[df_nodes["Tipo"] == 1, "Bairro"] = df_nodes.loc[df_nodes["Tipo"] == 1, "Bairro"].astype(str).str.strip().astype(int)

    # Converter IDs de df_aux para inteiro (garantindo limpeza de espaços)
    df_aux["ID"] = df_aux["ID"].astype(str).str.strip().astype(int)

    for i in range(len(df_aux)):
        idades = []
        id_bairro_aux = int(df_aux.at[i, "ID"])  # Converter para int

        for j in range(len(df_nodes)):
            if df_nodes.at[j, "Tipo"] == 1:  # Considerando apenas pessoas
                bairro = int(df_nodes.at[j, "Bairro"])  # Converter para int

                if bairro == id_bairro_aux:  # Agora ambos são int
                    idade = df_nodes.at[j, "Idade Aparente"]
                    if idade != -1:
                        idades.append(idade)

        if idades:
            media_idade = int(np.mean(idades))  # Média como número inteiro
            desvio_padrao = round(np.std(idades, ddof=0), 2)  # Desvio padrão com 2 casas decimais
        else:
            media_idade = -1
            desvio_padrao = -1

        df_aux.at[i, "Media Idade"] = media_idade
        df_aux.at[i, "Desvio Padrao Idade"] = desvio_padrao

    # Salvar CSV com os resultados
    file_path = "datasets/output/dados/media/media_idade.csv"
    df_aux.to_csv(file_path, index=False)
    print("Média de idade salva em", file_path)

    return df_aux

def media_cor(df_nodes, df_aux):
    """
    Calcula a cor predominante e o desvio padrão da distribuição de cores para um bairro.
    """

    # Garantir que os IDs dos bairros em df_aux sejam inteiros e bem formatados
    df_aux["ID"] = df_aux["ID"].astype(str).str.strip().astype(int)

    # Criar dicionários para armazenar os resultados
    cor_predominante = {}
    desvio_padrao_cor = {}

    # Filtrar apenas as pessoas (Tipo == 1) e converter "Bairro" para inteiro apenas nesses casos
    df_pessoas = df_nodes[df_nodes["Tipo"] == 1].copy()
    df_pessoas.loc[:, "Bairro"] = df_pessoas["Bairro"].astype(str).str.strip().astype(int)

    # Agrupar por bairro e cor para contar quantas pessoas de cada cor existem
    contagem_cores = df_pessoas.groupby(["Bairro", "Raca Cor"]).size().reset_index(name="Quantidade")

    for _, row in df_aux.iterrows():
        bairro_id = row["ID"]

        # Filtrar apenas as contagens desse bairro
        cores_bairro = contagem_cores[contagem_cores["Bairro"] == bairro_id]

        if not cores_bairro.empty:
            # Encontrar a cor predominante
            cor_mais_comum = cores_bairro.loc[cores_bairro["Quantidade"].idxmax(), "Raca Cor"]
            cor_predominante[bairro_id] = cor_mais_comum

            # Calcular as proporções de cada cor no bairro
            total = cores_bairro["Quantidade"].sum()
            proporcoes = cores_bairro["Quantidade"] / total

            # Calcular desvio padrão das proporções
            desvio_padrao = round(np.sqrt(np.sum(proporcoes * (1 - proporcoes))), 4)
            desvio_padrao_cor[bairro_id] = desvio_padrao
        else:
            cor_predominante[bairro_id] = "DESCONHECIDO"
            desvio_padrao_cor[bairro_id] = -1  # Sem dados

    # Aplicar os resultados no DataFrame df_aux sem gerar `SettingWithCopyWarning`
    df_aux = df_aux.copy()
    df_aux["Cor Predominante"] = df_aux["ID"].map(cor_predominante)
    df_aux["Desvio Padrao Cor"] = df_aux["ID"].map(desvio_padrao_cor)

    # Salvar CSV com os resultados
    file_path = "datasets/output/dados/media/media_cor.csv"
    df_aux.to_csv(file_path, index=False)
    print("Cor predominante salva em", file_path)

    return df_aux

def media_escolaridade(df_nodes, df_aux):
    """
    Calcula a escolaridade predominante e o desvio padrão da distribuição de escolaridade para um bairro.
    """

    # Garantir que os IDs dos bairros em df_aux sejam inteiros e bem formatados
    df_aux["ID"] = df_aux["ID"].astype(str).str.strip().astype(int)

    # Criar dicionários para armazenar os resultados
    escolaridade_predominante = {}
    desvio_padrao_escolaridade = {}

    # Filtrar apenas as pessoas (Tipo == 1) e converter "Bairro" para inteiro apenas nesses casos
    df_pessoas = df_nodes[df_nodes["Tipo"] == 1].copy()
    df_pessoas.loc[:, "Bairro"] = df_pessoas["Bairro"].astype(str).str.strip().astype(int)

    # Agrupar por bairro e escolaridade para contar quantas pessoas de cada nível escolar existem
    contagem_escolaridade = df_pessoas.groupby(["Bairro", "Escolaridade"]).size().reset_index(name="Quantidade")

    for _, row in df_aux.iterrows():
        bairro_id = row["ID"]

        # Filtrar apenas as contagens desse bairro
        escolaridade_bairro = contagem_escolaridade[contagem_escolaridade["Bairro"] == bairro_id]

        if not escolaridade_bairro.empty:
            # Encontrar a escolaridade predominante
            escolaridade_mais_comum = escolaridade_bairro.loc[escolaridade_bairro["Quantidade"].idxmax(), "Escolaridade"]
            escolaridade_predominante[bairro_id] = escolaridade_mais_comum

            # Calcular as proporções de cada escolaridade no bairro
            total = escolaridade_bairro["Quantidade"].sum()
            proporcoes = escolaridade_bairro["Quantidade"] / total

            # Calcular desvio padrão das proporções
            desvio_padrao = round(np.sqrt(np.sum(proporcoes * (1 - proporcoes))), 4)
            desvio_padrao_escolaridade[bairro_id] = desvio_padrao
        else:
            escolaridade_predominante[bairro_id] = "DESCONHECIDO"
            desvio_padrao_escolaridade[bairro_id] = -1  # Sem dados

    # Aplicar os resultados no DataFrame df_aux sem gerar `SettingWithCopyWarning`
    df_aux = df_aux.copy()
    df_aux["Escolaridade Predominante"] = df_aux["ID"].map(escolaridade_predominante)
    df_aux["Desvio Padrao Escolaridade"] = df_aux["ID"].map(desvio_padrao_escolaridade)

    # Salvar CSV com os resultados
    file_path = "datasets/output/dados/media/media_escolaridade.csv"
    df_aux.to_csv(file_path, index=False)
    print("Escolaridade predominante salva em", file_path)

    return df_aux

def media_classificacao(df_nodes, df_aux):
    # Garantir que os IDs dos bairros em df_aux sejam inteiros e bem formatados
    df_aux["ID"] = df_aux["ID"].astype(str).str.strip().astype(int)

    # Criar dicionários para armazenar os resultados
    classificacao_predominante = {}
    desvio_padrao_classificacao = {}

    # Filtrar apenas as pessoas (Tipo == 1) e converter "Bairro" para inteiro apenas nesses casos
    df_pessoas = df_nodes[df_nodes["Tipo"] == 1].copy()
    df_pessoas.loc[:, "Bairro"] = df_pessoas["Bairro"].astype(str).str.strip().astype(int)

    # Agrupar por bairro e classificacao para contar quantas pessoas de cada nível escolar existem
    contagem_classificacao = df_pessoas.groupby(["Bairro", "Classificacao"]).size().reset_index(name="Quantidade")

    for _, row in df_aux.iterrows():
        bairro_id = row["ID"]

        # Filtrar apenas as contagens desse bairro
        classificacao_bairro = contagem_classificacao[contagem_classificacao["Bairro"] == bairro_id]

        if not classificacao_bairro.empty:
            # Encontrar a classificacao predominante
            classificacao_mais_comum = classificacao_bairro.loc[classificacao_bairro["Quantidade"].idxmax(), "Classificacao"]
            classificacao_predominante[bairro_id] = classificacao_mais_comum

            # Calcular as proporções de cada classificacao no bairro
            total = classificacao_bairro["Quantidade"].sum()
            proporcoes = classificacao_bairro["Quantidade"] / total

            # Calcular desvio padrão das proporções
            desvio_padrao = round(np.sqrt(np.sum(proporcoes * (1 - proporcoes))), 4)
            desvio_padrao_classificacao[bairro_id] = desvio_padrao
        else:
            classificacao_predominante[bairro_id] = "DESCONHECIDO"
            desvio_padrao_classificacao[bairro_id] = -1  # Sem dados

    # Aplicar os resultados no DataFrame df_aux sem gerar `SettingWithCopyWarning`
    df_aux = df_aux.copy()
    df_aux["Classificacao Predominante"] = df_aux["ID"].map(classificacao_predominante)
    df_aux["Desvio Padrao Classificacao"] = df_aux["ID"].map(desvio_padrao_classificacao)

    # Salvar CSV com os resultados
    file_path = "datasets/output/dados/media/media_classificacao.csv"
    df_aux.to_csv(file_path, index=False)
    print("Classificacao predominante salva em", file_path)

    return df_aux

def grafico_idade_grau_casos(df_nodes):
    # Filtrar apenas as pessoas (Tipo == 1)
    df_pessoas = df_nodes[df_nodes["Tipo"] == 1]

    # 📌 1. Criar o gráfico de dispersão
    plt.figure(figsize=(10, 7))
    plt.scatter(df_pessoas["Idade Aparente"], df_pessoas["Classificacao"], color="skyblue", alpha=0.7)
    plt.xlabel("Idade", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Classificação", fontsize=14)  # Ajuste o tamanho do label do eixo Y
    plt.title("Idade vs. Classificação", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/gerais/grafico_idade_classificacao.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()

    print("Gráfico salvo em", file_path)

def grafico_media_idade_grau_casos(df_idade, df_classificacao):
    # Ordenar por média de idade
    df_idade = df_idade.sort_values(by="Media Idade", ascending=False)

    # 📌 1. Criar o gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.scatter(df_idade["Media Idade"], df_classificacao["Classificacao Predominante"], color="skyblue", alpha=0.7)
    plt.xlabel("Média de Idade", fontsize=14)  # Ajuste o tamanho do label do eixo X
    plt.ylabel("Classificação Predominante", fontsize=14)  # Ajuste o tamanho do label do eixo Y    
    plt.title("Média de Idade vs. Classificação Predominante", fontsize=16)  # Ajuste o tamanho do título
    plt.grid(linestyle="--", alpha=0.7)

    # Salvar o gráfico como um arquivo PNG
    file_path = "datasets/output/graphs/media/grafico_media_idade_classificacao.png"
    plt.savefig(file_path, dpi=300, bbox_inches="tight")

    # Fechar a figura para liberar memória
    plt.close()

    print("Gráfico salvo em", file_path)
    
def main():
    df_divinopolis = pd.read_csv("datasets/output/dados/dados_divinopolis.csv")
    grafico_distribuicao_idade(df_divinopolis)
    grafico_distribuicao_cor(df_divinopolis)
    grafico_distribuicao_escolaridade(df_divinopolis)

    # Carregar os dados do arquivo nodes.csv
    df_bairros = pd.read_csv("datasets/output/dados/nodes-edges/nodes_bairros.csv") 
    grafico_bairro_casos(df_bairros, 10)
    
    # estudo da dispersão dos casos em relação a idadae, raca/cor e escolaridade
    # primeiro tirar bairros com numeros muito estremos de casos, ou 0 ou muito alto
    df_bairros = normalizar_bairros(df_bairros)

    # Carregar os dados dos arquivos nodes.csv e edges.csv
    df_nodes = pd.read_csv("datasets/output/dados/nodes-edges/nodes.csv")
    df_edges = pd.read_csv("datasets/output/dados/nodes-edges/edges.csv")

    # 📌 1. Calcular Métricas
    # centralidade de betweenness para entender a importância dos bairros
    betweenness_centrality(df_nodes, df_edges)
    df_betweenness = pd.read_csv("datasets/output/dados/betweenness/bairros_betweenness.csv")
    grafico_betweenness(df_betweenness, 10)
    grafico_betweenness_casos(df_betweenness, df_bairros)

    # centralidade de closeness para entender a proximidade dos bairros de acordo com a quantidade de casos
    closeness_centrality(df_nodes, df_edges)
    df_closeness = pd.read_csv("datasets/output/dados/closeness/bairros_closeness.csv")
    grafico_closeness(df_closeness, 10)
    grafico_closeness_casos(df_closeness, df_bairros)
    
    # morans i para entender a autocorrelação espacial dos casos
    calcular_morans_i(df_nodes, df_edges)

    # pagerank para entender a importância dos bairros
    calcular_pagerank(df_nodes, df_edges)
    df_pagerank = pd.read_csv("datasets/output/dados/pagerank/bairros_pagerank.csv")
    grafico_pagerank(df_pagerank, 10)
    grafico_pagerank_casos(df_pagerank, df_bairros)

    # coeficiente de correlação de Pearson para entender a relação entre a quantidade de casos dos bairros e seus vizinhos
    pearson_correlation_coefficient(df_nodes, df_edges)
    df_assortatividade = pd.read_csv("datasets/output/dados/assortatividade/bairros_assortatividade.csv")
    grafico_assortatividade(df_assortatividade, 10)
    grafico_assortatividade_casos(df_assortatividade)

    # p-valor para entender a significância estatística da correlação de Pearson
    correlacao, p_valor = calcular_pvalor_assortatividade(df_assortatividade)
    print(f"Correlação de Pearson: {correlacao:.4f}")
    print(f"P-valor: {p_valor:.4f}")
    # 📌 3. Interpretar o p-valor
    if p_valor < 0.05:
        print("A correlação é estatisticamente significativa (p < 0.05).")
    else:
        print("A correlação NÃO é estatisticamente significativa (p >= 0.05).")

    # teste de permutação para entender a significância estatística da correlação de Pearson
    teste_permutacao_assortatividade(df_assortatividade)
    
    # 📌 2. Detectar Comunidades
    detectar_comunidades(df_nodes, df_edges)
    df_comunidades = pd.read_csv("datasets/output/dados/comunidades/bairros_comunidades.csv")
    # gerar gráficos para cada modelo de comunidade

    color_map = {}
    for df in [df_comunidades["Comunidade Girvan-Newman"], df_comunidades["Comunidade Louvain"], df_comunidades["Comunidade Label Propagation"], df_comunidades["Comunidade Leiden"]]:
        df_aux = pd.DataFrame()
        df_aux["ID"] = df_comunidades["ID"]
        df_aux["Bairro"] = df_comunidades["Bairro"]
        df_aux["Comunidade"] = df
        # name é o algoritmo de comunidade
        name = "Girvan-Newman" if df is df_comunidades["Comunidade Girvan-Newman"] else "Louvain" if df is df_comunidades["Comunidade Louvain"] else "Label Propagation" if df is df_comunidades["Comunidade Label Propagation"] else "Leiden"
        aux, df_aux1 = grafo_por_comunidade(df_nodes, df_edges, df_aux, name)

        if name == "Leiden":
            color_map = aux
            df_bairros["Comunidade"] = df_aux1["Comunidade"]
        
        i = 0
        for df_aux1 in [df_nodes[df_nodes["Tipo"] == 2], df_betweenness, df_closeness, df_pagerank, df_assortatividade]:
            coluna = "N de casos Total" if i == 0 else "Media Casos Vizinhos" if i == 4 else df_aux1.columns[2]
            print(coluna)   
            grafico_comunidade(df_aux, df_aux1, name, coluna)
            i += 1

    # Definir a cor branca para a comunidade -1
    color_map[-1] = (1.0, 1.0, 1.0, 1.0)  # Branco em formato RGBA

    df_aux = pd.DataFrame()
    df_aux["ID"] = df_bairros["ID"]
    df_aux["Bairro"] = df_bairros["Bairro"]
    df_idade = media_idade(df_nodes, df_aux)
    df_cor = media_cor(df_nodes, df_aux)
    df_escolaridade = media_escolaridade(df_nodes, df_aux)
    df_classificacao = media_classificacao(df_nodes, df_aux)

    df_idade = pd.read_csv("datasets/output/dados/media/media_idade.csv")
    df_cor = pd.read_csv("datasets/output/dados/media/media_cor.csv")
    df_escolaridade = pd.read_csv("datasets/output/dados/media/media_escolaridade.csv")
    df_classificacao = pd.read_csv("datasets/output/dados/media/media_classificacao.csv")

    grafico_idade_casos(df_nodes)
    grafico_cor_casos(df_nodes)
    grafico_escolaridade_casos(df_nodes)
    grafico_classificacao_casos(df_nodes)

    # grafico idade e numero de casos
    grafico_media_idade_casos(df_idade, df_bairros, color_map)

    # grafico cor predominante e numero de casos
    grafico_media_cor_casos(df_cor, df_bairros, color_map)

    # grafico escolaridade predominante e numero de casos
    grafico_media_escolaridade_casos(df_escolaridade, df_bairros, color_map)

    # grafico classificacao predominante e numero de casos
    grafico_media_classificacao_casos(df_classificacao, df_bairros, color_map)
                                   
if __name__ == "__main__":
    main()