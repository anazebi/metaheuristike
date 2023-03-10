import random
import numpy as np

def fitness_function(C):                    # vraca ukupnu vrijednost ruksaka s konfiguracijom C[]
    suma = 0
    for i in range(n):
        suma += V[i] * C[i]
    return suma

def crossover1(A, B):                        
    C = [0 for i in range(n)]
    for i in range(n):
        a = random.randint(0, 1)
        if(a == 0):
            C[i] = A[i]
        else:
            C[i] = B[i]
    return C

def crossover2(A, B):                   # provodi crossover sa slucajno izabranim bitom raspolavljanja

    djeca = []
    a = random.randint(0, n-1)
    C = A.copy()
    D = A.copy()
    for i in range(a, n):
        C[i] = B[i]
    for i in range(a):
        D[i] = B[i]
    djeca.append(C)
    djeca.append(D)
    return djeca

def mutiraj(C):                         # mutira bitove  u konfiguraciji C
    for i in range(int(0.02 * n)):
        a = random.randint(0, n-1)
        C[a] = abs(C[a] - 1)
    return C

def provjeri_kapacitet(R):              # vraca 1 ako je suma tezina predmeta bilo koje dimenzije veca od preostalog kapaciteta ruksaka            
    for i in range(m):                  # inace 0
        if(R[i] > B[i]):
            return 1
    return 0


def update(R, j, korak):                # korak poprima vrijednosti 1 i -1
    for i in range(m):                  
        if(korak == -1):                # korak = -1 znaci da iz ruksaka uklanjamo j-ti predmet
            R[i] -= W[i][j]
        else:
            R[i] += W[i][j]             # korak = 1 znaci da u ruksak dodajemo j-ti predmet


def provjeri_update(R, j):              # vraca jedan ako dodavanje j-tog predmeta ne prelazi nijedan od kapacitet ruksaka
    for i in range(m):                  # vraca 0 inace
        if(R[i] + W[i][j] > B[i]):
            return 0
    return 1


def stvori(C):                          # za konfiguraciju C[] vraca vektor R za koji vrijedi R[i] = ukupna vrijednost i-te dimenzije konfiguracije C
    R = [0 for i in range(m)]
    for i in range(m):
        for j in range(n):
            R[i] += C[j]*W[i][j]
    return R


def najmanji(P):                       # vraca najslabiju jedinku populacije P

    mini = 0
    najmanji_do_sada = fitness_function(P[0])
    for i in range(1, len(P)):
        if(fitness_function(P[i]) < najmanji_do_sada):
            najmanji_do_sada = fitness_function(P[i])
            mini = i
    return mini


def najveci(P):                         # vraca najjacu jedinku populacije P
    maxi = 0
    najveci_do_sada = fitness_function(P[0])
    for i in range(1, len(P)):
        if(fitness_function(P[i]) > najveci_do_sada):
            maxi = i
            najveci_do_sada = fitness_function(P[i])
    return maxi


def odaberi_roditelje(P):
    A = P.copy()
    Rez = []
    
    a = random.randint(0,len(P) - 1)
    b = random.randint(0,len(P) - 1)
    while(a == b):
        a = random.randint(0,len(P) - 1)
        b = random.randint(0,len(P) - 1)
    if(fitness_function(P[a]) > fitness_function(P[b])):
        P1 = A[a]
    else:
        P1 = A[b]
    A = np.delete(A, a, 0)
    
    a = random.randint(0,len(A) - 1)
    b = random.randint(0,len(A) - 1)
    if(fitness_function(A[a]) > fitness_function(A[b])):
        P2 = A[a]
    else:
        P2 = A[b]
        
    Rez.append(P1)
    Rez.append(P2)
    return Rez


def ratio(n, m):
    A = [0 for i in range(n)]
    for i in range(n):
        suma = 0
        for j in range(m):
            suma += W[j][i]
        A[i] = V[i]/suma
    return A

def najv(A):
    i = 0
    for j in range(1,len(A)):
        if(A[j] > A[i]):
            i = j
    return i

def najm(A):
    i = 0
    for j in range(1,len(A)):
        if(A[j] < A[i]):
            i = j
    return i
    
