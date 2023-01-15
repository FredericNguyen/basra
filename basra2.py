import os, random

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

	def is_valet(self):
		return self.numero == "V"

	def carte_nb(self):
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

class Table(Paquet):
	super().__init__([])

	def ajoute_carte(self, carte: Carte):
		self.cartes.append(carte)

	def get_table(self):
		return self.cartes

	def update_table(self, pile: list): #on retire une combinaison gagnée
		for carte in pile:
			self.cartes.remove(carte)
	
	def table_vide(self):
		return not self.cartes

	def set_table(self, cartes: list):
		self.cartes = cartes
	
	def affiche_table(self): 
		for carte in self.cartes:
			print(f"{str(carte): >4}", end = "")
		print()

	def contient_deux_trefle(self):
		#return l'indice du 2 trefle dans la table , -1 dans le cas ou elle n'existe pas ou table vide
		if self.table_vide():
			return -1
		else:
			deux_trefle = carte("2","♣")
			for i, carte in enumerate(self.cartes):
				if carte == deux_trefle:
					return i
			return -1
	
	def contient_dix_carreau(self):
		if self.table_vide():
			return -1
		else:
			dix_carreau = carte("10","♦")
			for i, carte in enumerate(self.cartes):
				if carte == dix_carreau:
					return i
			return -1
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

		table = list(self.cartes)
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
			table = self.cartes
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


class Joeur(Paquet):
	def __init__(self) -> None:
		self.dealer = False
		self.tour_jouer = False
		self.ai = True
	
	super().__init__([])
	
	def affiche_jeu(self):
		if self.tour_jouer == False:
			cacher_carte = "▄"
			print(f"{cacher_carte:>4}"*len(self.cartes), end = "")
		else:
			self.affiche()

class AI:
	pass

class Table(Paquet):
	super().__init__([])

	def ajoute_carte(self, carte: Carte):
		self.cartes.append(carte)

	def get_table(self):
		return self.cartes

	def update_table(self, pile: list): #on retire une combinaison gagnée
		for carte in pile:
			self.cartes.remove(carte)
	
	def table_vide(self):
		return not self.cartes

	def set_table(self, cartes: list):
		self.cartes = cartes
	
	def affiche_table(self): 
		for carte in self.cartes:
			print(f"{str(carte): >4}", end = "")
		print()

	def contient_deux_trefle(self):
		#return l'indice du 2 trefle dans la table , -1 dans le cas ou elle n'existe pas ou table vide
		if self.table_vide():
			return -1
		else:
			deux_trefle = carte("2","♣")
			for i, carte in enumerate(self.cartes):
				if carte == deux_trefle:
					return i
			return -1
	
	def contient_dix_carreau(self):
		if self.table_vide():
			return -1
		else:
			dix_carreau = carte("10","♦")
			for i, carte in enumerate(self.cartes):
				if carte == dix_carreau:
					return i
			return -1
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

		table = list(self.cartes)
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
			table = self.cartes
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

class Partie:
	pass

class Jeu:
	def __init__(self) -> None:
		pass

	