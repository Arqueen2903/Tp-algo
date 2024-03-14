import csv
from datetime import datetime

class Client:
    def __init__(self, nom, date_naissance, abonnes):
        self.nom = nom
        self.date_naissance = date_naissance
        self.abonnes = abonnes
        self.facture = 0.0

class GestionClients:
    def __init__(self):
        self.clients = []

    def ajouter_client(self, client):
        self.clients.append(client)

class ImportCDR:
    @staticmethod
    def importer_fichier(fichier):
        cdrs = []
        with open(fichier, 'r') as f:
            for line in f:
                cdr = line.strip().split('|')
                cdrs.append(cdr)
        return cdrs

class Facturation:
    TARIFS = {
        'sms': { 'meme_reseau': 0.001, 'autre_reseau': 0.002 },
        'appel': { 'meme_reseau': 0.025, 'autre_reseau': 0.05 },
        'internet': 0.03
    }

    @staticmethod
    def calculer_facture(cdrs, client):
        for cdr in cdrs:
            if cdr[3] in client.abonnes:
                type_call = int(cdr[1])
                duree = int(cdr[5]) if cdr[5] else 0
                total_volume = int(cdr[7]) if cdr[7] else 0
                taxe = int(cdr[6])

                if type_call == 0: # Appel
                    tarif = Facturation.TARIFS['appel']['meme_reseau'] if cdr[3] == cdr[4] else Facturation.TARIFS['appel']['autre_reseau']
                    client.facture += duree / 60 * tarif
                elif type_call == 1: # SMS
                    tarif = Facturation.TARIFS['sms']['meme_reseau'] if cdr[3] == cdr[4] else Facturation.TARIFS['sms']['autre_reseau']
                    client.facture += tarif
                elif type_call == 2: # Internet
                    client.facture += total_volume * Facturation.TARIFS['internet']

        if taxe == 1: # ACCISE
            client.facture *= 1.10
        elif taxe == 2: # TVA
            client.facture *= 1.16

class Statistique:
    @staticmethod
    def statistiques(cdrs, client):
        stats = { 'appels': 0, 'duree_appels': 0, 'sms': 0, 'internet': 0 }
        for cdr in cdrs:
            if cdr[3] in client.abonnes:
                type_call = int(cdr[1])
                duree = int(cdr[5]) if cdr[5] else 0
                total_volume = int(cdr[7]) if cdr[7] else 0

                if type_call == 0: # Appel
                    stats['appels'] += 1
                    stats['duree_appels'] += duree
                elif type_call == 1: # SMS
                    stats['sms'] += 1
                elif type_call == 2: # Internet
                    stats['internet'] += total_volume
        return stats

# Utilisation des classes
gestion_clients = GestionClients()
client_polytechnique = Client("POLYTECHNIQUE", datetime(1980, 1, 1), ["243818140560", "24381814012"])
gestion_clients.ajouter_client(client_polytechnique)

cdrs1 = ImportCDR.importer_fichier("cdr.txt")
print("CDRs importés : ", cdrs1)  # Ajout d'une déclaration print pour le débogage
cdrs2= ImportCDR.importer_fichier("tp_algo.txt")
print("CDRs2 importés : ", cdrs2)
cdrs= cdrs1+cdrs2
Facturation.calculer_facture(cdrs, client_polytechnique)
print(f"Facture pour le client {client_polytechnique.nom} : {client_polytechnique.facture} $")  # Ajout d'une déclaration print pour le débogage

stats = Statistique.statistiques(cdrs, client_polytechnique)
print(f"Statistiques pour le client {client_polytechnique.nom} : ", stats)  # Ajout d'une déclaration print pour le débogage
