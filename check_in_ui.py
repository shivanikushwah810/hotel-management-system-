import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# ----------------------------
# DATABASE FUNCTIONS
# ----------------------------

def get_room_details(room_number):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT room_type, price, status FROM hotel_data WHERE room_number=?", (room_number,))
    data = cursor.fetchone()

    conn.close()
    return data


def get_available_rooms():
    """Return room numbers where status = Available"""
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT room_number FROM hotel_data WHERE status='Available'")
    rooms = [str(row[0]) for row in cursor.fetchall()]

    conn.close()
    return rooms


# ----------------------------
# CHECK-IN UI CLASS
# ----------------------------
class CheckIn(ctk.CTk):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title("Guest Check-In | Hotel Management System")
        self.geometry("1000x700")
        self.configure(fg_color="#101820")

        # Header
        header = ctk.CTkLabel(
            self,
            text="Guest Check-In",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#15d3ba"
        )
        header.pack(pady=25)

        # Main Frame
        form_frame = ctk.CTkFrame(self, fg_color="#1C1C1C", corner_radius=20)
        form_frame.pack(padx=40, pady=20, fill="x")

        # Variables
        self.name_var = ctk.StringVar(self)
        self.address_var = ctk.StringVar(self)
        self.mobile_var = ctk.StringVar(self)
        self.days_var = ctk.StringVar(self)
        self.room_var = ctk.StringVar(self)

        # ---------------------
        # FORM FIELDS
        # ---------------------
        labels = ["Full Name", "Address", "Mobile Number", "Number of Days"]
        variables = [self.name_var, self.address_var, self.mobile_var, self.days_var]

        for i, (label_text, var) in enumerate(zip(labels, variables)):
            ctk.CTkLabel(form_frame, text=label_text + ":", font=ctk.CTkFont(size=18)).grid(
                row=i, column=0, padx=20, pady=15, sticky="e"
            )
            ctk.CTkEntry(form_frame, textvariable=var, width=250, height=40).grid(
                row=i, column=1, padx=10, pady=15, sticky="w"
            )

        # ----------------------------
        # ROOM SELECTION DROPDOWN
        # ----------------------------
        ctk.CTkLabel(form_frame, text="Room Number:", font=ctk.CTkFont(size=18)).grid(
            row=4, column=0, padx=20, pady=15, sticky="e"
        )

        available_rooms = get_available_rooms()

        self.room_dd = ctk.CTkComboBox(
            form_frame,
            values=available_rooms,
            width=250,
            height=40,
            variable=self.room_var,
            command=self.show_room_info
        )
        self.room_dd.grid(row=4, column=1, padx=10, pady=15, sticky="w")

        # Room Info Label
        self.room_info_label = ctk.CTkLabel(
            form_frame, text="", font=ctk.CTkFont(size=16), text_color="#15d3ba"
        )
        self.room_info_label.grid(row=5, column=0, columnspan=2, pady=10)

        # ----------------------------
        # BUTTONS
        # ----------------------------
        btn_frame = ctk.CTkFrame(self, fg_color="#101820")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Check In", width=180, height=45,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#15d3ba", hover_color="#0bbfa5",
            command=self.check_in
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            btn_frame, text="Home", width=180, height=45,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#15d3ba", hover_color="#0bbfa5",
            command=self.go_home
        ).grid(row=0, column=1, padx=20)

    # -----------------------------------
    # SHOW ROOM PRICE + TYPE AUTOMATICALLY
    # -----------------------------------
    def show_room_info(self, room_number):
        if not room_number:
            self.room_info_label.configure(text="")
            return

        room_details = get_room_details(int(room_number))
        if room_details:
            r_type, price, _ = room_details
            self.room_info_label.configure(
                text=f"Room Type: {r_type}     |     Price: ₹{price}"
            )

    # ----------------------------
    # CHECK-IN FUNCTION
    # ----------------------------
    def check_in(self):
        name = self.name_var.get().strip()
        address = self.address_var.get().strip()
        mobile = self.mobile_var.get().strip()
        days = self.days_var.get().strip()
        room_no = self.room_var.get().strip()

        # Input validation
        if not all([name, address, mobile, days, room_no]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Error", "Enter a valid 10-digit mobile number")
            return

        if not days.isdigit():
            messagebox.showerror("Error", "Days must be a number")
            return

        room_no = int(room_no)
        room_info = get_room_details(room_no)

        if room_info is None:
            messagebox.showerror("Error", "Room not found in database")
            return

        _, _, status = room_info

        if status.lower() == "booked":
            messagebox.showerror("Unavailable", f"Room {room_no} is already Booked.")
            return

        # Insert guest into database
        conn = sqlite3.connect("hotel.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Hotel (
            Fullname TEXT,
            Address TEXT,
            mobile_number TEXT,
            number_days INTEGER,
            room_number INTEGER
        )''')

        cursor.execute(
            "INSERT INTO Hotel (Fullname, Address, mobile_number, number_days, room_number) VALUES (?, ?, ?, ?, ?)",
            (name, address, mobile, days, room_no)
        )

        # Update room status
        cursor.execute("UPDATE hotel_data SET status='Booked' WHERE room_number=?", (room_no,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{name} has successfully checked in!")

        self.clear_fields()
        self.room_dd.configure(values=get_available_rooms())  # Refresh available rooms

    # ----------------------------
    # CLEAR INPUT FIELDS
    # ----------------------------
    def clear_fields(self):
        self.name_var.set("")
        self.address_var.set("")
        self.mobile_var.set("")
        self.days_var.set("")
        self.room_var.set("")
        self.room_info_label.configure(text="")

    # ----------------------------
    # BACK TO HOME
    # ----------------------------
    def go_home(self):
        self.destroy()
        self.parent.show_main()


# ----------------------------
# WINDOW LAUNCH FUNCTION
# ----------------------------
def check_in_ui_fun(parent):
    app = CheckIn(parent)
    app.mainloop()
