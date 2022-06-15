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


        #Adciona aresta
    def add_aresta(self, u, v, c, w=0):
        """Adiciona aresta de u a v com capacidade c e peso w"""

        if u < self.num_vert and v < self.num_vert:  #verificando se o vertice que está sendo ligado existe
            self.lista_adj[u].append((v, w, c))
            self.mat_adj[u][v] = [w, c]
            self.num_arestas += 1
        else:
            print("Aresta invalida!")



        #Le os arquivos de disciplinas e retorna os dados
    def ler_arquivo(self, arq_disc):
        print("Lendo arquivo...\n")

        df_disc = pd.read_csv(arq_disc, sep=";")
        print(df_disc.to_string())
        lista_teste = df_disc.iloc[:, 0].values.tolist() #Lendo todas as linhas da coluna 0 do arquivo de disciplinas
        print(lista_teste)
        print("\ntotal de disciplinas = ", self.num_disciplinas, "\n")

        # PEGA O TOTAL DE TURMAS OFERECIDAS
        num_turmas = 0
        lista_de_turmas = df_disc.iloc[:, 2].values.tolist() #Lendo todas as linhas da coluna 2 do arquivo de disciplinas
        self.num_turmas = sum(lista_de_turmas)  # Função soma todos os elementos da lista
        print(self.num_turmas)
        list_disciplinas = df_disc.iloc[:, ].dropna().values.tolist() #Lendo todas as colunas e linhas do arquivo de discplinas

        return list_disciplinas




        #Tira valores NaN das listas
    def tiranan(self, lista_disciplina):
        lista_unica = []
        lista_lixo = []
        for i, item in enumerate(lista_disciplina):    #Para cada indice i item na lista de disciplina
            for j, disciplina in enumerate(item):      #Para cada indice j disciplina no item
                if disciplina in lista_unica:          #Se a disciplina está na lista unica
                    lista_lixo.append(disciplina)      #ela vai para lixo
                elif str(disciplina) != 'nan':         #Se não, se ela for diferente de nan, ela vai para lista unica
                    lista_unica.append(disciplina)

        return lista_unica



        #tira valores NaN das listas de professores
    def tirananprofessores(self, list_professores):
        list_copy = []
        for i, item in enumerate(list_professores):  #Para cada indice i e item na lista de professores
            list_copy.append(
                [dado for dado in item if str(dado) != 'nan'])  #Adiciona dados para cada item se os dados forem diferentes de nan

        return list_copy




        #Le o arquivo de professores e retorna o seu conteudo
    def lerprof(self, arq_prof):

        print("Lendo arquivo...\n")

        df_prof = pd.read_csv(arq_prof, sep=";")
        print(df_prof.to_string())
        lista_testedisciplina = df_prof.iloc[:, [2, 3, 4, 5]].values.tolist() #Le todas as linhas e as colunas 2,3,4,5

        lista_disciplina_ofertada = df_prof.iloc[:, 1].values.tolist() #Le todas as linhas e a couluna 1
        lista_teste = df_prof.iloc[:, 0].values.tolist()  #Le todas as linhas e a coluna 0
        lista_limpa = self.tiranan(lista_testedisciplina) #Tira o nan da lista de disciplinas
        self.num_disciplinas = len(lista_limpa)   #Atualiza o numero de disciplinas
        self.num_professores = len(lista_teste)    #Atualiza o numero de professores
        print("\ntotal de professores = ", self.num_professores, "\n")

        list_professores = df_prof.iloc[:,].values.tolist()  #pega todos os dados da lista de professores
        list_professores = self.tirananprofessores(list_professores)  #tira o nan da lista
        print(f"antes do retorno{lista_teste}")
        return list_professores, lista_teste, lista_disciplina_ofertada #retorna lista de professores, teste, e list disciplinas




        #Implementa a rede da origem aos professores
    def implementarede(self, list_disciplinas, list_professores):
        origem = self.mat_adj[0] #Começa do vertice de origem(superoferta)

        copia = [0]  # Para que não haja conexões errada entre o vertice de origem
        copia = copia + list_disciplinas.copy() #Copia a lista de disciplinas junto com o zero
        for i in range(0, len(list_professores) + 1): #Liga a origem a todos os professores
            Destiny = i #professor destino
            capacidade = copia[i] #Numero de turmas do professor
            self.add_aresta(origem[i], Destiny, capacidade)  #Ligando a origem ao professor i



        #Testa as funções que foram criadas
    def teste(self, professores, disciplinas):
        (list_professores, lista_teste, lista_disciplina_ofertada) = self.lerprof(professores) #Obtendo dados de professores
        list_disciplinas = self.ler_arquivo(disciplinas)  #Obtendo os dados das disciplinas

        self.num_vert = self.num_professores + self.num_disciplinas + 2
        self.mat_adj = [[0 for j in range(self.num_vert)] for i in
                        range(self.num_vert)]  # Atualizando matrix atrvés dos num de vert obtidos

        self.mat_cap = [[None for j in range(self.num_vert)] for i in range(self.num_vert)]
        self.lista_adj = [[] for i in range(self.num_vert)] #Atualizando as estrturas
        self.implementarede(lista_disciplina_ofertada, lista_teste)  #Atualiza a rede da origem dos professores
        self.implementaDestiny(list_disciplinas) #Atualiza a rede das discplinas ao destino
        self.preenchediscionary(list_professores, list_disciplinas) #Preenche o dicionario
        self.ligaprof()  #Atualiza a rede professores para disciplinas
        print("teste")



        #Implementa a rede das disciplinas ao vertice de demanda
    def implementaDestiny(self,disciplinas):
     list_capacidade = []  #Define a capacidade como vazio
     for disciplina in disciplinas:
         list_capacidade.append(disciplina[2]) #Adciona as capacidades na lista
     print(list_capacidade)
     for i in range(self.num_professores+1,self.num_vert-1): #Liga as dicsiplinas ao superdemanda
         for capacidade in list_capacidade: #Atualiza as capacidades
             capacidade_disciplina = capacidade
             list_capacidade.remove(capacidade)
             break

         self.add_aresta(i,self.num_vert-1,capacidade_disciplina)




         #Preenche o discionario
    def preenchediscionary(self,professores,disciplinas):
         for i in range(0,len(professores)): #Adciona os vertices de professores no dicionario
             self.dic[i+1] = professores[i]#começando do 1 pois o 0 é superoferta

         for j in range(len(professores),self.num_vert-1):  #Adiciona os vertices de disciplinas no dicionario
             for i, disciplina in enumerate(disciplinas): #Para cada indice e diciplina na lista displina atualiza a mesma
                self.dic[j+1] = disciplinas[i]
                disciplinas.remove(disciplina)
                break




    # liga os professores as disciplinas
    def ligaprof(self):
        custo = [0, 3, 5, 8, 10]  # para saber qual é o custo de cada aresta

        for i in range(0, self.num_professores):
            professor = self.dic[i + 1]

            for j in range(self.num_professores + 1, self.num_vert - 1): #começa o for da poisção 2 até o final das disciplinas,
                for k in range(2, len(professor)):  # guarda o indice de cada diciplina no k e se essa disciplina for ofertada pelo professor uma ligação
                    disciplinas = professor[2:len(professor)] #Disciplinas é um subvetor que contém somente as disiplinas do professor
                    #vet porf de 2 pra frente = disicplinas pra saber qual o ultimo indice = tam vetor, logo de 2 até len professor terá todas as disciplinas do professor.

                    if professor[k] in self.dic[j]:
                        id = professor[k]   #pega o codigo da disciplina
                        self.add_aresta(i + 1, j, self.dic[j][2], custo[disciplinas.index(id)]) #pega o custo(disciplina no indice da displcina encontrada)
                        # pega a preferencia da disciplina e faz a aresta com base no custo da preferencia da mesma.




    def bellman_ford(self, s, t):
        """Obtem o caminho minimo de s para todos os vertices do grafo (funciona para grafos com arestas negativas)."""
        dist = [float('inf') for v in range(self.num_vert)]  # Inicializa vetor dist com infinito em cada pos.
        pred = [None for v in range(self.num_vert)]  # Inicializa vetor pred com None em cada pos.
        dist[s] = 0  # Distancia para origem eh 0
        E = [(None, None, None, None) for x in range(
            self.num_arestas)]  # Inicializa uma lista de tuplas que contera as arestas e seus respectivos pesos. indice[0][1] possuem as arestas e o [2] o peso
        x = 0  # Variavel auxiliar para ajudar a atribuir valores na lista E

        for i in range(len(self.lista_adj)):
            for j in range(len(self.lista_adj[i])):
                print("-----------E------------", E)
                E[x] = (i, self.lista_adj[i][j][0], self.lista_adj[i][j][1], self.lista_adj[i][j][2])
                x = x + 1

        # Laco principal
        for i in range(self.num_vert - 1):  # Percorremos todas os vertices do grafo
            trocou = False  # Flag para encerrar o algoritmo mais cedo, salvando custos
            for (u, v, w) in E:  # Percorremos todas as arestas dos vertices do grafo
                if dist[v] > dist[u] + w:  # Se encontrar um caminho melhor atraves de determinada aresta...
                    dist[v] = dist[u] + w
                    pred[v] = u
                    trocou = True  # Atualiza flag, sinalizando que houve troca

        # obtendo caminho
        caminho = [t]
        x = t
        # Itera ate encontrar a origem, assim obtendo todo o caminho
        while x != s:
            x = pred[x]
            caminho.append(x)
        # Inverte o caminho encontrado anteriormente, pois a ordem do vetor pred eh inversa
        caminho.reverse()

        if trocou == False:  # Se percorremos todo os vertices/arestas e nao houve troca, significa que podemos encerrar o algoritmo
            return caminho











