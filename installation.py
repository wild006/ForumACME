#!/usr/bin/env python3
import mysql.connector
import re

def connectionDB(user, password, host, nomDB):
    return mysql.connector.connect(user=user, password=password, host=host,database=nomDB)

def executeScript(path,db):
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
            print("Commande pas valide")

def startUp():
    user = "root"
    passwd = "AAAaaa111"
    host = "127.0.0.1"
    nomDB = "FORUM"
    try:
        db = mysql.connector.connect(user=user, password=passwd,
                                    host=host,
                                    database=nomDB)
        print("Déjà installé")
            #Tester toutes les tables ? (Corrumption)
    except:
        print("Lancement de l'installation !")
        db = mysql.connector.connect(host=host,
                                    user=user,passwd=passwd)
        executeScript("forumDB.sql", db)
        print("Fin création BD")
        db = connectionDB(user,passwd,host,nomDB)
        try:
            executeScript("forumUser.sql", db)
            print("Fin création Usager")
        except:
            print("Usager déjà créé")
        executeScript("forumTables.sql", db)
        print("Fin création Tables")
        print("Fin de l'installation !")

if __name__ == "__main__":
    startUp()
