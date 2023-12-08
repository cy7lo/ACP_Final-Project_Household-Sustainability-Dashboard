# Libraries
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
import pymysql

# FUNCTIONS
# Data info
def dataInfo(ev):
    viewInfo = data_records.focus()
    eData = data_records.item(viewInfo)
    row = eData["values"]
    ElectricityID.set(row[0])
    ElectricityDate.set(row[1])
    EnergyConsumption.set(row[2])
    Costpk.set(row[3])
    TotalBill.set(row[4])

# Add data
    # database = Electricity_Db
    # table = Electricity_Tbl
def addData():
    if entElecDate.get() == " " or entEnergyCon.get() == " " or entCostpk.get() == " ":
        messagebox.showerror("Household Sustainability Dashboard", "Please enter all data.")
    
    else:
        try:
            sqlCon = pymysql.connect(host="localhost", user="root", password="", database="Electricity_Db")
            cur = sqlCon.cursor()
            query = "INSERT INTO Electricity_Tbl (ElectricityDate, EnergyConsumption, Costpk) VALUES (%s, %s, %s)"
            values = (entElecDate.get(), entEnergyCon.get(), entCostpk.get())
            cur.execute(query, values)
            
            sqlCon.commit()
            sqlCon.close()
            messagebox.showinfo("Household Sustainability Dashboard", "Record entered successfully!")
            resetData()
        
        except Exception as e:
            messagebox.showerror("Household Sustainability Dashboard", "Please enter all data.")

# Display data
def displayData():
    sqlCon = pymysql.connect(host="localhost", user="root", password="", database="Electricity_Db")
    cur = sqlCon.cursor()
    query = "SELECT * FROM Electricity_Tbl"
    cur.execute(query)
    
    result = cur.fetchall()
    data_records.delete(*data_records.get_children())  # Clear existing data
    
    if len(result) != 0:
        for row in result:
            total_bill = float(row[2]) * float(row[3])
            data_records.insert("", END, values=(row[0], row[1], row[2], row[3], total_bill))
        sqlCon.commit()
    sqlCon.close()

# Clear date entry field when cursor clicks
def user_enter(event):
    if entElecDate.get() == "Month and Year":
        entElecDate.delete(0, END)

# Display bill
def displayBill():
    try:
        energy_consumption = float(entEnergyCon.get())
        cost_per_kw = float(entCostpk.get())
        total_bill = energy_consumption * cost_per_kw
        TotalBill.set(total_bill)
    except ValueError:
        pass

# Update data
def updateData():
    selected_item = data_records.selection()
    if not selected_item:
        messagebox.showerror("Household Sustainability Dashboard", "Please select a record to update.")
        return
    
    try:
        sqlCon = pymysql.connect(host="localhost", user="root", password="", database="Electricity_Db")
        cur = sqlCon.cursor()

        # Get selected row values
        row_id = data_records.item(selected_item, 'values')[0]
        cur.execute(
            "UPDATE Electricity_Tbl SET ElectricityDate=%s, EnergyConsumption=%s, Costpk=%s, TotalBill=%s\
            WHERE ElectricityID=%s",
            (entElecDate.get(), entEnergyCon.get(), entCostpk.get(), TotalBill.get(), row_id)
        )

        sqlCon.commit()
        sqlCon.close()
        messagebox.showinfo("Household Sustainability Dashboard", "Record updated successfully!")
        displayData()
    
    except Exception as e:
        messagebox.showerror("Household Sustainability Dashboard", "Please enter all data.")
    
# Delete data
def deleteData():
    sqlCon=pymysql.connect(host="localhost",user="root",password="",database="Electricity_Db")
    cur=sqlCon.cursor()
    cur.execute("DELETE FROM Electricity_Tbl WHERE ElectricityID= %s",ElectricityID.get())
    
    sqlCon.commit()
    displayData()
    sqlCon.close()
    messagebox.showinfo("Household Sustainability Dashboard", "Record deleted succesfully!")

# Search data
def searchData():
    try:
        sqlCon = pymysql.connect(host="localhost", user="root", password="", database="Electricity_Db")
        cur = sqlCon.cursor()
        cur.execute("SELECT * FROM Electricity_Tbl WHERE ElectricityID=%s or ElectricityDate=%s or EnergyConsumption=%s or Costpk=%s or TotalBill=%s",
                    (entElecID.get(), entElecDate.get(), entEnergyCon.get(), entCostpk.get(), entTotalBill.get()))
        row = cur.fetchone()
        
        ElectricityID.set(row[0])
        ElectricityDate.set(row[1])
        EnergyConsumption.set(row[2])
        Costpk.set(row[3])
        TotalBill.set(row[4])
    
    except:
        messagebox.showerror("Household Sustainability Dashboard", "No record found.")
    
    finally:
        sqlCon.close()

