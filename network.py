import pandas as pd


class Rede:
    def __init__(self, num_vert=0, num_arestas=0, lista_adj=None, mat_adj=None, mat_cap=None):
        self.num_vert = num_vert
        self.num_arestas = num_arestas
        if lista_adj is None:
            self.lista_adj = [[] for i in range(num_vert)]
        else:
            self.lista_adj = lista_adj
        if mat_adj is None:
            self.mat_adj = [[0 for _ in range(num_vert)] for _ in range(num_vert)]
        if mat_cap is None:
            self.mat_cap = [[None for j in range(num_vert)] for i in range(num_vert)]

        self.dic = {}
        self.num_turmas = 0
        self.num_professores = 0
        self.num_disciplinas = 0
    def add_aresta(self, u, v, c, w=0):
        """Adiciona aresta de u a v com capacidade c e peso w"""

        if u < self.num_vert and v < self.num_vert:
            self.lista_adj[u].append((v, w, c))
            self.mat_adj[u][v] = [w, c]
            self.num_arestas += 1
        else:
            print("Aresta invalida!")

    def ler_arquivo(self, arq_disc):
        print("Lendo arquivo...\n")

        df_disc = pd.read_csv(arq_disc, sep=";")
        print(df_disc.to_string())
        lista_teste = df_disc.iloc[:, 0].values.tolist()
        print(lista_teste)
        self.num_professores = len(lista_teste)
        print("\ntotal de disciplinas = ", self.num_disciplinas, "\n")

        # PEGA O TOTAL DE TURMAS OFERECIDAS
        num_turmas = 0
        lista_de_turmas = df_disc.iloc[:, 2].values.tolist()
        self.num_turmas = sum(lista_de_turmas)  # Função soma todos os elementos da lista
        print(self.num_turmas)
        list_disciplinas = df_disc.iloc[:, ].dropna().values.tolist()

        return list_disciplinas
    def tiranan(self, lista_disciplina):
        lista_unica = []
        for i, item in enumerate(lista_disciplina):  # indice e item = valor interno
            for j, disciplina in enumerate(item):
                if disciplina == "nan":
                    lista_disciplina.remove(disciplina)
                if disciplina in lista_unica:
                    break
                else:
                    lista_unica.append(disciplina)

        return lista_unica

    def lerprof(self, arq_prof):

        print("Lendo arquivo...\n")

        df_prof = pd.read_csv(arq_prof, sep=";")
        print(df_prof.to_string())
        lista_testedisciplina = df_prof.iloc[:, [2, 3, 4, 5]].values.tolist()

        lista_disciplina_ofertada = df_prof.iloc[:, 1].values.tolist()
        lista_teste = df_prof.iloc[:, 0].values.tolist()
        lista_limpa = self.tiranan(lista_testedisciplina)
        self.num_disciplinas = len(lista_limpa)
        self.num_professores = len(lista_teste)
        print("\ntotal de professores = ", self.num_professores, "\n")

        list_professores = df_prof.iloc[:, ].dropna().values.tolist()
        print(f"antes do retorno{lista_teste}")
        return list_professores, lista_teste, lista_disciplina_ofertada
    def implementarede(self, list_disciplinas, list_professores):
        # Começando da origem para cada prof, criando vert e origem
        origem = self.mat_adj[0]

        copia = [0]  # Para o vertice de origem não fazer ligações usando dados dos vertices subsequentes
        copia = copia + list_disciplinas.copy()
        print(list_professores)
        print(list_disciplinas)
        for i in range(0, len(list_professores) + 1):
            Destiny = i
            capacidade = copia[i]
            self.add_aresta(origem[i], Destiny, capacidade)  # ligando vertice 0 ao vertice i

    def teste(self, professores, disciplinas):
        (list_professores, lista_teste, lista_disciplina_ofertada) = self.lerprof(professores)
        list_disciplinas = self.ler_arquivo(disciplinas)

        self.num_vert = self.num_professores + self.num_disciplinas + 2
        self.mat_adj = [[0 for j in range(self.num_vert)] for i in
                        range(self.num_vert)]  # Atualizando matrix atrvés dos num de vert obtidos

        self.mat_cap = [[None for j in range(self.num_vert)] for i in range(self.num_vert)]
        self.lista_adj = [[] for i in range(self.num_vert)]
        self.implementarede(lista_disciplina_ofertada, lista_teste)