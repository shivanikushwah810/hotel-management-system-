import customtkinter as ctk
import sqlite3

class CustomerInfo(ctk.CTk):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title("Guest Information | Hotel Management System")
        self.geometry("1000x700")
        self.configure(fg_color="#101820")

        # Header
        ctk.CTkLabel(
            self,
            text="Guest Information",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#15d3ba"
        ).pack(pady=30)

        # Output Box
        self.output_box = ctk.CTkTextbox(self, width=900, height=400, corner_radius=12)
        self.output_box.pack(pady=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="#101820")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Show Guests", width=180, height=45,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#15d3ba", hover_color="#0bbfa5",
            command=self.show_guests
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            btn_frame, text="Home", width=180, height=45,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#15d3ba", hover_color="#0bbfa5",
            command=self.go_home
        ).grid(row=0, column=1, padx=20)

    # ------------------------------------------------
    # SHOW ALL GUESTS CURRENTLY CHECKED IN
    # ------------------------------------------------
    def show_guests(self):
        self.output_box.delete("0.0", "end")

        conn = sqlite3.connect("Hotel.db")
        cursor = conn.cursor()

        # Fetch all guests
        cursor.execute("SELECT * FROM Hotel")
        rows = cursor.fetchall()

        if rows:
            for guest in rows:
                name, address, mobile, days, room = guest
                self.output_box.insert(
                    "end",
                    f"Name: {name}\nAddress: {address}\nMobile: {mobile}\n"
                    f"Days: {days}\nRoom Number: {room}\n"
                    f"{'-'*70}\n"
                )
        else:
            self.output_box.insert("end", "No guests currently checked in.\n")

        conn.close()

    def go_home(self):
        self.destroy()
        self.parent.show_main()


def customer_info_ui(parent):
    CustomerInfo(parent)
