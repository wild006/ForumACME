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
        sujets = self.commandes.searchSujets() #[Sujet(1, "Un", "hier", "2", "demain", None), Sujet(2, "Deux", "demain", "3", "hier", None)]
        for sujet in sujets:
            self.boxSujet.insert(END, ('Important Message: ' + sujet.nom, sujet.date, sujet.nbMessages))

    def visioner(self, event):
        MessageVue(event[0], self.commandes)

    def supprimer(self, event):
        self.commandes.supprimerSujetParID(event[0]) # TODO: Le faire :D
        self.remplirListe()
        
    def ajouter(self):
        nsujet = Tk()
        Label(nsujet, text="Titre").grid(column = 0, row = 0)
        titre = Entry(nsujet)
        titre.grid(column = 1, row = 0)
        Label(nsujet, text="Sujet").grid(column = 0, row = 1)
        sujet = Entry(nsujet)
        sujet.grid(column = 1, row = 1)
        Button(nsujet, text="Go", command=lambda:self.nouveau_sujet(nsujet, titre.get(), sujet.get())).grid()

    def nouveau_sujet(self, nsujet, titre, sujet):
        self.commandes.ajouteSujet(titre, sujet)
        nsujet.destroy()
        self.remplirListe()
        
class MessageVue():
    def __init__(self, n, commandes):
        """Affiche les messages du sujet a l'id `n'"""
        self.commandes = commandes
        self.id = int(n) + 1
        self.mess = Tk()
        self.message = MultiListbox(self.mess, (('Texte', 40), ('Auteur', 20), ('Date', 10)))
        self.message.pack(expand=YES, fill=BOTH)
        self.messages = [] # Tous les messages de la liste
        self.remplirListe()

        Button(self.mess, text="Ajouter", command=self.ajouter).pack()
        Button(self.mess, text="Supprimer", command=lambda: self.supprimer(self.message.curselection())).pack()

    def remplirListe(self):
        self.message.delete(0, END)
        messages = self.commandes.searchMessages(self.id) #[Message(1, "Premier", "Jamais", "Moi", self.id, self.id), Message(2, "Second", "Toujours", "L'autre", self.id, self.id)]
        for m in messages:
            self.message.insert(END,(m.texte, m.auteur, m.date))

    def ajouter(self):
        nmess = Tk()
        texte = Text(nmess)
        texte.pack()
        Button(nmess, text="Envoyer", command=lambda: self.nouveau_message(nmess, texte)).pack()

    def nouveau_message(self, nmess, texte):
        self.commandes.ajouteMessage(texte.get("1.0", END), self.id) # END ajoute un \n à la fin. On veut ça?
        nmess.destroy()
        self.remplirListe()

    def supprimer(self, n):
        self.commandes.supprimerMessageParID(event[0], self.id) # TODO: Prend l'id du sujet pour trouver le bon message
        self.replirListe()
