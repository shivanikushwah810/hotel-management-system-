import customtkinter as ctk
import sqlite3
import check_in_ui
import check_out
import get_info
import customer_info

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hotel Management System")
        self.geometry("1200x700")
        self.configure(fg_color="#101820")

        self.build_main_screen()

    # --------------------------------------------------
    # FUNCTION TO GET ROOM DETAILS FROM DATABASE
    # --------------------------------------------------
    def get_room_details(self, room_number):
        conn = sqlite3.connect("Hotel.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_type, price, status FROM hotel_data WHERE room_number=?",
            (room_number,))
        data = cursor.fetchone()
        conn.close()
        return data

    # --------------------------------------------------
    # MAIN SCREEN UI
    # --------------------------------------------------
    def build_main_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        header = ctk.CTkLabel(
            self,
            text="WELCOME TO GRAND HOTEL",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#15d3ba"
        )
        header.pack(pady=40)

        btn_frame = ctk.CTkFrame(self, fg_color="#1C1C1C", corner_radius=20)
        btn_frame.pack(padx=40, pady=20, fill="both", expand=True)

        buttons = [
            (" Check In", lambda: check_in_ui.check_in_ui_fun(self)),
            (" Check Out", lambda: check_out.check_out_ui(self)),
            (" Room Information", lambda: get_info.get_info_ui(self)),
            (" Guest Information", lambda: customer_info.customer_info_ui(self)),
            (" Exit", self.quit)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                font=ctk.CTkFont(size=22, weight="bold"),
                fg_color="#15d3ba",
                hover_color="#0bbfa5",
                height=70,
                width=400,
                corner_radius=12,
                command=command
            )
            btn.pack(pady=18)

        footer = ctk.CTkLabel(
            self,
            text="© 2025 Hotel Management | Designed by Nidhi Arya",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=15)

    # --------------------------------------------------
    # SHOW MAIN SCREEN AFTER CHILD WINDOW CLOSES
    # --------------------------------------------------
    def show_main(self):
        self.deiconify()
        self.build_main_screen()


if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
