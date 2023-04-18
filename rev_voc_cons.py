# -*- coding: utf-8 -*-
# le \ permet de continuer la ligne précédentes à la ligne suivantes
# les il signifie le programme


"""revise questions_math in console
"""


import random as rdm
import re


def add_count():
    """fonction qui ajoute un champ vide à la fin de chaque ligne
    """
    file = open("pc_MP2I.csv", "r", encoding="UTF-8")
    lines = []
    for i in file.readlines():
        newlines = i.rstrip("\n").rstrip("\"").split(";")
        newlines.insert(3, "0")
        lines.append(";".join(newlines))
    print(lines)
    file.close()

    file = open("IE.csv", "w")
    for i in lines:
        file.write(str(i)+";\n")
    file.close()
1


def questions_math():
    """fonction qui renvoie le dictionnaire avec l'ensemble des questions
    sous la forme:
    dictionnaire principal:
    clé : nb, nom du chapitre
    valeur : dictionnaire :
            - clé : question
            - valeur : [compte, réponse]
    """
    file = open("IE.csv", "r", encoding="UTF-8")
    lines = file.readlines()
    file.close()
    dic = {}
    for j, i in enumerate(lines[1:]):
        chapnb, chapnom, quest, compte, reponse, bac = i.split(";")
        chapkey = (chapnb, chapnom)
        if dic.get(chapkey) is None:
            dic[chapkey] = {}
        dic[chapkey][quest] = [int(compte), reponse]
    return dic.copy()


def comp(dic, src : dict = questions_math()):
    """fonction qui compare dic à questions_math en compte de question
    """
    v1 = src
    keys = list(dic.keys())
    somme = 0
    somme2 = 0
    for i, j in keys:
        l1 = len(v1[i,j])
        l2 = len(dic[i,j])
        somme += l1
        somme2 += l2
        print(f"'{i}' , '{j}') {l1} ;\t len dic = {l2}") 
    print(f"questions_math() somme = {somme} ; dic somme = {somme2}")


def questions_phys_1():
    """fonction qui renvoie le dictionnaire avec l'ensemble des questions
    sous la forme:
    dictionnaire principal:
    clé : nb, nom du chapitre
    valeur : dictionnaire :
            - clé : question
            - valeur : [compte, réponse]
    """
    file = open("pc_MP2I.csv", "r", encoding="UTF-8")
    lines = file.readlines()[1:]
    file.close()
    dic = {}
    for j, i in enumerate(lines):
        chapnb, chapnom, quest, compte, reponse, bac = i.split(";")
        chapkey = (chapnb, chapnom)
        if dic.get(chapkey) is None:
            dic[chapkey] = {}
        dic[chapkey][quest] = [int(compte), reponse]
    return dic.copy()


def questions_phys_2():
    """fonction qui renvoie le dictionnaire avec l'ensemble des questions
    sous la forme:
    dictionnaire principal:
    clé : nb, nom du chapitre
    valeur : dictionnaire :
            - clé : question
            - valeur : [compte, réponse]
    """
    file = open("pc_MPI.csv", "r", encoding="UTF-8")
    lines = file.readlines()[1:]
    file.close()
    dic = {}
    for j, i in enumerate(lines):
        if (len(i.split(";")) != 6):
            print(i)
        chapnb, chapnom, quest, compte, reponse, bac = i.split(";")
        chapkey = (chapnb, chapnom)
        if dic.get(chapkey) is None:
            dic[chapkey] = {}
        dic[chapkey][quest] = [int(compte), reponse]
    return dic.copy()

def save(dic, mat):
    """fonction qui sauvegarde les compte de questions dans IE.csv
    """
    if mat == "math":
        fichiernom = "IE.csv"
    elif mat == "phys1":
        fichiernom = "pc_MP2I.csv"
    else:
        fichiernom = "pc_MPI.csv"

    file = open(fichiernom, "w", encoding="UTF-8")
    file.write("numero_chapitre;chapitre;énoncé;nb_sortie;reponse;\n")
    for key in list(dic.keys()):
        nb, nom = key
        for quest, lq in list(dic.get(key).items()):
            cpte, reponse = lq
            rep2 = reponse.replace("\n", "\\n")
            file.write(f"{nb};{nom};{quest};{cpte};{rep2};\n")
    file.close()


