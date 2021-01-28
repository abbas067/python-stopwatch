# Python program to illustrate a stop watch  
# using Tkinter  
#importing the required libraries
import requests,json
import pyodbc
import tkinter as tk 
import tkinter as Tkinter 
from tkinter import *
from tkinter import ttk
from datetime import date
from datetime import datetime
counter = 66600
running = False
p1_var=None
time=0
global L1,L2,L3
L2=[]
L1=[]
L3=[]
def counter_label(label):  
    def count():  
        if running:  
            global counter,display
    
            # To manage the intial delay.  
            if counter==66600:
                display="Starting..."
            else: 
                tt = datetime.fromtimestamp(counter) 
                string = tt.strftime("%H:%M:%S") 
                display=string  
    
            label['text']=display   # Or label.config(text=display)  
            print(display)
            # label.after(arg1, arg2) delays by   
            # first argument given in milliseconds  
            # and then calls the function given as second argument.  
            # Generally like here we need to call the   
            # function in which it is present repeatedly.  
            # Delays by 1000ms=1 seconds and call count again.  
            label.after(1000, count)   
            counter += 1
    
    # Triggering the start of the counter.  
    count()       
    
# start function of the stopwatch
def db():
    conn = pyodbc.connect('Driver={SQL Server native client 11.0};'
                      'Server=stopwatchdbserver.database.windows.net;'
                      'Database=stopwatchdb;'
                      "UID=azureuser;"
                        "PWD=Abbaskhan.92;"
                      'Trusted_Connection=no;')
    if (conn):
    # Carry out normal procedure
      print ("Connection successful")
      cursor = conn.cursor()
      query = ("INSERT INTO dbo.extendstopwatch(Person,Date,Time,Client,Project,Module,Task,Billable,Worktype,Description) VALUES (?,?,?,?,?,?,?,?,?,?)")    
      Values =[pname,today,display,client,project,module,task,bill,work,description]   
      cursor.execute(query,Values)
    #Commiting any pending transaction to the database.    
      conn.commit()
      print("Data Successfully Inserted")   
    else:
    # Terminate
      print ("Connection unsuccessful")
      # disconnect from server
      con.close()
def postdata():
    global bill
    if var1.get()==1:
        bill='t'
    else:
        bill='f'
    if pro.get()==L[0]:
        pid=959242
        url3="https://api.myintervals.com/projectworktype/?projectid=959242"
        url2="https://api.myintervals.com/projectmodule/?projectid=959242"
    if pro.get()==L[1]:
        pid=1002089
        url3="https://api.myintervals.com/projectworktype/?projectid=1002089"
        url2="https://api.myintervals.com/projectmodule/?projectid=1002089"

    if pro.get()==L[2]:
        pid=927405
        url3="https://api.myintervals.com/projectworktype/?projectid=927405"
        url2="https://api.myintervals.com/projectmodule/?projectid=927405"
    try:
        r4=requests.get(url3,headers=headers)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    data4=r4.json()
    proworktype=data4['projectworktype']
    worktype = [ sub['worktype'] for sub in proworktype ]
    worktypeid=[ sub['worktypeid'] for sub in proworktype ]
  
# using dictionary comprehension 
# to convert lists to dictionary 
    res = {worktype[i]:(worktypeid[i]) for i in range(len(worktype))}
    workid=res.get(workchoosen.get())
    pt = datetime.strptime(display,'%H:%M:%S')
    time= float(pt.second/3600 + pt.minute/60+ pt.hour)
    try:
        r2=requests.get(url2,headers=headers)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    data2=r2.json()
    projectmodule=data2['projectmodule']
    module = [ sub['module'] for sub in projectmodule ]
    moduleid=[ sub['moduleid'] for sub in projectmodule ]
#print(data2)
  
# using dictionary comprehension 
# to convert lists to dictionary 
    res1= {module[i]:moduleid[i] for i in range(len(module))} 
