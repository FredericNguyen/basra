# card = 10
# card1 = 10
# card2 = 2
# length = 4
# def capture(card1):
#     sortie = False
#     sum = []
#     while not sortie:
#         sum.append(card1)
#         if sum == card:
#             return sum
#         if card == length:
#             sortie = True
#         else:
#             capture(sum +card2)

import os, random

#Permet d'effacer ce qui est afficher à la console.
#Taken from https://stackoverflow.com/questions/2084508/clear-terminal-in-python
#By user: poke

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Carte:
    def __init__(self,  numero: str, couleur: str) -> None:
        self.numero = numero
        self.couleur = couleur
    
    def __str__(self) -> str:
        return self.numero + self.couleur
    
    def __eq__(self, autre_carte):
        if self.numero == autre_carte.numero and self.couleur == autre_carte.couleur:
            return True
        return False
        
    def __gt__(self, autre_carte): #pour les cartes non figures
        return int(self.numero ) > int(self.numero)

    def str_nb(self):
        return self.numero

    def valet(self):
        return self.numero == "V"
    
    def dame(self):
        return self.numero == "D"

    def roi(self):
        return self.numero == "R"
    
    def nb(self):
        return int(self.numero)

    def affiche_carte(self) -> None:
        print(f"{self}")

    def deux_trefle(self):
        return self.numero == "2" and self.couleur == "♣"

    def dix_carreau(self):
        return self.numero == "10" and self.couleur == "♦"
    
    def un_as(self):
        return self.numero == "1"
    
class Paquet:
    
    INDICE_MAX = 51
    LEN_STACK = 52
    LISTE_IMAGES = (Carte("V","♥"), Carte("V","♦"), Carte("V", "♣"),Carte("V", "♠"), 
                    Carte("D","♥"), Carte("D","♦"), Carte("D", "♣"),Carte("D", "♠"), 
                    Carte("R","♥"), Carte("R","♦"), Carte("R", "♣"),Carte("R", "♠") )
    
    def __init__(self) -> None:
        self.carte_jeu = [Carte(x, y) for y in ["♥","♦", "♣", "♠" ] 
                        for x in ["1", "2", "3","4","5","6","7","8","9","10", "V", "D", "R"]]
    
    def affiche_carte_jeu(self) -> None:
        for i in range(4):
            k = i*13 
            for j in range(k, k + 13):
                c = self.carte_jeu[j]
                print(f"{str(c): >4}", end = "")
            print()
    @staticmethod
    def affiche_pkt_joueur(pkt: list): # a le faire statique apres
        for carte in pkt:
            print(f"{str(carte): >4}", end = "")
        print()

    def brassage_inter_coupe(self) -> None:
        sub_carte1 = [self.carte_jeu[i] for i in range(26)]
        sub_carte2 = [self.carte_jeu[i] for i in range(26, 52)]
        for i in range(0, 52, 2):
            k = i//2
            self.carte_jeu[i], self.carte_jeu[i+1] = sub_carte1[k], sub_carte2[k]

    def brassage_par_paquets(self) -> None:
        pkt = [[] for i in range(13)]
        for i in range(13):
            k = i * 4
            pkt[i] = [self.carte_jeu[j] for j in range(k, k+4)]
        index = [6,0, 2, 12, 1, 3, 10, 5, 7, 4, 11, 9, 8]
        carte = []
        for idx in index:
            #carte.append(pkt[idx])
            carte += pkt[idx]
        self.carte_jeu = carte

    def brassage_par_hasard(self) -> None:
        limit = len(self.carte_jeu) - 1
        while limit > 0:
            index = random.randint(0,limit)
            self.carte_jeu[index], self.carte_jeu[limit] = self.carte_jeu[limit], self.carte_jeu[index]
            limit -= 1

    def couper_carte(self):
        k = random.randint(0, len(self.carte_jeu))
        coupe_1 = [self.carte_jeu[i] for i in range(k)]
        coupe_2 = [self.carte_jeu[i] for i in range(k,len(self.carte_jeu))]
        self.carte_jeu = coupe_2 + coupe_1

    def get_paquet_cartes_joueur(self, apartir_de: int, nombre: int):
        pt_suivant = apartir_de + nombre
        pkt = [self.carte_jeu[i] for i in range(apartir_de, pt_suivant)]
        return pkt, pt_suivant

    def get_paquet_cartes_table(self, apartir_de):
        nb = 0
        paket_table = []
        while nb < Partie_jeu.NB_CARTES_TABLE:
            if not self.carte_jeu[apartir_de].valet(): 
                paket_table.append(self.carte_jeu[apartir_de])
                apartir_de += 1
                nb += 1
            else:
                idx = random.randint(apartir_de +1, Paquet.INDICE_MAX)
                self.carte_jeu[apartir_de:] = self.carte_jeu[apartir_de + 1: idx] + [self.carte_jeu[apartir_de]] + self.carte_jeu[idx:]
        return  paket_table, apartir_de 