def save_score(score, demande, mat):
    """enregistre le score dans un fichier externe
    """
    file = open(("score_math.csv","score_phy.csv")[mat != "math"], "w+")
    lines = file.readlines()
    if lines == []:
        file.write("bonne_rep;nb_quest;\n")
    file.write("f{score};{demande};\n")
    file.close()


def choiceall(chapitre, cptechap):
    """fonction qui renvoie un chapitre parmi les chapitres données
    chapitre : liste d'entier
    """
    somquest = 0
    pool = []
    liitems = [(i, j) for i ,j in list(cptechap.items()) if i[0] in chapitre]
    for k, v in liitems:
        somquest += v
    for k, v in liitems: 
        pool.extend([k] * get_pool_nb(somquest, v))
    return rdm.choice(pool)


def get_pool_nb(tot, n):
    """calcule le nombre fois il faut mettre la question dans l'urne
    """
    if tot == 0:
        return 1
    return int((tot - n) / tot * 100) + 1

def choiceone(a, key):
    """fonction qui renvoie une question aléatoire dans le chapitre key
    """
    somquest = 0
    pool = []
    liitems = list(a.get(key).items())
    for k, v in liitems:
        somquest += v[0]
    for k, v in liitems: 
        pool.extend([k] * get_pool_nb(somquest, v[0]))
    return rdm.choice(pool)


def comptechap(a):
    """fonction qui compte le nombre de question sorti par chapitres
    """
    compteparchap = {}
    for key, dicquest in list(a.items()):
        if compteparchap.get(key) is None:
            compteparchap[key] = 0
        for quest, cpte in list(dicquest.items()):
            compteparchap[key] += int(cpte[0])
    return compteparchap


def plage_to_list_int_str(req : str):
    plages = re.findall("^(\d+[ ]*-[ ]*\d+([ ]*,[ ]*\d+[ ]*-[ ]*\d+)*)$", req)
    ret = ""
    ints = []
    if plages:
        plages = plages[0][0]
        for p in plages.split(","):
            start, end = p.split("-")
            for i in range(int(start), int(end) + 1):
                if i not in ints:
                    ret += str(i) + ", "
                    ints.append(i)
        return ret[:-2]
    else:
        ret = req
    return ret

