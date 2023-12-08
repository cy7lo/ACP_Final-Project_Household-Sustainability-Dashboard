# Libraries
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Connect to database
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="Electricity_Db"
)
mycursor = mydb.cursor()

# Generate graph
def update_plot(fig, ax, start_index, dates, consumption):
    ax.clear()
    ax.plot(dates[start_index:], consumption[start_index:], marker="o", label="Energy Consumption (kWh)", color="black")
    ax.set_facecolor("#B7E0D2")
    ax.set_title("ENERGY CONSUMPTION ANALYTICS\n",  fontdict={"fontsize": 16, "fontweight": "bold", "fontfamily": "Arial"})
    ax.set_xlabel ("Date")
    ax.set_ylabel("kWh")
    ax.legend()
    fig.canvas.draw()

# Graph animation
def animate(start_index=0):
    mycursor.execute("SELECT ElectricityDate, EnergyConsumption FROM electricity_tbl")
    data = mycursor.fetchall()
    dates = [entry[0] for entry in data]
    consumption = [entry[1] for entry in data]
    update_plot(fig, ax, start_index, dates, consumption)
    
    # Increment the index based on the number of data points for smoother animation
    start_index = (start_index + 1) % len(dates)
    
    # Graph Analysis
    # Check if there are exactly 12 data entry
    if len(dates) == 12:
        # Calculate total consumption for 12 months
        total_consumption_specified_months = sum(consumption)
        # Calculate the average household energy consumption per year
        average_annual_consumption = 10244  
        # Update the analysis label
        analysis_text = (
            f"This graph shows your household energy consumption. "
            f"For the past 12 months, your total household energy consumption is {total_consumption_specified_months} kWh which "
            f"{'exceeds' if total_consumption_specified_months > average_annual_consumption else 'is below'} "
            f"the average household energy consumption ({average_annual_consumption} kWh) per year. Source: Shrink That Footprint, 2023"
        )

    else:
        # Above or below 12 months
        total_consumption = sum(consumption)
        analysis_text = (
            f"This graph shows your household energy consumption. "
            f"Based on the specified months,\nyour total household energy consumption is {total_consumption} kWh."
        )

    analysis_label.config(text=analysis_text)
    update_plot(fig, ax, start_index, dates, consumption)
    graph_window.after(1000, animate, start_index) # Update every 3 seconds with shifted data or restart loop

# Go to Data Entry Page
def toDataEntry():
    graph_window.destroy()
    import data_entry

# Go to About Page
def toAbout():
    graph_window.destroy()
    import about

# Exit dashboard
def exit():
    exit = messagebox.askyesno("Household Sustainability Dashboard","Are you sure you want to exit?")
    if exit > 0:
        graph_window.destroy()
        import login

# Full screen
def toggle_fullscreen(event):
    graph_window.attributes("-fullscreen", not graph_window.attributes("-fullscreen"))

# GUI
# Create a window
graph_window = Tk()
graph_window.title("Graph")
graph_window.attributes("-fullscreen", True)
graph_window.bind("<Escape>", toggle_fullscreen)
graph_window.configure(bg="#809CCE") 

# Full screen
screen_width = graph_window.winfo_screenwidth()
screen_height = graph_window.winfo_screenheight()
graph_window.geometry(f"{screen_width}x{screen_height}")

# Create a frame for the logo and system name
top_frame = Frame(graph_window, bg="#B7E0D2")
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
separator_frame = Frame(graph_window, height=5, bg="black")
separator_frame.pack(fill="x")

# Create a frame for the navigation menu
nav_frame = Frame(graph_window, bg="#B7E0D2", width=200)
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
graph_label = Button(nav_frame, image=graph_icon, borderwidth=0, cursor=cursor_style)
graph_label.pack(fill="both", expand=True)

# About
about_label = Button(nav_frame, image=about_icon, borderwidth=0, cursor=cursor_style, command=toAbout)
about_label.pack(fill="both", expand=True)

# Exit
exit_label = Button(nav_frame, image=exit_icon, borderwidth=0, cursor=cursor_style, command=exit)
exit_label.pack(fill="both", expand=True)

# Graph canvas
fig = Figure(figsize=(6, 4), dpi=100, facecolor="#809CCE")
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=graph_window)
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

# Add analysis label
analysis_text = "This graph shows your household energy consumption over the months."
analysis_label = Label(graph_window, text=analysis_text, font=("Arial", 12, "bold italic"), wraplength=1000,
                       justify="center", bg="#809CCE" )
analysis_label.pack(side="top", padx=10, pady=20)

# Display graph
animate()

# Run the GUI main loop
graph_window.mainloop()