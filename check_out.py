import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class CheckOut(ctk.CTk):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title("Check-Out | Hotel Management System")
        self.geometry("1000x700")
        self.configure(fg_color="#101820")

        header = ctk.CTkLabel(
            self, text="Guest Check-Out",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#15d3ba"
        )
        header.pack(pady=30)

        # Room entry
        form_frame = ctk.CTkFrame(self, fg_color="#1C1C1C", corner_radius=20)
        form_frame.pack(padx=40, pady=20, fill="x")

        self.room_var = ctk.StringVar()
        ctk.CTkLabel(
            form_frame, text="Enter Room Number:", 
            font=ctk.CTkFont(size=18)
        ).grid(row=0, column=0, padx=20, pady=20, sticky="e")

        ctk.CTkEntry(
            form_frame, textvariable=self.room_var,
            width=200, height=40
        ).grid(row=0, column=1, padx=10, pady=20, sticky="w")

        # Output box
        self.output_box = ctk.CTkTextbox(self, width=800, height=250, corner_radius=12)
        self.output_box.pack(pady=25)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="#101820")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Check Out", width=180, height=45,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#15d3ba", hover_color="#0bbfa5",
            command=self.check_out
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            btn_frame, text="Home", width=180, height=45,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#15d3ba", hover_color="#0bbfa5",
            command=self.go_home
        ).grid(row=0, column=1, padx=20)

    # ------------------------------------------------
    # CHECK-OUT FUNCTION
    # ------------------------------------------------
    def check_out(self):
        room_number = self.room_var.get().strip()

        if not room_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid room number")
            return

        # VALID ROOM LIST
        valid_rooms = [str(i) for i in range(101, 112)]  # 101–111
        if room_number not in valid_rooms:
            messagebox.showerror("Error", "This room number does not exist in hotel")
            return

        conn = sqlite3.connect("hotel.db")
        cursor = conn.cursor()

        # Check guest inside Hotel table
        cursor.execute("SELECT Fullname FROM Hotel WHERE room_number = ?", (room_number,))
        result = cursor.fetchone()

        if result:
            guest_name = result[0]

            # Remove guest from Hotel table
            cursor.execute("DELETE FROM Hotel WHERE room_number = ?", (room_number,))
            
            # Update dataset → mark room Available again
            cursor.execute("UPDATE hotel_data SET status='Available' WHERE room_number=?", (room_number,))

            conn.commit()

            self.output_box.insert(
                "end",
                f"\n{guest_name} has successfully checked out from room {room_number}.\nRoom is now AVAILABLE.\n"
            )

            messagebox.showinfo("Success", f"{guest_name} checked out successfully")

        else:
            self.output_box.insert("end", "\nNo guest found in that room.\n")

        conn.close()

    def go_home(self):
        self.destroy()
        self.parent.show_main()


def check_out_ui(parent):
    CheckOut(parent)