class Paquet_jeu(Paquet) :
     
    def __init__(self) -> None:
        super().__init__() 
        self.pt_carte = 0

    def distribuer_cartes(self, nb_joueurs : int, debut: bool):
        
        paket_de_jeu : list[list]
        paket_de_jeu = []
        for i in range(nb_joueurs):
            pkt_joueur, self.pt_carte = self.get_paquet_cartes_joueur(self.pt_carte, Partie_jeu.NB_CARTES_PAR_JOUEUR)
            paket_de_jeu.append(pkt_joueur)
        if debut:
            pkt_table, self.pt_carte = self.get_paquet_cartes_table(self.pt_carte)
            paket_de_jeu.append(pkt_table)
        return paket_de_jeu

class Table:
    def __init__(self, pile: list):
        self.cartes_table = pile

    def ajoute_carte(self, carte: Carte):
        self.cartes_table.append(carte)

    def get_table(self):
        return self.cartes_table

    def update_table(self, pile: list): #on retire une combinaison gagnée
        for carte in pile:
            self.cartes_table.remove(carte)
    
    def table_vide(self):
        return not self.cartes_table

    def set_table(self, cartes_table: list):
        self.cartes_table = cartes_table
    
    def affiche_table(self): 
        for carte in self.cartes_table:
            print(f"{str(carte): >4}", end = "")
        print()

    def contient_deux_trefle(self):
        #return l'indice du 2 trefle dans la table , -1 dans le cas ou elle n'existe pas ou table vide
        if self.table_vide():
            return -1
        else:
            deux_trefle = carte("2","♣")
            for i, carte in enumerate(self.cartes_table):
                if carte == deux_trefle:
                    return i
            return -1
    
    def contient_dix_carreau(self):
        if self.table_vide():
            return -1
        else:
            dix_carreau = carte("10","♦")
            for i, carte in enumerate(self.cartes_table):
                if carte == dix_carreau:
                    return i
            return -1
    @staticmethod
    def calcul_liste_somme(val: int, table: list[Carte], attente: list, result: list[list]):
        if table :
            if table[0].nb() == val:
                result.append(attente + [table[0]] )
                Table.calcul_liste_somme(val, table[1:], attente, result) 
            elif table[0].nb() < val:
                    val_1 = val - int(table[0].str_nb())
                    Table.calcul_liste_somme(val_1, table[1:], attente + [table[0]], result)
                    Table.calcul_liste_somme(val, table[1:], attente, result )
            else:
                Table.calcul_liste_somme(val, table[1:], attente, result)
    @staticmethod
    def score_combinaison(comb: list):
        score = 0
        for c in comb:
            if c.deux_trefle():
                score += 2
            elif c.dix_carreau():
                score += 3
            elif c.valet() or c.un_as():
                score += 1
        return score
    @staticmethod    
    def ecarter_images(table: list):
        table_1 = []
        for elem in table:
            if not elem in  Paquet.LISTE_IMAGES:
                table_1.append(elem)
        return table_1
    
    def trouve_liste_choix_joueur(self) -> dict:

        def ajoute(liste_choix: dict, ky: str, c: Carte):
            if ky in liste_choix:
                    liste_choix[ky].append(c)
            else:
                liste_choix[ky] = [c]

        table = list(self.cartes_table)
        liste_choix : dict
        liste_choix = {}
        for c in table:
            if c in Paquet.LISTE_IMAGES:
                ajoute(liste_choix, c.str_nb(), c)
        table = Table.ecarter_images(table)    
        for c in table:
            val = c.nb()
            if not c.str_nb() in liste_choix:
                result = []
                Table.calcul_liste_somme(val, table, [], result)
                liste_choix[c.str_nb()] = result
            else:
                if not [c] in liste_choix[c.str_nb()]:
                    liste_choix[c.str_nb()].append([c])
        return liste_choix
    
    def trouve_combinaisons_ganante(self, c: Carte, liste_choix: dict):
        
        def intersecte(liste_1: list, liste_2: list):
            for elem in liste_1:
                if elem in liste_2:
                    return True
            return False
        resultat = []
        temp = []
        chr_nb = c.str_nb()
        if chr_nb in liste_choix: 
            if c in Paquet.LISTE_IMAGES:
                return liste_choix[chr_nb]
            temp = list(liste_choix[chr_nb])
        else:
            table = self.cartes_table
            if c in Paquet.LISTE_IMAGES:
                res = []
                for elem in table:
                    if c.str_nb() == elem.str_nb():
                        res.append(elem)
                return res
            table = Table.ecarter_images(table)
            Table.calcul_liste_somme(c.nb(), table, [], temp)
        fin = False
        while not fin:
            if temp:
                intersect_list = [temp[0]]
                scr = Table.score_combinaison(temp[0])
                res = temp[0]
                for comb in temp[1:]:
                    if intersecte(comb, temp[0]):
                        intersect_list.append(comb)
                        scr_c = Table.score_combinaison(comb)
                        if scr < scr_c:
                            res = comb
                            scr = scr_c
                        elif scr == scr_c:
                            if len(res) < len(comb):
                                res = comb
                resultat.append(res)
                for c in intersect_list:
                    if intersecte(res, c):
                        temp.remove(c) 
            else:
                fin = True
        resultat_final = []
        for elem in resultat:
            resultat_final += elem
        return resultat_final        

