from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class spareClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("MotoStockApp")
        self.root.config(bg="white")
        self.root.focus_force()
        #====================
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_sid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        spare_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        spare_Frame.place(x=10,y=10,width=450,height=480)
        
        #=====title====

        title=Label(spare_Frame,text="Descripción Repuestos",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #column1

        lbl_category=Label(spare_Frame,text="Categorias",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(spare_Frame,text="Proveedores",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_spare=Label(spare_Frame,text="Nombre Repuesto",font=("goudy old style",15),bg="white").place(x=30,y=160)
        lbl_price=Label(spare_Frame,text="Precio",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_qty_name=Label(spare_Frame,text="Cantidad",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(spare_Frame,text="Estado",font=("goudy old style",18),bg="white").place(x=30,y=310)

        txt_category=Label(spare_Frame,text="Categorias",font=("goudy old style",18),bg="white").place(x=30,y=60)
        
        #====column2====
        cmb_cat=ttk.Combobox(spare_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_cat.place(x=210,y=60,width=220)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(spare_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_sup.place(x=210,y=110,width=220)
        cmb_sup.current(0)

        txt_name=Entry(spare_Frame,textvariable=self.var_name,font=("time new roman",15),bg='lightyellow').place(x=213,y=160,width=220)
        txt_price=Entry(spare_Frame,textvariable=self.var_price,font=("time new roman",15),bg='lightyellow').place(x=210,y=210,width=220)
        txt_qty=Entry(spare_Frame,textvariable=self.var_qty,font=("time new roman",15),bg='lightyellow').place(x=210,y=260,width=220)

        cmb_status=ttk.Combobox(spare_Frame,textvariable=self.var_status,values=("Activo","Inactivo"),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_status.place(x=210,y=310,width=220)
        cmb_status.current(0)
        
        #=====buttons====
        btn_add=Button(spare_Frame,text="Guardar",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(spare_Frame,text="Actualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(spare_Frame,text="Borrar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(spare_Frame,text="Limpiar",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #====searchFrame=====

        SearchFrame=LabelFrame(self.root,text="Busqueda repuesto",font=("goudy old style",12),bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #====options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("selct","category","supplier","name"),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_search.place(x=5,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=190,y=10)
        btn_search=Button(SearchFrame,text="Busqueda",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=460,y=9,width=130,height=30)

        #=====spare details====

        S_frame=Frame(self.root,bd=3,relief=RIDGE)
        S_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(S_frame,orient=VERTICAL)
        scrollx=Scrollbar(S_frame,orient=HORIZONTAL)

        self.spare_Table=ttk.Treeview(S_frame,columns=("sid","category","supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.spare_Table.xview)
        scrolly.config(command=self.spare_Table.yview)
        self.spare_Table.heading("sid",text="sid")
        self.spare_Table.heading("category",text="category")
        self.spare_Table.heading("supplier",text="supplier")
        self.spare_Table.heading("name",text="name")
        self.spare_Table.heading("price",text="price")
        self.spare_Table.heading("qty",text="qty")
        self.spare_Table.heading("status",text="status")
        
        self.spare_Table["show"]="headings"

        self.spare_Table.pack(fill=BOTH,expand=1)

        self.spare_Table.column("sid",width=100)
        self.spare_Table.column("category",width=100)
        self.spare_Table.column("supplier",width=100)
        self.spare_Table.column("name",width=100)
        self.spare_Table.column("price",width=100)
        self.spare_Table.column("qty",width=100)
        self.spare_Table.column("status",width=100)
        self.spare_Table.pack(fill=BOTH,expand=1)
        self.spare_Table.bind("<ButtonRelease-1>",self.get_data)

        self.show()

        #=======================================================
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("select")
                for i in cat:
                    self.cat_list.append(i[0])
    
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)
    
        

    def add(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="Select":
                messagebox.showerror("Error!","Llene todos los campos",parent=self.root)
            else:
                cur.execute("Select * from spare where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error!","Repuesto ya esta asignado",parent=self.root)
                else:
                    cur.execute("Insert into spare (category,supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                                            
                                            self.var_cat.get(),
                                            self.var_sup.get(),
                                            self.var_name.get(),
                                            self.var_price.get(),
                                            self.var_qty.get(),
                                            self.var_status.get(),
                                            ))
                    con.commit()
                    messagebox.showinfo("OK!", "Repuesto creado con exito!",parent=self.root)
                    self.show()
                                        
                    
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            cur.execute("select * from spare")
            rows=cur.fetchall()
            self.spare_Table.delete(*self.spare_Table.get_children())
            for row in rows:
                self.spare_Table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.spare_Table.focus()
        content=(self.spare_Table.item(f))
        row=content['values']
        self.var_sid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

        
    def update(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_sid.get()=="":
                messagebox.showerror("Error!","Seleccione repuesto de lista",parent=self.root)

            else:
                cur.execute("Select * from spare where sid=?",(self.var_sid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error!","Repuesot Invalido",parent=self.root)
                else:
                    cur.execute("Update spare set category=?,supplier=?,name=?,price=?,qty=?,status=? where sid=?",(
                                            self.var_cat.get(),
                                            self.var_sup.get(),
                                            self.var_name.get(),
                                            self.var_price.get(),
                                            self.var_qty.get(),
                                            self.var_status.get(),
                                            self.var_sid.get()
                                            
                    ))
                    con.commit()
                    messagebox.showinfo("OK!", "Repuesto actualizado con exito!",parent=self.root)
                    self.show()           
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)       
    
    def delete(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_sid.get()=="":
                messagebox.showerror("Error!","Seleccione repuesto lista",parent=self.root)
            else:
                cur.execute("Select * from spare where sid=?",(self.var_sid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error!","Repuesto invalido",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Realmete desea borrar registro?",parent=self.root)
                    if op==True:
                        cur.execute("delete from spare where sid=?",(self.var_sid.get(),))
                        con.commit()
                        messagebox.showinfo("Borrado","Repuesto borrado con exito!",parent=self.root)
                        self.clear()
                        
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

    def clear(self):

        self.var_cat.set(""),
        self.var_sup.set(""),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set(""),
        self.var_sid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("select")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error!","Seleccionar campo de busqueda",parent=self.root)
            
            else:
                cur.execute("select * from spare where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.spare_Table.delete(*self.spare_Table.get_children())
                    for row in rows:
                        self.spare_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error!","Repuesto no encontrado!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

if __name__=="__main__":  

    root=Tk()
    obj=spareClass(root)
    root.mainloop()