# Printing resultant dictionary  
    modid=res1.get(modchoosen.get())
    d={  "projectid":pid,
     "moduleid":modid,
    "worktypeid":workid,
    "personid": 339905,
    "date": passw_entry.get(),
    "time":time,
    "billable":bill,
     "description":description
}
    response = requests.post('https://api.myintervals.com/time/',headers=headers,json=d)
    print("Status code: ", response.status_code)
    print("Printing Entire Post Request")
    print(response.json())
def Start(label):  
    global running  
    running=True
    counter_label(label)  
    start['state']='disabled'
    stop['state']='normal'
    reset['state']='normal'
#sum time
def sum(L1):
    import datetime
    mysum = datetime.timedelta()
    for i in L1:
        (h, m, s) = i.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        mysum += d
    return str(mysum)

# Stop function of the stopwatch
def Stop():  
    global running
    start['state']='normal'
    stop['state']='disabled'
    reset['state']='normal'
    running = False
   # p_entry=tk.Entry(root, 
   #                textvariable= p1_var,
    #                font = ('calibre',10,'normal'), 
     #               )
   # p_entry.pack()
   # p_entry.insert(END, [display,pro.get()])
    if pro.get()==L[0]:
        time=display
        L1.append(time)
        p1_entry.delete(0,END)   #Clear the text window so we can write.

        p1_entry.insert(END,sum(L1))
        Reset(label)
    if pro.get()==L[1]:
        time=display
        L2.append(time)
        p2_entry.delete(0,END)   #Clear the text window so we can write.

        p2_entry.insert(END,sum(L2))
        Reset(label)

    if pro.get()==L[2]:
        time=display
        L3.append(time)
        p3_entry.delete(0,END)   #Clear the text window so we can write.

        p3_entry.insert(END, sum(L3))
        Reset(label)

# Reset function of the stopwatch  
def Reset(label):  
    global counter  
    counter=66600
    
    # If rest is pressed after pressing stop.  
    if running==False:        
        reset['state']='disabled'
        label['text']='Welcome!'
    
    # If reset is pressed while the stopwatch is running.  
    else:                 
        label['text']='Starting...'
def get(n):
    global pname
    global assignby,today,client,project,module,task,description,bill,work
    pname=name_entry.get() 
    assignby=passw_entry.get()
    client=cli_entry.get() 
    project=p_entry.get()

    module=modchoosen.get()  
    task=taskchoosen.get()
    work=workchoosen.get()
    description=desc_entry.get() 
    project=pro.get() 
    if n==1:
        display=p1_entry.get()
    if n==2:
        display=p2_entry.get()
    if n==3:
        display=p3_entry.get()
    if var1.get()==1:
        bill='t'
    else:
        bill='f'
    print("Peson name is : " + pname)
    today = date.today()
    print("date:", today)
    print("time  is : " + display)
    print("cilent  is : "+client )
    print("module  is : "+module )
    print("task  is : " +task)
    print("task  is : " +work)
    print("project  is : " +project)

    print("billable:",bill)

    print("description  is : " + description)
    #print("time:"+display)
    name_var.set("") 
    passw_var.set("")
    #db()
    postdata()
def open(args):
    global n
    if args==1:
        n=1
        print("button 1")
    if args==2:
        n=2
        print("button 2")
    if args==3:
        n=3
        print("button 3")
    Stop()
    root=tk.Tk()
    root.geometry('350x350') 
    global name_var
    global passw_var
    name_var=tk.StringVar() 
    passw_var=tk.StringVar()
    time_var=tk.StringVar()
# creating a label for person

    name_label = tk.Label(root, text = 'Person', 
                      font=('calibre', 
                            10, 'bold'))
    global name_entry
    name_entry = tk.Entry(root,textvariable= name_var,font=('calibre',10,'normal')) 
    name_entry.insert(END, person)
# creating a label for date 
    passw_label = tk.Label(root, 
                       text = 'Date', 
                       font = ('calibre',10,'bold')) 
    global passw_entry
# creating a entry for date
    passw_entry=tk.Entry(root, 
                     textvariable = passw_var, 
                     font = ('calibre',10,'normal'), 
                     ) 
    passw_entry.insert(END,date.today()) 

# creating a label for time 
    t_label = tk.Label(root, 
                       text = 'Time', 
                       font = ('calibre',10,'bold')) 

    global t_entry
