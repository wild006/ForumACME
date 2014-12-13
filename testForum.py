import mysql.connector
import re
import datetime
from forum import *

nomDB = "FORUM"

class Commandes():
    def __init__(self):
        self.user = "root"
        self.passwd = "AAAaaa111"
        self.host = "127.0.0.1"
        self.nomDB = "FORUM"
        self.startUp()
        self.v = SujetVue(self)
        self.v.forum.mainloop()


    def startUp(self):
        try:
            db = mysql.connector.connect(user=self.user, password=self.passwd,
                                          host=self.host,
                                         database= self.nomDB)
            #Tester toutes les tables ? (Corrumption)
        except:
            print("pas créé !")
            db = mysql.connector.connect(host=self.host,
                                         user=self.user,passwd=self.passwd)
            self.executeScript("forumDB.sql", db)
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            self.executeScript("forumTables.sql", db)

        #POUR DES TESTS
        #INSERTION DE SUJETS
        self.executeCommand("INSERT INTO SUJET(nom, date) VALUES('LOL', '1776-7-4 04:13:54')", True)
        self.executeCommand("INSERT INTO SUJET(nom, date) VALUES('Pourquoi pas ? ', '1776-7-4 04:13:54')", True)
        #INSERTION DE MESSAGES
        self.insererMessage("'LOL'", "'Premier insert'")
        self.insererMessage("'LOL'", "'Deuxième insert'")
        self.insererMessage("'Pourquoi pas ? '", "'Un autre message !!!'")
        #idSujet = self.trouveIdSujet("'LOL'")
        #print("id",idSujet)
        #if idSujet:
        #    self.executeCommand("INSERT INTO MESSAGE(texte, sujet) VALUES('Un message très important !!', " + str(idSujet) + ")", True)

    def connectionDB(self,user, password, host, nomBD):
        return mysql.connector.connect(user=user, password=password,
                                          host=host,
                                         database= nomDB)

    def executeCommand(self,command, commit = False):
        #POUR DES TESTS !
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        cursor.execute(command)
        if commit:
            db.commit()
        db.close()

    def insererMessage(self, nomSujet, texte):
        #POUR DES TESTS !
        idSujet = self.trouveIdSujet(nomSujet)
        print("id",idSujet)
        datePresent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datePresent = "'" + datePresent + "'"
        if idSujet:
            self.executeCommand("INSERT INTO MESSAGE(texte, sujet, date) VALUES(%s,%i,%s)"%(texte,idSujet,datePresent), True)

    def ajouteMessage(self, texte, idSujet):
        datePresent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datePresent = "'" + datePresent + "'"
        texte = "'" + texte + "'"
        if idSujet:
            self.executeCommand("INSERT INTO MESSAGE(texte, sujet, date) VALUES(%s,%i,%s)"%(texte,idSujet,datePresent), True)
    
    def trouveIdSujet(self,nomSujet):
        try:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            command = "SELECT id FROM SUJET WHERE nom = " + nomSujet
            print(command)
            cursor.execute(command, (nomSujet))
            print("cursor", cursor)
            result = cursor.fetchone()#Il devrait avoir qu'un sujet avec ce nom...
            db.close()
            return result[0]
        except:
            print("pas trouvé")
            db.close()

        return None
    
    def executeScript(self,path,db):
        file = open(path, 'r')
        fileCommands = file.read()
        file.close()

        sqlCommands = fileCommands.split(';')

        for command in sqlCommands:
            print(command)
            regex = re.search(r'\S', command, re.I)
            if regex:
                cursor = db.cursor()
                cursor.execute(command)
            else:
                print("pas valide")
                print(command)


    def creerUser(self,nom,prenom,username,passwd,mail):
        if searchUser(username):
            pass

    def searchUser(self,username):
        try:
            cursor = self.db.cursor()
            command = "SELECT * FROM USER WHERE username = " + username
            print(command)
            cursor.execute(command)
            print("cursor", cursor)
        except:
            print("pas trouvé")

    def searchSujets(self):
        cursor = -1 #Pas trouvé
        try:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            command = "SELECT * FROM SUJET"
            print(command)
            cursor.execute(command)
            print("cursor", cursor)
        except:
            print("pas trouvé")

        sujets = []
        for (_id, nom, date, dernier,parent) in cursor:
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
            print(sujet)
            idSujet = self.trouveIdSujet(sujet)
            if idSujet == None:
                db.close()
                return 0
            command = "SELECT COUNT(*) FROM MESSAGE WHERE sujet = " + str(idSujet)
            print(command)
            cursor.execute(command)
            print("cursor", cursor)

            result = cursor.fetchone()
            db.close()
            print(result[0])
            return result[0]
        except:
            print("pas trouvé")
            db.close()
            
        return 0

    def searchMessages(self, idSujet):
        try:
            db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
            cursor = db.cursor()
            command = "SELECT * FROM MESSAGE WHERE sujet = " + str(idSujet)
            cursor.execute(command)
        except:
            db.close()

        messages = []
        
        for (_id, text, date, reponse,user,sujet) in cursor:
            message = Message(_id,text,date,user,reponse, sujet)
            messages.append(message)
        db.close()
        return messages

    def supprimerMessageParID(self, idMessage, idSujet):
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        command = "DELETE FROM MESSAGE WHERE id = %i AND sujet = %i  " % (idMessage, idSujet)
        print(command)
        cursor.execute(command)
        db.commit()
        db.close()

    def supprimerSujetParID(self, idSujet):
        print("SUpprimer", idSujet)
        #Supprimer tous les messages de ce sujet
        messages = self.searchMessages(idSujet)
        if messages:
            for message in messages:
                self.supprimerMessageParID(message.id, idSujet)

        #Supprimer le sujet
        db = self.connectionDB(self.user,self.passwd,self.host,self.nomDB)
        cursor = db.cursor()
        command = "DELETE FROM SUJET WHERE id = %i" % (idSujet)
        print(command)
        cursor.execute(command)
        db.commit()
        db.close()


    def connectionUser(self):
        pass

    def nouveauMessage(self):
        pass


def main():
    c = Commandes()
    #searchUser("Luc",db)
    #searchUser("Luc",db)

if __name__ == "__main__":
    main()
