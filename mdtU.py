import re

def controlloInput(T, x):
    # Configurazione più piccola -> (101020101)
    if len(T) < 11:
        return False

    # Controllo parentesi
    if T[0] != '(' and T[len(T) - 1] != ')':
        return False

    # Controllo esistenza stato di accettazione
    i = 0
    cont = 0
    while T[i] != ')':
        if T[i] == '2':
            cont += 1
        i += 1

    if cont != 1:
        return False

    # Controllo sintassi configurazioni
    i = 0
    cont = 0
    if T[1] != '1':
        return False
    while T[i] != ')':
        if cont == 5:
            return False
        elif cont == 4:
            if T[i] == '-':
                if T[i + 1] == ')':
                    return False
                cont = 0
        elif T[i] == '0':
            cont += 1
        i += 1

    # Controllo input
    if x[0] != '1' and x[len(x) - 1] != '1':
        return False
    i = 0
    cont = 0
    while i < len(x):
        if cont > 1:
            return False
        elif x[i] == '0':
            cont += 1
        elif x[i] == '1':
            cont = 0
        i += 1
    return True

def shift_string_left(stringa, posizione_di_partenza):
    stringaShift = stringa[:posizione_di_partenza] + stringa[posizione_di_partenza + 1: len(stringa)]
    return stringaShift

def add_char_string(stringa, carattere, posizione_di_partenza):
    stringa = stringa[:posizione_di_partenza] + carattere + stringa[posizione_di_partenza : len(stringa)]
    return stringa

def trovaConfigurazione(n1, n2, n3, testinaN1, testinaN2, testinaN3):
    # Confronto lo stato in n3 con lo stato della configurazione
    while testinaN3 < len(n3) and n1[testinaN1] != '0':
        testinaN1 += 1
        testinaN3 += 1

    # Se lo stato corrente della configurazione è lo stesso dello stato attuale
    if testinaN3 == len(n3) and n1[testinaN1] == '0':
        testinaN3 = 0

        # Porto la testina al carattere da leggere
        testinaN1 += 1

        # Verifico il carattere letto nella configurazione con quello della testina di n2
        appoggio = testinaN2
        uguali = True
        while testinaN2 < len(n2) and n2[testinaN2] != '0' and n1[testinaN1] != '0':
            if n2[testinaN2] != n1[testinaN1]:
                uguali = False
            testinaN1 += 1
            testinaN2 += 1

        # Se l'input corrente della configurazione è lo stesso di quello in n2
        if (testinaN2 == len(n2) or n2[testinaN2] == '0') and n1[testinaN1] == '0' and uguali == True:
            testinaN2 = appoggio
            testinaN1 += 1
            return True, testinaN1, testinaN2, testinaN3

        # Se l'input corrente della configurazione non è lo stesso di quello letto in n2
        elif (testinaN2 == len(n2) and n1[testinaN1] == '1') or (n2[testinaN2] == '1' and n1[testinaN1] == '0') or (
                n2[testinaN2] == '0' and n1[testinaN1] == '1'):
            # Resetto la testina di N2
            testinaN2 = appoggio

            # Cerco la prossima configurazione in N1
            while n1[testinaN1] != '-':
                # Se la lettura è arrivata all'estremità si N1, setto testina N1 alla prima configurazione
                if n1[testinaN1] == ')':
                    testinaN1 = 1
                    return False, testinaN1, testinaN2, testinaN3
                testinaN1 += 1

            testinaN1 += 1

            return False, testinaN1, testinaN2, testinaN3

    # Se lo stato corrente della configurazione non è lo stesso dello stato attuale
    elif (testinaN3 == len(n3) and n1[testinaN1] == '1') or (testinaN3 != len(n3) and n1[testinaN1] == '0'):
        # Riporto testina n3 in posizione iniziale
        testinaN3 = 0

        # Cerco la prossima configurazione in N1
        while n1[testinaN1] != '-':
            # Se la lettura è arrivata all'estremità si N1, setto testina N1 alla prima configurazione
            if n1[testinaN1] == ')':
                testinaN1 = 1
                return False, testinaN1, testinaN2, testinaN3
            testinaN1 += 1

        # Testina in posizione della nuova configurazione trovata
        testinaN1 += 1

        return False, testinaN1, testinaN2, testinaN3
    testinaN2 = appoggio
    return False, testinaN1, testinaN2, testinaN3

def copiaStatoSuccessivo(n1, n3, testinaN1, testinaN3):
    n3 = ""

    while n1[testinaN1] != '0':
        n3 = n3 + n1[testinaN1]
        testinaN1 += 1

    testinaN1 += 1

    return n3, testinaN1, testinaN3