# creating a entry for time
    t_entry=tk.Entry(root, 
                     font = ('calibre',10,'normal'), 
                     )
    if args==1:
        display=p1_entry.get()
    if args==2:
        display=p2_entry.get()
    if args==3:
        display=p3_entry.get()
    t_entry.insert(END,display)

# creating a label for client 
    cli_label = tk.Label(root, 
                       text = 'Client', 
                       font = ('calibre',10,'bold')) 

    global cli_entry
# creating a entry for client
    cli_entry=tk.Entry(root, 
                     font = ('calibre',10,'normal'), 
                     ) 
    cli_entry.insert(END,'Nathcorp') 
# creating a label for module 
    Mod_label = tk.Label(root, 
                       text = 'Module', 
                       font = ('calibre',10,'bold'))
   
  
# Adding combobox drop down list for module 
    n1 = tk.StringVar() 
    global modchoosen
    modchoosen = ttk.Combobox(root, width = 27)
    if pro.get()==L[0]:
        url4="https://api.myintervals.com/projectmodule/?projectid=959242"
    if pro.get()==L[1]:
        url4="https://api.myintervals.com/projectmodule/?projectid=1002089"
    if pro.get()==L[2]:
        url4="https://api.myintervals.com/projectmodule/?projectid=927405"
    r2=requests.get(url4,headers=headers)
    data2=r2.json()
    projectmodule=data2['projectmodule']
    module = [ sub['module'] for sub in projectmodule ]
    modchoosen['values'] = (module) 


# creating a label for task 
    task_label = tk.Label(root, 
                       text = 'Task', 
                       font = ('calibre',10,'bold'))
    n2 = tk.StringVar() 
    global taskchoosen

    taskchoosen = ttk.Combobox(root, width = 27,  
                            textvariable = n2)
#filter task data based on module id
    #modid=res.get(modchoosen.get())
    #url5="https://api.myintervals.com/task/?moduleid=modid"
    #r5=requests.get(url5,headers=headers)
    #data5=r5.json()
    
# Adding combobox drop down list for task 
    taskchoosen['values'] = () 
   
  
# creating a label for worktype 
    work_label = tk.Label(root, 
                       text = 'Worktype', 
                       font = ('calibre',10,'bold'))
    n3 = tk.StringVar() 
    global workchoosen
    workchoosen = ttk.Combobox(root, width = 27,  
                            textvariable = n3)
    if pro.get()==L[0]:
        url3="https://api.myintervals.com/projectworktype/?projectid=959242"
    if pro.get()==L[1]:
        url3="https://https://api.myintervals.com/projectworktype/?projectid=1002089"
    if pro.get()==L[2]:
        url3="https://api.myintervals.com/projectworktype/?projectid=927405"
    r4=requests.get(url3,headers=headers)
    data4=r4.json()
    projectworktype=data4['projectworktype']
    worktype = [ sub['worktype'] for sub in projectworktype ]
# Adding combobox drop down list for worktype 
    workchoosen['values'] = (worktype)
# Shows Documentation as a default value 
    workchoosen.current(1)  
# creating a label for bilable 
    bill_label = tk.Label(root, 
                       text = 'Bilable', 
                       font = ('calibre',10,'bold'))

#check button
    global var1
    var1 = StringVar()
    Button1 = Checkbutton(root, 
                      variable = var1,
                          onvalue=1, offvalue=0
                          )
    var1.set(0)   # Default value is kept as unchecked

# creating a label for description 
    desc_label = tk.Label(root, 
                       text = 'Description', 
                       font = ('calibre',10,'bold'))
    global desc_entry
# creating a entry for description
    desc_entry=tk.Entry(root, 
                     font = ('calibre',10,'normal')) 
 # creating a button using the widget  
