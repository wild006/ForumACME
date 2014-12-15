#!/usr/bin/env python3

from tkinter import *
import tkinter.ttk  as ttk #Pour le combo Box
from multilistbox import *
from autocompleteEntry import *
from testMessageCanvas import *
import getpass

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
            self.boxSujet.insert(END, (sujet.nom, sujet.date, sujet.nbMessages))

    def visioner(self, event):
        MessageVue(self.sujets[int(event[0])].id, self.commandes, self.forum)

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
    def __init__(self, n, commandes, root):
        """Affiche les messages du sujet a l'id `n'"""
        self.commandes = commandes
        self.id = int(n)
        self.forum = root
        self.mess = Toplevel(self.forum)

        self.mess.title(self.commandes.trouveTitreSujetByID(self.id)) # Voir l'item du TODO
        self.messageGraphic = []
        #self.message = MultiListbox(self.mess, (('Texte', 40), ('Auteur', 20), ('Date', 10)))
        #self.message.pack(expand=YES, fill=BOTH)
        self.messages = [] # Tous les messages de la liste

        #Mettre un canvas pour le scroll
        frame = Frame(self.mess, bd=2, relief=SUNKEN)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.yscrollbar = Scrollbar(frame)
        self.yscrollbar.grid(row=0, column=1, sticky=N+S)

        self.canevas = Canvas(frame, bd=0, scrollregion=(0, 0, 1000, 1000),
                yscrollcommand=self.yscrollbar.set)
        self.canevas.grid(row=0, column=0, sticky=N+S+E+W)

        self.yscrollbar.config(command=self.canevas.yview)

        frame.pack()
        # Choix du Order by
        self.panelHaut = PanedWindow(self.canevas,orient=HORIZONTAL)
        self.canevas.create_window((0,0),window=self.panelHaut,anchor='nw', tags="panelHaut")
        
        self.choixOrder = ('Date croisante', 'Date décroisant', 'Nom (A-Z)', 'Nom (Z-A)')
        self.listeOrder = ttk.Combobox(self.panelHaut,values = self.choixOrder, state = 'readonly')
        self.listeOrder.set(self.choixOrder[0])
        self.listeOrder.pack(side=RIGHT)

        #self.searchField = Entry(self.panelHaut)
        self.searchField = AutocompleteEntry(self.commandes, self.canevas)
       
        
        self.panelHaut.pack()

        self.searchField.pack()
        
        #scrollbar = Scrollbar(self.mess)
        #scrollbar.pack(side=RIGHT, fill=Y)
        #self.canevas = Canvas(self.mess, bd=0, highlightthickness=0,yscrollcommand=scrollbar.set)
        #scrollbar.config(command=self.canevas.yview)
        #self.canevas.pack()
        #self.m = self.canevas.create_window((0,0),window=PanedWindow(self.canevas,orient=VERTICAL),anchor='nw')
        self.m = PanedWindow(self.canevas,orient=VERTICAL)
        self.canevas.create_window((0,0),window=self.m,anchor='nw', tags="panelMessage")
        self.m.pack()
        self.remplirListe()
        #self.m.pack()
        self.canevas.tag_raise("panelHaut")
        self.canevas.tag_lower("panelMessage")
        #events
        self.mess.bind_all("<MouseWheel>",self.scroll)
        self.yscrollbar.bind('<ButtonRelease-1>',self.scroll)
        self.listeOrder.bind('<<ComboboxSelected>>', self.onComboBox)
        self.searchField.bind('<Key>', self.onSearchField)
        
        Button(self.canevas, text="Ajouter", command=self.ajouter).pack()
        #Button(self.canevas, text="Répondre", command=lambda: self.repondre(self.message.curselection())).pack()
        #Button(self.canevas, text="Supprimer", command=lambda: self.supprimer(self.message.curselection())).pack()
        
    def scroll(self,event): #event
        print("scroll", event.delta)
        #self.yscrollbar.config(command=self.canevas.yview)

    def onComboBox(self, event): #event
        print("combo", event, self.listeOrder.get())
        self.remplirListe()

    def onSearchField(self, event): #event
        print("key", event.char)
        #self.searchField
        self.canevas.tag_raise("panelHaut")
        self.canevas.tag_lower("panelMessage")
    
    def remplirListe(self):
        #Delete messages
        for message in self.messageGraphic:
            message.canevas.destroy()
        self.messageGraphic = []
        
        self.messages = self.commandes.searchMessages(self.id,self.listeOrder.get() ) #[Message(1, "Premier", "Jamais", "Moi", self.id, self.id), Message(2, "Second", "Toujours", "L'autre", self.id, self.id)]
        for m in self.messages:
            #m.texte = self.chopMessage(m)
            self.messageGraphic.append(MesssageCanvas(self.m,self, m))
            #self.message.insert(END,(m.texte, m.auteur, m.date))

    def chopMessage(self,mess):
        achop = False
        result = ""
        for i in range(len(mess.texte)):
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

    def nouveau_message(self, nmess, texte, messageRepondu = None):
        self.commandes.ajouteMessage(texte.get("1.0", END), self.id, getpass.getuser(), messageRepondu) # END ajoute un \n à la fin. On veut ça?
        nmess.destroy()
        self.remplirListe()

    def supprimer(self, messageAsupprimer):
        #indiceMessageListe = n[0]
        #messageAsupprimer = self.messages[indiceMessageListe]
        self.commandes.supprimerMessageParID(messageAsupprimer.id, self.id)
        self.remplirListe()

    def repondre(self, messageArepondre):
        #indiceMessageListe = n[0]
        #messageArepondre = self.messages[indiceMessageListe]
        message = self.commandes.searchMessageParID(messageArepondre.id) # C'est clair? Enfin, dans l'idée c'est ça.
        self.ajouter(message.texte)