def revise_voc_in_console_math(a: dict = questions_math(), b: dict = questions_math()):
    """fonction principal
    """
    # récupération des chapitres de la bases
    listchap = list(a.keys())
    
    compteparchap = comptechap(a)

    # affichage de la requête pour l'utilisateur
    request = input(
        """Choisissez parmi les propositions suivantes:
tout, \n{lst}

Liste à étudier (rien est comme écrire "tout") (sous forme de liste de nombre ex: 1, 3, 19; ou de plage : 1-3, 4 - 5, 19-19 (le chapitre 19), 21- 22) (pas de mélange de format)= 
""".format(
            lst="\n".join(
                str(i) +":"+ str(j)
                for i,j in listchap
            )
        )
    )
    # contrôle des réponses
    while not re.findall("^(\d+(, *\d+)*|tout|\d+[ ]*-[ ]*\d+([ ]*,[ ]*\d+[ ]*-[ ]*\d+)*)?$", request):
        request = input("input incorrect; nouvelle input = ")

    if request == "":
        request = "tout"

    # demande nobre de questions
    nb_demande = input("combien de question vous seront posées = ")
    while not re.findall("^\d+$", nb_demande):
        nb_demande = input("combien de question vous seront posées = ")
    nb_demande = int(nb_demande)

    # compte des bonnes réponses
    compteur = 0
    i = 1
    run = True

    # questionnaire sur tous les chapitres
    if request == "tout":
        while i <= nb_demande and run:
            # sélectionne un chaptire parmi tous les chaptires restants
            requestnb, requestnom = choiceall([i for i,j in list(a.keys())], comptechap(a))
            
            key = (requestnb, requestnom)
            
            # séléctionne une question du chapitre
            quest = choiceone(a, key)

            show = input("{} / {}) {}, {} : {} \n montrer la réponse [entrer] ".format(i, nb_demande, request, requestnom, key))
            if show == "1":
                answer = "1"
            else:
                print(f"réponse si ajoutée est : {a[key][quest][1]}")
                answer = input("score = ")

            # bonne réponse
            if (answer == "1"):
                compteur += 1
                del a[key][quest]
                b[key][quest][0] += 1
                if len(a[key]) == 0:
                    del a[key]
                    request2 = input("continuer? yes or no (ou oui ou non)\n")
                    if request2 == "" or request2[0] in "YyoO" or (request2[0] in "YyoO" and request2[1] in "EeuU" 
                            and request2[2] in "SsiI"):
                        a[key] = b.copy().get(request)
                    else:
                        run = False
            i += 1

    # liste de chapitre 
    else:
        # change les plages s'il y en a en liste de chapitre
        request = plage_to_list_int_str(request)

        # liste des chaps en ["a", "b", "c"]
        reql = [str(int(j)) for j in request.split(",")]

        while i <= nb_demande and run:
            
            # liste des chaps qui sont encore dans la liste
            listechap = [i for i,j in list(a.keys()) if i in reql]

            # on sélection un des chapitres
            request, requestnom = choiceall(listechap, compteparchap)
            liste = request, requestnom
            
            # on sélectionne la question
            key = choiceone(a, liste)

            show = input("{} / {}) {}, {} : {} \n montrer la réponse [entrer] ".format(i, nb_demande, request, requestnom, key))
            if show == "1":
                answer = "1"
            else:
                print(f"réponse si ajoutée est : {a[key][quest][1]}")
                answer = input("score = ")

            # bonne réponse
            if (answer == "1"):
                compteur += 1
                del a[liste][key]
                b[liste][key][0] += 1
                if len(a[liste]) == 0:
                    del a[liste]
                    request2 = input("continuer? yes or no (ou oui ou non)\n")
                    if request2[0] in "YyoO" or request2 == "" or ((request2[0] in "YyoO") and (request2[1] in "EeUu") 
                            and (request2[2] in "SsIi")):
                        a[liste] = b.get(liste).copy()

                    else:
                        run = False

            i += 1
                

    if nb_demande == 0:
        print("Pas de question à poser")
    else:
        print(
                "{} / {} soit {} % de bonnes réponses".format(
                        compteur,
                        i - 1,
                        round(compteur / (i - 1) * 100, 2)
                    )
            )

    # sauvegarde des comptes
    save(b, "math")

    # pour sauvegarder les scores dans un fichier externe décommenter la ligne ci-dessous
    # save_score(compteur, i - 1)

