import tkinter as tk
import customtkinter as ctk
import csv

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Output(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Schedule")
        self.geometry("1280x720")
        self.orderList = []
        
        self.day1 = []
        self.day1_max = 200
        
        self.day2 = []
        self.day2_max = 200
        
        self.day3 = []
        self.day3_max = 200
        
        self.day4 = []
        self.day4_max = 200
        
        self.day5 = []
        self.day5_max = 200

        self.schedule_frame = ctk.CTkFrame(self)
        self.schedule_frame.pack(expand=True, fill="both")
        
        for i in range(4):
            self.schedule_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.schedule_frame.grid_columnconfigure(j, weight=1)

        #ctk.CTkButton(self, text="Add Order", command=self.open_Input).pack(expand=True)
        ctk.CTkButton(self, text="Sort by Priority", command=self.sorting_Alg).pack(side = "left", pady = 10, expand = True)
        ctk.CTkButton(self, text="Save to CSV", command=self.save_to_csv).pack(side = "left", pady = 10, expand = True)

        self.load_initial_state()

    def open_Input(self):
        input = Input(self)
        input.grab_set()

    def update_Schedule(self):
        # Clear existing widgets in the schedule_frame
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        for i in range(4):  # Rows
            for j in range(5):  # Columns
                label_text = f"Day {(j+1)+(i*5)}"
                label = ctk.CTkLabel(self.schedule_frame, text=label_text, cursor="hand2")
                label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                label.bind("<Button-1>", lambda event, day=(j+1) + (i*5): self.show_day_schedule(day))

        for order in self.orderList:
            orderLabel = ctk.CTkLabel(
                self.schedule_frame,
                text=f"Customer Name: {order['Customer Name']}, Amount: {order['Amount']}, Product: {order['Product']}, Priority Level: {order['Priority Level']}",
            )
            #orderLabel.pack(fill="x")

    def show_day_schedule(self, day):
        day_window = tk.Toplevel(self)
        day_window.title(f"Day {day} Schedule")

        day_frame = ctk.CTkFrame(day_window)
        day_frame.pack(expand=True, fill="both")

    def sorting_Alg(self):
        self.orderList = sorted(self.orderList, key=lambda order: int(order["Priority Level"]))
        self.update_Schedule()

    def save_to_csv(self):
        filename = "orders.csv"
        try:
            with open(filename, mode='w', newline='') as file:
                fieldnames = ["Customer Name", "Amount", "Product", "Priority Level"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(self.orderList)
        except Exception as e:
            print(f"Error while saving to CSV: {e}")

    def load_initial_state(self):
        filename = "orders.csv"
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                self.orderList = [row for row in reader]
            self.update_Schedule()
        except FileNotFoundError:
            pass

class Input(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("National Manhole Covers")
        self.geometry("420x470")

        # Customer Label
        self.customerLabel = ctk.CTkLabel(self, text="Customer Name")
        self.customerLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Customer Textbox
        self.name = ctk.CTkEntry(self, placeholder_text="eg. ithuba ccc")
        self.name.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Amount Label
        self.amountLabel = ctk.CTkLabel(self, text="Amount")
        self.amountLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # Amount Textbox
        self.amount = ctk.CTkEntry(self, placeholder_text="1375")
        self.amount.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Product Label
        self.productLabel = ctk.CTkLabel(self, text="Product")
        self.productLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # Product Textbox
        self.product = ctk.CTkEntry(self, placeholder_text="eg. T8 C MD")
        self.product.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Priority Label
        self.choiceLabel = ctk.CTkLabel(self, text="Priority Level")
        self.choiceLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        # Priority level
        self.priorityVar = tk.StringVar(value="Priority 1")

        self.priority1 = ctk.CTkRadioButton(
            self, text="Priority 1", variable=self.priorityVar, value="1"
        )
        self.priority1.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

        self.priority2 = ctk.CTkRadioButton(
            self, text="Priority 2", variable=self.priorityVar, value="2"
        )
        self.priority2.grid(row=3, column=2, padx=20, pady=20, sticky="ew")

        self.priority3 = ctk.CTkRadioButton(
            self, text="Priority 3", variable=self.priorityVar, value="3"
        )
        self.priority3.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

        self.priority4 = ctk.CTkRadioButton(
            self, text="Priority 4", variable=self.priorityVar, value="4"
        )
        self.priority4.grid(row=4, column=2, padx=20, pady=20, sticky="ew")

        self.priority5 = ctk.CTkRadioButton(
            self, text="Priority 5", variable=self.priorityVar, value="5"
        )
        self.priority5.grid(row=5, column=1, padx=20, pady=20, sticky="ew")

        # Add Order Button
        self.addOrderButton = ctk.CTkButton(
            self, text="Add Order", command=self.get_Info
        )
        self.addOrderButton.grid(
            row=6, column=1, columnspan=2, padx=20, pady=20, sticky="ew"
        )

    def get_Info(self):
        # Get all info from Input function
        name = self.name.get()
        amount = self.amount.get()
        product = self.product.get()
        priority = self.priorityVar.get()

        # Order format
        order = {
            "Customer Name": name,
            "Amount": amount,
            "Product": product,
            "Priority Level": priority,
        }

        # Add to Order List
        self.master.orderList.append(order)

        # Update the output
        self.master.update_Schedule()

        # Clear Input
        self.name.delete(0, "end")
        self.amount.delete(0, "end")
        self.product.delete(0, "end")
        self.priorityVar.set("1")
        

if __name__ == "__main__":
    app = Output()
    app.mainloop()
