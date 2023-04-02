# -*- coding: utf-8 -*-
# le \ permet de continuer la ligne précédentes à la ligne suivantes
# les il signifie le programme


"""revise voc in console
"""


import random as rdm
import re


def add_count():
    """fonction qui ajoute un champ vide à la fin de chaque ligne
    """
    file = open("IE.csv", "r")
    lines = [i.rstrip("\n") for i in file.readlines()]
    print(lines)
    file.close()

    file = open("IE.csv", "w")
    file.write(";\n".join(lines))
    file.close()




def voc():
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
    for i in lines[1:]:
        chapnb, chapnom, quest, compte, reponse, bac = i.split(";")
        chapkey = (chapnb, chapnom)
        if dic.get(chapkey) is None:
            dic[chapkey] = {}
        dic[chapkey][quest] = [int(compte), reponse]
    return dic.copy()


def comp(dic):
    """fonction qui compare dic à voc en compte de question
    """
    v1 = voc()
    keys = list(dic.keys())
    somme = 0
    somme2 = 0
    for i, j in keys:
        l1 = len(v1[i,j])
        l2 = len(dic[i,j])
        somme += l1
        somme2 += l2
        print(f"'{i}' , '{j}') {l1} ;\t len dic = {l2}") 
    print(f"voc() somme = {somme} ; dic somme = {somme2}")


def save(dic):
    """fonction qui sauvegarde les compte de questions dans IE.csv
    """
    file = open("IE.csv", "w", encoding="UTF-8")
    file.write("numero_chapitre;chapitre;énoncé;nb_sortie;reponse;\n")
    for key in list(dic.keys()):
        nb, nom = key
        for quest, lq in list(dic.get(key).items()):
            cpte, reponse = lq
            rep2 = reponse.replace("\n", "\\n")
            file.write(f"{nb};{nom};{quest};{cpte};{rep2};\n")
    file.close()


def save_score(score, demande):
    file = open("score.csv", "w+")
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
        pool.extend([k] * ((somquest - v) + 1))
    return rdm.choice(pool)


def choiceone(a, key):
    """fonction qui renvoie une question aléatoire dans le chapitre key
    """
    somquest = 0
    pool = []
    liitems = list(a.get(key).items())
    for k, v in liitems:
        somquest += v[0]
    for k, v in liitems: 
        pool.extend([k] * ((somquest - v[0]) + 1))
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


def revise_voc_in_console(a: dict = voc(), b: dict = voc()):
    """fonction principal
    """
    # récupération des chapitres de la bases
    listchap = list(a.keys())
    
    compteparchap = comptechap(a)

    # affichage de la requête pour l'utilisateur
    request = input(
        """Choisissez qu'UNE SEULE des propositions suivantes:
tout, {lst}

Liste à étudier (numéro des chapitres ou tout) (rien est considéré comme tout) = 
""".format(
            lst=", ".join(
                str(i) +":"+ str(j)
                for i,j in listchap
            )
        )
    )
    # contrôle des réponses
    while not re.findall("^(\d+(, *\d+)*|tout)?$", request):
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

            answer = input("{}, {} : {} \nscore = ".format(requestnb, requestnom, quest))
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
            print(f"réponse si ajouté est : {a[key][quest][1]}")
            i += 1

    # liste de chapitre 
    else:

        while i <= nb_demande and run:
            # liste des chaps en ["a", "b", "c"]
            reql = [str(int(j)) for j in request.split(",")]
            
            # liste des chaps qui sont encore dans la liste
            listechap = [i for i,j in list(a.keys()) if i in reql]

            # on sélection un des chapitres
            request, requestnom = choiceall(listechap, compteparchap)
            liste = request, requestnom
            
            # on sélectionne la question
            key = choiceone(a, liste)

            answer = input(
                    "{}, {} : {} \n score = ".format(
                            request, requestnom,
                            key
                        )
                )

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

            print(f"réponse si ajouté est : {a[key][quest][1]}")
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
    save(b)

    # pour sauvegarder les scores dans un fichier externe décommenter la ligne ci-dessous
    # save_score(compteur, i - 1)



if __name__ == "__main__":
    # éxécution du programme
    revise_voc_in_console()
    pass
