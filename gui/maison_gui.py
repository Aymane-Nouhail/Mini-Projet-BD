from tkinter import *
import sqlite3
from tkinter.ttk import *



class NewWindow(Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        self.title("New Window")
        self.geometry("200x200")
        label = Label(self, text ="")
        label.pack()

root_maison = Tk()
root_maison.title('Marisa')
root_maison.iconbitmap('./marisa_icon.ico')
root_maison.geometry("470x400")

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
#create submit function

def submit():
    conn = sqlite3.connect('DB_project.db')
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
    #clear text boxes
    id_maison.delete(0,END)
    nom_maison.delete(0,END)
    nb_chambres.delete(0,END)
    loyer_maison.delete(0,END)
    nb_personnes_max.delete(0,END)
    nom_ile.delete(0,END)

#create Query function
def query():
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    #Selecting from table
    c.execute("SELECT * from maison;")
    records = c.fetchall()
    query_titles = ["id maison : ", "nom maison : ", "loyer maison : ", "nombre chambres : ", "nombre personnes max : ", "nom ile : "]
    print_records = ''
    for i in range(len(records)):
        print_records += query_titles[i%6] + str(records[i]) + '\n'
    query_label = Label(root_maison, text = print_records)
    query_label.grid(row = 10, column = 0, columnspan=2)
    print(records)
    conn.commit()
    conn.close()

#create clear function
def clear():
    conn = sqlite3.connect('DB_project.db')
    c = conn.cursor()
    #deleting everything from table
    c.execute("DELETE from maison;")
    conn.commit()
    conn.close()

def get_any():
    get_list = [id_maison.get(),nom_maison.get(),loyer_maison.get(),nb_chambres.get(),nb_personnes_max.get(),nom_ile.get()]
    return_list = dict(id = '',nom = '', )
    for iter in get_list:
        if iter != '':
            return_list += iter
            return iter;
        
def search():
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
    query_label = Label(root_maison, text = records)
    query_label.grid(row=10,column=0,columnspan=2)
    conn.commit()
    conn.close()


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

#creating text box labels :
id_maison_label = Label(root_maison, text="Identifiant de la maison")
id_maison_label.grid(row=0, column=0,pady=(10,0))

nom_maison_label = Label(root_maison, text="Nom de la maison")
nom_maison_label.grid(row=1, column=0)

loyer_maison_label = Label(root_maison, text="Loyer de la maison")
loyer_maison_label.grid(row=2, column=0)

nb_chambres_label = Label(root_maison, text="Nombre de chambres de la maison")
nb_chambres_label.grid(row=3, column=0)



nb_personnes_max_label = Label(root_maison, text="Nombre maximal des personnes pour la maison")
nb_personnes_max_label.grid(row=4, column=0)

nom_ile_label = Label(root_maison, text="Nom d'ile de la maison")
nom_ile_label.grid(row=5, column=0)

#Create Submit Button
submit_btn = Button(root_maison, text = "Add record to database", command=submit)
submit_btn.grid(row = 6, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a Query Button
query_btn = Button(root_maison, text="Show all records in database", command=query)
query_btn.grid(row = 7, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

#Create a Clear Button
clear_btn = Button(root_maison, text="Clear/Erase all records in database", command=clear)
clear_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10,ipadx=100)
'''
class Table:
    def __init__(self,root):
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):

                self.e = Entry(root, width=20, fg='blue',
                font=('Arial',16,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])

# take the data
lst = [(1,'Raj','Mumbai',19),
(2,'Aaryan','Pune',18),
(3,'Vaishnavi','Mumbai',20),
(4,'Rachna','Mumbai',21),
(5,'Shubham','Delhi',21)]

# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])
'''

def search_new_window():
    top = Toplevel()
    top.title("Search Results")
    top.iconbitmap("./marisa_icon.ico")
    top.geometry("100x100")
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
            query_label = Entry(top, width=20,font=('Arial',16,'bold'))
            query_label.grid(row=i,column=j)
            query_label.insert(END, records[i][j])
    conn.commit()
    conn.close()
    #clearing all windows
    id_maison.delete(0,END)
    nom_maison.delete(0,END)
    nb_chambres.delete(0,END)
    loyer_maison.delete(0,END)
    nb_personnes_max.delete(0,END)
    nom_ile.delete(0,END)


#Create a search button
search_btn = Button(root_maison, text="Search for a record in database",command=search_new_window)
search_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10,ipadx=100)

'''  
search_btn = Button(root_maison, text="Search for a record in database", command=search)
search_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10,ipadx=100)
'''
#commit changes
conn.commit()
root_maison.mainloop()
#close connection
conn.close()
