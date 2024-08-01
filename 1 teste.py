import pandas as pd

# Caminho do arquivo CSV
filename = 'vendas.csv'

# Leitura do arquivo CSV em chunks de tamanho 450000
chunk_size = 450000 # Tamanho do chunk pode ser ajustado conforme necessário
chunks = pd.read_csv(filename, chunksize=chunk_size)

# Inicializando um DataFrame vazio para acumular os resultados
df = pd.DataFrame()

# Iterando sobre os chunks e acumulando no DataFrame final
for chunk in chunks:
    df = pd.concat([df, chunk])


# Agrupamento por 'Canal de vendas' e 'Tipo de item', somando 'Unidades vendidas'
sales_summary = df.groupby(['Sales Channel', 'Item Type'])['Units Sold'].sum().reset_index()

# Encontrando o 'Tipo de item' com mais 'Unidades vendidas' por 'Canal de vendas'
idx = sales_summary.groupby('Sales Channel')['Units Sold'].transform('max') == sales_summary['Units Sold']
top_items = sales_summary[idx]

# Exibindo o 'item' com mais 'Unidades vendidas' em cada 'Canal de vendas'
print(top_items[['Sales Channel', 'Item Type', 'Units Sold']])

