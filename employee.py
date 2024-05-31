from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class employeeClass:
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

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()
        
        #====searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Busqueda empleado",bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #====options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("select","email","name","contact"),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Busqueda",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #=====title====

        title=Label(self.root,text="Detalles empleados",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #=====content====
        #=====row11======

        lbl_empid=Label(self.root,text="EmpID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Genero",font=("goudy old style",15),bg="white").place(x=350,y=150)
        lbl_contact=Label(self.root,text="contact",font=("goudy old style",15),bg="white").place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("select","Hombre","Mujer","Otro"),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=850,y=150,width=180)

        #=====row2====

        lbl_name=Label(self.root,text="Nombre",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="F.D.N",font=("goudy old style",15),bg="white").place(x=350,y=190)
        lbl_dobj=Label(self.root,text="F.D.C",font=("goudy old style",15),bg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="lightyellow").place(x=500,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="lightyellow").place(x=850,y=190,width=180)

        #=====row3====

        lbl_email=Label(self.root,text="Correo",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="Clave",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="Tipo_Usuario",font=("goudy old style",11),bg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("select","Adminstrador","Empleado"),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #=====row4====

        lbl_address=Label(self.root,text="Dirección",font=("goudy old style",13),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salario",font=("goudy old style",15),bg="white").place(x=500,y=270)
        
        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",15),bg="lightyellow").place(x=600,y=270,width=180)
        

        #=====buttons====
        btn_add=Button(self.root,text="Guardar",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="Actualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="Borrar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="Limpiar",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #=====employee details====

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Nombre")
        self.EmployeeTable.heading("email",text="Correo")
        self.EmployeeTable.heading("gender",text="Genero")
        self.EmployeeTable.heading("contact",text="contact")
        self.EmployeeTable.heading("dob",text="F.D.N")
        self.EmployeeTable.heading("doj",text="F.D.C")
        self.EmployeeTable.heading("pass",text="Clave")
        self.EmployeeTable.heading("utype",text="T_Usuario")
        self.EmployeeTable.heading("address",text="Dirección")
        self.EmployeeTable.heading("salary",text="Salario")
        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.pack(fill=BOTH,expand=1)

        self.EmployeeTable.column("eid",width=80)
        self.EmployeeTable.column("name",width=150)
        self.EmployeeTable.column("email",width=150)
        self.EmployeeTable.column("gender",width=90)
        self.EmployeeTable.column("contact",width=90)
        self.EmployeeTable.column("dob",width=90)
        self.EmployeeTable.column("doj",width=90)
        self.EmployeeTable.column("pass",width=90)
        self.EmployeeTable.column("utype",width=90)
        self.EmployeeTable.column("address",width=90)
        self.EmployeeTable.column("salary",width=90)
        #self.EmployeeTable["show"]="headings" borrar?
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#=======================================================

    def add(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error!","EmpID debe ser ingresado",parent=self.root)

            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error!","EmID ya esta asignado",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                            self.var_emp_id.get(),
                                            self.var_name.get(),
                                            self.var_email.get(),
                                            self.var_gender.get(),
                                            self.var_contact.get(),
                                            
                                            self.var_dob.get(),
                                            self.var_doj.get(),
                                            
                                            self.var_pass.get(),
                                            self.var_utype.get(),
                                            self.txt_address.get('1.0',END),
                                            self.var_salary.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("OK!", "Empleado creado con exito!",parent=self.root)
                    self.show()

                                        
                    
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
                                            
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
                                            
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END),
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","EmpID debe ser ingresado",parent=self.root)

            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error!","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                                            self.var_name.get(),
                                            self.var_email.get(),
                                            self.var_gender.get(),
                                            self.var_contact.get(),
                                            
                                            self.var_dob.get(),
                                            self.var_doj.get(),
                                            
                                            self.var_pass.get(),
                                            self.var_utype.get(),
                                            self.txt_address.get('1.0',END),
                                            self.var_salary.get(),
                                            self.var_emp_id.get(),
                                            
                    ))
                    con.commit()
                    messagebox.showinfo("OK!", "Empleado actualizado con exito!",parent=self.root)
                    self.show()           
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)       
    
    def delete(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error!","EmpID debe ser ingresado",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error!","EmID ya esta asignado",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Realmete desea borrar registro?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Borrado","Empleado borrado con exito!",parent=self.root)
                        self.clear()
                        
        except Exception as ex:
            messagebox.showerror("Error!","EmpID debe ser ingresado",parent=self.root)

    def clear(self):

        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
                                            
        self.var_dob.set("")
        self.var_doj.set("")
                                            
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END),
        self.var_salary.set("")
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
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error!","Correo no encontrado!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)


if __name__=="__main__":  

    root=Tk()
    obj=employeeClass(root)
    root.mainloop()