import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import math

def posicionar_nos(G, raio_inicial=0.3, fator_espacamento=0.15):
    """
    Posiciona os nós do grafo de forma que:
      - Os nós de bairros (Tipo 2) são posicionados usando um layout (ex.: spring layout).
      - Para cada nó de bairro, os nós de casos (Tipo 1) conectados a ele são
        reposicionados formando um círculo ao redor do bairro.
    
    Parâmetros:
      - raio_inicial: raio mínimo para o círculo dos nós de caso.
      - fator_espacamento: fator multiplicador que aumenta o raio conforme o número de casos.
    """
    pos = {}

    # Separa os nós por tipo.
    nos_bairros = [n for n, data in G.nodes(data=True) if data.get("Tipo") == 2]
    nos_casos   = [n for n, data in G.nodes(data=True) if data.get("Tipo") == 1]

    # Posiciona os nós de bairros usando spring_layout com parâmetros ajustados para maior espaçamento.
    pos_bairros = nx.spring_layout(G.subgraph(nos_bairros), iterations=60, k=0.5)
    pos.update(pos_bairros)

    # Para cada bairro, reposiciona os nós de casos conectados a ele em um círculo.
    for bairro in nos_bairros:
        casos = [viz for viz in G.neighbors(bairro) if G.nodes[viz].get("Tipo") == 1]
        n_casos = len(casos)
        if n_casos == 0:
            continue

        bx, by = pos[bairro]
        # Ajusta o raio de acordo com o número de casos para evitar sobreposição
        raio = raio_inicial * (1 + n_casos * fator_espacamento)
        for i, caso in enumerate(casos):
            angulo = 2 * math.pi * i / n_casos  # Divide 360° igualmente
            x = bx + raio * math.cos(angulo)
            y = by + raio * math.sin(angulo)
            pos[caso] = (x, y)

    # Para nós isolados ou sem posição definida, usa spring_layout.
    nos_sem_pos = set(G.nodes()) - set(pos.keys())
    if nos_sem_pos:
        pos_restantes = nx.spring_layout(G.subgraph(nos_sem_pos), iterations=60, k=0.5)
        pos.update(pos_restantes)

    return pos

def load_data(nodes_file, edges_file):
    """
    Carrega os dados dos nós e arestas a partir dos arquivos CSV.
    """
    df_nodes = pd.read_csv(nodes_file)
    df_edges = pd.read_csv(edges_file)
    return df_nodes, df_edges

def build_graph(df_nodes, df_edges):
    """
    Cria o grafo adicionando nós e arestas a partir dos DataFrames.
    Cada nó recebe os atributos lidos do CSV.
    """
    G = nx.Graph()
    for _, row in df_nodes.iterrows():
        node_id = row["ID"]
        data = row.to_dict()
        G.add_node(node_id, **data)
    for _, row in df_edges.iterrows():
        source = row["Source"]
        target = row["Target"]
        weight = row.get("Weight", 1)
        G.add_edge(source, target, weight=weight)
    return G

def is_neighborhood(node_data):
    """
    Verifica se o nó é de bairro.
    Considera-se que o nó é bairro se o atributo "Classificacao" for "Bairro"
    (a comparação é feita em caixa alta).
    """
    classificacao = str(node_data.get("Classificacao", "")).strip().upper()
    return classificacao == "BAIRRO"

def compute_case_counts(G):
    """
    Para cada nó de bairro, conta quantos nós de caso (Tipo 1) estão conectados.
    Retorna um dicionário: {id_bairro: número_de_casos}.
    """
    counts = {}
    for node, data in G.nodes(data=True):
        if is_neighborhood(data):
            count = 0
            for neighbor in G.neighbors(node):
                if not is_neighborhood(G.nodes[neighbor]):
                    count += 1
            counts[node] = count
    return counts

