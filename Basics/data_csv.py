import pandas as pd
import matplotlib.pyplot as pl

csv_file = "/Users/patelshivam/Documents/PythonLab/Advance Python/Basics/electronic-card-transactions-june-2024-csv-tables.xlsx.csv"
a = [1,2,3,4,5]
b = [10,20,30,40,50]

df = pd.read_csv(csv_file)



print(df.head(4))
pl.plot(a,b)
