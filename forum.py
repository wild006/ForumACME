#!/usr/bin/env python3
import mysql.connector
import re
import datetime
from forumvue import *

nomDB = "FORUM"

class Commandes():
    def __init__(self):
        self.user = "userForum"
        self.passwd = "AAAaaa111"
        self.host = "127.0.0.1"
        self.nomDB = "FORUM"
        self.orderByValue = {'Date croissante':"date ASC ", 'Date décroissante':"date DESC", 'Auteur (A-Z)':"user ASC", 'Auteur (Z-A)':"user DESC", 'Nom sujet (A-Z)':"nom ASC",'Nom sujet (Z-A)':"nom DESC"}
        self.searchTypeValue = {'Message contenant':1, 'Message commençant par':2,'Sujet contenant':3, 'Sujet commençant par':4}
        self.v = SujetVue(self)
        self.v.forum.mainloop()
  

    def connectionDB(self,user, password, host, nomBD):
        return mysql.connector.connect(user=user, password=password,
                                          host=host,
                                         database= nomDB)

    def executeCommand(self,command, commit = False):
        #connection, execution et commit
        
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        
        cursor = db.cursor()
        cursor.execute(command)
        
        if commit:
            db.commit()
            
        db.close()

    def insererMessage(self, nomSujet, texte):
        #POUR DES TESTS !
        idSujet = self.trouveIdSujet(nomSujet)
        datePresent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datePresent = "'" + datePresent + "'"
        if idSujet:
            self.executeCommand("INSERT INTO MESSAGE(texte, sujet, date) VALUES(%s,%i,%s)"%(texte,idSujet,datePresent), True)

    def ajouteMessage(self, texte, idSujet, user, messageRepondu):
        if messageRepondu:
            messageReponduId = messageRepondu.id #Une réponse à un autre message
        else:
            messageReponduId = None

        #Formater le texte
        datePresent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datePresent = "'" + datePresent + "'"
        texte = re.escape(texte)
        texte = "'" + texte + "'"
        user = "'" + user + "'"
        
        if idSujet and messageReponduId: #Une réponse à un autre message
            self.executeCommand("INSERT INTO MESSAGE(texte, sujet, date,user, reponse) VALUES(%s,%i,%s,%s, %i)"%(texte,idSujet,datePresent,user, messageReponduId), True)
        elif not messageReponduId:
            self.executeCommand("INSERT INTO MESSAGE(texte, sujet, date,user) VALUES(%s,%i,%s,%s)"%(texte,idSujet,datePresent,user), True)

    def ajouteSujet(self, nom, user):
        #Formater le texte
        datePresent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datePresent = "'" + datePresent + "'"
        nom = re.escape(nom)
        nom = "'" + nom + "'"
        user = "'" + user + "'"
        
        self.executeCommand("INSERT INTO SUJET(nom, date, user) VALUES(%s,%s, %s)"%(nom,datePresent, user), True)
    
    def trouveIdSujet(self,nomSujet):
        try:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            command = "SELECT id FROM SUJET WHERE nom = " + nomSujet
            cursor.execute(command, (nomSujet))
            result = cursor.fetchone()#Il devrait avoir qu'un sujet avec ce nom...
            db.close()
            return result[0]
        except:
            print("pas trouvé")
            db.close()

        return None

    def trouveTitreSujetByID(self, idSujet): 
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        command = "SELECT nom FROM SUJET WHERE id = %i" % (idSujet)
        cursor.execute(command)
        nom = cursor.fetchone()
        db.close()
        return nom[0]
    
    def executeScript(self,path,db):
        file = open(path, 'r')
        fileCommands = file.read()
        file.close()

        sqlCommands = fileCommands.split(';')

        for command in sqlCommands:
            regex = re.search(r'\S', command, re.I)
            if regex:
                cursor = db.cursor()
                cursor.execute(command)
            else:
                print("pas valide")

    def searchUser(self,username):
        try:
            cursor = self.db.cursor()
            command = "SELECT * FROM USER WHERE username = " + username
            cursor.execute(command)
        except:
            print("pas trouvé")

    def searchSujets(self, orderById = 'Date croissante'):
        cursor = -1 #Pas trouvé
        try:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            orderByClause = self.orderByValue[orderById]
            command = "SELECT * FROM SUJET ORDER BY %s" %(orderByClause)
            cursor.execute(command)
        except:
            print("pas trouvé")
            return []

        sujets = []
        for (_id, nom, date, dernier,parent) in cursor:
            #Construction de l'objet sujet
            nbMessages = self.searchNbMessages("'" + nom + "'")
            sujet = Sujet(_id,nom,date,nbMessages,dernier,parent)
            print("i", _id,nom,date,dernier,parent)
            sujets.append(sujet)
        db.close()

        return sujets

    def searchNbMessages(self,sujet):
        try:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            idSujet = self.trouveIdSujet(sujet)
            if idSujet == None:
                db.close()
                return 0 #Aucun message dans le sujet
            command = "SELECT COUNT(*) FROM MESSAGE WHERE sujet = " + str(idSujet)
            cursor.execute(command)

            result = cursor.fetchone() #Il n'y a qu'un result: le count 
            db.close()
            return result[0]
        except:
            print("pas trouvé")
            db.close()
            
        return 0

    def searchMessageParID(self,idMessage):
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        command = "SELECT * FROM MESSAGE WHERE id = " + str(idMessage)
        cursor.execute(command)
        db.close()
        result = cursor.fetchone()
        return Message(result[0], result[1], result[2], result[4], result[3], result[5])

    def searchMessages(self, idSujet, orderById = 'Date décroissante'):
        if True:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            orderByClause = self.orderByValue[orderById]
            cursor = db.cursor()
            command = "SELECT * FROM MESSAGE WHERE sujet = %i ORDER BY %s" % (idSujet,orderByClause)
            cursor.execute(command)
        else:
            db.close()

        messages = []

        for (_id, text, date, reponse,user,sujet) in cursor:
            #Construction de l'objet sujet
            message = Message(_id,text,date,user,reponse, sujet)
            messages.append(message)
        db.close()
        return messages

    def searchTextSujet(self,letters, typeSearch = 'Message contenant'):
        idTypeSearch = self.searchTypeValue[typeSearch]
        if idTypeSearch == 1 or idTypeSearch == 2: #Recherche Messages
            return self.searchTextMessage(letters, None, typeSearch)

        #Recherche Sujet
        try:
            letters = self.formatTextSearch(idTypeSearch, letters)
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            command = "SELECT * FROM SUJET WHERE nom LIKE %s" % (letters)
            cursor.execute(command)
            db.close()
        except:
            db.close()
            return [] #Pas trouvé

        sujets = []

        for (_id, nom, date, dernier,parent) in cursor:
            nbMessages = self.searchNbMessages("'" + nom + "'")
            sujet = Sujet(_id,nom,date,nbMessages,dernier,parent)
            print("i", _id,nom,date,dernier,parent)
            sujets.append(sujet)

        return sujets

    def searchTextMessage(self,letters,idSujet, typeSearch = 'Message contenant'):
        try:
            if idSujet:
                sujetSearch = "sujet = %i  AND " % (idSujet) #les messages d'un sujet
            else:
                sujetSearch = " " #Tous les messages
                
            letters = self.formatTextSearch(self.searchTypeValue[typeSearch], letters)
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            command = "SELECT * FROM MESSAGE WHERE %s texte LIKE %s" % (sujetSearch, letters)
            cursor.execute(command)
            db.close()
        except:
            db.close()
            return [] #Pas trouvé

        messages = []
        
        for (_id, text, date, reponse,user,sujet) in cursor:
            message = Message(_id,text,date,user,reponse, sujet)
            messages.append(message)
        return messages

    def formatTextSearch(self, idTypeSearch, texte):
        #Formater le texte selon le type de recherche
        if idTypeSearch == 1 or idTypeSearch == 3:
            texte = "'%" + texte + "%'"
        elif idTypeSearch == 2 or idTypeSearch == 4:
            texte = "'" + texte + "%'"

        return texte

    def supprimerMessageParID(self, idMessage, idSujet, usr = ""):
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        usr = "'" + usr + "'"
        command = "DELETE FROM MESSAGE WHERE id = %i AND sujet = %i AND user = %s " % (idMessage, idSujet, usr)
        cursor.execute(command)
        db.commit()
        db.close()

    def supprimerSujetParID(self, idSujet):
        #Supprimer tous les messages de ce sujet
        messages = self.searchMessages(idSujet)
        if messages:
            for message in messages:
                self.supprimerMessageParID(message.id, idSujet)

        #Supprimer le sujet
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        command = "DELETE FROM SUJET WHERE id = %i" % (idSujet)
        cursor.execute(command)
        db.commit()
        db.close()


def main():
    c = Commandes()

if __name__ == "__main__":
    main()
