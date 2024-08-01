import pandas as pd
import psutil
import time

# Função para ler e processar o arquivo CSV com chunking
def read_and_process_csv(filename, chunksize):
    # Função para obter o uso de memória atual
    def get_memory_usage():
        process = psutil.Process()
        return process.memory_info().rss

    # Obter uso de memória antes da leitura do arquivo
    memory_before = get_memory_usage()

    # Inicializar um contador para controlar o número total de linhas lidas
    total_rows = 0

    # Obter o tempo antes de iniciar a leitura do arquivo
    start_time = time.time()

    # Iterar sobre os chunks do arquivo CSV
    for chunk in pd.read_csv(filename, chunksize=chunksize):
        # Atualizar o contador de linhas
        total_rows += len(chunk)

        # Processar o DataFrame (apenas imprimir o tamanho)
        print(chunk.shape)

    # Obter o tempo após a leitura do arquivo
    end_time = time.time()

    # Obter uso de memória após a leitura do arquivo
    memory_after = get_memory_usage()

    # Calcular memória usada durante a leitura do arquivo (em bytes)
    memory_used = memory_after - memory_before

    # Converter bytes para megabytes (MiB)
    memory_used_mib = memory_used / (1024 * 1024)

    # Calcular o tempo de execução
    execution_time = end_time - start_time

    print(f"Memória usada durante a leitura do arquivo: {memory_used_mib:.2f} MiB")
    print(f"Tempo de execução: {execution_time:.2f} segundos")
    print(f"Total de linhas processadas: {total_rows}")

# Caminho do arquivo
filename = 'vendas.csv'

# Tamanho do chunk para leitura
chunksize = 450000  # ajustar o tamanho do chunk conforme necessário e testar. o desempenho pode depender da capacidade de memória disponível

# Chamada da função para ler e processar o arquivo CSV
read_and_process_csv(filename, chunksize)