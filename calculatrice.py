

# Projet étudiant réalisé par Louis Bergès à l'Université de Technologie de Compiègne

import tkinter.font
from collections import deque
from tkinter import *
from math import *


class Fenetre(Tk):
    def __init__(self, l=300, h=200):
        Tk.__init__(self)
        self.__hist_afficher = False  # Initialisation des variables
        self.__hist = deque()
        self.__calcul = ""
        self.__affichage = ""

        self.create_fenetre()  # Appels des fonctions
        self.create_label()
        self.create_entree()
        self.create_boutons()


    def create_fenetre(self):  # Créer la fenêtre graphique
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        fenetre_x = 700
        fenetre_y = 700
        pos_x = ecran_x // 2 - fenetre_x // 2
        pos_y = ecran_y // 2 - fenetre_y // 2
        geometrie = f"{fenetre_x}x{fenetre_y}+{pos_x}+{pos_y}"
        self.geometry(geometrie)
        self.title("Calculatrice")

    def create_label(self):  # Créer les Labels
        Label(self,text="Calculatrice", font=("Arial", 12, "bold")).grid(row=1, column=1, columnspan=6) #Titre

    def create_entree(self):
        self.__entree = Label(self, font=("arial", 12, "bold"), bg="white", bd="10", relief="sunken")
        self.__entree.grid(row=2, columnspan=6, column=1, sticky="nesw")

    def create_boutons(self):  # Créer les boutons
        default_params_1 = {"font": ("Arial", 12, "bold"), 'relief': "raised",'bd':20}
        default_params_2 = {"sticky":'nesw', "ipady":1,"ipadx":1, "pady":20,"padx":10}

        #Créer les chiffres de 1 à 9
        for i in range(1,10):
            Button(self,text=str(i),command=lambda num=i:self.affichage_calcul(num),bg="yellow",**default_params_1).grid(column=3 if i%3==0 else i%3,row=(3+i//3) if i%3!=0 else 2+i//3,**default_params_2)
        Button(self, text="0", command=lambda: self.affichage_calcul(0), bg="yellow",**default_params_1).grid(column=2, row=6, **default_params_2)

        # Fonctions spéciales
        Button(self, text="sin", command=lambda: self.affichage_calcul("sin"),bg="purple",**default_params_1).grid(column=4,row=3,**default_params_2)
        Button(self, text="√", command=lambda: self.affichage_calcul("sqrt"),bg="purple",**default_params_1).grid(column=5,row=3,**default_params_2)
        Button(self, text="cos", command=lambda: self.affichage_calcul("cos"),bg="purple",**default_params_1).grid(column=4,row=4,**default_params_2)
        Button(self, text="²", command=lambda: self.affichage_calcul("**2"),bg="purple",**default_params_1).grid(column=5,row=4,**default_params_2)
        Button(self, text="tan", command=lambda: self.affichage_calcul("tan"),bg="purple",**default_params_1).grid(column=4,row=5,**default_params_2)
        Button(self, text="π", command=lambda: self.affichage_calcul(pi),bg="purple",**default_params_1).grid(column=5, row=5, **default_params_2)
                                                                                                               
        # Opérateurs et caractères spéciaux
        Button(self, text="(", command=lambda: self.affichage_calcul("("),bg="purple",**default_params_1).grid(column=4, row=6,**default_params_2)
        Button(self, text=")", command=lambda: self.affichage_calcul(")"),bg="purple",**default_params_1).grid(column=5, row=6,**default_params_2)
        Button(self, text="+", command=lambda: self.affichage_calcul("+"), bg="cyan",**default_params_1).grid(column=6, row=3, **default_params_2)
        Button(self, text="-", command=lambda: self.affichage_calcul("-"), bg="cyan",**default_params_1).grid(column=6, row=4, **default_params_2)
        Button(self, text="*", command=lambda: self.affichage_calcul("*"), bg="cyan",**default_params_1).grid(column=6, row=5, **default_params_2)
        Button(self, text="/", command=lambda: self.affichage_calcul("/"), bg="cyan",**default_params_1).grid(column=6, row=6, **default_params_2)
        Button(self, text=".", command=lambda: self.affichage_calcul("."), bg="yellow",**default_params_1).grid(column=3, row=6, **default_params_2)

        # Boutons de traitements
        Button(self, text="=", command=lambda: self.calcul(), bg="red", **default_params_1).grid(column=1,row=6,**default_params_2)
        Button(self, text="historique", command=lambda: self.historique(), bg="brown",**default_params_1).grid(column=1,row=7,columnspan=2, **default_params_2)
        Button(self, text='clear all', command=self.effacer, bg="green", **default_params_1).grid(column=3,row=7,columnspan=2,**default_params_2)

    def affichage_calcul(self, x):  #Affichage de l'opération entrée par l'utilisateur
        if x == "sqrt":     #Il faut prendre en charge les différents affichages spéciaux (sqrt,x**2...) par des conditions
            self.__affichage += "√("
            self.__calcul += str(x)
            self.__calcul += "("
        elif x == "**2":
            self.__affichage += "²"
            self.__calcul += str(x)
        elif x == pi:
            self.__affichage += "π"
            self.__calcul += str(x)

        elif x in ["sin", "cos", "tan"]:
            self.__affichage += str(x) + "("
            self.__calcul += str(x)
            self.__calcul += "("

        else:
            self.__affichage += str(x)
            self.__calcul += str(x)
        self.__entree.configure(text=self.__affichage) #On aurait pu aussi utiliser une StringVar

    def calcul(self):   #Calcul de l'opération entrée par l'utilisateur
        try:
            self.__entree.configure(text=eval(self.__calcul))

        except ZeroDivisionError:  #Test de division par O
            self.__entree.configure(text="Il y a division par 0")
            self.__hist.append(str(self.__calcul) + ":" + "ZeroDivisionError")
            if self.__hist_afficher == True:
                self.refresh_historique()
            self.__calcul = ""
            self.__affichage = ""
        except ValueError:  #Test de calculs interdits divers
            self.__entree.configure(text="Vous sortez du domaine mathématique")
            self.__hist.append(str(self.__calcul) + ":" + "ValueError")
            if self.__hist_afficher == True:
                self.refresh_historique()
            self.__calcul = ""
            self.__affichage = ""
        except (SyntaxError, TypeError): #Tests de syntaxe et de types
            self.__entree.configure(text="Mauvaise Syntaxe")
            self.__hist.append(str(self.__calcul) + ":" + "SyntaxError")
            if self.__hist_afficher == True:
                self.refresh_historique()
            self.__calcul = ""
            self.__affichage = ""
        else:                                   #Effectué si aucune exception
            h = str(self.__calcul) + '='
            self.__hist.append(h + str(eval(self.__calcul)))
            if self.__hist_afficher == True:
                self.refresh_historique()
            self.__calcul = ""
            self.__affichage = ""


    def effacer(self):  #Effacer l'entrée
        self.__calcul = ""
        self.__affichage = ""
        self.__entree.configure(text="")


    def delete_historique(self): #Ne plus afficher l'historique
        self.__historique.destroy()

    def refresh_historique(self):   #Vérification de la longueur de l'historique
        if len(self.__hist) == 11:
            del self.__hist[0]
        v = ""
        for i in self.__hist:
            v = v + f"{i}\n"
        self.__historique.configure(text=v)

    def historique(self): #Création de l'historique
        if self.__hist_afficher == False:
            self.__hist_afficher = True
            self.__historique = Label(self, font=("arial", 12, "bold"), bg="white", bd="5", relief="sunken")
            self.__historique.grid(row=3, columnspan=1, rowspan=3, column=7, sticky="nesw")
            self.refresh_historique()
        else:
            self.__historique.destroy()
            self.__hist_afficher = False


def main():
    fenetre = Fenetre()
    fenetre.mainloop()


if __name__ == '__main__':
    main()
