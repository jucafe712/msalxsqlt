from tkinter import*
from PIL import ImageTk # pip install pillow
from tkinter import messagebox
import emailp
import sqlite3
import os
import smtplib
import time
import random
import string
from email.mime.text import MIMEText
class login:
    def __init__(self,root):
        self.root=root
        self.root.title("Acceso Sistema MotoStockApp")
        self.root.geometry("1350x700+0+0")
        #self.root.geometry("1199x600+100+50")
        self.root.resizable(False,False)
        self.root.config(bg="#FAFAFA")

        #images====

        #self.icon_side=PhotoImage(file="images/login12.jpg")

        #self.phone_image=ImageTk.PhotoImage(file="images/login1.png")
        #self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0)
        #self.bg=ImageTk.PhotoImage(file="images/login12.jpg")
        #self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwildth=1,relwidht=1)
        #self.bg=ImageTk.PhotoImage(file="images/login12.jpg")
        #self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwildth=1,relwidht=1)
        #===Login_Frame====
        self.employee_id=StringVar()
        self.password=StringVar()
        #self.username=StringVar()
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=150,y=90,width=500,height=460)
        #login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        #login_frame.place(x=650,y=90,width=350,height=460)

        #title=Label(login_frame,text="Ingreso Sistema MSA",font=("Elephant",30,"bold"),bg="white").place(x=0,y=100)
        title=Label(login_frame,text="Ingreso Sistema MSA",font=("Elephant",20,"bold"),fg="#d77337",bg="white").place(x=90,y=30)
        desc=Label(login_frame,text="Ingreso Funcionarios",font=("Goudy old style",15,"bold"),fg="#d25d17",bg="white").place(x=90,y=100)

        lbl_user=Label(login_frame,text="ID Funcionario",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=90,y=140)
        self.txt_user=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="lightgray")
        self.txt_user.place(x=90,y=170,width=350,height=35)

        lbl_pass=Label(login_frame,text="Clave",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=90,y=210)
        self.txt_pass=Entry(login_frame,textvariable=self.password,show="?",font=("times new roman",15),bg="lightgray")
        self.txt_pass.place(x=90,y=240,width=350,height=35)

        #forget_btn=Button(login_frame,text="Olvido Clave?",command=self.forget_win,bd=0,font=("times new roman",12),bg="white",fg="#d77337",activebackground="white",activeforeground="#00759E").place(x=90,y=280)
        #btn_login=Button(login_frame,command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0f0",bd=0,activebackground="#00B0F0",fg="white",activeforeground="#00759E",cursor="hand2").place(x=50,y=300,width=250,height=35)
        
        login_btn=Button(self.root,command=self.login,text="Login",bd=0,font=("times new roman",20),bg="#d77337",fg="white",activebackground="white",activeforeground="#00759E").place(x=360,y=410,width=180,height=40)
        #lbl_user=Label(login_frame,text="Username",font=("Andalus",15),bg="white",fg="#767171").place(x=0,y=200)
        
        #txt_username=Entry(login_frame,textvariable=self.username,font=("times new roman",15))

        #lbl_pass=Label(login_frame,text="Clave",font=("Andalus",15),bg=("white"),fg="#767171").place(x=0,y=10)
        #txt_pass=Entry(login_frame,textvariable=self.password,show="*"font=("times new roman",15),bg="white")

        #btn_login=Button(login_frame,command=self.login,text="Ingreso Sistema"),font=("Arial Rounded MT Bold",10)

        #hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        #or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_forget=Button(login_frame,text="Olvido Clave?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=100,y=390)

        ####frame2=======
        #register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        #register_frame.place(x=650,y=570,width=350,height=60)

        #lbl_reg=Label(register_frame,text="Suscribirse | Compartir",font=("times new roman",13),bg="white").place(x=40,y=20,relwidth=1)
        #btn_signup=Button(register_frame,text="Registrarse",font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=200,y=17)

        #animated images======
        #self.im1=ImageTk.PhotoImage(file="images/*")
        #self.im2=ImageTk.PhotoImage(file="images/*")
        #self.im3=ImageTk.PhotoImage(file="images/*")

        #self.lbl_change_image=Label(self.root,bg="white")
        #self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        #self.animate()

        #====all functions======


    #def animate(self):

            #self.im=self.im1
            #self.im1=self.im2
            #self.im2=self.im
            #self.im3=self.im
            #self.lbl_change_image.config(image=self.im)
            #self.lbl_change_image.after(2000,self.animate)
    
    def login(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error!',"Llene todo los campos!!!",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error!',"Nombre / Clave:Usuario Invalido!!!",parent=self.root)
                else:
                    #print(user)
                    if user[0]!="Adminstrador":
                        self.root.destroy()
                        os.system("python billing.py")
                    else:
                        self.root.destroy()
                        os.system("python dashboard.py")

        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root) 

    def forget_window(self):
        con=sqlite3.connect(database=r'msa.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error!',"Id funcionario Requerido!!!",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error!',"ID funcionario incorrecto!!!",parent=self.root)
                else:
                    #====Forget Window=====
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send_email_function()
                    chk=self.send_email(email[0])
                if chk=='f':
                        messagebox.showerror("Atencion!!","Error de conexion!!!",parent=self.root)
                else:
                    self.forget_win=Toplevel(self.root)
                    self.forget_win.title('Reestablecer Clave')
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()
                    self.btn_reset=Button(self.forget_win,text="Enviar",command=self.validate_otp,font=("times new roman",15),bg='lightblue')
                    self.btn_reset.place(x=280,y=100,width=100,height=30)


                    title=Label(self.forget_win,text='Reestablecer Clave',font=('goudy old style',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                    lbl_reset=Label(self.forget_win,text="Ingrese OTP Enviado a correo",font=("times new roman",15)).place(x=20,y=60)
                    txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg='lightyellow').place(x=20,y=100,width=250,height=30)
                        
                    lbl_new_pass=Label(self.forget_win,text='Ingrese Nueva Clave',font=("times new roman",15)).place(x=20,y=160)
                    txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg='lightyellow').place(x=20,y=190,width=250,height=30)
                        
                    lbl_c_pass=Label(self.forget_win,text='Reescriba Clave',font=("times new roman",15)).place(x=20,y=225)
                    txt_c_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg='lightyellow').place(x=20,y=255,width=250,height=30)
                        
                    self.btn_update=Button(self.forget_win,text="Actualizar",command=self.update_password,state=DISABLED,font=("times new roman",15),bg='lightblue')
                    self.btn_update.place(x=150,y=300,width=100,height=30)
                    
        
        except Exception as ex:
            messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root) 

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error!!", "Clave necesaria",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Atencion!!!", "Clave NO es igual!!!",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'msa.db')
            cur=con.cursor()
            try:
                cur.execute("update employee set pass=? where eid=?",(self.var_new_pass.get(),self.employee_id))
                con.commit()
                messagebox.showinfo("Atencion!!!","Clave Actualizada Exitosamente!!!",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error!",f"Error due to:{str(ex)}",parent=self.root)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Atencion!!","Codigo OTP Invalido!!",parent=self.forget_win)

    def send_email(self,to_): 
        s=smtplib.SMTP('smtp.live.com',587)
        s.starttls()
        email_=emailp.email_
        pass_=emailp.pass_
        

        s.login(email_,pass_)

        self.otp=int(time.strftime('%H%M%S'))+int(time.strftime("%S"))
        #print(self.otp)
        
        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\n With Regards,\nMSA Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        #s.send(bytes(magicword, "utf-8"))
        s.sendmail(email_, to_, msg.encode('utf-8'))
        #s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'


    

if __name__=="__main__":  
    root=Tk()
    obj=login(root)
    root.mainloop()