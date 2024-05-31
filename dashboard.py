from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from spare import spareClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time

class msa:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("MotoStockApp")
        self.root.config(bg="white")
        #===title=====
        self.icon_title=PhotoImage(file="images/icon5.png")
        title=Label(self.root,text="MotoStockApp",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
    
        #===btn_logout===
        btn_logout=Button(self.root,text="Salir",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #===clock====
        self.lbl_clock=Label(self.root,text="Bienvenido a MotoStockApp\t\t Fecha: DD-MM-AAAA\t\t Hora: HH:MM:SS",font=("times new roman",15,),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #===left menu===
        #self.MenuLogo=Image.open("images/invent.png")
        #self.MenuLogo=self.MenuLogo.resize((200,200)),Image.ANTIALIAS
        #self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        #lbl_menuLogo=Label(LeftMenu,image=self.Menulogo)
        #lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/angle.png")

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20,"bold"),bg="#009688").pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu,text="Empleado",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Proveedor",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Categoria",command=self.category,image=self.icon_side,compound=LEFT,padx=5,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_replacement=Button(LeftMenu,text="Repuesto",command=self.spare,image=self.icon_side,compound=LEFT,padx=5,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="ventas",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Salir",image=self.icon_side,compound=LEFT,padx=5,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #===content====

        self.lbl_employee=Label(self.root,text="Total Empleados\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)
        
        self.lbl_supplier=Label(self.root,text="Total Proveedor\n[0]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Categoria\n[0]",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)
        
        self.lbl_spare=Label(self.root,text="Total Repuesto\n[0]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_spare.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Venta\n[0]",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)
        
        

        #===Footer====
        lbl_footer=Label(self.root,text="Sistema inventarios moto partes MSA | made by jucafe712\ncorreo: jucafe712@gmail.com\nBogota - Colombia",font=("times new roman",9,),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        
        self.update_content()
#===============================================================================

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def spare(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=spareClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            cur.execute("select * from spare")
            spare=cur.fetchall()
            self.lbl_spare.config(text=f'Total Repuestos\n[{str(len(spare))}]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Proveedores\n[{str(len(supplier))}]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Categorias\n[{str(len(category))}]')

            #cur.execute("select * from sales")
            #sales=cur.fetchall()
            #self.lbl_sales.config(text=f'Total Categorias\n[{str(len(sales))}]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Funcionarios\n[{str(len(employee))}]')
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Ventas [{str(bill)}]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Bienvenido!! Sistema Inventarios Moto Partes MSA\t\t Fecha: {str(date_)}\t\t Hora: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)



        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root) 

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":  

    root=Tk()
    obj=msa(root)
    root.mainloop()