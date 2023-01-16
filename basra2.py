import os, random

def min(list_nb):
	min_card = 0
	for card in list_nb:
		if card < min_card:
			min_card = card
	return min_card
	
def sort_ascending(cartes:list):
	sortie = False
	ascending_list = []
	while not sortie:
		if len(cartes) == 0:
			sortie = True
		else:
			min_card = min(cartes)
			ascending_list.append(min_card)
	return ascending_list

class Carte:
	def __init__(self,  numero: str, couleur: str) -> None:
		self.numero = numero
		self.couleur = couleur
	
	def __str__(self) -> str:
		return self.numero + self.couleur
	
	def __eq__(self, autre_carte:object):
		if self.numero == autre_carte.numero:
			return True
		return False

	def __lt__(self, autre_carte): #pour les cartes non figures
		return int(self.numero ) < int(self.numero)

	def __add__(self, autre_carte:object):
		return self.nb() + autre_carte.nb()

	def is_valet(self):
		return self.numero == "V"

	def nb(self):
		return int(self.numero)

	def affiche_carte(self) -> None:
		if self.numero == "1":
			print(f"A{self.couleur:<4}", end="")
		else:
			print(f"{self.numero + self.couleur:<4}", end="")

	def is_deux_trefle(self):
		return self.numero == "2" and self.couleur == "♣"

	def is_dix_carreau(self):
		return self.numero == "10" and self.couleur == "♦"
	
	def is_as(self):
		return self.numero == "1"

class Paquet:
	def __init__(self, cartes:list) -> None:
		self.cartes = cartes

	def affiche(self):
		for carte in self.cartes:
			carte.affiche_carte()
		print()

class Paquet_Du_jeu(Paquet):
	def initial():
		NUMBERS = [str(i) for i in list(range(1,11))]
		ROYAL = ["V", "D", "R"]
		COULEURS = ["♥","♦", "♣", "♠" ]
		carte_jeu = [Carte(x, y) for y in COULEURS for x in NUMBERS + ROYAL]
		return carte_jeu

	super().__init__(initial())

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

	def get_paquet_joueur(self):
		paquet_joeur_length = 4
		paquet = self.carte_jeu[0:paquet_joeur_length]
		self.carte_jeu = self.carte_jeu[paquet_joeur_length:]
		return paquet

	def get_paquet_cartes_table(self):
		nb = 0
		paquet_table = []
		sortie = False
		while not sortie:
			if len(paquet_table) == 4:
				sortie = True
				return paquet_table
			elif self.carte_jeu[0].is_valet:
				self.carte_jeu.insert(random.randint(len(paquet_table) + 1, len(self.carte_jeu)), self.carte_jeu[0])
				self.carte_jeu.pop(0)
			else:
				paquet_table.append(self.carte_jeu[0])
				self.carte_jeu.pop(0)

class Table():
	def __init__(self, paquet:Paquet) -> None:
		self.paquet = paquet
		self.basra = False

	def ajoute_carte(self, carte: Carte):
		self.paquet.cartes.append(carte)

	def get_table(self):
		return self.paquet.cartes

	def update_table(self, pile: list): #on retire une combinaison gagnée
		for carte in pile:
			self.paquet.cartes.remove(carte)
	
	def table_vide(self):
		return not self.paquet.cartes

	def set_table(self, cartes: list):
		self.paquet.cartes = cartes
	
	def affiche_table(self): 
		for carte in self.paquet.cartes:
			print(f"{str(carte): >4}", end = "")
		print()
	
	def ascending_card_nbs(self, carte_joeur:Carte):
		nb_cards_only = []
		for carte_table in self.get_table():
			if carte_table.isnumeric():
				nb_cards_only.append(carte_table)
		nb_cards_only = sort_ascending(nb_cards_only)
		exclude_higher_card = []
		for card in nb_cards_only:
			if card < carte_joeur:
				exclude_higher_card.append(nb_cards_only)
		return exclude_higher_card

	def find_duplicates(self, carte_joeur:Carte):
		combination_duplicates = []
		found_duplicates = []
		table = self.get_table()
		for table_carte in table:
			if table_carte == carte_joeur:
				found_duplicates.append(table_carte)
				combination_duplicates.append(found_duplicates)
		self.update_table(found_duplicates[-1])
		return combination_duplicates
	
	def sum_cards(cartes:list):
		sum_cartes = 0
		if len(cartes) == 0:
			return 0
		elif len(cartes) == 1:
			return cartes[0].nb()
		for carte in cartes:
			sum_cartes += carte.nb()
		return sum_cartes

	def table_combinaisons(self, cartes:list, somme_objectif:int, somme_table=[]):
		list_combinations = []
		somme_table = somme_table
		if self.sum_cards(somme_table) == somme_objectif:
			list_combinations.append(somme_table)
		if self.sum_cards(somme_table) >= somme_objectif:
			return list_combinations
		for i in range(len(cartes)):
			carte_verif = cartes[i]
			cartes_restantes = cartes[i+1:]
		list_combinations.append(self.table_combinaisons(cartes_restantes, somme_objectif, somme_table + [carte_verif]))

	def choix_joeur(self, carte_joeur:Carte):
		if self.table_vide():
			self.ajoute_carte(carte_joeur)
			return {"1" : Paquet([carte_joeur])}
		elif carte_joeur.is_valet():
			return {"1" : Paquet([carte_joeur] + self.paquet.cartes)}
		else:
			temp_table = self
			possibilites_capture = temp_table.find_duplicates()
			if carte_joeur.numero.isnumeric():
				possibilites_capture + temp_table.table_combinaisons(temp_table.ascending_card_nbs(carte_joeur), carte_joeur.nb())
			return possibilites_capture


class Joeur():
	def __init__(self, paquet:Paquet) -> None:
		self.dealer = False
		self.tour_jouer = False
		self.ai = True
		self.paquet = paquet
	
	def affiche_jeu(self):
		if self.tour_jouer == False:
			cacher_carte = "▄"
			print(f"{cacher_carte:>4}"*len(self.paquet.cartes), end = "")
		else:
			self.paquet.affiche()



class AI:
	pass

class Partie:
	pass

class Jeu:
	def __init__(self) -> None:
		pass

	