import os
def main():
    # exectar os comandos do sistema

    # python3 src/data_preprocessing.py
    os.system('python3 src/data_preprocessing.py')

    # python3 src/modeling_data.py
    os.system('python3 src/modeling_data.py')

    # python3 src/modeling_graph.py
    os.system('python3 src/modeling_graph.py')

if __name__ == '__main__':
    main()
