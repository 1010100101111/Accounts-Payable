import re
import sqlite3
import tkinter
import tkinter.ttk
import tkinter.messagebox
from datetime import date
database=sqlite3.connect('C:\\Users\\christopher\\Downloads\\Python\\My Codes\\AccountPayables.db')
query=database.cursor()
window=tkinter.Tk()
try:
    window.wm_iconbitmap("pyc.ico")
except:
    try:
        window.wm_iconbitmap("C:\\Users\\christopher\\Downloads\\Python\\My Codes\\pyc.ico")
    except:
        pass
tkinter.messagebox.showinfo("RECCOMENDATIONS","Use full-screen mode to easy usage.")
window.title("Account Payables - PT. Express Transindo Utama.Tbk")
text=tkinter.Label(window,text="Click on the buttons to get information.")
text.grid(column=0,row=0)
result=tkinter.Label(window,text="")
result.grid(column=3,row=2)
def summary_info():
    query.execute('SELECT DISTINCT Vendor FROM details')
    vendor=query.fetchall()
    res=""
    for i in range(len(vendor)):
        query.execute('SELECT SUM(InvoiceAmount) FROM details WHERE Vendor="{}"'.format(vendor[i][0]))
        amount=query.fetchall()
        res+="Vendor : {}\nInvoice Amount : {}\n\n".format(vendor[i][0],int(amount[0][0]))
    result.configure(text="SUMMARY\n---------------\n\n"+res)
def detailed_info():
    query.execute('SELECT * FROM details')
    sqlfetch=query.fetchall()
    res="DETAILS\n---------------\n\n"
    for i in range(len(sqlfetch)):
        res+="Vendor : {}\nInvoice No. {}\nInvoice Date : {}\nInvoice Amount : {}\n\n".format(sqlfetch[i][0],sqlfetch[i][1],sqlfetch[i][2],int(sqlfetch[i][3]))
    result.configure(text=res)
def add():
    addtext0=tkinter.Label(window,text="Vendor : ")
    addtext0.grid(column=1,row=3)
    addtext1=tkinter.Label(window,text="Invoice No. ")
    addtext1.grid(column=3,row=3)
    addtext2=tkinter.Label(window,text="Date (YYYY-MM-DD format) : ")
    addtext2.grid(column=5,row=3)
    addtext3=tkinter.Label(window,text="Amount : ")
    addtext3.grid(column=7,row=3)
    entry0=tkinter.Entry(window,)
    entry0.grid(column=2,row=3)
    entry1=tkinter.Entry(window)
    entry1.grid(column=4,row=3)
    entry2=tkinter.Entry(window)
    entry2.grid(column=6,row=3)
    entry3=tkinter.Entry(window)
    entry3.grid(column=8,row=3)
    def get():
        vendor=entry0.get()
        no=entry1.get()
        date=entry2.get()
        amount=entry3.get()
        format_date=r"\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])*"
        if not re.match(format_date,date):
            tkinter.messagebox.showwarning("WRONG FORMAT","The format for date accepted is YYYY-MM-DD")
            return
        query.execute('INSERT INTO details VALUES ("{}","{}","{}",{})'.format(vendor,no,date,amount))
        database.commit()
        tkinter.messagebox.showinfo("DONE","Invoice has been added to database.")
    button_add=tkinter.Button(window,text="Confirm",command=get)
    button_add.grid(column=9,row=3)
    entry0.focus()