def revise_voc_in_console_phy1(a: dict = questions_phys_1(), b: dict = questions_phys_1()):
    """fonction principal
    """
    # récupération des chapitres de la bases
    listchap = list(a.keys())
    
    compteparchap = comptechap(a)

    # affichage de la requête pour l'utilisateur
    request = input(
        """Choisissez qu'UNE SEULE des propositions suivantes:
tout, \n{lst}

Liste à étudier (rien est comme écrire "tout") (sous forme de liste de nombre ex: 1, 3, 19; ou de plage : 1-3, 4 - 5, 19-19 (le chapitre 19), 21- 22) (pas de mélange de format)= 
""".format(
            lst="\n".join(
                str(i) +": "+ str(j)
                for i,j in listchap
            )
        )
    )
    # contrôle des réponses
    while not re.findall("^(\d+(, *\d+)*|tout|\d+[ ]*-[ ]*\d+([ ]*,[ ]*\d+[ ]*-[ ]*\d+)*)?$", request):
        request = input("input incorrect; nouvelle input = ")

    if request == "":
        request = "tout"

    # demande nobre de questions
    nb_demande = input("combien de question vous seront posées = ")
    while not re.findall("^\d+$", nb_demande):
        nb_demande = input("combien de question vous seront posées = ")
    nb_demande = int(nb_demande)

    # compte des bonnes réponses
    compteur = 0
    i = 1
    run = True

    # questionnaire sur tous les chapitres
    if request == "tout":
        while i <= nb_demande and run:
            # sélectionne un chaptire parmi tous les chaptires restants
            requestnb, requestnom = choiceall([i for i,j in list(a.keys())], comptechap(a))
            
            key = (requestnb, requestnom)
            
            # séléctionne une question du chapitre
            quest = choiceone(a, key)

            show = input("{} / {}) {}, {} : {} \n montrer la réponse [entrer] ".format(i, nb_demande, requestnb, requestnom, quest))
            if show == "1":
                answer = "1"
            else:
                print(f"réponse si ajoutée est : {a[key][quest][1]}")
                answer = input("score = ")
            
            # bonne réponse
            if (answer == "1"):
                compteur += 1
                del a[key][quest]
                b[key][quest][0] += 1
                if len(a[key]) == 0:
                    del a[key]
                    request2 = input("continuer? yes or no (ou oui ou non)\n")
                    if request2 == "" or request2[0] in "YyoO" or (request2[0] in "YyoO" and request2[1] in "EeuU" 
                            and request2[2] in "SsiI"):
                        a[key] = b.copy().get(request)
                    else:
                        run = False
            i += 1

    # liste de chapitre 
    else:

        # change les plages s'il y en a en liste de chapitre
        request = plage_to_list_int_str(request)

        # liste des chaps en ["a", "b", "c"]
        reql = [str(int(j)) for j in request.split(",")]

        while i <= nb_demande and run:
            
            # liste des chaps qui sont encore dans la liste
            listechap = [i for i,j in list(a.keys()) if i in reql]

            # on sélection un des chapitres
            request, requestnom = choiceall(listechap, compteparchap)
            liste = request, requestnom
            
            # on sélectionne la question
            key = choiceone(a, liste)

            show = input("{} / {}) {}, {} : {} \n montrer la réponse [entrer] ".format(i, nb_demande, request, requestnom, key))
            if show == "1":
                answer = "1"
            else:
                print(f"réponse si ajoutée est : {a[liste][key][1]}")
                answer = input("score = ")

            # bonne réponse
            if (answer == "1"):
                compteur += 1
                del a[liste][key]
                b[liste][key][0] += 1
                if len(a[liste]) == 0:
                    del a[liste]
                    request2 = input("continuer? yes or no (ou oui ou non)\n")
                    if request2[0] in "YyoO" or request2 == "" or ((request2[0] in "YyoO") and (request2[1] in "EeUu") 
                            and (request2[2] in "SsIi")):
                        a[liste] = b.get(liste).copy()

                    else:
                        run = False

            i += 1
                

    if nb_demande == 0:
        print("Pas de question à poser")
    else:
        print(
                "{} / {} soit {} % de bonnes réponses".format(
                        compteur,
                        i - 1,
                        round(compteur / (i - 1) * 100, 2)
                    )
            )

    # sauvegarde des comptes
    save(b, "phys1")

    # pour sauvegarder les scores dans un fichier externe décommenter la ligne ci-dessous
    # save_score(compteur, i - 1)

