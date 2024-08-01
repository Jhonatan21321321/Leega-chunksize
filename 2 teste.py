import pandas as pd

# Caminho do arquivo CSV
filename = 'vendas.csv'

# Leitura do arquivo CSV em chunks para eficiência
chunksize = 450000  # Tamanho do chunk pode ser ajustado conforme necessário
df_chunks = pd.read_csv(filename, chunksize=chunksize)

# Inicializando um DataFrame vazio para acumular resultados
sales_summary = pd.DataFrame()

# Iterando sobre os chunks e agrupando por 'Country' e 'Region' somando 'Units Sold'
for chunk in df_chunks:
    chunk_summary = chunk.groupby(['Country', 'Region'])['Units Sold'].sum().reset_index()
    sales_summary = pd.concat([sales_summary, chunk_summary], ignore_index=True)

# Calculando a soma total de Units Sold por país e por região
total_units_sold_country = sales_summary.groupby('Country')['Units Sold'].sum()
total_units_sold_region = sales_summary.groupby('Region')['Units Sold'].sum()

# Encontrando o país com a maior soma de Units Sold
country_with_max_units_sold = total_units_sold_country.idxmax()
max_units_sold_country = total_units_sold_country.max()

# Encontrando a região com a maior soma de Units Sold
region_with_max_units_sold = total_units_sold_region.idxmax()
max_units_sold_region = total_units_sold_region.max()

# Criando o DataFrame organizado
summary_df = pd.DataFrame([
    {'País': country_with_max_units_sold, 'País Units ': max_units_sold_country,
     'Região': region_with_max_units_sold, 'Região Units': max_units_sold_region}
])

# Exibindo o DataFrame
print(summary_df)
