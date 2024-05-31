from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("MotoStockApp")
        self.root.config(bg="white")
        self.root.focus_force()
        #====================
        #=====All variables===
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        
        #====searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Busqueda empleado",bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #====options====
        lbl_search=Label(SearchFrame,text="Buscar Factura#",bg="white",font=("goudy old style",15))
        lbl_search.place(x=10,y=10)
        

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Busqueda",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #=====title====

        title=Label(self.root,text="Datos Proveedores",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #=====content====
        #=====row1======

        lbl_suplier_invoice=Label(self.root,text="Factura#",font=("goudy old style",15),bg="white").place(x=50,y=150)
        txt_lbl_suplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        
        #=====row2====

        lbl_name=Label(self.root,text="Nombre",font=("goudy old style",15),bg="white").place(x=50,y=190)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        
        #=====row3====

        lbl_contact=Label(self.root,text="Contacto",font=("goudy old style",15),bg="white").place(x=50,y=230)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        
        #=====row4====

        lbl_desc=Label(self.root,text="Descripción",font=("goudy old style",12),bg="white").place(x=50,y=270)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=150,y=270,width=300,height=60)
        
        #=====buttons====
        btn_add=Button(self.root,text="Guardar",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="Actualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="Borrar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="Limpiar",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #=====supplier details====

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Factura#")
        self.supplierTable.heading("name",text="Nombre")
        self.supplierTable.heading("contact",text="Contacto")
        self.supplierTable.heading("desc",text="Descripción")
        self.supplierTable["show"]="headings"

        self.supplierTable.pack(fill=BOTH,expand=1)

        self.supplierTable.column("invoice",width=80)
        self.supplierTable.column("name",width=150)
        self.supplierTable.column("contact",width=150)
        self.supplierTable.column("desc",width=90)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#=======================================================

    def add(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error!","Factura debe ser ingresada",parent=self.root)

            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error!","Factura ya esta asignada",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                            self.var_sup_invoice.get(),
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            self.txt_desc.get('1.0',END),

                    ))
                    con.commit()
                    messagebox.showinfo("OK!", "Proveedor creado con exito!",parent=self.root)
                    self.show()

        except Exception as ex:
                        messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)
                        
    def show(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                    self.supplierTable.insert('',END,values=row)

        except Exception as ex:
                messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)
                                        
                
    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3])
        
    def update(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error!","Num. Factura debe ser ingresado",parent=self.root)

            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error!","Num.Factura invalido",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            self.txt_desc.get('1.0',END),
                                            self.var_sup_invoice.get(),
                                            
                    ))
                    con.commit()
                    messagebox.showinfo("OK!", "Proveedor actualizado con exito!",parent=self.root)
                    self.show()           
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)       
    
    def delete(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error!","Num. Factura debe ser ingresada",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error!","Num. Factura ya esta asignado",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Realmete desea borrar factura?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Borrado","Proveedor borrado con exito!",parent=self.root)
                        self.clear()
                        
        except Exception as ex:
            messagebox.showerror("Error!","EmpID debe ser ingresado",parent=self.root)

    def clear(self):

        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END),
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error!","Num. Factura es requerido",parent=self.root)
            
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error!","Factura no encontrada!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)


if __name__=="__main__":  

    root=Tk()
    obj=supplierClass(root)
    root.mainloop()