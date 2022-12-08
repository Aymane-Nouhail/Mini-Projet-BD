from tkinter import *
import sqlite3
from tkinter.ttk import *


root_maison = Tk()
root_maison.title('Marisa')
root_maison.iconbitmap('./marisa_icon.ico')
root_maison.geometry("500x450")

#Create a database or conntect to one
conn = sqlite3.connect('DB_project.db')

#creating cursor
c = conn.cursor()

#enabling the use of foreign keys 
conn.execute("PRAGMA foreign_keys = 1")
#c.execute("DROP TABLE maison;")
'''
#create a table
c.execute("""
CREATE TABLE maison(
   ID_maison INT,
   nom_maison text,
   Loyer DECIMAL(15,2),
   nb_chambres text,
   nb_personnnes_max INT,
   nom_ile text,
   PRIMARY KEY(ID_maison),
   CONSTRAINT loyer_min CHECK(loyer>=100)
);
""")
'''

################################    defining functions      ##############################################""

def clear_input_lines_maison():
    id_maison.delete(0,END)
    nom_maison.delete(0,END)
    nb_chambres.delete(0,END)
    loyer_maison.delete(0,END)
    nb_personnes_max.delete(0,END)
    nom_ile.delete(0,END)
    return

#Submit function : INSERT INTO maison VALUES (user_input)
def submit():
    conn = sqlite3.connect('DB_project.db')
    #checking if constraint is validated :
    if loyer_maison.get() != '' and int(loyer_maison.get())<100:
         print_label= Label(root_maison, text="The query has failed, loyer value should be greater than 100.")
         print_label.grid(row=11,column=0)
    else:
        c = conn.cursor()
        #Inserting into table
        c.execute("INSERT INTO maison VALUES(:ID_maison, :nom_maison, :Loyer, :nb_chambres, :nb_personnes_max, :nom_ile)",
        {
            'ID_maison' : id_maison.get(),
            'nom_maison' : nom_maison.get(),
            'Loyer' : loyer_maison.get(),
            'nb_chambres' : nb_chambres.get(),
            'nb_personnes_max' : nb_personnes_max.get(),
            'nom_ile' : nom_ile.get()
        }
        )
        conn.commit()
        conn.close()
    print_label= Label(root_maison, text="The query has failed, loyer value should be greater than 100.")
    print_label = Label(root_maison, text="The query has been added to the database successfully.")
    print_label.grid(row=11,column=0)
    clear_input_lines_maison()
    return

