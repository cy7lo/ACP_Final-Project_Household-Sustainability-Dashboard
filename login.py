# Libraries
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

# FUNCTIONS
# User login
def login_user():
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error", "All fields are required!")

    else:
        try:
            connect = pymysql.connect(host="localhost", user="root", password="")
            mycursor = connect.cursor()
        except:
            messagebox.showerror("Error", "Database connectivity issue. Please try again.")
            return
        
        query = "USE UserData_Db"
        mycursor.execute(query)
        query = "SELECT * FROM UserData_Tbl WHERE Username=%s and Password=%s"
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror("Error", "Invalid username or password!")

        else:
            messagebox.showinfo("Welcome", "Login is successful!")
            login_window.destroy()
            import data_entry

# Username
def user_enter(event):
    if usernameEntry.get() == "Username":
        # Clear if cursor clicks
        usernameEntry.delete(0, END)

# Password
def password_enter(event):
    if passwordEntry.get() == "Password":
        # Clear if cursor clicks
        passwordEntry.delete(0, END)

# Encrypt password
def hide():
    passwordEntry.config(show="*")
    eyeButton.config(image=closeeye, command=show)

# Decrypt password
def show():
    passwordEntry.config(show="")
    eyeButton.config(image=openeye, command=hide)

# Link to signup page
def signup_page():
    login_window.destroy()
    import signup

# Full screen
def toggle_fullscreen(event):
    login_window.attributes("-fullscreen", not login_window.attributes("-fullscreen"))

# GUI
# Create a window
login_window = Tk()
login_window.title("Login")
login_window.attributes("-fullscreen", True)
login_window.bind("<Escape>", toggle_fullscreen)

# Full screen
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()      
login_window.geometry(f"{screen_width}x{screen_height}")        

# Add background image
loginBg = ImageTk.PhotoImage(file="login-bg.jpg")
loginLabel = Label(login_window, image=loginBg)
loginLabel.place(x=0, y=0)

# Add heading
loginHeading = Label(login_window, text="User Login", font=("Poppins", 18, "bold"), fg="#545454", bg="white")
loginHeading.place(x=905, y=295)

# Add username entry field
usernameEntry = Entry(login_window, width=33, font=("Microsoft Yahei UI Light", 14), bd=2, fg="#545454")
usernameEntry.place(x=790, y=390)
usernameEntry.insert(0, "Username")
usernameEntry.bind("<FocusIn>", user_enter)

# Add password entry field
passwordEntry = Entry(login_window, width=33, font=("Microsoft Yahei UI Light", 14), bd=2, fg="#545454")
passwordEntry.place(x=790, y=450)
passwordEntry.insert(0, "Password")
passwordEntry.bind('<FocusIn>', password_enter)

# Add password eye icon
openeye = ImageTk.PhotoImage(file="open-eye.jpg")
closeeye = ImageTk.PhotoImage(file="close-eye.jpg")
eyeButton = Button(login_window, image=openeye, bd=0, bg="white", activebackground="white",
                   cursor="hand2", command=hide)
eyeButton.place(x=1130, y=455)

# Add login button
loginButton = Button(login_window, text="Login", font=("Arial", 16, "bold"),
                        fg="white", bg="#809CCE", activeforeground="white", activebackground="#D1D8E2", 
                        cursor="hand2", bd=0, width=32, command=login_user)
loginButton.place(x=762, y=560)

# Add signup button
newaccButton = Button(login_window, text="Don't have an account?", font=("Poppins", 12, "italic underline"),
                        fg="#545454", bg="white", activeforeground="#809CCE", activebackground="white", 
                        cursor="hand2", bd=0, command=signup_page)
newaccButton.place(x=975, y=510)

# Run the GUI main loop
login_window.mainloop()