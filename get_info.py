import customtkinter as ctk
import sqlite3

class RoomInfo(ctk.CTk):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title("Room Information | Hotel Management System")
        self.geometry("1000x700")
        self.configure(fg_color="#101820")

        ctk.CTkLabel(self, text="Room Information", font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#15d3ba").pack(pady=30)

        self.output_box = ctk.CTkTextbox(self, width=900, height=400, corner_radius=12)
        self.output_box.pack(pady=20)

        btn_frame = ctk.CTkFrame(self, fg_color="#101820")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Show Rooms", width=180, height=45,
                      font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#15d3ba", hover_color="#0bbfa5",
                      command=self.show_rooms).grid(row=0, column=0, padx=20)

        ctk.CTkButton(btn_frame, text="Home", width=180, height=45,
                      font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#15d3ba", hover_color="#0bbfa5",
                      command=self.go_home).grid(row=0, column=1, padx=20)

    def show_rooms(self):
        self.output_box.delete("0.0", "end")

        # List of all rooms 101–111
        all_rooms = list(range(101, 112))

        conn = sqlite3.connect("Hotel.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Fullname, room_number FROM Hotel")
        booked = cursor.fetchall()

        booked_dict = {room: name for name, room in booked}

        for room in all_rooms:
            if room in booked_dict:
                self.output_box.insert("end", f"🔴 Room {room}: Booked by {booked_dict[room]}\n")
            else:
                self.output_box.insert("end", f"🟢 Room {room}: Available\n")

        conn.close()

    def go_home(self):
        self.destroy()
        self.parent.show_main()


def get_info_ui(parent):
    RoomInfo(parent)