class Joueur_Carte:
    
    def __init__(self, nom: str, table: Table, compteur_cartes_non_jouees):
       self.cartes_joueur = []
       self.cartes_gagnees = [] 
       self.table = table
       self.nom == nom
       self.super_gain = 0
       self.compteur_cartes_non_jouees = compteur_cartes_non_jouees 
    
    def contient_dix_carreau(self):
        dix_carreau = carte("10","♦")
        for i, carte in enumerate(self.cartes_joueur):
            if carte == dix_carreau:
                return i
        return -1
    
    def possede_nb(self, n: str):
        rdx, nb = -1, 0
        for i, carte in enumerate(self.cartes_joueur):
            if carte.nb() == n:
                nb += 1
                if rdx < 0:
                    rdx = i
        return i, nb 

    def affiche_cartes_joueur(self):
        for carte in self.cartes_joueur:
            print(f"{str(carte): >4}", end = "")
        print()

    def affiche_cartes_cachees(self):
        ch = "▄"
        for carte in self.cartes_joueur:
            print(f"{ch:>4}", end = "")

    def longueur_pile_gagne(self):
        return len(self.cartes_gagnees)

    def set_cartes_joueur(self, cartes_joueur: list):
        self.cartes_joueur = cartes_joueur
        
    def get_score(self):
    
        for carte in self.cartes_gagnees:    
            if carte.dix_carreau():
                score += 3
            elif carte.deux_trefle():
                score += 2
            elif carte.valet() or carte.un_as() :
                score += 1
            
    def contient_deux_trefle(self):
        #return l'indice du 2 trefle dans la table , -1 dans le cas ou elle n'existe pas ou table vide
        deux_trefle = carte("2","♣")
        for i, carte in enumerate(self.cartes_joueur):
            if carte == deux_trefle:
                return i
        return -1
    def update_compteurs_cartes_non_jouees(self, c: Carte):
        self.compteur_cartes_non_jouees[c.str_nb()] -= 1
    
    def update_compteurs_cartes_non_jouees(self, pile: list[Carte]):
        for carte in pile:
            self.update_compteurs_cartes_non_jouees(carte)

    def listes_cartes_restants(self):
        resultat = []
        for carte in self.cartes_joueur:
            resultat.append([carte, self.compteur_cartes_non_jouees[carte.str_nb()]])
        l = len(resultat) - 1
        fin = False
        for i in range(l) and not fin:
            fin = True
            for j in range(l-i):
                if resultat[j][1] < resultat[j+1][1]:
                    resultat[j][1], resultat[j+1][1] = resultat[j+1][1] < resultat[j][1]
                    fin = False
        return resultat

    def image_jouee(self):
        carte_a_jouer = None
        rdx1, nb1 = self.possede_nb("R")
        rdx2, nb2 = self.possede_nb("D")
        if rdx1 >= 0 or rdx2 >= 0:
            if nb1 > nb2:
                carte_a_jouer = self.cartes_joueur[rdx1]
            elif  nb1 < nb2:
                carte_a_jouer = self.cartes_joueur[rdx2]
            elif nb1 > 0:
                k = random.randint(1)
                l = [rdx1, rdx2]
                carte_a_jouer = self.cartes_joueur[l[k]]
        if carte_a_jouer != None:
            self.update_compteurs_cartes_non_jouees(carte_a_jouer)
            self.table.get_table().append(carte_a_jouer)
            self.cartes_joueur.remove(carte_a_jouer)
            self.update_compteurs_cartes_non_jouees(carte_a_jouer)
        return carte_a_jouer != None

    def ramasser_table(self, rdx : int): 
        t = self.table.get_table()
        l = self.table.get_table() + [self.cartes_joueur[rdx]]
        self.cartes_gagnees += l
        self.update_compteurs_cartes_non_jouees(l)
        self.cartes_joueur.remove(self.cartes_joueur[rdx])
        self.table.set_table([])

    def determine_carte_a_jouer_somme_moins_10(self, somme_cartes_table: int):
        somme_numbers = []
        for i, carte in enumerate(self.cartes_joueur):
            ch = str(carte.nb() + somme_cartes_table)
            occ = self.compteur_cartes_non_jouees[ch]
            somme_numbers.append([ch,occ,i])
        min = somme_numbers[0][1]
        for elem in somme_numbers:
            if min > elem[1]:
                min = elem[1]
        indices = []
        for elem in somme_numbers:
            if min == elem[1]:
                indices.append(elem[2])
        return self.carte_joueur[indices[random.randint(len(indices) - 1)]]

    def traite_cas_une_carte_a_table(self, dernier_etape: bool):
        
        def choisir_carte(carte_table: Carte):
            list_cartes = self.listes_cartes_restants()
            for elem in list_cartes:
                if carte_table in Paquet.list_IMAGES:
                    if not elem[0].deux_trefle(self) and not elem[0].dix_carreau(self):
                        return elem[0]
                elif elem[0].nb() + carte_table.nb() > 10:
                    return elem[0]
            return self.determine_carte_a_jouer_somme_moins_10(carte_table.nb())
        t = self.table.get_table()
        rdx, n = self.possede_nb(t[0].nb())
        if rdx >= 0:
           self.super_gain += 10
           self.ramasser_table(rdx)
        else:
            rdx, n = self.possede_nb("V") 
            if n >= 2:
                self.ramasser_table(rdx)    
            elif n == 1 and dernier_etape:
                self.ramasser_table()
            elif n == 1 and len(self.carte_joueur) == 2:
                self.ramasser_table()
            elif n == 1 and random.randint(1) == 0:
                self.ramasser_table(rdx)
            elif not self.image_jouee():
                pass   

