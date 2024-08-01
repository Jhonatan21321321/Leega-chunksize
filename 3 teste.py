import pandas as pd

# Caminho do arquivo CSV
filename = 'vendas.csv'

# Leitura completa do arquivo CSV em chunks
chunksize = 450000  # Tamanho do chunk pode ser ajustado conforme necessário
df_chunks = pd.read_csv(filename, chunksize=chunksize)

# Inicializando um DataFrame vazio para acumular resultados
sales_summary = pd.DataFrame()

# reforçando os chunks e agrupando por mês e 'Item Type', somando 'Units Sold'
# precisei abaixo resolver um problema de despadronização de datas com formato dd/mm/aaaa e mm/dd/aaaa na coluna Order Date.
for chunk in df_chunks:
    # Verificar o formato predominante das datas
    sample_date = pd.to_datetime(chunk['Order Date'].iloc[0], errors='coerce')
    day_first_format = sample_date.day <= 12  # Verifica se o dia é <= 12 para decidir o formato

    # Converter 'Order Date' para datetime, assumindo dayfirst=True se for o formato correto
    chunk['Order Date'] = pd.to_datetime(chunk['Order Date'], dayfirst=day_first_format, errors='coerce')

    # Agrupar por mês (truncado) e 'Item Type', somando 'Units Sold'
    chunk_summary = chunk.groupby([chunk['Order Date'].dt.to_period('M'), 'Item Type'])['Units Sold'].sum().reset_index()

    # Concatenar com o DataFrame principal
    sales_summary = pd.concat([sales_summary, chunk_summary])

# Renomear colunas
sales_summary.columns = ['Month', 'Item Type', 'Total Units Sold']

# Calcular a média de vendas por produto naquele mês
# Calcular dinamicamente o número de dias no mês
sales_summary['Days in Month'] = sales_summary['Month'].dt.days_in_month

# Calcular a média de vendas por produto naquele mês
sales_summary['Average Units Sold'] = sales_summary['Total Units Sold'] / sales_summary['Days in Month']

# Ordenar por 'Month' de forma descendente (do mais recente para o mais antigo)
sales_summary.sort_values(by='Month', ascending=False, inplace=True)

# Resetar o índice do DataFrame resultante
sales_summary.reset_index(drop=True, inplace=True)

# Exibe uma tabela ordenada por mês mais recente e agrupada.  Gerando uma média de unidades vendidas de produto Mensais.
print(sales_summary[['Month', 'Item Type', 'Total Units Sold', 'Average Units Sold']])
