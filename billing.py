
from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
from tkinter import messagebox, END
import sqlite3
import time
import os
import tempfile
import subprocess
import cups
from fpdf import FPDF
import pdfplumber
import webbrowser
from tkinter import messagebox, Toplevel, Text, Scrollbar, VERTICAL, RIGHT, Y, END


class billingClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("MotoStockApp")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        self.conn = cups.Connection()
        #===title=====
        self.icon_title=PhotoImage(file="images/icon5.png")
        title=Label(self.root,text="MotoStockApp",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
    
        #===btn_logout===
        btn_logout=Button(self.root,text="Salir",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
        #===clock====
        self.lbl_clock=Label(self.root,text="Bienvenido a MotoStockApp\t\t Fecha: DD-MM-AAAA\t\t Hora: HH:MM:SS",font=("times new roman",15,),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #====spare_Frame++++
    
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="Todos los Repuestos",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        #=======spare seach frame=========
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Buscar Nombre Repuesto ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Nombre Repuesto",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15,),bg="lightyellow").place(x=165,y=47,width=140,height=22)
        btn_search=Button(ProductFrame2,text="Buscar",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white").place(x=310,y=45,width=80,height=25)
        btn_show_all=Button(ProductFrame2,text="Mostrar todo",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=235,y=10,width=150,height=25)

        #spare details frame====
        SpareFrame3=Frame(self.root,bd=3,relief=RIDGE)
        SpareFrame3.place(x=12,y=250,width=398,height=400)

        scrolly=Scrollbar(SpareFrame3,orient=VERTICAL)
        scrollx=Scrollbar(SpareFrame3,orient=HORIZONTAL)

        self.spare_Table=ttk.Treeview(SpareFrame3,columns=("sid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.spare_Table.xview)
        scrolly.config(command=self.spare_Table.yview)

        self.spare_Table.heading("sid",text="Items")
        self.spare_Table.heading("name",text="Nombre")
        self.spare_Table.heading("price",text="Precio")
        self.spare_Table.heading("qty",text="Cantidad")
        self.spare_Table.heading("status",text="Estado")
        self.spare_Table["show"]="headings"

        self.spare_Table.pack(fill=BOTH,expand=1)

        self.spare_Table.column("sid",width=50)
        self.spare_Table.column("name",width=100)
        self.spare_Table.column("price",width=50)
        self.spare_Table.column("qty",width=40)
        self.spare_Table.column("status",width=90)
        self.spare_Table.pack(fill=BOTH,expand=1)
        self.spare_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(SpareFrame3,text="Atencion! Ingrese 0 para remover repuesto",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #customer Frame
        self.var_name=StringVar()
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Datos Clientes",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Nombre",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13,),bg="lightyellow").place(x=80,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="#contacto",font=("times new roman",15),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13,),bg="lightyellow").place(x=380,y=35,width=140)
        
        #cal cart frame
        
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #=====calculatorframe-------
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly')
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=2,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=2,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=2,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=2,pady=10,cursor="hand2").grid(row=1,column=3)
        
        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=2,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=2,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=6,width=2,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=2,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=2,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=2,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=2,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=2,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=2,pady=30,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=2,pady=30,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=2,pady=30,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=2,pady=30,cursor="hand2").grid(row=4,column=3)
        
        #+++++cart frame------
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(Cart_Frame,text="Total\tItems:[0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(Cart_Frame,columns=("sid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("sid",text="Rid#")
        self.CartTable.heading("name",text="Repuesto")
        self.CartTable.heading("price",text="Precio")
        self.CartTable.heading("qty",text="UNDs")
        self.CartTable.pack(fill=BOTH,expand=1)
        #self.CartTable.heading("status",text="status")
        self.CartTable["show"]="headings"
        self.CartTable.column("sid",width=40) 
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        #self.CartTable.column("status",width=90) delete this line by jcf
        #self.CartTable.pack(fill=BOTH,expand=1) delete this line by jcf
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #====add cart widget frame=====
        self.var_sid=StringVar()
        self.var_sname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        #self.var_cname=StringVar()
        #self.var_ccontact=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Nombre Repuesto",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_sname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Precio * Cantidad",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Cantidad",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=90,height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="Disponibles",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Limpiar",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Agregar | Actualizar",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

        #####billing area====
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=410,height=410)
        
        BTitle=Label(billFrame,text="Factura Cliente",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #billing buttons

        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=410,height=140)

        self.lbl_amnt=Label(billMenuFrame,text='GranTotal\n[0]',font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text='Descuento\n[5%]',font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text='PagoNeto\n[0]',font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text='Imprimir',command=self.print_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=55)

        btn_clear_all=Button(billMenuFrame,text='Limpiar\nTodo',command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=55)

        #btn_generate=Button(billMenuFrame,text='Generar/Guardar\nFactura',command=self.generate_bill,cursor="hand2",font=("goudy old style",12,"bold"),bg="#009688",fg="white")
        btn_generate=Button(billMenuFrame,text='Generar/Guardar\nFactura',command=self.generate_bill,cursor="hand2",font=("goudy old style",12,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=55)

        #===Footer====
        lbl_footer=Label(self.root,text="Sistema inventarios moto partes MSA | made by jucafe712\ncorreo: jucafe712@gmail.com\nBogota - Colombia",font=("times new roman",9,),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        
        self.show()
        #self.bill_top()
        self.update_date_time()
    
        #===all functions=====
        
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            #self.spare_Table=ttk.Treeview(SpareFrame3,columns=("sid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            cur.execute("select sid,name,price,qty,status from spare where status='Activo'")
            rows=cur.fetchall()
            self.spare_Table.delete(*self.spare_Table.get_children())
            for row in rows:
                self.spare_Table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error!","Seleccionar campo de busqueda",parent=self.root)
            else:
                cur.execute("select sid,name,price,qty,status from spare where name LIKE '%"+self.var_search.get()+"%'and status='Activo'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.spare_Table.delete(*self.spare_Table.get_children())
                    for row in rows:
                        self.spare_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error!","Repuesto no encontrado!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.spare_Table.focus()
        content=(self.spare_Table.item(f))
        row=content['values']
        self.var_sid.set(row[0])
        self.var_sname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"Disponibles[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        #sid,name,price,qty,stock
        self.var_sid.set(row[0])
        self.var_sname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"Disponibles[{str(row[4])}]")
        self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_sid.get()=='':
            messagebox.showerror('Error!',"Por favor seleccione repuesto!",parent=self.root)

        elif self.var_qty.get()=='':
            messagebox.showerror('Error!',"Cantidad es Requerida",parent=self.root)

        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error!',"Inventario Insuficiente!!!",parent=self.root)

        else:
            price_cal=int(self.var_qty.get())*float(self.var_price.get())
            price_cal=float(price_cal)
            #print(price_cal)
            price_cal=self.var_price.get()
            #pid,name,price,qty,stock
            cart_data=[self.var_sid.get(),self.var_sname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #self.cart_list.append(cart_data)
            #===update cart====
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_sid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirmar',"Producto ya esta en lista\nactualizar lista? o quitar?",parent=self.root)
                if op==True:
                        if self.var_qty.get()=="0":
                            self.cart_list.pop(index_)
                        else:
                            #sid,name,price,qty,status
                            self.cart_list[index_][2]=price_cal #price
                            self.cart_list[index_][3]=self.var_qty.get #qty

            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            #sid,name,price,qty,stock
            self.bill_amnt=self.bill_amnt+float(row[2])*int(row[3])
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount

        self.lbl_amnt.config(text=f'GranTotal\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Pago Neto\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Total\tItems:[{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root) 

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error!",f"Llenar datos Cliente!!!",parent=self.root) 
        elif len(self.cart_list)==0:
            messagebox.showerror("Error!",f"Por favor agregar repuesto!!!",parent=self.root) 

        else:
            #bill top
            self.bill_top()
            #bill middle
            
            self.bill_middle()

            #bill botton
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Atencion!!!',"Factura guardada en segundo plano!!!",parent=self.root)
            self.chk_print=1
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        #print(invoice)
        bill_top_temp=f'''
\t\tMotoStockApp
\t Tel.: +573025321019, Bogota - 111821
{str("="*47)}
Nombre Cliente: {self.var_cname.get()}
Tel.:{self.var_contact.get()}
Factura No.{str(self.invoice)}\t\t\Precio: {str(time.strftime("%d%m%Y"))}
{str("="*47)}
Nombre Repuesto\t\t\tUNDs\tPrecio
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Total Factura\t\t\t\t${self.bill_amnt}
Descuento 5%:\t\t\t\t${self.discount}
Pago Neto\t\t\t\t${self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            #cur.execute('Update spare set qty=?,status=? where sid=?')
            for row in self.cart_list:
                #sid,name,price,qty,stock
                sid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactivo'
                if int(row[3])!=int(row[4]):
                    status='Activo'

                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\t$"+price)

                #update quantity in spare table=====
                cur.execute('Update spare set qty=?,status=? where sid=?',(
                    qty,
                    status,
                    sid
                ))
                con.commit()
            con.close()
            self.show()
                
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root) 

    def clear_cart(self):
        self.var_sid.set('')
        self.var_sname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"Disponibles")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Total\tItems:[0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):  
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Bienvenido!! Sistema Inventarios Moto Partes MSA\t\t Fecha: {str(date_)}\t\t Hora: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    #this code lines are disigned for windows os
    #def print_bill(self):
        #if self.chk_print==1:
            #messagebox.showinfo('Estado Impresora!!!',"Por favor esperar, imprimiendo!!!",parent=self.root)
            #new_file=tempfile.mktemp('.txt')
            #open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            #os.startfile(new_file,'print')
        #else:
            #messagebox.showerror('Estado Impresora!!!',"Por favor generar factura a imprimir!!!",parent=self.root)
    
    def print_bill(self):
        if self.chk_print == 1:
            new_file = tempfile.mktemp('.txt')
            with open(new_file, 'w') as f:
                f.write(self.txt_bill_area.get('1.0', END))
            
            # Preview the TXT file
            self.preview_txt(new_file)
            
            # Print the bill
            try:
                subprocess.run(["lp", new_file])
                messagebox.showinfo('Estado Impresora!!!', "Por favor esperar, imprimiendo!!!", parent=self.root)
            except FileNotFoundError:
                messagebox.showerror('Error', 'El comando "lp" no está disponible. No se pudo imprimir.', parent=self.root)
        else:
            messagebox.showerror('Estado Impresora!!!', "Por favor generar factura a imprimir!!!", parent=self.root)

    def preview_txt(self, txt_file):
        # Create a new window for TXT preview
        preview_window = Toplevel(self.root)
        preview_window.title("TXT Preview")
        
        # Create a Text widget and a Scrollbar
        text = Text(preview_window, wrap='word')
        text.pack(expand=1, fill='both')
        scrollbar = Scrollbar(preview_window, command=text.yview, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        text.config(yscrollcommand=scrollbar.set)
        
        # Insert content of the TXT file into the Text widget
        with open(txt_file, 'r') as f:
            content = f.read()
            text.insert(END, content)
    
        text.config(state='disabled')
        
    def logout(self):
        self.root.destroy()
        os.system("python login.py")       

if __name__=="__main__":  

    root=Tk()
    obj=billingClass(root)
    root.mainloop()
