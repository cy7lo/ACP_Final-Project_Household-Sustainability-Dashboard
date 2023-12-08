# Libraries
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk 
import pymysql

# FUNCTIONS
# Connect to database
def connect_database():
    if usernameEntry.get()=="" or passwordEntry.get()=="" or confirmEntry.get()=="":
        messagebox.showerror("Error", "All fields are required!")
        
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror("Error", "Passwords do not match!")

    else:
        try:
            connect = pymysql.connect(host="localhost", user="root", password="")
            mycursor = connect.cursor()
        except:
            messagebox.showerror("Error", "Database connectivity issue. Please try again.")
            return
        try: 
            query = "CREATE DATABASE UserData_Db"
            mycursor.execute(query)
            query = "USE UserData_Db"
            mycursor.execute(query)
            query = "CREATE TABLE UserData_Tbl (UserID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Username VARCHAR(100), Password VARCHAR(20))"
            mycursor.execute(query)
        except:
            mycursor.execute("USE UserData_Db")

        query = "SELECT * FROM UserData_Tbl WHERE Username=%s"
        mycursor.execute(query, (usernameEntry.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror("Error", "Account already exists!")
        
        else:
            query = "INSERT INTO UserData_Tbl (Username, Password) VALUES (%s, %s)"
            mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
            connect.commit()
            connect.close()
            messagebox.showinfo("Success", "Registration is successful!")
            clear()
            signup_window.destroy()
            import login

# Clear entry fields
def clear():
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)

# Change entry fields color
def username_entry_focus_in(event):
    usernameEntry.config(bg="white")
def username_entry_focus_out(event):
    usernameEntry.config(bg="#809CCE")
def password_entry_focus_in(event):
    passwordEntry.config(bg="white")
def password_entry_focus_out(event):
    passwordEntry.config(bg="#809CCE")
def confirm_entry_focus_in(event):
    confirmEntry.config(bg="white")
def confirm_entry_focus_out(event):
    confirmEntry.config(bg="#809CCE")

# Link to login page
def login_page():
    signup_window.destroy()
    import login

# Full screen
def toggle_fullscreen(event):
    signup_window.attributes("-fullscreen", not signup_window.attributes("-fullscreen"))

# GUI
# Create a window
signup_window = Tk()
signup_window.title("Sign Up")
signup_window.attributes("-fullscreen", True)
signup_window.bind("<Escape>", toggle_fullscreen)

# Full screen
screen_width = signup_window.winfo_screenwidth()
screen_height = signup_window.winfo_screenheight()      
signup_window.geometry(f"{screen_width}x{screen_height}") 

# Add background image
signupBg = ImageTk.PhotoImage(file="signup-bg.jpg")
signupLabel = Label(signup_window, image=signupBg)
signupLabel.grid()

# Add heading
signupHeading = Label(signup_window, text="Create An Account", font=("Poppins", 18, "bold"), fg="#545454", bg="white")
signupHeading.place(x=875, y=190)

# Add username entry field
usernameLabel = Label(signup_window, text="Username", font=("Calibri Light", 16, "bold"), bg="white", fg="#809CCE")
usernameLabel.place(x=810, y=270)
usernameEntry = Entry(signup_window, width=40, font=("Microsoft Yahei UI Light", 12), bd=1, bg = "#809CCE", fg="black")
usernameEntry.place(x=815, y=305)

# Add password entry field
passwordLabel = Label(signup_window, text="Password", font=("Calibri Light", 16, "bold"), bg="white", fg="#809CCE")
passwordLabel.place(x=810, y=340)
passwordEntry = Entry(signup_window, width=40, font=("Microsoft Yahei UI Light", 12), bd=1, bg = "#809CCE", fg="black")
passwordEntry.place(x=815, y=375)

# Add confirm password entry field
confirmLabel = Label(signup_window, text="Confirm Password", font=("Calibri Light", 16, "bold"), bg="white", fg="#809CCE")
confirmLabel.place(x=810, y=410)
confirmEntry = Entry(signup_window, width=40, font=("Microsoft Yahei UI Light", 12), bd=1, bg = "#809CCE", fg="black")
confirmEntry.place(x=815, y=445)

# Add signup button
signupButton = Button(signup_window, text="Sign Up", font=("Arial", 16, "bold"), fg="white", bg="#809CCE",
                      activeforeground="white", activebackground="#D1D8E2", cursor="hand2", bd=0, width=32,
                    command=connect_database)
signupButton.place(x=786, y=558)

# Add login button
loginButton = Button(signup_window, text="Already have an account?", font=("Poppins", 12, "italic underline"),
                        fg="#545454", bg="white", activeforeground="#809CCE",
                        activebackground="white", cursor="hand2", bd=0, command=login_page)
loginButton.place(x=975, y=510)

# Bind focus events to change background color
usernameEntry.bind("<FocusIn>", username_entry_focus_in)
usernameEntry.bind("<FocusOut>", username_entry_focus_out)
passwordEntry.bind("<FocusIn>", password_entry_focus_in)
passwordEntry.bind("<FocusOut>", password_entry_focus_out)
confirmEntry.bind("<FocusIn>", confirm_entry_focus_in)
confirmEntry.bind("<FocusOut>", confirm_entry_focus_out)

# Run the GUI main loop
signup_window.mainloop()