def revise_voc_in_console_phy2(a: dict = questions_phys_2(), b: dict = questions_phys_2()):
    """fonction principal
    """
    # récupération des chapitres de la bases
    listchap = list(a.keys())
    
    compteparchap = comptechap(a)

    # affichage de la requête pour l'utilisateur
    request = input(
        """Choisissez qu'UNE SEULE des propositions suivantes:
tout, \n{lst}

Liste à étudier (rien est comme écrire "tout") (sous forme de liste de nombre ex: 1, 3, 19; ou de plage : 1-3, 4 - 5, 19-19 (le chapitre 19), 21- 22) (pas de mélange de format) = 
""".format(
            lst="\n".join(
                str(i) +": "+ str(j)
                for i,j in listchap
            )
        )
    )
    # contrôle des réponses
    while not re.findall("^(\d+([ ]*,[ ]*\d+)*|tout|\d+[ ]*-[ ]*\d+([ ]*,[ ]*\d+[ ]*-[ ]*\d+)*)?$", request):
        request = input("input incorrect; nouvelle input = ")

    if request == "":
        request = "tout"

    # demande nobre de questions
    nb_demande = input("combien de question vous seront posées = ")
    while not re.findall("^\d+$", nb_demande):
        nb_demande = input("combien de question vous seront posées = ")
    nb_demande = int(nb_demande)

    # compte des bonnes réponses
    compteur = 0
    i = 1
    run = True

    # questionnaire sur tous les chapitres
    if request == "tout":
        while i <= nb_demande and run:
            # sélectionne un chaptire parmi tous les chaptires restants
            requestnb, requestnom = choiceall([i for i,j in list(a.keys())], comptechap(a))
            
            key = (requestnb, requestnom)
            
            # séléctionne une question du chapitre
            quest = choiceone(a, key)

            show = input("{} / {}) {}, {} : {} \n montrer la réponse [entrer] ".format(i, nb_demande, requestnb, requestnom, quest))
            if show == "1":
                answer = "1"
            else:
                print(f"réponse si ajoutée est : {a[key][quest][1]}")
                answer = input("score = ")
            
            # bonne réponse
            if (answer == "1"):
                compteur += 1
                del a[key][quest]
                b[key][quest][0] += 1
                if len(a[key]) == 0:
                    del a[key]
                    request2 = input("continuer? yes or no (ou oui ou non)\n")
                    if (request2[0] in "YyoO" and request2[1] in "EeuU" 
                            and request2[2] in "SsiI") or request2[0] in "YyoO" \
                                or request2 == "":
                        a[key] = b.copy().get(request)
                    else:
                        run = False
            i += 1

    # liste de chapitre 
    else:

        # change les plages s'il y en a en liste de chapitre
        request = plage_to_list_int_str(request)

        # liste des chaps en ["a", "b", "c"]
        reql = [str(int(j)) for j in request.split(",")]

        while i <= nb_demande and run:
            
            # liste des chaps qui sont encore dans la liste
            listechap = [i for i,j in list(a.keys()) if i in reql]

            # on sélection un des chapitres
            request, requestnom = choiceall(listechap, compteparchap)
            liste = request, requestnom
            
            # on sélectionne la question
            key = choiceone(a, liste)

            show = input("{} / {}) {}, {} : {} \n montrer la réponse [entrer] ".format(i, nb_demande, request, requestnom, key))
            if show == "1":
                answer = "1"
            else:
                print(f"réponse si ajoutée est : {a[liste][key][1]}")
                answer = input("score = ")

            # bonne réponse
            if (answer == "1"):
                compteur += 1
                del a[liste][key]
                b[liste][key][0] += 1
                if len(a[liste]) == 0:
                    del a[liste]
                    request2 = input("continuer? yes or no (ou oui ou non)\n")
                    if request2 == "" or request2[0] in "YyoO" or (request2[0] in "YyoO" and request2[1] in "EeuU" 
                            and request2[2] in "SsiI"):
                        a[liste] = b.get(liste).copy()

                    else:
                        run = False

            i += 1
                

    if nb_demande == 0:
        print("Pas de question à poser")
    else:
        print(
                "{} / {} soit {} % de bonnes réponses".format(
                        compteur,
                        i - 1,
                        round(compteur / (i - 1) * 100, 2)
                    )
            )

    # sauvegarde des comptes
    save(b, "phys2")

    # pour sauvegarder les scores dans un fichier externe décommenter la ligne ci-dessous
    # save_score(compteur, i - 1)

def revise_voc_in_console():
    rep = input("matière m ou rien pour math p pour physique ")
    if rep == "" or rep in "mM":
        revise_voc_in_console_math()
    elif rep in "pP":
        annee = input("Quel année réviser 1 pour 1ere année 2 pour 2e année ")
        if annee == "1":
            revise_voc_in_console_phy1()
        elif annee == "2":
            revise_voc_in_console_phy2()


if __name__ == "__main__":
    # éxécution du programme
    revise_voc_in_console()
    pass
