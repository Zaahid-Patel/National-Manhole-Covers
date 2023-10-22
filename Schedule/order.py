import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Output(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Schedule")
        self.geometry("1280x720")
        self.orderList = []

        self.schedule_frame = ctk.CTkFrame(self)
        self.schedule_frame.pack(expand=True, fill="both")

        ctk.CTkButton(self, text="Add Order", command=self.open_Input).pack(expand=True)
        ctk.CTkButton(self, text="Sort by Priority", command=self.sorting_Alg).pack(expand=True)

    def open_Input(self):
        input = Input(self)
        input.grab_set()

    def update_Schedule(self):
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        for order in self.orderList:
            orderLabel = ctk.CTkLabel(
                self.schedule_frame,
                text=f"Customer Name: {order['Customer Name']}, Amount: {order['Amount']}, Product: {order['Product']}, Priority Level: {order['Priority Level']}",
            )
            orderLabel.pack(fill="x")

    def sorting_Alg(self):
        self.orderList = sorted(self.orderList, key=lambda order: int(order["Priority Level"]))
        self.update_Schedule()

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
