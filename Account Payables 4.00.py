import re
import sqlite3
import tkinter
import tkinter.ttk
import tkinter.messagebox
from datetime import date
try:
    database=sqlite3.connect('AccountPayables.db')
except:
    database = sqlite3.connect('C:\\Users\\christopher\\Downloads\\Python\\My Codes\\AccountPayables.db')
query=database.cursor()
window=tkinter.Tk()
try:
    window.wm_iconbitmap("pyc.ico")
except:
    try:
        window.wm_iconbitmap("C:\\Users\\christopher\\Downloads\\Python\\My Codes\\pyc.ico")
    except:
        pass
try:
    query.execute("CREATE TABLE IF NOT EXISTS moredetails(Vendor varchar NOT NULL, InvoiceNo varchar NOT NULL PRIMARY KEY, InvoiceDate timestamp without timezone NOT NULL, InvoiceAmount int NOT NULL, DueDate timestamp without timezone);")
except:
    pass
finally:
    database.commit()
    print("Database ready.")
def refresh():
    today=str(date.today())
    query.execute('SELECT * FROM moredetails WHERE DueDate>={}'.format(today))
    duedates=query.fetchall()
    if not duedates==[]:
        for res in duedates:
            if res[4]=="None":
                continue
            query.execute('SELECT DueDate FROM moredetails WHERE Vendor="{}" AND InvoiceNo="{}"'.format(res[0],res[1]))
            duedate=query.fetchall()
            message="is today" if duedate[0][0]==today else "has expired"
            tkinter.messagebox.showinfo("SYSTEM - Due date alert","Invoice no.{} from vendor {}'s due date {}. ".format(res[1],res[0],message))
    query.execute('SELECT DISTINCT Vendor FROM moredetails')
    vendor=query.fetchall()
    list0=[]
    for i in range(len(vendor)):
        vendor_no=vendor[i][0]
        list0.append(vendor_no)
    value0=[]
    for i in range(len(list0)):
        value0.append(list0[i])
    combo0['values']=tuple(value0)
    button_conf.configure(state="disabled")
    entry.configure(state='disabled')
    button_pay.configure(state="disabled")
    summary_info()
    detailed_info()
tkinter.messagebox.showinfo("RECCOMENDATIONS","Use full-screen mode to easy usage.")
window.title("Account Payables - PT. Express Transindo Utama.Tbk")
tabControl = tkinter.ttk.Notebook(window) # Create Tab Control
tab1 = tkinter.ttk.Frame(tabControl)
tabControl.add(tab1, text='Summary AP')
tab2 = tkinter.ttk.Frame(tabControl)
tabControl.add(tab2, text='Detailed AP')
tab3 = tkinter.ttk.Frame(tabControl)
tabControl.add(tab3, text='Add Invoice')
tab4 = tkinter.ttk.Frame(tabControl)
tabControl.add(tab4, text='Pay Invoice')
tabControl.grid(column=0,row=0)
try:
    pythonsig=tkinter.PhotoImage(file="Python-Powered.png")
    pythonlabel=tkinter.Label(window,image=pythonsig)
    pythonlabel.grid(column=0,row=1)
except:
        try:
            pythonsig=tkinter.PhotoImage(file="C:\\Users\\christopher\\Downloads\\Python\\My Codes\\Python-Powered.png")
            pythonlabel=tkinter.Label(window, image=pythonsig)
            pythonlabel.grid(column=0, row=5)
        except:
            pass
summary = tkinter.ttk.LabelFrame(tab1,text='  Summary Account Payables  ')
summary.grid(column=0, row=0)
result_sum=tkinter.Label(summary,text="")
result_sum.grid(column=0,row=0)
def summary_info():
    query.execute('SELECT DISTINCT Vendor FROM moredetails')
    vendor=query.fetchall()
    res=""
    for i in range(len(vendor)):
        query.execute('SELECT SUM(InvoiceAmount) FROM moredetails WHERE Vendor="{}"'.format(vendor[i][0]))
        amount=query.fetchall()
        res+="Vendor : {}\nInvoice Amount : {:_}\n\n".format(vendor[i][0],int(amount[0][0])).replace("_",",")
    result_sum.configure(text="SUMMARY\n---------------\n\n"+res)
