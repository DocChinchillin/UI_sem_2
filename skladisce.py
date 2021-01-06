from graf import Graph
import collections
import winsound

duration = 3000
freq = 440


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


def napolni(graf, start_m, kopija):
    start = list_to_tuple(start_m)
    for p in range(1, P+1):
        for r in range(1, P+1):
            kopija = naredi_matriko(start_m)
            x = prestavi(p, r, kopija)
            tuple_x = list_to_tuple(x)
            if tuple_x != start:
                graf.add(start, tuple_x)


def BFS(graf, root):


    oce_od_elementa = collections.defaultdict(tuple)

    vrsta = []

    seen = set()

    #dodam root
    vrsta.append(list_to_tuple(root))
    seen.add(str(root))
    kopija = naredi_matriko(root) #kopija start
    napolni(graf, root, kopija)
    i = 0
    while vrsta:

        vozlisce = vrsta.pop(0)

        for neighbour in graf.get(vozlisce):
            if str(neighbour) not in seen:
                #print(i, ".")
                #i += 1
                kopija_neig = naredi_matriko(neighbour)
                napolni(graf, neighbour, kopija_neig)
                vrsta.append(neighbour)
                seen.add(str(neighbour))
                if tuple_to_list(neighbour) == NxP_end:
                    #winsound.Beep(freq, duration)
                    return neighbour



g = Graph()

print(BFS(g, NxP_start))
#g.print()

