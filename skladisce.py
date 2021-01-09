import itertools
import copy
from graf import Graph
import collections
import sys
import math


'''
NxP_start = [
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['B', '', '', '', ''],
    ['A', 'C', 'D', 'E', 'F']
]

NxP_end = [
    ['', 'C', '', '', ''],
    ['', 'E', '', '', ''],
    ['F', 'D', '', '', ''],
    ['B', 'A', '', '', '']
]

NxP_start = [
    ['', '', ''],
    ['', '', ''],
    ['A', 'B', 'C']
]


NxP_end = [
    ['A', '', ''],
    ['B', '', ''],
    ['C', '', '']
]

NxP_start = [
    ['B', '', ''],
    ['A', '', '']
]

NxP_end = [
    ['', 'B', ''],
    ['', 'A', '']
]


NxP_start = [
    ['', '', '', ''],
    ['E', 'F', '', ''],
    ['A', 'C', 'D', 'B']
]

NxP_end = [
    ['', '', '', ''],
    ['D', 'E', '', 'C'],
    ['B', 'A', '', 'F']
]
'''

NxP_start = [
    ['B','D','F','',''],
    ['A','C','E','','']
]

NxP_end = [
    ['A','C','E','',''],
    ['B','D','F','','']

]

N = len(NxP_start)
P = len(NxP_start[N - 1])
st_obiskanih_vozlisc = 0

# P - odstavnih polozajev
# N - velikih skatelj ena na drugo

# p => 1 <= p <= P
# r => 1 <= r <= P

def prestavi(p, r, matrika1):
    matrika = matrika1[:]

    first_element = ''
    delete_i = -1
    delete_p_1 = -1

    # ce je p, r return matriko
    if p == r:
        return matrika
    # dokler nenajdes nepraznega in ga shranis v first_element
    for i in range(0, N):
        if matrika[i][p - 1] != '':
            first_element = matrika[i][p - 1]
            delete_i = i
            delete_p_1 = p - 1
            break
    # dokler nenajdes prvega praznega od spodi navzgor in shranis element iz
    # first_element v ta prostor in zbrises element iz kordinati i in p-1
    for j in range(N - 1, -1, -1):
        if matrika[j][r - 1] == '':
            matrika[j][r - 1] = first_element
            if delete_i > -1 and delete_p_1 > -1:
                matrika[delete_i][delete_p_1] = ''
            break

    return matrika


def izpis(NxP):
    for a in NxP:
        print(a)


# for dict key = tuple
def tuple_to_list(t):
    return [list(i) for i in t]


def list_to_tuple(l):
    t = tuple()
    for i in l:
        t += tuple(i),
    return t


def naredi_matriko(matrika):
    return [list(i) for i in matrika]


def napolni(graf, start_m):
    start = list_to_tuple(start_m)
    for p in range(1, P + 1):
        for r in range(1, P + 1):
            kopija = naredi_matriko(start_m)
            x = prestavi(p, r, kopija)
            tuple_x = list_to_tuple(x)
            if tuple_x != start:
                graf.add(start, tuple_x)
                graf.addPremik(start, tuple_x, (p, r))


def BFS(graf, root):
    oce_od_elementa = collections.defaultdict(tuple)

    vrsta = []

    seen = set()

    # dodam root
    vrsta.append(list_to_tuple(root))
    seen.add(str(root))
    # kopija = naredi_matriko(root) #kopija start

    napolni(graf, root)
    stevilo_pregledanih_vozlisc = 1
    while vrsta:

        vozlisce = vrsta.pop(0)

        for neighbour in graf.get(vozlisce):
            if str(neighbour) not in seen:
                stevilo_pregledanih_vozlisc += 1
                oce_od_elementa[(neighbour)] = (vozlisce)
                napolni(graf, neighbour)
                vrsta.append(neighbour)
                seen.add(str(neighbour))
                if tuple_to_list(neighbour) == NxP_end:
                    print("Stevilo pregledanih vozlisc:", stevilo_pregledanih_vozlisc)
                    return find_path(graf, neighbour, oce_od_elementa)


def stolpci_s_skatlo(matrika):
    stolpci = set()
    for vrstica in matrika:
        i = 1
        for pod in vrstica:
            if pod != "":
                stolpci.add(i)
            i += 1

    return stolpci


def stolpci_s_prostorom(matrika):
    stolpci = set()
    vrstica = matrika[0]
    i = 1
    for pod in vrstica:
        if pod == "" or pod == " ":
            stolpci.add(i)
        i += 1

    return stolpci


def mozni_premiki(matrika): #vrne set tuplov moznih premikov
    moznosti = set()
    for a in stolpci_s_skatlo(matrika):
        for b in stolpci_s_prostorom(matrika):
            if a != b:
                moznosti.add((a, b))
    return moznosti

def IDS(max_globina, start_matrika, end_matrika):
    globina = 0

    while globina < max_globina:
        for premik in mozni_premiki(start_matrika):
            output = dls(globina, prestavi(premik[0], premik[1], copy.deepcopy(start_matrika)), end_matrika, premik)
            if output:
                break
        if output:
            break
        globina += 1

    return list(reversed(output))