button1=tkinter.Button(summary,text="Summary",command=summary_info)
button1.grid(column=0,row=1)
details = tkinter.ttk.LabelFrame(tab2,text='  Detailed Account Payables  ')
details.grid(column=0, row=0)
result_det=tkinter.Label(details,text="")
result_det.grid(column=0,row=0)
def detailed_info():
    query.execute('SELECT * FROM moredetails')
    sqlfetch=query.fetchall()
    res="DETAILS\n---------------\n\n"
    for i in range(len(sqlfetch)):
        res+="Vendor : {}\nInvoice No. {}\nInvoice Date : {}\nInvoice Amount : {:_}\nDue Date : {}\n\n".format(sqlfetch[i][0],sqlfetch[i][1],sqlfetch[i][2],int(sqlfetch[i][3]),sqlfetch[i][4]).replace("_",",")
    result_det.configure(text=res)
button2=tkinter.Button(details,text="Details",command=detailed_info)
button2.grid(column=0,row=1)
add_frame = tkinter.ttk.LabelFrame(tab3,text='  Add Invoice  ')
add_frame.grid(column=0, row=0)
addtext0=tkinter.Label(add_frame,text="Vendor")
addtext0.grid(column=0,row=0)
addtext1=tkinter.Label(add_frame,text="Invoice No.")
addtext1.grid(column=0,row=3)
addtext2=tkinter.Label(add_frame,text="Date (YYYY-MM-DD format)")
addtext2.grid(column=0,row=5)
addtext3=tkinter.Label(add_frame,text="Amount")
addtext3.grid(column=0,row=7)
addtext4=tkinter.Label(add_frame,text="Due date(if any)")
addtext4.grid(column=0,row=9)
entry0=tkinter.Entry(add_frame,width=20)
entry0.grid(column=0,row=2)
entry1=tkinter.Entry(add_frame,width=20)
entry1.grid(column=0,row=4)
entry2=tkinter.Entry(add_frame,width=20)
entry2.grid(column=0,row=6)
entry3=tkinter.Entry(add_frame,width=20)
entry3.grid(column=0,row=8)
entry4=tkinter.Entry(add_frame,width=20)
entry4.grid(column=0,row=10)
def get():
    vendor=entry0.get()
    no=entry1.get()
    date=entry2.get()
    amount=entry3.get()
    duedate=entry4.get()
    format_date=r"\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])*"
    if not re.match(format_date,date):
        tkinter.messagebox.showwarning("WRONG FORMAT","The format for date accepted is YYYY-MM-DD")
        return
    if duedate=="":
        duedate=None
    query.execute('INSERT INTO moredetails VALUES ("{}","{}","{}",{},"{}")'.format(vendor,no,date,amount,duedate))
    database.commit()
    refresh()
    tkinter.messagebox.showinfo("DONE","Invoice has been added to database.")
button_add=tkinter.Button(add_frame,text="Confirm",command=get)
button_add.grid(column=0,row=11)
entry0.focus()
pay_frame = tkinter.ttk.LabelFrame(tab4,text='  Pay Invoice  ')
pay_frame.grid(column=0, row=0)
today=str(date.today())
query.execute('SELECT * FROM moredetails WHERE DueDate>={}'.format(today))
duedates=query.fetchall()
if not duedates==[]:
    for res in duedates:
        if res[4]=="None":
            continue
        query.execute('SELECT DueDate FROM moredetails WHERE Vendor="{}" AND InvoiceNo="{}"'.format(res[0],res[1]))
        duedate=query.fetchall()
        message="is today" if duedate[0][0]==today else "has expired"
        tkinter.messagebox.showinfo("SYSTEM - Due date alert","Invoice no.{} from vendor {}'s due date {}. ".format(res[1],res[0],message))
