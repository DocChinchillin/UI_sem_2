from graf import Graph
import collections


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
    ['B', '', ''],
    ['A', '', '']
]

NxP_end = [
    ['', 'B', ''],
    ['', 'A', '']
]
'''
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
'''
NxP_start = [
    ['B', '', ''],
    ['A', '', '']
]

NxP_end = [
    ['', 'B', ''],
    ['', 'A', '']
]
'''
N = len(NxP_start)
P = len(NxP_start[N-1])


#P - odstavnih polozajev
#N - velikih skatelj ena na drugo

# p => 1 <= p <= P
# r => 1 <= r <= P

def prestavi(p, r, matrika1):

    matrika = matrika1[:]

    first_element = ''
    delete_i = -1
    delete_p_1 = -1

    #ce je p, r return matriko
    if p == r:
        return matrika
    # dokler nenajdes nepraznega in ga shranis v first_element
    for i in range(0, N):
        if matrika[i][p-1] != '':
            first_element = matrika[i][p-1]
            delete_i = i
            delete_p_1 = p-1
            break
    # dokler nenajdes prvega praznega od spodi navzgor in shranis element iz
    # first_element v ta prostor in zbrises element iz kordinati i in p-1
    for j in range(N-1, -1, -1):
        if matrika[j][r-1] == '':
            matrika[j][r-1] = first_element
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
    for p in range(1, P+1):
        for r in range(1, P+1):
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

    #dodam root
    vrsta.append(list_to_tuple(root))
    seen.add(str(root))
    #kopija = naredi_matriko(root) #kopija start
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



def find_path(graf, neighbour, oce_sin_dict):
    path = [neighbour]
    while neighbour != list_to_tuple(NxP_start):
        neighbour = oce_sin_dict[neighbour]
        path.append(neighbour)
    path = path[::-1] #obrnem
    premiki = []
    i = 0
    j = 1
    while i < len(path)-1 and j < len(path):
        premiki.append(graf.getPremik(path[i], path[j]))
        i += 1
        j += 1
    print("Max globina:", len(path)-1)
    return "Pot: " + str(premiki)




g = Graph()

print(BFS(g, NxP_start))