# Button that will call the submit function     
    sub_btn=tk.Button(root,text = 'Submit',command=lambda:get(n)) 
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    passw_label.grid(row=1,column=0)
    passw_entry.grid(row=1,column=1)
    t_label.grid(row=2,column=0)
    t_entry.grid(row=2,column=1)
    cli_label.grid(row=3,column=0)
    cli_entry.grid(row=3,column=1)
    Mod_label.grid(row=5,column=0)
    modchoosen.grid(column = 1, row =5) 
    task_label.grid(row=6,column=0)
    taskchoosen.grid(column = 1, row =6) 
    work_label.grid(row=7,column=0)
    workchoosen.grid(column = 1, row =7) 

    bill_label.grid(row=8,column=0)
    Button1.grid(row=8,column=1)
    desc_label.grid(row=9,column=0)
    desc_entry.grid(row=9,column=1)

    sub_btn.grid(row=10,column=1)
root = Tkinter.Tk()  
root.title("Stopwatch")  
    
# Fixing the window size.  
root.minsize(width=350, height=100)  
label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")  
label.pack()
#p_entry=tk.Entry(root, 
     #                textvariable= p1_var,
      #               
       #              font = ('calibre',10,'normal'), 
        #             )
#p_entry.pack()
#p_entry.insert(END, 'HRIS')

n3 = tk.StringVar() 
global pro
pro= ttk.Combobox(root, width = 27,  
                            textvariable = n3) 
  
# Adding combobox drop down list for worktype

#adding json data from intervals
L=[]
id=[]
password='NTYyZ3BiN3psZzE6YWJiYXNraGFuLjky'
headers={'Host': 'api.myintervals.com',
'Accept': 'application/json',
         'Authorization':'Basic NTYyZ3BiN3psZzE6YWJiYXNraGFuLjky'
         }
url="https://api.myintervals.com/project/"
url1="https://nathcorp.projectaccount.com/time/"
r=requests.get(url,headers=headers)
data=r.json()
project=data['project']
res = [ sub['name'] for sub in project ]
res1 = [ sub['id'] for sub in project ] 

#print(r.text)
for r in res:
    L.append(r)
for r1 in res1:
    id.append(r1)
r1=requests.get(url1,headers=headers)
data1=r1.json()
person=data1['time'][0]['person']

    
pro['values']=(L)
pro.pack()
f = Tkinter.Frame(root) 
start = Tkinter.Button(f, text='Start', width=6, command=lambda:Start(label))  
stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop)  
reset = Tkinter.Button(f, text='Reset',width=6, state='disabled', command=lambda:Reset(label))  
f.pack(anchor = 'center',pady=5) 
start.pack(side="left")  
stop.pack(side ="left")  
reset.pack(side="left")


p_entry=tk.Entry(root, 
                   textvariable= p1_var,
                    font = ('calibre',10,'normal'), 
                    )
p_entry.pack()
p_entry.insert(END, L[0])
p1_entry=tk.Entry(root, 
                   textvariable= p1_var,
                    font = ('calibre',10,'normal'), 
                    )
p1_entry.pack()
f1 = Tkinter.Frame(root) 
f1.pack(anchor = 'center',pady=5)
submit = Tkinter.Button(f1, text='Submit',width=6, command=lambda:open(1))  
submit.pack(side="left")  


p_entry=tk.Entry(root, 
                   textvariable= p1_var,
                    
                    font = ('calibre',10,'normal'), 
                    )
p_entry.pack()
p_entry.insert(END, L[1])
p2_entry=tk.Entry(root, 
                   textvariable= p1_var,
                    font = ('calibre',10,'normal'), 
                    )
p2_entry.pack()
f2 = Tkinter.Frame(root) 
f2.pack(anchor = 'center',pady=5)
submit = Tkinter.Button(f2, text='Submit',width=6, command=lambda:open(2))  
submit.pack(side="left")


p_entry=tk.Entry(root, 
                   textvariable= p1_var,
                    
                    font = ('calibre',10,'normal'), 
                    )
p_entry.pack()
p_entry.insert(END, L[2])
p3_entry=tk.Entry(root, 
                   textvariable= p1_var,
                    font = ('calibre',10,'normal'), 
                    )
p3_entry.pack()
f3 = Tkinter.Frame(root) 
f3.pack(anchor = 'center',pady=5)
submit = Tkinter.Button(f3, text='Submit',width=6, command=lambda:open(3))  
submit.pack(side="left")



root.mainloop() 

  
  



