from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

# FUNCTIONS
# Full screen
def toggle_fullscreen(event):
    about_window.attributes("-fullscreen", not about_window.attributes("-fullscreen"))

# Go to data entry page
def toDataEntry():
    about_window.destroy()
    import data_entry

# Go to data entry page
def toGraph():
    about_window.destroy()
    import graph

# Exit dashboard
def exit():
    exit = messagebox.askyesno("Household Sustainability Dashboard","Are you sure you want to exit?")
    if exit > 0:
        about_window.destroy()
        import login

# GUI
# Create a window
about_window = Tk()
about_window.title("Graph")
about_window.attributes("-fullscreen", True)
about_window.bind("<Escape>", toggle_fullscreen)

# Full screen
screen_width = about_window.winfo_screenwidth()
screen_height = about_window.winfo_screenheight()
about_window.geometry(f"{screen_width}x{screen_height}")

# Add background image
aboutBg = ImageTk.PhotoImage(file="about-bg.jpg")

# Create a frame for the logo and system name
top_frame = Frame(about_window, bg="#B7E0D2")
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
separator_frame = Frame(about_window, height=5, bg="black")
separator_frame.pack(fill="x")

# Create a frame for the navigation menu
nav_frame = Frame(about_window, bg="#B7E0D2", width=200)
nav_frame.pack(side="left", fill="both")

# Create labels for icons
dataentry_icon = ImageTk.PhotoImage(file='data-entry.png')
graph_icon = ImageTk.PhotoImage(file='graph.png')
about_icon = ImageTk.PhotoImage(file='about.png')
exit_icon = ImageTk.PhotoImage(file='exit.png')
cursor_style = "hand2" 

# NAVIGATION ICONS
# Data entry
dataentry_label = Button(nav_frame, image=dataentry_icon, borderwidth=0, cursor=cursor_style, command=toDataEntry, width=60)
dataentry_label.pack(fill="both", expand=True)

# Graph
graph_label = Button(nav_frame, image=graph_icon, borderwidth=0, cursor=cursor_style, command=toGraph)
graph_label.pack(fill="both", expand=True)

# About
about_label = Button(nav_frame, image=about_icon, borderwidth=0, cursor=cursor_style)
about_label.pack(fill="both", expand=True)

# Exit
exit_label = Button(nav_frame, image=exit_icon, borderwidth=0, cursor=cursor_style, command=exit)
exit_label.pack(fill="both", expand=True)

# Create a canvas
canvas = Canvas(about_window, width=screen_width, height=screen_height)
canvas.pack()

# Add the background image to the canvas
canvas.create_image(0, 0, anchor=NW, image=aboutBg)

# Add a vertical scrollbar
scrollbar = Scrollbar(about_window, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Run the GUI main loop
about_window.mainloop()
