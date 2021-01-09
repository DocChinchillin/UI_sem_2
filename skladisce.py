import itertools
import copy
from graf import Graph
import collections
import sys
import math
st_obiskanih_vozlisc = 0
globina = 0


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

#N = len(NxP_start)
#P = len(NxP_start[N - 1])

# P - odstavnih polozajev
# N - velikih skatelj ena na drugo

# p => 1 <= p <= P
# r => 1 <= r <= P

def prestavi(p, r, matrika1):
    matrika = matrika1[:]
    N = len(matrika)
    P = len(matrika[N - 1])
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
    N = len(start_m)
    P = len(start_m[N - 1])
    start = list_to_tuple(start_m)

    for p in range(1, P + 1):
        for r in range(1, P + 1):
            kopija = naredi_matriko(start_m)
            x = prestavi(p, r, kopija)
            tuple_x = list_to_tuple(x)
            if tuple_x != start:
                graf.add(start, tuple_x)
                graf.addPremik(start, tuple_x, (p, r))


def BFS(root, end):
    oce_od_elementa = collections.defaultdict(tuple)
    graf = Graph()
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
                oce_od_elementa[neighbour] = vozlisce
                napolni(graf, neighbour)
                vrsta.append(neighbour)
                seen.add(str(neighbour))

                if tuple_to_list(neighbour) == end:
                    print("Stevilo pregledanih vozlisc:", stevilo_pregledanih_vozlisc)
                    return find_path(graf, neighbour, oce_od_elementa, root)


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


def find_path(graf, neighbour, oce_sin_dict, NxP_start):
    path = [neighbour]
    global globina
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
    globina = max(len(path) - 1, globina)
    return premiki


def find_path_reverse(graf, neighbour, oce_sin_dict, start):
    path = [neighbour]
    global globina
    while neighbour != list_to_tuple(start):
        neighbour = oce_sin_dict[neighbour]
        path.append(neighbour)
    path = path[::-1]  # obrnem
    premiki = []
    i = 0
    j = 1
    while i < len(path) - 1 and j < len(path):
        premiki.append(graf.getPremik(path[j], path[i]))
        i += 1
        j += 1
    globina = max(len(path) - 1, globina)
    return list(reversed(premiki))


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


def lep_izpis_ids(start_path,end_path):
    start_m, end_m = get_matrike(start_path,end_path)
    print("############Izpis IDS:############")
    print("Start matrika:")
    izpis(start_m)
    print("\nEnd matrika:")
    izpis(end_m)
    pot = IDS(12, start_m, end_m)
    print("\nPot:")
    print(pot)
    print("Število obiskanih vozlisc", st_obiskanih_vozlisc)
    print()
    izrisi_pot(copy.deepcopy(start_m), copy.deepcopy(end_m), pot)





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


def A_star(root):
    graf = Graph()
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


def dvosmerno_bfs(root, end):
    global st_obiskanih_vozlisc
    oce_od_elementa = collections.defaultdict(tuple)
    oce_od_elementa_nzj = collections.defaultdict(tuple)
    g = Graph()
    ng = Graph()
    vrsta = []
    vrsta_nzj = []
    seen = set()
    seen_nzj = set()
    # dodam root
    vrsta.append(list_to_tuple(root))
    vrsta_nzj.append(list_to_tuple(end))
    seen.add(str(root))
    seen_nzj.add(str(end))
    # kopija = naredi_matriko(root) #kopija start
    resitve = (list_to_tuple(end),)
    konci = (list_to_tuple(root),)
    napolni(g, root)
    napolni(ng, end)
    stevilo_pregledanih_vozlisc = 1
    while vrsta:
        vozlisce = vrsta.pop(0)
        vozlisce_nzj = vrsta_nzj.pop(0)
        for neighbour in ng.get(vozlisce_nzj):
            if str(neighbour) not in seen_nzj:
                stevilo_pregledanih_vozlisc += 1
                oce_od_elementa_nzj[neighbour] = vozlisce_nzj
                napolni(ng, neighbour)
                vrsta_nzj.append(neighbour)
                seen_nzj.add(str(neighbour))
                resitve += (neighbour,)
                if neighbour in konci:
                    st_obiskanih_vozlisc = stevilo_pregledanih_vozlisc
                    return find_path(g, neighbour, oce_od_elementa, root) + find_path_reverse(ng, neighbour, oce_od_elementa_nzj, end)

        for neighbour in g.get(vozlisce):
            if str(neighbour) not in seen:
                stevilo_pregledanih_vozlisc += 1
                oce_od_elementa[neighbour] = vozlisce
                napolni(g, neighbour)
                vrsta.append(neighbour)
                seen.add(str(neighbour))
                konci += (neighbour,)
                if neighbour in resitve:

                    st_obiskanih_vozlisc = stevilo_pregledanih_vozlisc
                    return find_path(g, neighbour, oce_od_elementa, root) + find_path_reverse(ng, neighbour, oce_od_elementa_nzj, end)

def izpis_dvo_bfs(start_path, end_path):
    print("############Izpis dvosmerni bfs:############")
    start_m, end_m = get_matrike(start_path, end_path)  # ce podas 0, 0 bo hotu iz system.in
    print("Start matrika:")
    izpis(start_m)
    print("End matrika:")
    izpis(end_m)
    path = dvosmerno_bfs(start_m, end_m)
    print("Pot:")
    print(path)
    #izrisi_pot(start_m, end_m, path)
    print("#######################################")


path_s = "D:\\Python\\UI_sem_2\\primer5_zacetna.txt"
path_e = "D:\\Python\\UI_sem_2\\primer5_koncna.txt"
#lep_izpis_ids(path_s, path_e)
izpis_dvo_bfs(path_s, path_e)
#s_m, e_m =get_matrike("D:\\Python\\UI_sem_2\\primer5_zacetna.txt","D:\\Python\\UI_sem_2\\primer5_koncna.txt")
#print(BFS(s_m, e_m))

#print(A_star(NxP_start))