# Reset data
def resetData():
    ElectricityID.set(0)
    ElectricityDate.set("Month and Year")
    EnergyConsumption.set(0)
    Costpk.set(0.0)
    TotalBill.set(0.0)
    
    # Clear
    entElecID.delete(0, END)
    entElecDate.delete(0, END)
    entEnergyCon.delete(0, END)
    entCostpk.delete(0, END)
    entTotalBill.delete(0, END)

# Go to Graph Page
def toGraph():
    dataentry_window.destroy()
    import graph

# Go to About Page
def toAbout():
    dataentry_window.destroy()
    import about

# Exit dashboard
def exit():
    exit = messagebox.askyesno("Household Sustainability Dashboard", "Are you sure you want to exit?")
    if exit > 0:
        dataentry_window.destroy()
        import login

# Full screen
def toggle_fullscreen(event):
    dataentry_window.attributes("-fullscreen", not dataentry_window.attributes("-fullscreen"))

# GUI
# Create a window
dataentry_window = Tk()
dataentry_window.title("Data Entry")
dataentry_window.attributes("-fullscreen", True)
dataentry_window.bind("<Escape>", toggle_fullscreen)

# Full screen
screen_width = dataentry_window.winfo_screenwidth()
screen_height = dataentry_window.winfo_screenheight()
dataentry_window.geometry(f"{screen_width}x{screen_height}")

# Variables
ElectricityID = IntVar()
ElectricityDate = StringVar()
EnergyConsumption = DoubleVar()
Costpk = DoubleVar()
TotalBill = DoubleVar()

# Add background image
dataBg = ImageTk.PhotoImage(file="main-bg.jpg")
dataLabel = Label(dataentry_window, image=dataBg)
dataLabel.place(x=0, y=0)