query.execute('SELECT DISTINCT Vendor FROM moredetails')
vendor=query.fetchall()
list0=[]
for i in range(len(vendor)):
    vendor_no=vendor[i][0]
    list0.append(vendor_no)
addtext0=tkinter.Label(pay_frame,text="PAY-Vendor : ")
addtext0.grid(column=0,row=0)
addtext1=tkinter.Label(pay_frame,text="PAY-Invoice No. ")
addtext1.grid(column=0,row=1)
addtext2=tkinter.Label(pay_frame,text="PAY-Amount : ")
addtext2.grid(column=0,row=2)
combo0=tkinter.ttk.Combobox(pay_frame)
combo0.grid(column=1,row=0)
value0=[]
for i in range(len(list0)):
    value0.append(list0[i])
combo0['values']=tuple(value0)
combo1=tkinter.ttk.Combobox(pay_frame)
combo1.grid(column=1,row=1)
entry=tkinter.Entry(pay_frame,state="disabled")
entry.grid(column=1,row=2)
def setpay():
    vendor=combo0.get()
    if vendor=="":
        tkinter.messagebox.showerror("ERROR","Please set the vendor name.")
        return
    query.execute('SELECT InvoiceNo FROM moredetails WHERE Vendor="{}"'.format(vendor))
    list1=query.fetchall()
    value1=[]
    for i in range(len(list1)):
        value1.append(list1[i][0])
    combo1['values']=tuple(value1)
    button_conf.configure(state="normal")
def entrycheck():
    vendor=combo0.get()
    no=combo1.get()
    query.execute('SELECT InvoiceAmount FROM moredetails WHERE Vendor="{}" AND InvoiceNo="{}"'.format(vendor,no))
    total=query.fetchall()
    addtext2.configure(text="Amount : {:_} PAY-Amount : ".format(int(total[0][0])).replace("_",","))
    entry.configure(state='normal')
    button_pay.configure(state="normal")
    entry.focus()
button_set=tkinter.Button(pay_frame,text="Set vendor name",command=setpay)
button_set.grid(column=2,row=0)
button_conf=tkinter.Button(pay_frame,text="Show amount",command=entrycheck,state="disabled")
button_conf.grid(column=2,row=1)
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
    query.execute('SELECT InvoiceAmount FROM moredetails WHERE Vendor="{}" AND InvoiceNo="{}"'.format(vendor,no))
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
        if tkinter.messagebox.askokcancel("Confirmation","Are you sure you want to pay this invoice?\n\nAmount = {:_}".format(int(total[0][0])).replace("_",",")):
            query.execute('DELETE FROM moredetails WHERE Vendor="{}" AND InvoiceNo="{}"'.format(vendor,no))
            database.commit()
            refresh()
            tkinter.messagebox.showinfo("Done","Successfully paid invoice no. {} to {}.".format(no,vendor))
        else:
            tkinter.messagebox.showinfo("CANCEL","Canceled payment to {} invoice no. {}".format(vendor,no))
            return
    else:
        remains=int(total[0][0])-amount
        if tkinter.messagebox.askokcancel("Confirmation - PARTIAL PAYMENT","Are you sure you want to pay this invoice?\n\nAmount = {:_}\nPayment amount = {:_}\nRemaining invoice amount = {:_}".format(int(total[0][0]),amount,remains).replace("_",",")):
            query.execute('UPDATE moredetails SET InvoiceAmount={} WHERE Vendor="{}" AND InvoiceNo="{}"'.format(remains,vendor,no))
            database.commit()
            refresh()
            tkinter.messagebox.showinfo("Done","Successfully paid invoice no. {} to {}.\nRemaining amount = {:_}".format(no,vendor,remains).replace("_",","))
        else:
            tkinter.messagebox.showinfo("CANCEL","Canceled payment to {} invoice no. {}".format(vendor,no))
            return
button_pay=tkinter.Button(pay_frame,text="Pay",command=paid,state="disabled")
button_pay.grid(column=2,row=2)

window.mainloop()