def dls(max_globina, start_matrika, end_matrika, parent_premik):
    global st_obiskanih_vozlisc
    if max_globina == 0:
        if start_matrika == end_matrika:
            return [parent_premik]
        else:
            return None
    elif max_globina > 0:
        for premik in mozni_premiki(start_matrika):
            st_obiskanih_vozlisc += 1
            cur_matrika = prestavi(premik[0], premik[1], copy.deepcopy(start_matrika))
            neki = dls(max_globina-1, cur_matrika, end_matrika, premik)
            if neki:
                poped = neki.pop()
                if poped == premik:
                    neki.append(premik)
                    neki.append(parent_premik)
                    return neki


def find_path(graf, neighbour, oce_sin_dict):
    path = [neighbour]
    while neighbour != list_to_tuple(NxP_start):
        neighbour = oce_sin_dict[neighbour]
        path.append(neighbour)
    path = path[::-1]  # obrnem
    premiki = []
    i = 0
    j = 1
    while i < len(path) - 1 and j < len(path):
        premiki.append(graf.getPremik(path[i], path[j]))
        i += 1
        j += 1
    print("Max globina:", len(path) - 1)
    return "Pot: " + str(premiki)


def get_matrike(start, end):  # če podas 0 ,0 kot argument hoce poti iz System.in drgace podas absolutne poti do start matrike file in end matrike file vrne ti matrike
    if start == 0:
        start_path = input("Input start matrix path \n")
    start_path = start
    f = open(start_path, "r")
    start_matrika = []

    for x in f:
        vrstica = (x.replace("'", "").replace("\n", "").replace(" ", "").split(","))
        start_matrika.append(vrstica)
    f.close()
    if end == 0:
        end_path = input("Input end matrix path \n")
    end_path = end
    f = open(end_path, "r")
    end_matrika = []

    for x in f:
        vrstica = (x.replace("'", "").replace("\n", "").replace(" ", "").split(","))
        end_matrika.append(vrstica)
    f.close()
    return start_matrika,end_matrika


def izrisi_pot(start, end, pot):
    print("Start matrika:")
    izpis(start)
    print()
    for premik in pot:
        print("Premik", premik)
        iz, v = premik
        prestavi(iz,v,start)
        izpis(start)
    print()
    print("End matrika:")
    izpis(end)


def lep_izpis_ids():
    start_m, end_m = get_matrike("D:\\Python\\UI_sem_2\\primer1_zacetna.txt",  # ce podas 0, 0 bo hotu iz system.in
                                 "D:\\Python\\UI_sem_2\\primer1_koncna.txt")
    pot = IDS(10, start_m, end_m)
    print("Start matrika:")
    izpis(start_m)
    print("End matrika:")
    izpis(end_m)
    print("\nPot:")
    print(pot)
    print("Število obiskanih vozlisc", st_obiskanih_vozlisc)
    print()
    izrisi_pot(copy.deepcopy(start_m), copy.deepcopy(end_m), pot)

lep_izpis_ids()



def pitagorov_izrek(x1, y1, x2, y2):
    return int(math.sqrt(abs(x2 - x1) + abs(y2 - y1)))

def get_distacne(element, end):
    for y in range(len(end)):
        for x in range(len(end[y])):
            if end[y][x] != '':
                if element == end[y][x]:
                    return x, y
#formula za hevristiko
def eucledian_distance(now, end):
    sum = 0
    for y in range(len(now)):
        for x in range(len(now[y])):
            if now[y][x] != '':
                x2, y2 = get_distacne(now[y][x], end)
                sum += pitagorov_izrek(x, y, x2, y2)
    return sum

def distance(now, end):
    sum = 0
    for y in range(len(now)):
        for x in range(len(now[y])):
            if now[y][x] != '':
                x2, y2 = get_distacne(now[y][x], end)
                sum += pitagorov_izrek(x, y, x2, y2)
    return sum

def min_value_dict(vrsta, f_score_dict): #returns tuple
    min = sys.maxsize
    min_element = tuple()

    for ele in vrsta:
        ele_t = list_to_tuple(ele)
        if min > f_score_dict[ele_t]:
            min = f_score_dict[ele_t]
            min_element = ele_t
    return min_element

def A_star(graf, root):

    queue = [list_to_tuple(root)]

    seen = set()

    oce_od_elementa = collections.defaultdict(tuple)

    g_score = collections.defaultdict(int)
    g_score[list_to_tuple(root)] = 0

    f_score = collections.defaultdict(int)
    f_score[list_to_tuple(root)] = eucledian_distance(root, NxP_end)

    napolni(graf, root)    #napolni vse moznosti iz root-a

    seen.add(str(root))

    while queue:

        current = min_value_dict(queue, f_score)   #get lowest score in f_score dict

        if current == list_to_tuple(NxP_end):
            return current

        queue.remove(current)


        for neighbour in graf.get(current):
            if neighbour not in seen:
                #dodam soseda v g_score z max value
                g_score[neighbour] = sys.maxsize

                zacasen_g_score = g_score[list_to_tuple(current)] + distance(current, neighbour)

                seen.add(str(neighbour))

                if zacasen_g_score < g_score[neighbour]:


                    g_score[neighbour] = zacasen_g_score
                    f_score[neighbour] = g_score[neighbour] + eucledian_distance(current, NxP_end)
                    #dodam v graf vse podvozisse vozlisc neigbour
                    napolni(graf, neighbour)
                    if neighbour not in queue:
                        oce_od_elementa[neighbour] = current
                        queue.append(neighbour)






g = Graph()

#print(BFS(g, NxP_start))
#print(A_star(g, NxP_start))