# Title label
lbltitle = Label(dataentry_window, font=("Arial", 22, "bold"), text="ENERGY CONSUMPTION", bg="#B7E0D2")
lbltitle.place(x=screen_width // 3, y=110)

# ENTRY FIELDS
# Create a frame for the entry fields
data_frame = Frame(dataentry_window, bg="#B7E0D2")
data_frame.place(x=220, y=170)

# Electricity ID label and entry
lblElecID = Label(data_frame, font=("Arial", 12, "bold"), text="Electricity ID", bg="#B7E0D2")
lblElecID.grid(row=0, column=0, padx=10, pady=10)
entElecID = Entry(data_frame, font=("Arial", 12, "bold"), width=44, justify="right", textvariable=ElectricityID)
entElecID.grid(row=0, column=1, padx=10, pady=10)

# Electricity Date label and entry
lblElecDate = Label(data_frame, font=("Arial", 12, "bold"), text="Electricity Date", bg="#B7E0D2")
lblElecDate.grid(row=1, column=0, padx=10, pady=10)
entElecDate = Entry(data_frame, font=("Arial", 12, "bold"), width=44, justify="right", textvariable=ElectricityDate)
entElecDate.insert(0, 'Month and Year')
entElecDate.bind('<FocusIn>', user_enter)
entElecDate.grid(row=1, column=1, padx=10, pady=10)

# Energy Consumption label and entry
lblEnergyCon = Label(data_frame, font=("Arial", 12, "bold"), text="Energy Consumption", bg="#B7E0D2")
lblEnergyCon.grid(row=2, column=0, padx=10, pady=10)
entEnergyCon = Entry(data_frame, font=("Arial", 12, "bold"), width=44, justify="right", textvariable=EnergyConsumption)
entEnergyCon.grid(row=2, column=1, padx=10, pady=10)

# Cost label and entry
lblCostpk = Label(data_frame, font=("Arial", 12, "bold"), text="Cost per kWh", bg="#B7E0D2")
lblCostpk.grid(row=3, column=0, padx=10, pady=10)
entCostpk = Entry(data_frame, font=("Arial", 12, "bold"), width=44, justify="right", textvariable=Costpk)
entCostpk.grid(row=3, column=1, padx=10, pady=10)

# Total Bill label and entry
lblTotalBill = Label(data_frame, font=("Arial", 12, "bold"), text="Total Bill", bg="#B7E0D2")
lblTotalBill.grid(row=4, column=0, padx=10, pady=10)
entTotalBill = Entry(data_frame, font=("Arial", 12, "bold"), width=44, justify="right", textvariable=TotalBill, state='readonly')
entTotalBill.grid(row=4, column=1, padx=10, pady=10)
entEnergyCon.bind('<KeyRelease>', lambda event: displayBill())
entCostpk.bind('<KeyRelease>', lambda event: displayBill())
displayBill()

# Table treeview
data_records = ttk.Treeview(data_frame, height=12, columns=("ElecID", "ElecDate", "EnergyCon", "Costpk", "TBill"))
data_records.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Treeview scrollbar
scroll_y = Scrollbar(data_frame, orient=VERTICAL, command=data_records.yview)
scroll_y.grid(row=5, column=2, sticky="ns")
data_records.config(yscrollcommand=scroll_y.set)

# Treeivew headings
data_records.heading("ElecID", text="Electricity ID")
data_records.heading("ElecDate", text="Electricity Date")
data_records.heading("EnergyCon", text="Energy Consumption")
data_records.heading("Costpk", text="Cost per kWh")
data_records.heading("TBill", text="Total Bill")
data_records["show"] = "headings"

# Treeview columns
data_records.column("ElecID", width=100)
data_records.column("ElecDate", width=110)
data_records.column("EnergyCon", width=120)
data_records.column("Costpk", width=100)
data_records.column("TBill", width=100)

# Display data on treeview
data_records.bind("<ButtonRelease-1>", dataInfo)
displayData()

# Expand properly with the window
data_frame.columnconfigure(0, weight=1)
data_frame.rowconfigure(5, weight=1)

# BUTTONS
# Create a frame for the buttons
button_frame = Frame(dataentry_window, bg="#B7E0D2")
button_frame.place(x=880, y=170)

# Add button
btnAddNew = Button(button_frame, font=("Arial", 14, "bold"), text="Add", bd=4, pady=1, padx=24,
                   width=8, height=2, activebackground="#809CCE", command=addData)
btnAddNew.pack(fill='x', padx=10, pady=10)

# Display button
btnUpdate = Button(button_frame, font=("Arial", 14, "bold"), text="Display", bd=4, pady=1, padx=24,
                   width=8, height=2, activebackground="#809CCE", command=displayData)
btnUpdate.pack(fill='x', padx=10, pady=10)

# Update button
btnUpdate = Button(button_frame, font=("Arial", 14, "bold"), text="Update", bd=4, pady=1, padx=24,
                   width=8, height=2, command=updateData)
btnUpdate.pack(fill='x', padx=10, pady=10)

# Delete button
btnDelete = Button(button_frame, font=("Arial", 14, "bold"), text="Delete", bd=4, pady=1, padx=24,
                   width=8, height=2, activebackground="#809CCE", command=deleteData)
btnDelete.pack(fill='x', padx=10, pady=10)

# Search button
btnSearch = Button(button_frame, font=("Arial", 14, "bold"), text="Search", bd=4, pady=1, padx=24,
                   width=8, height=2, activebackground="#809CCE", command=searchData)
btnSearch.pack(fill='x', padx=10, pady=10)

# Reset button
btnReset = Button(button_frame, font=("Arial", 14, "bold"), text="Reset", bd=4, pady=1, padx=24,
                  width=8, height=2, activebackground="#809CCE", command=resetData)
btnReset.pack(fill='x', padx=10, pady=11)

# Create a frame for the logo and system name
top_frame = Frame(dataentry_window, bg="#B7E0D2")
top_frame.pack(side="top", fill="x")

# Add logo and system name
logoImage = ImageTk.PhotoImage(file='logo.jpg')
logo_label = Label(top_frame, image=logoImage, borderwidth=0, highlightthickness=0, highlightbackground="#B7E0D2")
logo_label.pack(side="left")
system_name_label = Label(top_frame, text=" Household Sustainability Dashboard",
                          font=("Poppins Bold", 18, 'bold'), fg="black", bg="#B7E0D2")
system_name_label.pack(side="left")

# Separate heading and menu frames
blank_label = Label(top_frame, text="", bg="#B7E0D2")
blank_label.pack(side="top")
separator_frame = Frame(dataentry_window, height=5, bg="black")
separator_frame.pack(fill="x")

# Create a frame for the navigation menu
nav_frame = Frame(dataentry_window, bg="#B7E0D2", width=200)
nav_frame.pack(side="left", fill="both")

# Create labels for icons
dataentry_icon = ImageTk.PhotoImage(file='data-entry.png')
graph_icon = ImageTk.PhotoImage(file='graph.png')
about_icon = ImageTk.PhotoImage(file='about.png')
exit_icon = ImageTk.PhotoImage(file='exit.png')
cursor_style = "hand2" 

# NAVIGATION ICONS
# Data entry
dataentry_label = Label(nav_frame, image=dataentry_icon, borderwidth=0, cursor=cursor_style, width=60)
dataentry_label.pack(fill="both", expand=True)

# Graph
graph_label = Button(nav_frame, image=graph_icon, borderwidth=0, cursor=cursor_style, command=toGraph)
graph_label.pack(fill="both", expand=True)

# About
about_label = Button(nav_frame, image=about_icon, borderwidth=0, cursor=cursor_style, command=toAbout)
about_label.pack(fill="both", expand=True)

# Exit
exit_label = Button(nav_frame, image=exit_icon, borderwidth=0, cursor=cursor_style, command=exit)
exit_label.pack(fill="both", expand=True)

# Run the GUI main loop
dataentry_window.mainloop()