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
        self.orderList = {f'day{i}': [] for i in range(1, 21)}
        self.day_max = []
        for i in range(1, 21):
            self.day_max.append(200)
        self.schedule_frame = ctk.CTkFrame(self)
        self.schedule_frame.pack(expand=True, fill = "both")
        self.day_windows = {}  # Dictionary to store day windows

        ctk.CTkButton(self, text="Add Order", command=self.open_Input).pack(side = "left", pady = 10, expand = True)
        ctk.CTkButton(self, text="Sort by Priority", command=self.sorting_Alg).pack(side = "left", pady = 10, expand = True)
        ctk.CTkButton(self, text="Clear", command=self.clear).pack(side = "left", pady = 10, expand = True)
        ctk.CTkButton(self, text="Save to CSV", command=self.save_to_csv).pack(side = "left", pady = 10, expand = True)

        self.load_initial_state()

    def clear(self):
        self.orderList = {f'day{i}': [] for i in range(1, 21)}
    
    def open_Input(self):
        input = Input(self)
        input.grab_set()
        
    def open_day_Input(self,day):
        day_input = Day_Input(self, day=day)
        day_input.grab_set()

    def update_Schedule(self):
        # Clear existing widgets in the schedule_frame
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        for i in range(4):  # Rows
            for j in range(5):  # Columns
                day_label_text = f"Day {(j+1)+(i*5)}"
                max_label_text = "Max: "
                # Create labels for day and max
                day_label = ctk.CTkLabel(self.schedule_frame, text=day_label_text, cursor="hand2")
                #max_label = ctk.CTkLabel(self.schedule_frame, text=max_label_text)
                # Create entry widget for max
                #max_box = ctk.CTkEntry(self.schedule_frame, placeholder_text="200")
                #max_button = ctk.CTkButton(self.schedule_frame, text="Set", width=1, command=lambda d=(j+1) + (i*5): self.set_day_max(d, max_box))

                # Grid the widgets
                day_label.grid(row=i*2, column=j*3, padx=1, pady=1, sticky="ew", columnspan=3)
                #max_label.grid(row=i*2+1, column=j*3, padx=1, pady=1, sticky="ew")
                #max_box.grid(row=i*2+1, column=j*3+1, padx=1, pady=1, sticky="ew")
                #max_button.grid(row=i*2+1, column=j*3+2, padx=1, pady=1, sticky="ew")

                self.schedule_frame.grid_rowconfigure(i * 2, weight=3, minsize=3)
                self.schedule_frame.grid_rowconfigure(i * 2 + 1, weight=1, minsize=2)
                self.schedule_frame.grid_columnconfigure(j * 3, weight=2)
                self.schedule_frame.grid_columnconfigure(j * 3 + 1, weight=2)
                self.schedule_frame.grid_columnconfigure(j * 3 + 2, weight=1)

                day_label.bind("<Button-1>", lambda event, day=(j+1) + (i*5): self.update_day_schedule(day))

    def set_day_max(self, day, max_box):
        entered_value = max_box.get()
        self.day_max[day-1] = entered_value



    def update_day_schedule(self, day):
        if day in self.day_windows:
            if not self.day_windows[day].winfo_exists():
                # Create a new Toplevel window for the day if it doesn't exist
                self.day_windows[day] = tk.Toplevel(self)
                self.day_windows[day].title(f"Day {day} Schedule")
        else:
            # Create a new Toplevel window for the day
            self.day_windows[day] = tk.Toplevel(self)
            self.day_windows[day].title(f"Day {day} Schedule")

        # Destroy existing widgets in day_frame
        for widget in self.day_windows[day].winfo_children():
            widget.destroy()

        day_frame = ctk.CTkFrame(self.day_windows[day])
        day_frame.pack(expand=True, fill="both")

        # Add up and down arrows for changing order
        for order in self.orderList.get(f'day{day}', []):
            order_frame = ctk.CTkFrame(day_frame)
            order_frame.pack(fill="x")

            order_text = f"\nCustomer Name: {order['Customer Name']}\n" \
                         f"Amount: {order['Amount']}\n" \
                         f"Product: {order['Product']}\n" \
                         f"Priority Level: {order['Priority Level']}\n"

            # Use a lambda function to pass both day and order to the callback
            orderLabel = ctk.CTkLabel(
                order_frame,
                text=order_text,
                cursor="hand2"
            )
            orderLabel.bind("<Button-1>", lambda event, d=day, o=order: self.open_edit_window(d, o))
            orderLabel.pack(side="left", fill="x")

            up_button = ctk.CTkButton(order_frame, text="↑", command=lambda o=order: self.move_order_up(day, o))
            up_button.pack(side="left", padx=5)
            down_button = ctk.CTkButton(order_frame, text="↓", command=lambda o=order: self.move_order_down(day, o))
            down_button.pack(side="left", padx=5)
            

        max_frame = ctk.CTkFrame(day_frame)
        max_frame.pack(side="top", pady=10)
        ctk.CTkLabel(max_frame, text="Max: ").pack(side="left")
        max_box = ctk.CTkEntry(max_frame, placeholder_text="200")
        max_box.pack(side="left")
        ctk.CTkButton(max_frame, text="Set", width=1, command=lambda d=day: self.set_day_max(d, max_box)).pack(side="left")
        ctk.CTkButton(day_frame, text="Add Order", command=lambda d=day: self.open_day_Input(d)).pack(side="left", pady=10, expand=True)
        ctk.CTkButton(day_frame, text="Sort by Priority per Day", command=lambda d=day: self.sorting_Alg_per_day(d)).pack(side="left", pady=10, expand=True)
        ctk.CTkButton(day_frame, text="Clear Day", command=lambda d=day: self.clear_day(d)).pack(side="left", pady=10, expand=True)
    
    def open_edit_window(self, day, order):
        # Create an edit window similar to the Input window
        edit_input = EditInput(self, day, order)
        edit_input.grab_set()
    
    def clear_day(self, day):
        self.orderList[f'day{day}'] = []
        self.update_day_schedule(day)

    def move_order_up(self, day, order):
        order_list = self.orderList.get(f'day{day}', [])
        index = order_list.index(order)
        if index > 0:
            order_list[index], order_list[index - 1] = order_list[index - 1], order_list[index]
            self.update_day_schedule(day)

    def move_order_down(self, day, order):
        order_list = self.orderList.get(f'day{day}', [])
        index = order_list.index(order)
        if index < len(order_list) - 1:
            order_list[index], order_list[index + 1] = order_list[index + 1], order_list[index]
            self.update_day_schedule(day)

    def sorting_Alg(self):
        self.orderList = sorted(self.orderList, key=lambda order: int(order["Priority Level"]))
        self.update_Schedule()
        
    def sorting_Alg_per_day(self, day):
        # Sort orders for the specified day by priority
        self.orderList[f'day{day}'] = sorted(self.orderList[f'day{day}'], key=lambda order: int(order["Priority Level"]))

        # Update the schedule after sorting
        self.update_day_schedule(day)

    def save_to_csv(self):
        filename = "orders.csv"
        try:
            with open(filename, mode='w', newline='') as file:
                fieldnames = ["Day", "Customer Name", "Amount", "Product", "Priority Level"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write header
                writer.writeheader()

                # Write orders for each day
                for day, orders in self.orderList.items():
                    for order in orders:
                        # Add the day information to each order
                        order_with_day = {'Day': day, **order}
                        writer.writerow(order_with_day)
        except Exception as e:
            print(f"Error while saving to CSV: {e}")


    def load_initial_state(self):
        filename = "orders.csv"
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)

                # Clear existing orderList
                self.orderList = {}

                # Populate orderList with orders for each day
                for row in reader:
                    day = row.pop('Day')  # Extract the day from the row
                    self.orderList.setdefault(day, []).append(row)

                # Update the schedule after loading orders
                self.update_Schedule()
        except FileNotFoundError:
            # Create a new CSV file if it doesn't exist
            with open(filename, mode='w', newline='') as file:
                fieldnames = ["Day", "Customer Name", "Amount", "Product", "Priority Level"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            print(f"Created a new CSV file: {filename}")
            # Update the schedule after creating a new CSV file
            self.update_Schedule()


class Input(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Add Order")
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
        self.master.orderList['day1'].append(order)

        # Update the output
        self.master.update_Schedule()

        # Clear Input
        self.name.delete(0, "end")
        self.amount.delete(0, "end")
        self.product.delete(0, "end")
        self.priorityVar.set("1")
        
class Day_Input(ctk.CTkToplevel):
    def __init__(self, parent, day):
        super().__init__(parent)
        self.day =day

        self.title("Add Order")
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
            self, text="Add Order", command=self.get_Info_Day
        )
        self.addOrderButton.grid(
            row=6, column=1, columnspan=2, padx=20, pady=20, sticky="ew"
        )

    def get_Info_Day(self):
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

        # Add to Order List using dynamic day
        day_key = f'day{self.day}'
        self.master.orderList.setdefault(day_key, []).append(order)

        # Refresh the day_window
        self.master.update_day_schedule(self.day)

        # Update the output
        self.master.update_Schedule()

        # Clear Input
        self.name.delete(0, "end")
        self.amount.delete(0, "end")
        self.product.delete(0, "end")
        self.priorityVar.set("1")
        
class EditInput(ctk.CTkToplevel):
    def __init__(self, parent, day, order):
        super().__init__(parent)
        self.day = day
        self.order = order

        self.title(f"Edit Order - Day {day}")
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

        # Add a button to apply changes
        self.applyChangesButton = ctk.CTkButton(
            self, text="Apply Changes", command=self.apply_changes
        )
        self.applyChangesButton.grid(
            row=6, column=1, columnspan=2, padx=20, pady=20, sticky="ew"
        )

    def apply_changes(self):
        # Get updated information from the input fields
        updated_name = self.name.get()
        updated_amount = self.amount.get()
        updated_product = self.product.get()
        updated_priority = self.priorityVar.get()

        # Update the order details
        self.order["Customer Name"] = updated_name
        self.order["Amount"] = updated_amount
        self.order["Product"] = updated_product
        self.order["Priority Level"] = updated_priority

        # Refresh the day_window
        self.master.update_day_schedule(self.day)

        # Update the output
        self.master.update_Schedule()

        # Close the edit window
        self.destroy()

if __name__ == "__main__":
    app = Output()
    app.mainloop()