class Partie_jeu:
    USER = 0
    NB_CARTES_TABLE = 4
    NB_CARTES_PAR_JOUEUR = 6
    def __init__(self, pkt_jeu : Paquet_jeu, nb_joueurs: int):
        self.joueurs = [Joueur_Carte]
        self.score_1, self.score_2  = 0, 0 # score des deux groupes
        self.joueurs.append(Joueur_Carte(input("Nom du joueur de l'utilisateur:")))
        self.joueurs += [Joueur_Carte(input(f"Nom du joueur #{i+1}: ")) for i in range(1, nb_joueurs)]
        self.pkt_jeu = Paquet_jeu()
        self.table = Table()
        self.compteur_cartes_non_jouees = {}
        self.debuteur = self.determiner_debuteur()
        
    def determiner_debuteur(self):
        self.pkt_jeu.brassage_par_hasard()
        l = len(self.pkt_jeu) - 1
        rdx_d = random.randint(l)
        carte_d = self.pkt_jeu[rdx_d]
        debut = self.USER
        for i in range(1, self.len(self.joueurs)):
            self.pkt_jeu = self.pkt_jeu[:rdx_d] + self.pkt_jeu[rdx_d + 1:] + [carte_d]
            rdx_c = random.randint(l - i)
            if  self.pkt_jeu[rdx_c] > carte_d:
                debut = i
                carte_d = self.pkt_jeu[rdx_c]
            elif carte_d == self.pkt_jeu[rdx_c] :
               gr = (debut, i )
               debut = gr[random.randint(1)]
        return  debut 

    def update_score_groupes(self):
        #appelée a la fin de chaque jeu
        nb_joueurs = len(self.joueurs)
        index = ((self.debuteur + i) % nb_joueurs for i in range(nb_joueurs)) 
        if nb_joueurs == 4:
            self.score_1 += self.joueurs[index[0]].get_score() + self.joueurs[index[2]].get_score() 
            self.score_2 += self.joueurs[index[1]].get_score() + self.joueurs[index[3]].get_score()
            longueur_1 = self.joueurs[index[0]].longueur_pile_gagne() + self.joueurs[index[2]].longueur_pile_gagne()
            longueur_2 = self.joueurs[index[0]].longueur_pile_gagne() + self.joueurs[index[2]].longueur_pile_gagne()
        else:
            self.score_1 += self.joueurs[index[0]].get_score()  
            self.score_2 += self.joueurs[index[1]].get_score() 
            longueur_1 = self.joueurs[index[0]].longueur_pile_gagne() 
            longueur_2 = self.joueurs[index[0]].longueur_pile_gagne() 
        if longueur_1 > longueur_2:
            longueur_1 += 3
        elif longueur_2 > longueur_2:
            longueur_2 += 3
        if self.score_1 >= 101 or self.score_2 >= 101:
            if self.nb_joueurs == 4:
                if self.score_1 > self.score_2:
                    return (True, self.joueurs[index[0]].nom, self.joueurs[index[2]].nom, self.score_1)
                else:
                    return (True, self.joueurs[index[1]].nom, self.joueurs[index[3]].nom, self.score_2)
            else:
                if self.score_1 > self.score_2:
                    return (True, self.joueurs[index[0]].nom, self.score_1)
                else:
                    return (True, self.joueurs[index[1]].nom, self.score_2)
        return (False)

    def init_compteurs_cartes_non_jouees(self) :  
        self.compteur_cartes_non_jouees = {str(i) : 4 for i in range(1,11)}
        self.compteur_cartes_non_jouees["V"] = 4
        self.compteur_cartes_non_jouees["D"] = 4
        self.compteur_cartes_non_jouees["R"] = 4
    
    def affiche_jeu(self):
        def deplacer_curseur():
            ch = " "
            print(f"{ch: >24}",end = "")
            print("\t\t", end = "" )
        if len(self.joueurs) == 4:  
            self.joueurs[2].affiche_cartes_cachees()
            (print() for i in range(2))
            self.joueurs[3].affiche_cartes_cachees()
            print("\t\t", end = "")
            self.table.affiche_table()
            print("\t\t", end = "")
            self.joueurs[1].affiche_cartes_cachees()
            deplacer_curseur()
            self.joueurs[0].affiche_cartes_joueur()
        else:
            deplacer_curseur()
            self.joueur[1].affiche_cartes_cachees()
            (print() for i in range(2))
            deplacer_curseur()
            self.table.affiche_table()
            print()
            deplacer_curseur()
            self.joueurs[0].affiche_cartes_joueur()
            
    def determine_carte_a_jouer_table_vide(self, cartes_joueur: list):
        min = self.compteur_cartes_non_jouees["1"]
        for c in cartes_joueur:
            str_nbr = c.str_nb()
            if self.compteur_cartes_non_jouees[str_nbr] < min:
                min = self.compteur_cartes_non_jouees[str_nbr]
        min_cartes = []
        for carte in cartes_joueur:
            if self.compteur_cartes_non_jouees[carte.str_nb()] == min:
                min_cartes.append(carte)
        return min_cartes[random.randint(len(min_cartes) - 1)]

    def effectuer_etape(self, numero_etape: int):
        nb_joueur = len(self.joueurs)
        pkt = self.pkt_jeu.distribuer_cartes(nb_joueur, numero_etape)
        for i, joueur in enumerate(self.joueurs):
            joueur.set_cartes_joueur(self, pkt[i])
        if not numero_etape:  #premiere etape, on doit initialiser la table
            self.table.set_table(pkt[nb_joueur])
        pass
    def effectuer_jeu(self):
        nb_etapes = {2: 4, 3: 2, 4: 2}
        self.pkt_jeu.brassage_par_hasard()
        self.pkt_jeu.couper_carte()
        compteurs = Partie_jeu.init_compteurs_cartes()
        for i in range(nb_etapes[len(self.joueurs)]):
           self. effectuer_etape()
        pass

