import network

rede = network.Rede()

print("MENU")
escolha = int(input("Digite o numero correspondendo a qual arquivo quer usar:\n1 - toy\n2 - padrao\n"))
while (True):
    if escolha == 1:
        rede.constroi_rede("professores_toy.csv","disciplinas_toy.csv")
        print(rede.imprime_dados("professores_toy.csv", "disciplinas_toy.csv", rede.scm(0, rede.num_vert-1), rede.dic))
        break
    elif escolha == 2:
        rede.constroi_rede("professores.csv","disciplinas.csv")
        print(rede.imprime_dados("professores.csv", "disciplinas.csv", rede.scm(0, rede.num_vert-1), rede.dic))
        break
    else:
        print("Valor invalido")
print("Fim do programa!")