#!/usr/bin/env python3

from tkinter import *
import tkinter.ttk  as ttk #Pour le combo Box
from multilistbox import *
from autocompleteEntry import *
from messageCanvas import *
import getpass

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
        
        self.boxSujet = MultiListbox(self.forum, (('Message', 40), ('Date', 20), ('Nombre de messages', 10), ('Dernier message', 40)))
        self.sujets = [] # Tous les sujets
        
        self.boxSujet.grid(row=1,column=0,sticky = E+W+N+S, columnspan=3)
        self.setSearchPanel()
        self.setEvents()
        self.remplirListe()
        
        Button(self.forum, text="Visioner", command=lambda: self.visioner(self.boxSujet.curselection())).grid(row=2,column=0)
        Button(self.forum, text="Supprimer", command=lambda: self.supprimer(self.boxSujet.curselection())).grid(row=2,column=1)
        Button(self.forum, text="Ajouter", command=self.ajouter).grid(row=2,column=2)

    def setSearchPanel(self):        
        self.choixOrder = ('Date croissante', 'Date décroissante', 'Auteur (A-Z)', 'Auteur (Z-A)', 'Nom sujet (A-Z)','Nom sujet (Z-A)')
        self.listeOrder = ttk.Combobox(self.forum,values = self.choixOrder, state = 'readonly')
        self.listeOrder.set(self.choixOrder[0])
        self.listeOrder.grid(row=0,column=0)
        
        self.searchField = AutocompleteEntry(self.commandes, self, self.forum)
        self.searchField.grid(row=0,column=1, sticky = W+E)
        
        Button(text="Go!", command=self.recherche).grid(row=0, column=3)
        
        self.choixSearch = ('Sujet contenant', 'Sujet commençant par', 'Message contenant', 'Message commençant par')
        self.listeSearch= ttk.Combobox(self.forum,values = self.choixSearch, state = 'readonly')
        self.listeSearch.set(self.choixSearch[0])
        self.listeSearch.grid(row=0,column=2, sticky = E+W)

    def remplirListe(self):
        self.boxSujet.delete(0, END)
        self.sujets = self.commandes.searchSujets(self.listeOrder.get())
        for sujet in self.sujets:
            m = self.commandes.searchMessages(sujet.id)
            if m:
                self.boxSujet.insert(END, (sujet.nom, sujet.date, sujet.nbMessages, m[0].date))
            else:
                self.boxSujet.insert(END, (sujet.nom, sujet.date, sujet.nbMessages, 'Jamais'))
    def onSearchComparaison(self,texte):
        return self.commandes.searchTextSujet(texte, self.listeSearch.get())

    def visioner(self, event):
        MessageVue(self.sujets[int(event[0])].id, self.commandes, self.forum, self)

    def supprimer(self, event):
        indiceSujetListe = event[0]
        sujetASupprimer = self.sujets[int(indiceSujetListe)]
        self.commandes.supprimerSujetParID(sujetASupprimer.id)
        self.remplirListe()
        
    def ajouter(self):
        nsujet = Tk()
        Label(nsujet, text="Titre").grid(column = 0, row = 0)
        titre = Entry(nsujet)
        titre.grid(column = 1, row = 0)
        Button(nsujet, text="Go", command=lambda:self.nouveau_sujet(nsujet, titre.get())).grid()

    def nouveau_sujet(self, nsujet, titre):
        self.commandes.ajouteSujet(titre, getpass.getuser())
        nsujet.destroy()
        self.remplirListe()

    def setEvents(self):
        self.listeOrder.bind('<<ComboboxSelected>>', self.onComboBox)
        #self.searchField.bind("\n", self.recherche)

    def recherche(self):
        print(self.searchField.get())
        trouve = self.onSearchComparaison(self.searchField.get())
        
        if self.listeSearch.get() == self.choixSearch[0] or self.listeSearch.get() == self.choixSearch[1]:
            MessageVue(trouve[0].id, self.commandes, self.forum, self)
        else:
            self.ouvreUn(trouve[0])

    def onComboBox(self,event):
        self.remplirListe()

    def ouvreUn(self, mess):
        top = Toplevel(self.forum)
        MesssageCanvas(top, self, mess)
        
