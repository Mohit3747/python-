import tkinter as tk
from tkinter import ttk, messagebox

# Movies and showtimes
movies = {
    "Avengers: Endgame": ["10:00 AM", "2:00 PM", "6:00 PM", "9:00 PM"],
    "Inception": ["11:00 AM", "3:00 PM", "7:00 PM"],
    "Interstellar": ["9:30 AM", "1:30 PM", "5:30 PM", "8:30 PM"],
    "RRR": ["10:15 AM", "2:15 PM", "6:15 PM", "9:45 PM"]
}

ticket_price = 150  # per ticket

# Booking function
def book_ticket():
    name = entry_name.get()
    movie = combo_movie.get()
    time = combo_time.get()
    seats = entry_seats.get()

    if not (name and movie and time and seats):
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    try:
        seats = int(seats)
        if seats <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid", "Please enter a valid number of seats")
        return

    total = seats * ticket_price
    receipt = f"""
    🎟️ Ticket Booking Successful 🎟️

    Name: {name}
    Movie: {movie}
    Time: {time}
    Seats: {seats}
    Price per Ticket: ₹{ticket_price}
    ------------------------------
    Total: ₹{total}
    """
    messagebox.showinfo("Booking Receipt", receipt)

# Update showtimes when movie changes
def update_showtimes(event):
    selected_movie = combo_movie.get()
    combo_time["values"] = movies[selected_movie]
    combo_time.current(0)

# Tkinter UI setup
root = tk.Tk()
root.title("Movie Ticket Booking System")
root.geometry("500x400")
root.config(bg="#222")

title = tk.Label(root, text="🎬 Movie Ticket Booking 🎬", font=("Arial", 16, "bold"), bg="#222", fg="white")
title.pack(pady=10)

frame = tk.Frame(root, bg="#333", padx=20, pady=20)
frame.pack(pady=20)

# Name
tk.Label(frame, text="Your Name:", bg="#333", fg="white").grid(row=0, column=0, pady=5, sticky="w")
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, pady=5)

# Movie
tk.Label(frame, text="Select Movie:", bg="#333", fg="white").grid(row=1, column=0, pady=5, sticky="w")
combo_movie = ttk.Combobox(frame, values=list(movies.keys()), state="readonly", width=28)
combo_movie.grid(row=1, column=1, pady=5)
combo_movie.current(0)
combo_movie.bind("<<ComboboxSelected>>", update_showtimes)

# Show time
tk.Label(frame, text="Show Time:", bg="#333", fg="white").grid(row=2, column=0, pady=5, sticky="w")
combo_time = ttk.Combobox(frame, values=movies[combo_movie.get()], state="readonly", width=28)
combo_time.grid(row=2, column=1, pady=5)
combo_time.current(0)

# Seats
tk.Label(frame, text="Number of Seats:", bg="#333", fg="white").grid(row=3, column=0, pady=5, sticky="w")
entry_seats = tk.Entry(frame, width=30)
entry_seats.grid(row=3, column=1, pady=5)

# Book button
btn_book = tk.Button(root, text="Book Ticket", font=("Arial", 12, "bold"), bg="green", fg="white", command=book_ticket)
btn_book.pack(pady=20)

root.mainloop()