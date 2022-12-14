# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 22:27:45 2022

@author: Mehdi
"""

from tkinter import *
import sqlite3



root = Tk()
root.title("Interface Graphique")
root.geometry("720x480")
root.iconbitmap('./marisa_icon.ico')
root.config(background='#ABC8C2')
frame= Frame(root, bg='#ABC8C2')

Titre= Label(frame, text="Veuillez choisir un espace :", bg='#ABC8C2', fg='white',font=("Oswald",25))
Titre.grid(row=0)

def pageMaison() :
    maison_root=Tk()
    maison_root.mainloop()

def pageClient() :
    client_root=Tk()
    client_root.mainloop()
def pageReservation():
    reservation_root=Tk()
    reservation_root.mainloop()
    
#Boutons espace
Maisonbutton= Button(frame, text="Espace Maison",bg='white', fg='#ABC8C2',font=("Oswald",25),padx=15,pady=15, command=pageMaison)
Maisonbutton.grid(row=1, column=0,columnspan=2, sticky='ew')
    
Clientbutton= Button(frame, text="Espace Client",bg='white', fg='#ABC8C2',font=("Oswald",25),padx=15,pady=15, command=pageClient)
Clientbutton.grid(row=2, column=0,columnspan=2, sticky='ew')

    
Reservationbutton= Button(frame, text="Espace Reservation",bg='white', fg='#ABC8C2',font=("Oswald",25),padx=15,pady=15, command=pageReservation)
Reservationbutton.grid(row=3, column=0,columnspan=2, sticky='ew')


    


frame.pack(expand='YES')
root.mainloop()