cls()  
p = Paquet_jeu()
p.brassage_par_hasard()
p.couper_carte()
p.affiche_carte_jeu()
print()
print()
p.brassage_inter_coupe()
#p.affiche_carte_jeu()
paket_de_jeu = p.distribuer_cartes(4, True, 2)
for pkt in paket_de_jeu:
    p.affiche_pkt_joueur(pkt)
print()
rdx = random.randint(0, 5)
c = paket_de_jeu[2][rdx]
table = Table(paket_de_jeu[3]+ paket_de_jeu[4])
print("Carte de la table")
table.affiche_table()
d : dict
d = table.trouve_liste_choix_joueur()
print("Dictionnaire de choix:")
for ky, com in d.items():
    print(f"Liste de la {ky}: ")
    if( ky == "V" or ky == "D" or ky == "R"):
        for carte in com:
            print(f"{str(carte): >4}", end = "")
        print()
    else:
        for l in com:
            for carte in l:
                print(f"{str(carte): >4}", end = "")
            print()
print(f"La carte a jouer etait {str(c)}")
resultat = table.trouve_combinaisons_ganante(c, d)
print("Combinaison apres enlever les intersections")
for carte in resultat:
        print(f"{str(carte): >4}", end = "")
print()

#val = int(input("Numero de carte a jouer: "))
#result = []
#Paquet.calcul_liste_somme(val, table, [], result)
#for l in result:
    #p.affiche_pkt_joueur(l)
#d = Partie_jeu.init_compteurs_cartes()
#print(d)

