

<a name="readme-topo"></a>

<h1 align='center'>
  🧮👩🏽 Análise Geoespacial da Violência Contra a Mulher: Detecção de Padrões e Clusters para Monitoramento Contı́nuo
</h1>

<div align='center'>

[![SO][Ubuntu-badge]][Ubuntu-url]
[![IDE][vscode-badge]][vscode-url]
[![Python][Python-badge]][Python-url]
[![IEEE][ieee-badge]][ieee-url]

Algoritmos e Estruturas de Dados II <br>
Engenharia de Computação <br>
Prof. Michel Pires da Silva <br>
CEFET-MG Campus V <br>
2024/2  

</div>

<details> 
  <summary>
    <b style='font-size: 14px'> Abstract </b>
  </summary>
 A violência contra a mulher é uma realidade persistente no Brasil, apesar dos recursos legislativos, como a Lei Maria da Penha (Lei n. 11.340/2006) e a Lei do Feminicídio (Lei 13.104/2015). Este estudo propõe uma abordagem computacional para análise de padrões espaciais e temporais da violência contra mulheres, utilizando a cidade brasileira de Divinópolis/MG como estudo de caso, com os dados da Secretaria de Estado de Justiça e Segurança Pública de Minas Gerais. Para isso, foram testados diferentes algoritmos de detecção de clusters, e o algoritmo de Leiden se destacou por garantir clusters bem conectados internamente, evitando agrupamentos fragmentados que poderiam comprometer a análise espacial dos bairros. Também, analisa-se a variação do desvio padrão da escolaridade das vítimas ao longo do tempo, além de fatores como raça/cor e a classificação do caso, utilizando gráficos de dispersão. Os resultados indicam que, nos bairros com maior incidência de casos, a distribuição, por exemplo, da escolaridade tende a se estabilizar em um padrão relativamente uniforme, mas com um valor elevado. Isso sugere que a violência não está restrita a um nível educacional específico, atingindo vítimas de diferentes formações acadêmicas. Além disso, os bairros com alta incidência de violência estão geograficamente agrupados em comunidades próximas, que coincidem com áreas de maior criminalidade e risco socioeconômico. Com base nos achados, essa metodologia pode ser aplicada a um modelo de monitoramento contínuo, no qual variações anômalas nos padrões previamente identificados possam sinalizar novos focos de violência, mudanças inesperadas nas áreas de risco ou alteração no tipo de vítima. Isso pode apoiar órgãos públicos na identificação precoce de padrões emergentes de violência, contribuindo para políticas públicas mais eficazes e estratégias de prevenção baseadas em evidências. <br><br>
  🔑 <b>Keywords:</b> violência contra a mulher, análise geoespacial, clusters, detecção de padrões, Algoritmo de Leiden, dados socioeconômicos, monitoramento contínuo.
<br>
</details>

## 📚 O Projeto
O projeto tem como objetivo analisar a violência contra a mulher na cidade de Divinópolis/MG, utilizando dados da Secretaria de Estado de Justiça e Segurança Pública de Minas Gerais. Para isso, foram testados diferentes algoritmos de detecção de clusters, e o algoritmo de Leiden se destacou por garantir clusters bem conectados internamente, evitando agrupamentos fragmentados que poderiam comprometer a análise espacial dos bairros. Também, analisa-se a variação do desvio padrão da escolaridade das vítimas ao longo do tempo, além de fatores como raça/cor e a classificação do caso, utilizando gráficos de dispersão. Os resultados indicam que, nos bairros com maior incidência de casos, a distribuição, por exemplo, da escolaridade tende a se estabilizar em um padrão relativamente uniforme, mas com um valor elevado. Isso sugere que a violência não está restrita a um nível educacional específico, atingindo vítimas de diferentes formações acadêmicas. Além disso, os bairros com alta incidência de violência estão geograficamente agrupados em comunidades próximas, que coincidem com áreas de maior criminalidade e risco socioeconômico. Com base nos achados, essa metodologia pode ser aplicada a um modelo de monitoramento contínuo, no qual variações anômalas nos padrões previamente identificados possam sinalizar novos focos de violência, mudanças inesperadas nas áreas de risco ou alteração no tipo de vítima. Isso pode apoiar órgãos públicos na identificação precoce de padrões emergentes de violência, contribuindo para políticas públicas mais eficazes e estratégias de prevenção baseadas em evidências.

# 
Neste repositório você encontrará o código fonte do projeto, bem como os dados utilizados para a análise. O projeto foi desenvolvido em Python. O foco principal deste trabalho é a criação de um artigo, que está disponível em PDF em [`Análise_Geoespacial_da_Violência_Contra_a_Mulher__Detecção_de_Padrões_e_Clusters_para_Monitoramento_Contínuo.pdf`](article/Análise_Geoespacial_da_Violência_Contra_a_Mulher__Detecção_de_Padrões_e_Clusters_para_Monitoramento_Contínuo.pdf).

