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
            self.mat_cap = [[0 for j in range(num_vert)] for i in range(num_vert)]

        self.dic = {}
        self.num_turmas = 0
        self.num_professores = 0
        self.num_disciplinas = 0

        # Adciona aresta

    def add_aresta(self, u, v, c, w=0):
        """Adiciona aresta de u a v com capacidade c e peso w"""
        if u < self.num_vert and v < self.num_vert:  # verificando se o vertice que está sendo ligado existe
            self.lista_adj[u].append((v, w, c))
            self.mat_adj[u][v] = [w, c]
            self.num_arestas += 1
            self.mat_cap[u][v] = c
        else:
            print("Aresta invalida!")

    def remove_aresta(self, u, v):
        """Remove aresta de u a v, se houver"""
        if u < self.num_vert and v < self.num_vert:
            if self.mat_adj[u][v] != 0:
                self.num_arestas -= 1
                self.mat_adj[u][v] = [0]
                for (v2, w2, c2) in self.lista_adj[u]:
                    if v2 == v:
                        self.lista_adj[u].remove((v2, w2, c2))
                        break
            else:
                print("Aresta inexistente!")
        else:
            print("Aresta invalida!")

        # Le os arquivos de disciplinas e retorna os dados

    def ler_disciplinas(self, arq_disc):
        print("Lendo arquivo disciplinas...\n")

        df_disc = pd.read_csv(arq_disc, sep=";") #recebe o arquivo

        # PEGA O TOTAL DE TURMAS OFERECIDAS
        lista_de_turmas = df_disc.iloc[:,2].values.tolist()  # Lendo todas as linhas da coluna 2 do arquivo de disciplinas
        self.num_turmas = sum(lista_de_turmas)  # Função soma todos os elementos da lista
        list_disciplinas = df_disc.iloc[:, ].dropna().values.tolist()  # Lendo todas as colunas e linhas do arquivo de discplinas, com execcao dos valores nulos

        return list_disciplinas

    # Tira valores NaN das listas
    def tiranandisciplinas(self, lista_disciplina):
        lista_unica = []
        lista_lixo = []
        for i, item in enumerate(lista_disciplina):  # Para cada indice i item na lista de disciplina
            for j, disciplina in enumerate(item):  # Para cada indice j disciplina no item
                if disciplina in lista_unica:  # Se a disciplina está na lista unica
                    lista_lixo.append(disciplina)  # ela vai para lixo
                elif str(disciplina) != 'nan':  # Se não, se ela for diferente de nan, ela vai para lista unica
                    lista_unica.append(disciplina)

        return lista_unica

    # tira valores NaN das listas de professores
    def tirananprofessores(self, list_professores):
        list_copy = []
        for item in list_professores:  # Para cada item na lista de professores...
            list_copy.append([dado for dado in item if str(dado) != 'nan'])  # Adiciona dados para cada item se os dados forem diferentes de nan

        return list_copy

    # Le o arquivo de professores e retorna o seu conteudo
    def lerprof(self, arq_prof):
        print("Lendo arquivo professores...\n")

        df_prof = pd.read_csv(arq_prof, sep=";") #recebe o arquivo
        lista_testedisciplina = df_prof.iloc[:, [2, 3, 4, 5, 6]].values.tolist()  # Le todas as linhas, e as colunas 2,3,4,5,6 que sao as colunas "preferencias" do arquivo de professores

        lista_disciplina_ofertada = df_prof.iloc[:, 1].values.tolist()  # Le todas as linhas e a couluna 1
        lista_nome_prof = df_prof.iloc[:, 0].values.tolist()  # Le todas as linhas e a coluna 0
        lista_limpa = self.tiranandisciplinas(lista_testedisciplina)  # Tira o nan da lista de disciplinas
        self.num_disciplinas = len(lista_limpa)  # Atualiza o numero de disciplinas
        self.num_professores = len(lista_nome_prof)  # Atualiza o numero de professores

        list_professores = df_prof.iloc[:, ].values.tolist()  # pega todos os dados da lista de professores
        list_professores = self.tirananprofessores(list_professores)  # tira o nan da lista

        return list_professores, lista_nome_prof, lista_disciplina_ofertada  # retorna lista de professores (todos os dados), lista soh com o nome dos professores, e lista de quantidade de disciplinas ofertadas por este prof


    # Implementa a rede da origem aos professores
    def liga_origem_prof(self, list_disciplinas, list_professores):
        origem = self.mat_adj[0]  # Começa do vertice de origem(superoferta)

        copia = [0]  # Para que não haja conexões erradas entre o vertice de origem
        copia = copia + list_disciplinas.copy()  # Copia a lista de disciplinas junto com o zero
        for i in range(0, len(list_professores) + 1):  # Liga a origem a todos os professores
            Destiny = i  # professor destino
            capacidade = copia[i]  # Numero de turmas do professor
            self.add_aresta(origem[i], Destiny, capacidade)  # Ligando a origem ao professor i
            
        #previne que haja laco no vertice 0 (origem)
        self.mat_adj[0][0] = 0
        self.lista_adj[0].pop(0)


    #constroi a rede
    def constroi_rede(self, professores, disciplinas):
        (list_professores, lista_teste, lista_disciplina_ofertada) = self.lerprof(professores)  # Obtendo dados de professores
        list_disciplinas = self.ler_arquivo(disciplinas)  # Obtendo os dados das disciplinas

        self.num_vert = self.num_professores + self.num_disciplinas + 2 #obtem numero de vertices

        # Atualizando listas a partir do numero de vertices obtido
        self.mat_adj = [[0 for j in range(self.num_vert)] for i in range(self.num_vert)]  
        self.mat_cap = [[0 for j in range(self.num_vert)] for i in range(self.num_vert)] 
        self.lista_adj = [[] for i in range(self.num_vert)]

        self.liga_origem_prof(lista_disciplina_ofertada, lista_teste)  # Atualiza a rede da origem dos professores
        self.implementa_destino(list_disciplinas)  # Atualiza a rede das discplinas ao destino
        self.preenche_dicionario(list_professores, list_disciplinas)  # Preenche o dicionario
        self.liga_prof_disciplina()  # Atualiza a rede professores para disciplinas
        

    # Implementa a rede das disciplinas ao vertice de demanda (destino)
    def implementa_destino(self, disciplinas):
        list_capacidade = []  # Define a capacidade como vazio
        for disciplina in disciplinas:
            list_capacidade.append(disciplina[2])  # Adciona as capacidades na lista ([2] para pegar quantas turmas que cada disciplina tem que ter)
        for i in range(self.num_professores + 1, self.num_vert - 1):  # Liga as dicsiplinas ao superdemanda
            for capacidade in list_capacidade:  # Atualiza as capacidades
                capacidade_disciplina = capacidade
                list_capacidade.remove(capacidade)
                break
            self.add_aresta(i, self.num_vert - 1, capacidade_disciplina)


    # liga os professores as disciplinas
    def liga_prof_disciplina(self):
        custo = [0, 3, 5, 8, 10]  # dita o custo conforme o pedido no trabalho (preferencia 1 = custo 0, preferencia 2 = custo 3...)

        for i in range(0, self.num_professores):
            professor = self.dic[i + 1]

            for j in range(self.num_professores + 1, self.num_vert - 1):  # começa o for da poisção 2 até o final das disciplinas,
                for k in range(2, len(professor)):  # guarda o indice de cada diciplina no k e se essa disciplina for ofertada pelo professor uma ligação
                    disciplinas = professor[2:len(professor)]  # Disciplinas é um subvetor que contém somente as disiplinas do professor
                    # vet porf de 2 pra frente = disicplinas pra saber qual o ultimo indice = tam vetor, logo de 2 até len professor terá todas as disciplinas do professor.

                    if professor[k] in self.dic[j]:
                        id = professor[k]  # pega o codigo da disciplina
                        if id == 'CSI000': #bloco que impede professor de pegar mais de uma eletiva ao fazer a capacidade = 1
                            self.add_aresta(i + 1, j, 1, custo[disciplinas.index(id)])
                        else:
                            self.add_aresta(i + 1, j, 2, custo[disciplinas.index(id)]) # pega o custo(disciplina no indice da displcina encontrada)
                        # pega a preferencia da disciplina e faz a aresta com base no custo da preferencia da mesma.

    # Preenche o discionario
    def preenche_dicionario(self, professores, disciplinas):
        self.dic[0] = "SUPER-OFERTA", "SUPER-OFERTA", "SUPER-OFERTA", "SUPER-OFERTA", "SUPER-OFERTA" # indice 0 vai ser o super oferta (origem)
        for i in range(0, len(professores)):  # Adciona os vertices de professores no dicionario
            self.dic[i + 1] = professores[i]  # começando do 1 pois o 0 é superoferta

        for j in range(len(professores), self.num_vert - 1):  # Adiciona os vertices de disciplinas no dicionario
            for i, disciplina in enumerate(disciplinas):  # Para cada indice e diciplina na lista displina atualiza a mesma
                self.dic[j + 1] = disciplinas[i]
                disciplinas.remove(disciplina)
                break
    
    #bellman-ford adaptado do trab 1
    def bellman_ford(self, s, t):
        """Obtem o caminho minimo de s para todos os vertice do grafo (no contexto de redes, nos importa apenas s a t"""
        dist = [float('inf') for v in range(self.num_vert)]  # Inicializa vetor dist com infinito em cada pos.
        pred = [None for v in range(self.num_vert)]  # Inicializa vetor pred com None em cada pos.
        dist[s] = 0  # Distancia para origem eh 0
        E = []  #lista de aresta (u, v), custo c, capacidade w)

        for i in range(len(self.lista_adj)):
            for j in range(len(self.lista_adj[i])):
                E.append((i, self.lista_adj[i][j][0], self.lista_adj[i][j][1], self.mat_cap[i][self.lista_adj[i][j][0]])) #atribui (u, v), custo c, capacidade w)

        # Laco principal
        for i in range(self.num_vert - 1):  # Percorremos todas os vertices do grafo
            trocou = False  # Flag para encerrar o algoritmo mais cedo, salvando custos
            for (u, v, w, c) in E:  # Percorremos todas as arestas dos vertices do grafo
                if c == 0:  # anteriormente self.mat_cap[u][v]
                    E.remove((u, v, w, c))
                    self.remove_aresta(u, v)

                if dist[v] > dist[u] + w:  # Se encontrar um caminho melhor atraves de determinada aresta...
                    dist[v] = dist[u] + w
                    pred[v] = u
                    trocou = True  # Atualiza flag, sinalizando que houve troca

        # obtendo caminho
        caminho = [t]
        x = t
        while x != s:  # Itera ate encontrar a origem, assim obtendo todo o caminho
            if x is None:
                break
            x = pred[x]
            caminho.append(x)
        # Inverte o caminho encontrado anteriormente, pois a ordem do vetor pred eh inversa
        caminho.reverse()

        if trocou == False:  # Se percorremos todo os vertices/arestas e nao houve troca, significa que podemos encerrar o algoritmo
            for i in range(len(caminho)): #percorre caminho para verificar quando retornar caminho vazio para o SCM
                if len(caminho) <= 1:
                    return []
                elif caminho[i] == None:
                    return []
                else:
                    return caminho

    def scm(self, s, t):  # nao recebemos c como o codigo padrao pq a classe ja possui uma matriz de capacidades
        # bloco para corrigir o int is not subscriptable, porque a matriz anteriormente possuia alguns indices que nao eram uma lista
        for i in range(self.num_vert):
            for j in range(self.num_vert):
                if type(self.mat_adj[i][j]) is int:
                    self.mat_adj[i][j] = [self.mat_adj[i][j]]

        b = [0 for _ in range(self.num_vert)]  # vetor de fluxos (b[0] = total de fluxo passado no indice 0...)
        b[0] = self.num_turmas
        b[self.num_vert - 1] = -self.num_turmas
        F = [[0 for i in range(self.num_vert)] for i in range(self.num_vert)]
        C = self.bellman_ford(s, t)  # C = Caminho mínimo

        while len(C) != 0 and b[s] != 0:  # enquanto houver caminho de S a T e ainda houver fluxo a ser enviado (b[s]!=0)
            f = float('inf')
            for i in range(1, len(C)):  # encontra o gargalo, que sera = f que e o total de fluxo a ser enviado
                u = C[i - 1]
                v = C[i]
                if self.mat_cap[u][v] < f:
                    f = self.mat_cap[u][v]
            for i in range(1, len(C)):
                u = C[i - 1]
                v = C[i]
                F[u][v] += f
                self.mat_cap[u][v] -= f
                self.mat_cap[v][u] += f
                if self.mat_cap[u][v] == 0:  # se a capacidade da aresta u, v for = 0, remova
                    self.mat_adj[u][v] = [0]  # aresta u v eh removida da matriz de adj
                    self.remove_aresta(u, v)
                if self.mat_adj[v][u] == 0:  # checa se a aresta reversa existe
                    self.mat_adj[v][u] = 1
                    self.add_aresta(v, u, float('inf'), -self.mat_adj[u][v][0])
                if self.mat_cap[v][u] != 0:
                    self.mat_cap[v][u] -= f
            b[s] -= f
            b[t] += f
            C = self.bellman_ford(s, t)
        return F

    def imprime_dados(self, arq_prof, arq_disc,  F, dic):
        #obtem lista de professores (nome)
        df_prof = pd.read_csv(arq_prof, sep=";")
        professores = df_prof.iloc[:, [0]].values.tolist()

        #obtem lista de disciplinas (nome)
        df_disc = pd.read_csv(arq_disc, sep=";")
        disciplinas = df_disc.iloc[:, [0, 1]].values.tolist()
        
        aux_vet = [] #vetor auxiliar para corrigir repeticoes

        #imprime dados
        for l in range(len(F[0])-1):
            for p in professores:
                if dic[l][0] == p[0]:
                    for y in range(len(F[0])-1):
                        for d in disciplinas:
                            if dic[y][0] == d[0]:
                                if F[l][y] != 0:
                                    if (p, d, F[l][y]) not in aux_vet:
                                        aux_vet.append((p, d, F[l][y]))
                                        print(p, d, F[l][y], end='')
                                        if d[0] in df_prof.iloc[:, 2].values.tolist():
                                            print(" ", F[l][y]*0)
                                        elif d[0] in df_prof.iloc[:, 3].values.tolist():
                                            print(" ", F[l][y]*3)
                                        elif d[0] in df_prof.iloc[:, 4].values.tolist():
                                            print(" ", F[l][y]*5)
                                        elif d[0] in df_prof.iloc[:, 5].values.tolist():
                                            print(" ", F[l][y]*8)
                                        else:
                                            print(" ", F[l][y]*10)