def visualize_full_graph_default(G, output_path):
    """
    Visualiza o grafo completo com:
      - Posicionamento personalizado (nós de casos em círculo ao redor dos bairros).
      - Bairros desenhados em preto (tamanho fixo);
      - Casos desenhados com cores de acordo com sua classificação:
            "NAO FATAL" -> verde,
            "POSSIVEL FATAL" -> laranja,
            "ALTO RISCO DE FATALIDADE" -> vermelho.
      - Rótulos apenas para os bairros.
    Salva a imagem em output_path.
    """
    pos = posicionar_nos(G, raio_inicial=10, fator_espacamento=0.15)
    neighborhoods = [n for n, d in G.nodes(data=True) if is_neighborhood(d)]
    cases = [n for n, d in G.nodes(data=True) if not is_neighborhood(d)]
    
    plt.figure(figsize=(12, 10))
    
    # Desenha os bairros (nós de Tipo 2) em preto, tamanho fixo
    nx.draw_networkx_nodes(G, pos,
                           nodelist=neighborhoods,
                           node_color="black",
                           node_size=300,
                           label="Bairros")
    
    # Define as cores para os casos com base na classificação
    classification_colors = {
        "NAO FATAL": "green",
        "POSSIVEL FATAL": "orange",
        "ALTO RISCO DE FATALIDADE": "red"
    }
    case_colors = [
        classification_colors.get(
            str(G.nodes[node].get("Classificacao", "Desconhecido")).strip().upper(),
            "gray"
        ) for node in cases
    ]
    # Desenha os casos em seus respectivos tons, tamanho fixo
    nx.draw_networkx_nodes(G, pos,
                           nodelist=cases,
                           node_color=case_colors,
                           node_size=5,
                           label="Casos")
    
   # Cria uma lista com a largura para cada aresta baseada no atributo "weight"
    edge_widths = [float(G[u][v].get("weight", 1)) * 1.5 for u, v in G.edges()]

    # Desenha as arestas usando a lista de larguras
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=edge_widths)
    
    # Rótulos apenas para os bairros
    labels = {n: G.nodes[n].get("Bairro", str(n)) for n in neighborhoods}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title("Grafo Completo - Visualização Padrão com Posicionamento Personalizado")
    plt.axis("off")
    plt.savefig(output_path, dpi=300)
    plt.close()

def filtrar_bairros_por_casos(G, case_counts, min_count):
    """
    Retorna um subgrafo contendo:
      - Bairros que tenham >= min_count casos,
      - E todos os casos (nós Tipo=1) ligados a esses bairros.

    Parâmetros:
      - G: Grafo completo.
      - case_counts: dicionário {bairro: qtd_casos}.
      - min_count: limite mínimo de casos para manter o bairro.

    Retorna:
      - H: subgrafo com nós filtrados.
      - neighborhoods_relevantes: lista dos IDs de bairros que foram mantidos.
    """
    # Identifica os bairros que atingem o mínimo de casos
    neighborhoods_relevantes = [b for b, cnt in case_counts.items() if cnt >= min_count]

    # Para cada bairro relevante, pega os casos diretamente conectados a ele
    casos_relevantes = []
    for bairro in neighborhoods_relevantes:
        # Filtra vizinhos que sejam casos (Tipo=1)
        casos = [viz for viz in G.neighbors(bairro) if G.nodes[viz].get("Tipo") == 1]
        casos_relevantes.extend(casos)

    # Conjunto de nós finais = bairros relevantes + casos conectados
    relevant_nodes = set(neighborhoods_relevantes) | set(casos_relevantes)

    # Cria o subgrafo e retorna
    H = G.subgraph(relevant_nodes).copy()
    return H, neighborhoods_relevantes