## Instalando
Para instalar o projeto, siga os passos abaixo:

<div align="justify">
  Com o ambiente preparado, os seguintes passos são para a instalação, compilação e execução do programa localmente:

  1. Clone o repositório no diretório desejado:
  ```console
  git clone https://github.com/dudatsouza/women-violence-graphs.git
  cd women-violence-graphs
  ```
  2. Para a execução é necessário ter as seguintes bibliotecas instaladas:
- `pandas`
- `matplotlib`
- `networkx`
- `numpy`
- `community`
- `fa2_modified`
- `igraph`
- `leidenalg`
- `seaborn`
- `statsmodels`

3. Execute o comando abaixo para roda o programa:
```console
python3 src/main.py
```

</div>

<p align="right">(<a href="#readme-topo">voltar ao topo</a>)</p>

## 🧪 Ambiente de Compilação e Execução

<div align="justify">

  O trabalho foi desenvolvido e testado em várias configurações de hardware. Podemos destacar algumas configurações de Sistema Operacional e Compilador, pois as demais configurações não influenciam diretamente no desempenho do programa.

</div>

<div align='center'>

[![SO][Ubuntu-badge]][Ubuntu-url]
[![IDE][vscode-badge]][vscode-url]
[![Python][Python-badge]][Python-url]
[![IEEE][ieee-badge]][ieee-url]

| *Hardware* | *Especificações* |
|:------------:|:-------------------:|
| *Laptop*   | Dell Inspiron 13 5330 |
| *Processador* | Intel Core i7-1360P |
| *Memória RAM* | 16 GB DDR5 |
| *Sistema Operacional* | Ubuntu 20.04 LTS |
| *IDE* | Visual Studio Code |
| *Placa de Vídeo* | Intel Iris Xe Graphics |

</div>

> [!IMPORTANT] 
> Para que os testes tenham validade, considere as especificações
> do ambiente de compilação e execução do programa.

<p align="right">(<a href="#readme-topo">voltar ao topo</a>)</p>

## 📨 Contato

Segue as informações de contato da autora do trabalho:

<div align='center'>


[![INSTA](https://img.shields.io/badge/-000?style=flat&logo=instagram&logoColor=red)](https://www.instagram.com/dudat_18)
[![DISCORD](https://img.shields.io/badge/-000?style=flat&logo=discord)](https://discord.com/invite/dudat_18)
[![GMAIL](https://img.shields.io/badge/-000?style=flat&logo=gmail)](dudateixeirasouza@gmail.com)
[![LINKEDIN](https://img.shields.io/badge/In-000?style=flat&logo=linkedin)](https://www.linkedin.com/in/dudatsouza)
[![TELEGRAM](https://img.shields.io/badge/-000?style=flat&logo=telegram&logoColor=blue)](https://t.me/dudat_18)
[![X](https://img.shields.io/badge/-000?style=flat&logo=x)](https://x.com/dudat_18)

</div>

<p align="right">(<a href="#readme-topo">voltar ao topo</a>)</p>





[vscode-badge]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[vscode-url]: https://code.visualstudio.com/docs/?dv=linux64_deb
[make-badge]: https://img.shields.io/badge/_-MAKEFILE-427819.svg?style=for-the-badge
[make-url]: https://www.gnu.org/software/make/manual/make.html
[cpp-badge]: https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white
[cpp-url]: https://en.cppreference.com/w/cpp
[github-prof]: https://github.com/mpiress
[main-ref]: src/main.cpp
[branchAMM-url]: https://github.com/alvarengazv/trabalhosAEDS1/tree/AlgoritmosMinMax
[makefile]: ./makefile
[bash-url]: https://www.hostgator.com.br/blog/o-que-e-bash/
[lenovo-badge]: https://img.shields.io/badge/lenovo%20laptop-E2231A?style=for-the-badge&logo=lenovo&logoColor=white
[ubuntu-badge]: https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white
[Ubuntu-url]: https://ubuntu.com/
[ryzen5500-badge]: https://img.shields.io/badge/AMD%20Ryzen_5_5500U-ED1C24?style=for-the-badge&logo=amd&logoColor=white
[ryzen3500-badge]: https://img.shields.io/badge/AMD%20Ryzen_5_3500X-ED1C24?style=for-the-badge&logo=amd&logoColor=white
[windows-badge]: https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white
[gcc-badge]: https://img.shields.io/badge/GCC-5C6EB8?style=for-the-badge&logo=gnu&logoColor=white
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[ieee-badge]: https://img.shields.io/badge/IEEE-00d77d?style=for-the-badge&logo=ieee&logoColor=white
[ieee-url]: https://www.ieee.org/