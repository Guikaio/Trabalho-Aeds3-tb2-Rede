import network

rede = network.Rede()

rede.teste("professores_toy.csv","disciplinas_toy.csv")
print(rede.lista_adj)
print("................................")
print(rede.mat_adj)
#print(f"-----BELLMAN FORD------{rede.bellman_ford(0, rede.num_vert-1)}")
#print("MATRIZ:\n", rede.mat_adj)
#print("LISTA:\n", rede.lista_adj)
#rede.teste("disciplinas_toy.csv","professores_toy.csv")