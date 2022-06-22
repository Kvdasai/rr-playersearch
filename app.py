from tkinter import *
from requests import *
import pandas as pd
from json import *


#Définir la fonction de recherche.
def nickSEARCH():
    nickname = nickENTRY.get(1.0, "end-1c")
    isRegister = get('https://mdtfinder.fr/api/players/' + nickname)
    #Si le joueur n'est pas register :
    if isRegister.text == '{"message":"Player not found","code":404}':
        print("Joueur non inscrit.")
    else:
        userINFO = pd.json_normalize(isRegister.json())
        userID = userINFO['id'][0]
        isBanned = get('https://mdtfinder.fr/api/tournaments/elo_rosters_ranked_s3/players/' + userID)
        qBAN = pd.json_normalize(isBanned.json())
        queueBAN = qBAN['isBanned'].bool()
        #Si le joueur n'est pas queue ban :
        if bool(queueBAN) is False:
            print("Le joueur " + nickname + " n'est pas queue ban.")
        else:
            #Si le joueur est queue ban et le motif du bannissement
            reasonQBAN = qBAN['banHistory'][0] ['reason']
            print("Le joueur " + nickname + " est queue ban pour la raison : " + reasonQBAN)
        #Donne l'elo maximum atteint + l'elo actuel
        maxELO = qBAN['topScore']
        print(maxELO)
        actuelELO = qBAN['score']
        print(actuelELO)
        
        
    

#Création et configuration de la fenêtre
app = Tk()
app.title("Roster Ranked Player")
app.geometry("807x403")
app.minsize(807, 403)
app.maxsize(807, 403)
app.config(bg='#565656')


#Création des frames
frame = Frame(app, bg='#565656')
notQBAN = Frame(app, bg='#565656')
isQBAN = Frame(app, bg='#565656')

#Endroit où faire la recherche
nickTITLE = Label(frame, text="Entrez le pseudo du joueur ici :", font=("Helvetic, 20"), bg='#565656', fg="white")
nickTITLE.pack()

#Endroit où entrer le pseudo
nickENTRY = Text(frame, font=("Helvetic, 20"), bg='#565656', height=1, width=20)
nickENTRY.pack()

#Bouton pour valider la recherche
nickENTER = Button(frame, text="Rechercher", font=("Roboto"), bg='#a9a9a9', fg='black', command=nickSEARCH)
nickENTER.pack(pady="5")

frame.pack()
app.mainloop()
