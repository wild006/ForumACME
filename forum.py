#!/usr/bin/env python3

from tkinter import *
from multilistbox import *

class User():
    def __init__(self, _id, nom, prenom, username, passwd, mail):
        self.id = _id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.passwd = passwd
        self.mail = mail

class Message():
    def __init__(self, _id, text, date, auteur,reponse, sujetid):
        self.id = _id
        self.texte = text
        self.date = date
        self.auteur = auteur
        self.reponse = reponse
        self.sujetid = sujetid
        
class Sujet():
    def __init__(self, _id, nom, date, nbMessages, dernier, parent):
        self.id = _id
        self.nom = nom
        self.date = date
        self.nbMessages = nbMessages
        self.dernier = dernier
        self.parent = parent

class SujetVue():
    def __init__(self, commandes):
        self.forum = Tk()
        self.commandes = commandes
        
        self.boxSujet = MultiListbox(self.forum, (('Message', 40), ('Date', 20), ('Nombre de messages', 10)))
        self.sujets = [] # Tous les sujets
        self.remplirListe()
        self.boxSujet.pack(expand=YES,fill=BOTH)

        Button(self.forum, text="Visioner", command=lambda: self.visioner(self.boxSujet.curselection())).pack()
        Button(self.forum, text="Supprimer", command=lambda: self.supprimer(self.boxSujet.curselection())).pack()
        Button(self.forum, text="Ajouter", command=self.ajouter).pack()

    def remplirListe(self):
        self.boxSujet.delete(0, END)
        self.sujets = self.commandes.searchSujets() #[Sujet(1, "Un", "hier", "2", "demain", None), Sujet(2, "Deux", "demain", "3", "hier", None)]
        for sujet in self.sujets:
            self.boxSujet.insert(END, ('Important Message: ' + sujet.nom, sujet.date, sujet.nbMessages))

    def visioner(self, event):
        MessageVue(event[0], self.commandes)

    def supprimer(self, event):
        indiceSujetListe = event[0]
        sujetASupprimer = self.sujets[indiceSujetListe]
        self.commandes.supprimerSujetParID(sujetASupprimer.id)
        self.remplirListe()
        
    def ajouter(self):
        nsujet = Tk()
        Label(nsujet, text="Titre").grid(column = 0, row = 0)
        titre = Entry(nsujet)
        titre.grid(column = 1, row = 0)
        Button(nsujet, text="Go", command=lambda:self.nouveau_sujet(nsujet, titre.get())).grid()

    def nouveau_sujet(self, nsujet, titre):
        self.commandes.ajouteSujet(titre)
        nsujet.destroy()
        self.remplirListe()
        
class MessageVue():
    def __init__(self, n, commandes):
        """Affiche les messages du sujet a l'id `n'"""
        self.commandes = commandes
        self.id = int(n) + 1
        self.mess = Tk()

        self.mess.title = self.commandes.trouveTitreSujetByID(self.id) # Voir l'item du TODO

        self.message = MultiListbox(self.mess, (('Texte', 40), ('Auteur', 20), ('Date', 10)))
        self.message.pack(expand=YES, fill=BOTH)
        self.messages = [] # Tous les messages de la liste
        self.remplirListe()

        Button(self.mess, text="Ajouter", command=self.ajouter).pack()
        Button(self.mess, text="Répondre", command=lambda: self.repondre(self.message.curselection()).pack()
        Button(self.mess, text="Supprimer", command=lambda: self.supprimer(self.message.curselection())).pack()

    def remplirListe(self):
        self.message.delete(0, END)
        self.messages = self.commandes.searchMessages(self.id) #[Message(1, "Premier", "Jamais", "Moi", self.id, self.id), Message(2, "Second", "Toujours", "L'autre", self.id, self.id)]
        for m in self.messages:
            m.texte = self.chopMessage(m)
            self.message.insert(END,(m.texte, m.auteur, m.date))

    def chopMessage(mess):
        achop = False
        result = ""
        for i in range(len(mess)):
            if (i % 80) == 0:
                achop = True
            if achop and mess.texte[i] == ' ':
                result += '\n'
                achop = False
            result += mess.texte[i]
        return result
            
    def ajouter(self, message=""):
        nmess = Tk()
        texte = Text(nmess)
        texte.insert(END, message)
        texte.pack()
        Button(nmess, text="Envoyer", command=lambda: self.nouveau_message(nmess, texte)).pack()

    def nouveau_message(self, nmess, texte):
        self.commandes.ajouteMessage(texte.get("1.0", END), self.id) # END ajoute un \n à la fin. On veut ça?
        nmess.destroy()
        self.remplirListe()

    def supprimer(self, n):
        indiceMessageListe = n[0]
        messageAsupprimer = self.messages[indiceMessageListe]
        self.commandes.supprimerMessageParID(messageAsupprimer.id, self.id)
        self.remplirListe()

    def repondre(self, n):
        indiceMessageListe = n[0]
        messageArepondre = self.messages[indiceMessageListe]
        message = self.commandes.getTexteMessageAvecAuteurAuDebutParID(messageArepondre) # C'est clair? Enfin, dans l'idée c'est ça.
        self.ajouter(message)