def pay():
    query.execute('SELECT DISTINCT Vendor FROM details')
    vendor=query.fetchall()
    list0=[]
    for i in range(len(vendor)):
        vendor_no=vendor[i][0]
        list0.append(vendor_no)
    addtext0=tkinter.Label(window,text="PAY-Vendor : ")
    addtext0.grid(column=1,row=4)
    addtext1=tkinter.Label(window,text="PAY-Invoice No. ")
    addtext1.grid(column=3,row=4)
    addtext2=tkinter.Label(window,text="PAY-Amount : ")
    addtext2.grid(column=5,row=4)
    combo0=tkinter.ttk.Combobox(window)
    combo0.grid(column=2,row=4)
    value0=[]
    for i in range(len(list0)):
        value0.append(list0[i])
    combo0['values']=tuple(value0)
    combo1=tkinter.ttk.Combobox(window)
    combo1.grid(column=4,row=4)
    entry=tkinter.Entry(window,state="disabled")
    entry.grid(column=6,row=4)
    def setpay():
        vendor=combo0.get()
        if vendor=="":
            tkinter.messagebox.showerror("ERROR","Please set the vendor name.")
            return
        query.execute('SELECT InvoiceNo FROM details WHERE Vendor="{}"'.format(vendor))
        list1=query.fetchall()
        value1=[]
        for i in range(len(list1)):
            value1.append(list1[i][0])
        combo1['values']=tuple(value1)
    def entrycheck():
        vendor=combo0.get()
        no=combo1.get()
        query.execute('SELECT InvoiceAmount FROM details WHERE Vendor="{}" AND InvoiceNo="{}"'.format(vendor,no))
        total=query.fetchall()
        addtext2.configure(text="Amount : {} PAY-Amount : ".format(int(total[0][0])))
        entry.configure(state='normal')
        entry.focus()
    button_set=tkinter.Button(window,text="Set vendor name",command=setpay)
    button_set.grid(column=2,row=5)
    button_conf=tkinter.Button(window,text="Show amount",command=entrycheck)
    button_conf.grid(column=4,row=5)
    def paid():
        vendor=combo0.get()
        no=combo1.get()
        try:
            amount=int(entry.get())
            assert amount>0
        except AssertionError:
            tkinter.messagebox.showerror('ERROR',"Enter a positive number.")
            return
        except:
            tkinter.messagebox.showerror("ERROR","Please enter a number.")
            return
        if amount<50000:
            tkinter.messagebox.showerror("ERROR","Minimum amount of invoice payment is Rp50.000")
            return
        query.execute('SELECT InvoiceAmount FROM details WHERE Vendor="{}" AND InvoiceNo="{}"'.format(vendor,no))
        total=query.fetchall()
        try:
            if total[0][0]=="":
                tkinter.messagebox.showerror("ERROR","We can't find the invoice in our database.\nPlease re-check your input.")
                return
        except IndexError:
            tkinter.messagebox.showerror("ERROR","We can't find the invoice in our database.\nPlease re-check your input.")
            return
        if amount>int(total[0][0]):
               tkinter.messagebox.showerror("ERROR","Your payment amount exceeds the invoice amount.")
        elif amount==int(total[0][0]):
            if tkinter.messagebox.askokcancel("Confirmation","Are you sure you want to pay this invoice?\n\nAmount = {}".format(int(total[0][0]))):
                query.execute('DELETE FROM details WHERE Vendor="{}" AND InvoiceNo="{}"'.format(vendor,no))
                database.commit()
                tkinter.messagebox.showinfo("Done","Successfully paid invoice no. {} to {}.".format(no,vendor))
            else:
                tkinter.messagebox.showinfo("CANCEL","Canceled payment to {} invoice no. {}".format(vendor,no))
                return
        else:
            remains=int(total[0][0])-amount
            if tkinter.messagebox.askokcancel("Confirmation - PARTIAL PAYMENT","Are you sure you want to pay this invoice?\n\nAmount = {}\nPayment amount = {}\nRemaining invoice amount = {}".format(int(total[0][0]),amount,remains)):
                query.execute('UPDATE details SET InvoiceAmount={} WHERE Vendor="{}" AND InvoiceNo="{}"'.format(remains,vendor,no))
                database.commit()
                tkinter.messagebox.showinfo("Done","Successfully paid invoice no. {} to {}.\nRemaining amount = {}".format(no,vendor,remains))
            else:
                tkinter.messagebox.showinfo("CANCEL","Canceled payment to {} invoice no. {}".format(vendor,no))
                return
    button_pay=tkinter.Button(window,text="Pay",command=paid)
    button_pay.grid(column=7,row=4)
try:
    pythonsig=tkinter.PhotoImage(file="Python-Powered.png")
    pythonlabel=tkinter.Label(window,image=pythonsig)
    pythonlabel.grid(column=0,row=5)
except:
        try:
            pythonsig = tkinter.PhotoImage(file="C:\\Users\\christopher\\Downloads\\Python\\My Codes\\Python-Powered.png")
            pythonlabel = tkinter.Label(window, image=pythonsig)
            pythonlabel.grid(column=0, row=5)
        except:
            pass
button1=tkinter.Button(window,text="Summary",command=summary_info)
button1.grid(column=0,row=1)
button2=tkinter.Button(window,text="Details",command=detailed_info)
button2.grid(column=0,row=2)
button3=tkinter.Button(window,text="Add invoice",command=add)
button3.grid(column=0,row=3)
button4=tkinter.Button(window,text="Pay invoice",command=pay)
button4.grid(column=0,row=4)
window.mainloop()