class MessageVue():
    def __init__(self, n, commandes, root, sujetVue=None):
        """Affiche les messages du sujet a l'id `n'"""
        self.commandes = commandes
        self.id = int(n)
        self.root = root
        self.parent = sujetVue
        self.messageGraphic = []
        self.messages = [] # Tous les messages de la liste
        
        self.initVue(root)

        
    def initVue(self, root):
        self.setTopLevel(root)
        self.setCanevas()
        self.setSearchPanel()
        self.setMessPanel()
        self.setEvents()
        
    def setTopLevel(self, root):
        self.mess = Toplevel(root)
        # self.mess.title(self.commandes.trouveTitreSujetByID(self.id))

        self.frame = Frame(self.mess, bd=2, relief=SUNKEN, width=800, height=500)
        # self.frame.grid_rowconfigure(0, weight=1)
        # self.frame.grid_columnconfigure(0, weight=3)
        
    def setCanevas(self):
        self.yscrollbar = Scrollbar(self.frame)

        self.yscrollbar.grid(row=1, column=4, sticky=N+S)

        self.canevas = Canvas(self.frame, bd=0, width=800, height=500, yscrollcommand=self.yscrollbar.set)
        self.canevas.grid(row=1, column = 0, columnspan = 4)

        self.yscrollbar.config(command=self.bouge)
        # self.frame.bind("<Configure>", self.OnFrameConfigure)
        # self.frame.grid(row=0, column=0, sticky=W+E+N+S)
        self.frame.pack()
        
    def setSearchPanel(self):        
        self.choixOrder = ('Date croissante', 'Date décroissante', 'Auteur (A-Z)', 'Auteur (Z-A)')
        self.listeOrder = ttk.Combobox(self.frame,values = self.choixOrder, state = 'readonly')
        self.listeOrder.set(self.choixOrder[0])
        self.listeOrder.grid(row=0,column=0)
        
        self.searchField = AutocompleteEntry(self.commandes,self, self.frame)
        self.searchField.grid(row=0,column=1, sticky = W+E)
        
        self.choixSearch = ('Message contenant', 'Message commençant par')
        self.listeSearch= ttk.Combobox(self.frame,values = self.choixSearch, state = 'readonly')
        self.listeSearch.set(self.choixSearch[0])
        self.listeSearch.grid(row=0,column=2, sticky = E+W)
        Button(self.frame, text="Go!", command=self.recherche).grid(row=0, column=3)
        
    def recherche(self):
        trouve = self.onSearchComparaison(self.searchField.get())
        self.ouvreUn(trouve[0])

    def ouvreUn(self, mess):
        top = Toplevel(self.root)
        MesssageCanvas(top, self, mess)
    
    def setMessPanel(self):
        self.m = PanedWindow(self.canevas,orient=VERTICAL)
        # self.canevas.create_window((400,), window=self.m, tags="panelMessage")
        # self.m.grid(row=2,column=0,columnspan=3,  sticky=W)
        
        self.remplirListe()
        
        self.canevas.tag_raise("panelHaut")
        self.canevas.tag_lower("panelMessage")

    def setEvents(self):
        self.mess.bind_all("<MouseWheel>",self.scroll)
        self.yscrollbar.bind('<ButtonRelease-1>',self.scroll)
        
        self.listeOrder.bind('<<ComboboxSelected>>', self.onComboBox)
        #self.searchField.bind('<Key>', self.onSearchField)
        
        Button(self.frame, text="Ajouter", command=self.ajouter).grid(row=0,column=4)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canevas.configure(scrollregion=self.canevas.bbox("all"))
        
    def bouge(self, type, amount, what=None):
        if what:
            self.canevas.yview(type, amount, what)
        else:
            self.canevas.yview(type, amount)

    def scroll(self, event):
        # print(event.delta)
        self.canevas.yview(SCROLL, -(event.delta*120), "units")
        
    def onComboBox(self, event): #event
        self.remplirListe()

    def onSearchComparaison(self,texte):
        return self.commandes.searchTextMessage(texte, self.id, self.listeSearch.get())
    
    def remplirListe(self):
        #Delete messages
        for message in self.messageGraphic:
            message.canevas.destroy()
        self.messageGraphic = []

        self.messages = []
        self.messages = self.commandes.searchMessages(self.id,self.listeOrder.get() )
        for m in self.messages:
            #m.texte = self.chopMessage(m)
            self.messageGraphic.append(MesssageCanvas(self.m, self, m))
            #self.message.insert(END,(m.texte, m.auteur, m.date))
        # self.canevas.configure(scrollregion=self.canevas.bbox("all"))
        self.canevas.config(scrollregion=(0,0, 800, (len(self.messages)+1)*(180)))
        self.canevas.create_window((400,(len(self.messages)+1)*(180/2)), window=self.m, tags="panelMessage")
         
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
        if self.parent:
            self.parent.remplirListe()
        
    def supprimer(self, messageAsupprimer):
        self.commandes.supprimerMessageParID(messageAsupprimer.id, self.id, getpass.getuser())
        self.remplirListe()
        if self.parent:
            self.parent.remplirListe()

    def repondre(self, messageArepondre):
        #indiceMessageListe = n[0]
        #messageArepondre = self.messages[indiceMessageListe]
        message = self.commandes.searchMessageParID(messageArepondre.id)
        rep = ""
        rep += message.auteur + " à dit: \n> "
        for c in message.texte:
            rep += c
            if c == '\n':
                rep += "> "
        rep += "\n\n"
        self.ajouter(rep)