def scriviCarattere(n1, n2, testinaN1, testinaN2):
    if testinaN2 == 0 and n2[testinaN2] != '$':
        while n2[testinaN2] != '0':
            n2 = shift_string_left(n2, testinaN2)
    elif n1[testinaN1] != '$':
        appoggio = testinaN2

        while testinaN2 < len(n2) and n2[testinaN2] != '0':
            testinaN2 += 1

        if testinaN2 == len(n2):
            while n2[len(n2) - 1] != '0':
                n2 = shift_string_left(n2, len(n2) - 1)
            testinaN2 = len(n2)
        else:
            testinaN2 = appoggio

            while n2[testinaN2] != '0':
                n2 = shift_string_left(n2, testinaN2)

    if n1[testinaN1] != '$':
        while n1[testinaN1] != '0':
            n2 = add_char_string(n2, n1[testinaN1], testinaN2)
            testinaN1 += 1

        if testinaN2 != 0:
            while n2[testinaN2] != '0':
                testinaN2 -= 1
            testinaN2 += 1
        testinaN1 += 1
    elif n1[testinaN1] == '$':
        n2[testinaN2] == '$'
        testinaN1 += 2

    return n2, testinaN1, testinaN2

def spostaTestina(n1, n2, testinaN1, testinaN2):
    cont = 0

    # Finche non trovo un altra configurazione o termina n1
    while n1[testinaN1] != '-' and n1[testinaN1] != ')':
        cont += 1
        testinaN1 += 1

    # Porto n1 in una nuova configurazione
    if n1[testinaN1] == '-':
        testinaN1 += 1
    elif n1[testinaN1] == ')':
        testinaN1 = 1

    # Sposto la testina di n2 a sinistra
    if cont == 1:
        while testinaN2 > 0 and n2[testinaN2] != '0':
            testinaN2 -= 1
        if testinaN2 == 0:
            testinaN2 = 0
            n2 = '$' + '0' + n2
        elif n2[testinaN2] == '0':
            testinaN2 -= 1

            while testinaN2 > 0 and n2[testinaN2] != '0':
                testinaN2 -= 1

            if testinaN2 == 0:
                testinaN2 = 0

            elif n2[testinaN2] == '0':
                testinaN2 += 1

    # Sposto la testina di n2 a destra
    elif cont == 2:
        while testinaN2 < len(n2) and n2[testinaN2] != '0':
            testinaN2 += 1

    if testinaN2 == len(n2):
        n2 = n2 + '0' + '$'
        testinaN2 += 1
    elif n2[testinaN2] == '0':
        testinaN2 += 1
    return n2, testinaN1, testinaN2

def U(T, x):
    n1 = T
    n2 = x
    n3 = ""
    n4 = "2"

    # Copio lo stato di partenza da n1 a n3
    i = 1
    while n1[i] != '0':
        n3 = n3 + n1[i]
        i += 1

    testinaN1 = 1
    testinaN2 = 0
    testinaN3 = 0
    testinaN4 = 0
    while n3[0] != n4[0]:
        isConfigurazione = False
        while isConfigurazione == False:
            isConfigurazione, testinaN1, testinaN2, testinaN3 = trovaConfigurazione(n1, n2, n3, testinaN1, testinaN2, testinaN3)
        if isConfigurazione == True:
            n3, testinaN1, testinaN3 = copiaStatoSuccessivo(n1, n3, testinaN1, testinaN3)
            n2, testinaN1, testinaN2 = scriviCarattere(n1, n2, testinaN1, testinaN2)
            n2, testinaN1, testinaN2 = spostaTestina(n1, n2, testinaN1, testinaN2)

    return

while True:
    scelta = -1
    while scelta != 1 and scelta != 2:
        print("\nMacchina di Turing Universale \n")
        print("1. Utilizza T e x di default")
        print("2. Dai in input T e x \n")
        scelta = int(input("Scelta: "))

    if scelta == 1:
        T = '(1011110101111011-10101101111011-110101101011-11011111011011111011-110110111011111011-1110110111011011' \
            '-111011111101110111111011-1110111011110111111011-11110111011110111011-11110111111011110111111011' \
            '-11110$0111110$01-11111011110111110111101-1111101111101111101111101-111110111111011111011111101' \
            '-111110$020$0111-11111011101111111011101-111110110111111101101-1111101011111110101-111111101011111110101' \
            '-11111110110111111101101-1111111011101111111011101-111111101111011111110111101' \
            '-11111110111110111111101111101-1111111011111101111111011111101-11111110$010$011)'
        x = '10101011011011011101110111'
        U(T, x)
        print("Configurazione Accettata!")

    else:
        T = input("Inserisci T: ")
        x = input("Inserisci x: ")

        if controlloInput(T, x):
            U(T, x)
            print("Configurazione Accettata!")
        else:
            print("Errori di sintassi in T o in x!")

    risposta = ""
    while risposta.lower() != "si" and risposta.lower() != "no":
        risposta = input("Vuoi compiere altre operazioni? (sì/no): ")

    if risposta.lower() == "no":
        break