def visualize_filtered_centrality(G, min_count, output_path):
    """
    1. Calcula a quantidade de casos por bairro (case_counts).
    2. Remove bairros que não atingem 'min_count' de casos.
    3. Mantém só os bairros relevantes e os casos deles.
    4. Aplica posicionar_nos no subgrafo final.
    5. Desenha com tamanho dos bairros proporcional aos casos e cores nas classificações.

    Salva a imagem em output_path.
    """
    # (1) Calcula a quantidade de casos por bairro
    case_counts = compute_case_counts(G)

    # (2) Filtra bairros com < min_count casos, mantendo só os relevantes
    H, neighborhoods_relevantes = filtrar_bairros_por_casos(G, case_counts, min_count)
    
    # Se não sobrou nenhum bairro relevante, encerra
    if len(neighborhoods_relevantes) == 0:
        print(f"Nenhum bairro possui >= {min_count} casos. Nada para visualizar.")
        return

    # (3) Posiciona os nós do subgrafo
    pos = posicionar_nos(H, raio_inicial=3.0, fator_espacamento=0.2)

    # Agora separamos bairros e casos dentro desse subgrafo H
    neighborhoods = [n for n, d in H.nodes(data=True) if d.get("Tipo") == 2]
    cases = [n for n, d in H.nodes(data=True) if d.get("Tipo") == 1]

    plt.figure(figsize=(12, 10))

    # Ajusta tamanhos: case_counts[n] ainda funciona, pois o ID n existe em G
    neighborhood_sizes = [300 + case_counts.get(n, 0) * 20 for n in neighborhoods]
    nx.draw_networkx_nodes(
        H, pos,
        nodelist=neighborhoods,
        node_color="black",
        node_size=neighborhood_sizes,
        label="Bairros"
    )

    # Define a coloração dos casos pela classificação
    classification_colors = {
        "NAO FATAL": "green",
        "POSSIVEL FATAL": "orange",
        "ALTO RISCO DE FATALIDADE": "red"
    }
    case_colors = []
    for node in cases:
        clas = str(H.nodes[node].get("Classificacao", "")).strip().upper()
        case_colors.append(classification_colors.get(clas, "gray"))

    nx.draw_networkx_nodes(
        H, pos,
        nodelist=cases,
        node_color=case_colors,
        node_size=5,
        label="Casos"
    )

    # Se quiser variar a grossura das arestas conforme 'weight'
    edge_widths = [H[u][v].get("weight", 1) * 0.5 for u, v in H.edges()]
    nx.draw_networkx_edges(H, pos, alpha=0.3, width=edge_widths)

    # Só rotulamos os bairros
    labels = {n: H.nodes[n].get("Bairro", str(n)) for n in neighborhoods}
    nx.draw_networkx_labels(H, pos, labels, font_size=8)

    plt.title(f"Bairros com >= {min_count} casos")
    plt.axis("off")
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    # Arquivos de dados
    nodes_file = "./datasets/nodes.csv"
    edges_file = "./datasets/edges.csv"
    
    # Carrega os dados
    df_nodes, df_edges = load_data(nodes_file, edges_file)
    # Cria o grafo completo
    G = build_graph(df_nodes, df_edges)
    print("Grafo criado com {} nós e {} arestas.".format(G.number_of_nodes(), G.number_of_edges()))
    
    # Cria o diretório para salvar as imagens, se não existir
    output_dir = "./datasets/graphs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Visualização padrão (todos os nós com posicionamento personalizado)
    default_output_path = os.path.join(output_dir, "full_graph_default.png")
    visualize_full_graph_default(G, default_output_path)
    print("Imagem do grafo completo (padrão) salva em:", default_output_path)
    
    # Calcula os "índices de centralidade" como a contagem dos casos conectados a cada bairro
  
    G = build_graph(df_nodes, df_edges)
    
    # Visualiza apenas bairros que tenham no mínimo 10 casos
    filtered_output_path = os.path.join(output_dir, "high_case_centrality.png")
    visualize_filtered_centrality(G, min_count=10, output_path=filtered_output_path)
    print("Imagem do grafo filtrado por casos salva em:", filtered_output_path)

if __name__ == "__main__":
    main()
