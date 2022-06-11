import pandas as pd

pd.__version__

df = pd.read_csv("professores_toy.csv", sep=";")

teste = df.iloc[:, 0].dropna().values.tolist()

dic = [{}]

dic[0] = {teste[0]: 0}

print(dic[0])


#print(df)