#Query Function : Select * from Maison
def query():
    top = Toplevel()
    top.title("Table of Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("1150x400")
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    #top.configure(bg='green')
    #Selecting from table
    c.execute("SELECT * from maison;")
    records = c.fetchall()
    records = [("identifiant","nom","loyer","nombre de chambres", "nombre des personnes max.","l'ile de la maison")] + records
    print(records)
    style = Style()
    style.configure("BW.TLabel", foreground="blue",background="white")
    for i in range(len(records)):
        for j in range(len(records[0])):
            if i==0:
                query_label = Entry(top,width=25,font=('Calibri',11,'bold italic'),style="BW.TLabel")
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                #query_label.config(state=DISABLED)
                #query_label.configure(style="BW.TLabel")
            else:
                query_label = Entry(top,width=25,font=('Calibri',11,'bold'))
                query_label.grid(row=i,column=j)
                query_label.insert(END, records[i][j])
                #query_label.config(state=DISABLED)
    conn.commit()
    conn.close()
    #clearing all windows
    clear_input_lines_maison()
    return

#clear function : DELETE FROM maison
def clear():
    def clear_all():
        conn = sqlite3.connect('DB_project.db')
        c = conn.cursor()
        c.execute("DELETE FROM maison;")
        conn.commit()
        conn.close()
        top.destroy()
        print_label = Label(root_maison, text='The database has been cleared successfully.')
        print_label.grid(row=11,column=0,padx=0)
    top = Toplevel()
    top.title("Confirmation Prompt")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("400x100")
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    print_label= Label(top, text="Are you sure you want to clear the database?")
    print_label.grid(row=0,column=0,padx=80)
    yes_btn = Button(top, text = "yes", command=clear_all)
    yes_btn.grid(row=1, column=0, padx=20,pady=(10,0))
    no_btn = Button(top, text = "no", command=top.destroy)
    no_btn.grid(row=2, column=0, padx=20,pady=(10,0))
    conn.commit()
    conn.close()
    return

def search():
    top = Toplevel()
    top.title("Search Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("1000x400")
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM maison WHERE
        id_maison = :ID_maison OR nom_maison = :nom_maison OR loyer = :Loyer OR nb_personnnes_max = :nb_personnes_max OR nom_ile = :nom_ile""",
    {
        'ID_maison' : id_maison.get(),
        'nom_maison' : nom_maison.get(),
        'Loyer' : loyer_maison.get(),
        'nb_chambres' : nb_chambres.get(),
        'nb_personnes_max' : nb_personnes_max.get(),
        'nom_ile' : nom_ile.get()
    })
    records = c.fetchall()
    records = [("identifiant","nom","loyer","nombre de chambres", "nombre des personnes max.","l'ile de la maison")] + records
    print(records)
    for i in range(len(records)):
        for j in range(len(records[0])):
            query_label = Entry(top, width=20,font=('Arial',10,'bold'))
            query_label.grid(row=i,column=j)
            query_label.insert(END, records[i][j])
    conn.commit()
    conn.close()
    #clearing all windows
    clear_input_lines_maison()
    return records[1:]

#create delete function
def remove():
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    c.execute("""DELETE FROM maison WHERE
        id_maison = :ID_maison OR nom_maison = :nom_maison OR loyer = :Loyer OR nb_personnnes_max = :nb_personnes_max OR nom_ile = :nom_ile""",
    {
        'ID_maison' : id_maison.get(),
        'nom_maison' : nom_maison.get(),
        'Loyer' : loyer_maison.get(),
        'nb_chambres' : nb_chambres.get(),
        'nb_personnes_max' : nb_personnes_max.get(),
        'nom_ile' : nom_ile.get()
    })
    conn.commit()
    conn.close()
    clear_input_lines_maison()
    return

#create a modify function
def mofidy():
    return
################################    defining Entry Fields     ##############################################

id_maison = Entry(root_maison,width=30)
id_maison.grid(row=0, column=1, padx=20,pady=(10,0))

nom_maison = Entry(root_maison,width=30)
nom_maison.grid(row=1, column=1, padx=20)

loyer_maison = Entry(root_maison,width=30)
loyer_maison.grid(row=2, column=1, padx=20)

nb_chambres = Entry(root_maison, width=30)
nb_chambres.grid(row=3, column=1, padx=20)

nb_personnes_max = Entry(root_maison,width=30)
nb_personnes_max.grid(row=4, column=1, padx=20)

nom_ile = Entry(root_maison,width=30)
nom_ile.grid(row=5, column=1, padx=20)

################################    defining text labels     ##############################################
id_maison_label = Label(root_maison, text="Identifiant de la maison")
id_maison_label.grid(row=0, column=0,pady=(10,0))

nom_maison_label = Label(root_maison, text="Nom de la maison")
nom_maison_label.grid(row=1, column=0)

loyer_maison_label = Label(root_maison, text="Loyer de la maison")
loyer_maison_label.grid(row=2, column=0)

nb_chambres_label = Label(root_maison, text="Nombre de chambres de la maison")
nb_chambres_label.grid(row=3, column=0)



nb_personnes_max_label = Label(root_maison, text="Nombre maximal des personnes pour la maison")
nb_personnes_max_label.grid(row=4, column=0,padx=10)

nom_ile_label = Label(root_maison, text="Nom d'ile de la maison")
nom_ile_label.grid(row=5, column=0)


################################    defining Buttons     ##############################################

#Create Submit Button
submit_btn = Button(root_maison, text = "Add record to database", command=submit)
submit_btn.grid(row = 6, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a Query Button
query_btn = Button(root_maison, text="Show all records in database", command=query)
query_btn.grid(row = 7, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a Clear Button
clear_btn = Button(root_maison, text="Clear/Erase all records in database", command=clear)
clear_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a search button
search_btn = Button(root_maison, text="Search for a record in database",command=search)
search_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#create a remove button
remove_btn = Button(root_maison, text="Remove an element from the database",command=remove)
remove_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

modify_btn = Button(root_maison,text="Modify an element from the database",command=mofidy)
modify_btn.grid(row=11,column=0,columnspan=2,padx=10,pady=10,ipadx=100)
#commit changes
conn.commit()
root_maison.mainloop()
#close connection
conn.close()