def repair(C, W):
    A = ratio(n, m)                     # vraca listu omjera vrijednosti i tezine za svaki predmet
    R = [0 for i in range(m)]

    for i in range(m):
        for j in range(n):
            R[i] += W[i][j] * C[j]
            
    kopijaA = A.copy()
    for i in range(n):
        j = najm(A)
        if(C[j] == 1 and provjeri_kapacitet(R) == 1):
            C[j] = 0
            update(R, j, -1)
        A[j] = 5000
        
    A = kopijaA.copy()
    for i in range(n):
        j = najv(A)
        if(C[j] == 0 and provjeri_update(R, j) == 1):
            C[j] = 1
            update(R, j, 1)
        A[j] = -1
    return C


def inicijaliziraj():
    # pocetna populacija od 100 jedinki
    P = [[0 for i in range(n)] for j in range(100)]

    for k in range(100):
        R = [0 for i in range(m)]
        T = [i for i in range(n)]
        j = random.choice(T)
        T.remove(j)
        while(provjeri_update(R, j)):
            P[k][j] = 1
            update(R, j, 1)
            j = random.choice(T)
            T.remove(j)
    return P

def provjera(C):                    # vraca preostali kapacitet dimenzija ruksaka za konfiguraciju C
    kapac = B.copy()
    print("na pocetku", kapac)
    for i in range(m):
        for j in range(n):
            if(C[j] == 1):
                kapac[i]-= W[i][j]
    print("kapacitet je ", kapac)
   

def pronadi_najbolje(P):
    A = P.copy()
    a = []
    i1 = najveci(P)
    A[i1] = [0 for i in range(n)]
    i2 = najveci(A)
    a.append(P[i1])
    a.append(P[i2]) 
    return a
    
def genetic_algorithm(iter = 200):
    P = inicijaliziraj()
    Fitness = [0 for i in range(len(P))]
    for i in range(len(P)):
        Fitness[i] = fitness_function(P[i])
    P_t = max(Fitness) # najveca vrijednost u pocetnoj populaciji
    print("Najveca pocetna: ", P_t)
    indeks = najveci(P)
    
    for j in range(iter):
        najbolji = pronadi_najbolje(P)
        prvi = najbolji[0]
        drugi = najbolji[1]
        
        roditelji = odaberi_roditelje(P)
        P1 = roditelji[0]
        P2 = roditelji[1]
        t = 0
        while t < 49:
            t = t + 1
            djeca = crossover2(P1, P2)
            C = djeca[0]
            D = djeca[1]
            C = repair(mutiraj(C), W)
            D = repair(mutiraj(D), W)
            
            if C in P:
                continue
            value_C = fitness_function(C)
            index = najmanji(P)
            P[index] = C  
            
            if D in P:
                continue
            value_D = fitness_function(D)
            index = najmanji(P)
            P[index] = D
            
            if(value_C > P_t):
                P_t = value_C
                indeks = index
            if(value_D > P_t):
                P_t = value_D
                indeks = index
                
        print("Iteracija: ", j , ", Trenutno najbolji: ", P_t )
        
        index = najmanji(P)
        P[index] = prvi
        index = najmanji(P)
        P[index] = drugi
        
    return P[indeks], P_t


def broj(l):
    br = 0
    for i in range(n):
        if(l[i] == 1):
            br += 1
    return br

def main(string, iter = 200):
    f = open(string)
    prvi = f.readline()
    prvi = prvi.split(' ')
    global n                                            # n - broj predmeta
    n = int(prvi[0])
    global m                                            # m - broj dimenzija
    m= int(prvi[1])
    drugi = f.readline().replace('\n', '').split(' ')
    global V                                            # V[] - vrijednosti predmeta
    V = [0 for i in range(n)]
    for i in range(n):
        V[i] = int(drugi[i])

    global W                                            # W[i][j] - vrijednost j-te dimenzije i-tog predmeta
    W = [[0 for i in range(n)] for j in range(m)]
    for i in range(m):
        l = f.readline()
        l = l.replace('\n', '').split(' ')
        for j in range(n):
            W[i][j] = int(l[j])

    global B
    B = [0 for i in range(m)]                           # B[i] - kapacitet i-te dimenzije ruksaka
    l = f.readline().replace('\n', '').split(' ')
    for i in range(m):
        B[i] = int(l[i])

    Rjesenja = genetic_algorithm(iter)
    provjera(Rjesenja[0])
    print("Broj predmeta je ", broj(Rjesenja[0]))
    print(Rjesenja)
    return Rjesenja
    

    
