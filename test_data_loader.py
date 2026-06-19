from data.histo_data_loader import load_initial_data

df = load_initial_data()

print(df.head())
print(df.shape)
print(df.tail())