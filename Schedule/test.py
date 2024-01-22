import tkinter as tk
from tkcalendar import Calendar
import customtkinter as ctk
import csv
from datetime import datetime, timedelta

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
        self.date_picker_button = ctk.CTkButton(self, text="Select Date", command=self.show_calendar)
        self.date_picker_button.pack(side="left", pady=10, expand=True)

        # Initialize real_day variable to store the selected date
        self.day1 = None
        self.day2 = None
        self.day3 = None
        self.day4 = None
        self.day5 = None
        
        self.day6 = None
        self.day7 = None
        self.day8 = None
        self.day9 = None
        self.day10 = None
        
        self.day11 = None
        self.day12 = None
        self.day13 = None
        self.day14 = None
        self.day15 = None
        
        self.day16 = None
        self.day17 = None
        self.day18 = None
        self.day19 = None
        self.day20 = None

        # Call a function to update the schedule with the real_day
        self.update_Schedule()

        self.load_initial_state()

    def show_calendar(self):
        # Function to display a calendar and get the selected date
        top = tk.Toplevel(self)
        cal = Calendar(top, selectmode="day", year=2024, month=2, day=1)  # Set your desired starting date
        cal.pack(padx=10, pady=10)

        def set_date():
            # Set the real_day and update the schedule when a date is selected
            self.day1 = cal.selection_get()
            self.day2 = self.day1 + timedelta(days=1)
            self.day3 = self.day1 + timedelta(days=2)
            self.day4 = self.day1 + timedelta(days=3)
            self.day5 = self.day1 + timedelta(days=4)
            
            self.day6 = self.day1 + timedelta(days=7)
            self.day7 = self.day1 + timedelta(days=8)
            self.day8 = self.day1 + timedelta(days=9)
            self.day9 = self.day1 + timedelta(days=10)
            self.day10 = self.day1 + timedelta(days=11)
            
            self.day11 = self.day1 + timedelta(days=14)
            self.day12 = self.day1 + timedelta(days=15)
            self.day13 = self.day1 + timedelta(days=16)
            self.day14 = self.day1 + timedelta(days=17)
            self.day15 = self.day1 + timedelta(days=18)
            
            self.day16 = self.day1 + timedelta(days=21)
            self.day17 = self.day1 + timedelta(days=22)
            self.day18 = self.day1 + timedelta(days=23)
            self.day19 = self.day1 + timedelta(days=24)
            self.day20 = self.day1 + timedelta(days=25)
            
            self.update_Schedule()
            top.destroy()

        ctk.CTkButton(top, text="Set Date", command=set_date).pack(pady=10)

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

        if self.day1:
            for i in range(4):  # Rows
                for j in range(5):  # Columns
                    day_label_text = f"Day {(j+1)+(i*5)}"
                    text=f"{getattr(self, f'day{(j+1)+(i*5)}').strftime('%A, %d %B %Y')}"
                    # Create labels for day
                    day_label = ctk.CTkLabel(self.schedule_frame, text=day_label_text+"\n"+text, cursor="hand2")

                    # Grid the widgets
                    day_label.grid(row=i*2, column=j*3, padx=1, pady=1, sticky="ew", columnspan=3)

                    self.schedule_frame.grid_rowconfigure(i * 2, weight=1, minsize=1)
                    self.schedule_frame.grid_columnconfigure(j * 3, weight=2)

                    day_label.bind("<Button-1>", lambda event, day=(j+1) + (i*5): self.update_day_schedule(day))
            
        else:
            for i in range(4):  # Rows
                for j in range(5):  # Columns
                    day_label_text = f"Day {(j+1)+(i*5)}"
                    # Create labels for day
                    day_label = ctk.CTkLabel(self.schedule_frame, text=day_label_text, cursor="hand2")

                    # Grid the widgets
                    day_label.grid(row=i*2, column=j*3, padx=1, pady=1, sticky="ew", columnspan=3)

                    self.schedule_frame.grid_rowconfigure(i * 2, weight=3, minsize=3)
                    self.schedule_frame.grid_rowconfigure(i * 2 + 1, weight=1, minsize=2)
                    self.schedule_frame.grid_columnconfigure(j * 3, weight=2)

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
                self.day_windows[day].geometry("700x720")
        else:
            # Create a new Toplevel window for the day
            self.day_windows[day] = tk.Toplevel(self)
            self.day_windows[day].title(f"Day {day} Schedule")
            self.day_windows[day].geometry("700x720")

        # Destroy existing widgets in day_frame
        for widget in self.day_windows[day].winfo_children():
            widget.destroy()

        day_frame = ctk.CTkScrollableFrame(self.day_windows[day])
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
            up_button.pack(side="right", padx=5)
            down_button = ctk.CTkButton(order_frame, text="↓", command=lambda o=order: self.move_order_down(day, o))
            down_button.pack(side="right", padx=5)
            

        max_frame = ctk.CTkFrame(day_frame)
        max_frame.pack(side="top", pady=10)
        ctk.CTkLabel(max_frame, text="Max: ").pack(side="left")
        max_box = ctk.CTkEntry(max_frame, placeholder_text="200")
        max_box.insert(0, self.day_max[day-1])  # Pre-fill with existing value
        max_box.pack(side="left")
        ctk.CTkButton(max_frame, text="Set", width=1, command=lambda d=day: self.set_day_max(d, max_box)).pack(side="left")
        ctk.CTkButton(day_frame, text="Add Order", command=lambda d=day: self.open_day_Input(d)).pack(side="left", pady=10, expand=True)
        ctk.CTkButton(day_frame, text="Sort by Priority per Day", command=lambda d=day: self.sorting_Alg_per_day(d)).pack(side="left", pady=10, expand=True)
        ctk.CTkButton(day_frame, text="Clear Day", command=lambda d=day: self.clear_day(d)).pack(side="left", pady=10, expand=True)
        
    def calculate_total_amount(self, day):
        # Calculate the total amount of existing orders for the specified day
        total_amount = sum(int(order.get("Amount", 0)) for order in self.orderList.get(f'day{day}', []))
        
        # Get the current day max capacity
        current_capacity = self.day_max[day-1]

        # Update the remaining capacity
        remaining_capacity = current_capacity - total_amount

        # Return the remaining capacity if needed
        return remaining_capacity
    
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
        for day in range(1, 21):
            # Check if the day exists in self.orderList
            if f'day{day}' in self.orderList and len(self.orderList[f'day{day}']) > 0:
                self.orderList[f'day{day}'] = sorted(self.orderList[f'day{day}'], key=lambda order: int(order["Priority Level"]))
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
                writer = csv.DictWriter(file, fieldnames=fieldnames + ["Values"])
    
                # Write header
                writer.writeheader()
    
                # Write day_max
                writer.writerow({"Values": ",".join(map(str, self.day_max))})
    
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
    
                # Clear existing orderList and day_max
                self.orderList = {}
                self.day_max = []
    
                # Read day_max from the first row
                first_row = next(reader)
                values_str = first_row.get("Values", "")
                self.day_max = list(map(int, values_str.split(",")))
    
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
                writer = csv.DictWriter(file, fieldnames=fieldnames + ["Values"])
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
        # Get order details from the input fields
        name = self.name.get()
        amount = int(self.amount.get())  # Ensure amount is an integer
        product = self.product.get()
        priority = self.priorityVar.get()

        # Find the next available day with remaining amount
        next_available_day = self.find_next_available_day()

        # If there's a day available
        if next_available_day is not None:
            # Calculate the amount to be added on the next available day
            amount_on_next_day = min(amount, self.master.calculate_total_amount(next_available_day))
            remaining_amount = amount - amount_on_next_day

            # Add order to the next available day
            day_key = f'day{next_available_day}'
            order = {
                "Customer Name": name,
                "Amount": amount_on_next_day,
                "Product": product,
                "Priority Level": priority,
            }
            self.master.orderList.setdefault(day_key, []).append(order)

            # Distribute remaining amount across subsequent days
            current_day = next_available_day + 1
            while remaining_amount > 0 and current_day <= len(self.master.day_max):
                max_amount = self.master.day_max[current_day - 1]
                amount_on_current_day = min(remaining_amount, max_amount)

                day_key = f'day{current_day}'
                order = {
                    "Customer Name": name,
                    "Amount": amount_on_current_day,
                    "Product": product,
                    "Priority Level": priority,
                }
                self.master.orderList.setdefault(day_key, []).append(order)

                remaining_amount -= amount_on_current_day
                current_day += 1

            # Update the output
            self.master.update_Schedule()


            # Clear Input
            self.name.delete(0, "end")
            self.amount.delete(0, "end")
            self.product.delete(0, "end")
            self.priorityVar.set("1")
            
    def find_next_available_day(self):
        for day in range(1, 21):
            remaining_capacity = self.master.calculate_total_amount(day)
            if remaining_capacity > 0:
                return day
        return None

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
        self.amount.insert(0, self.master.calculate_total_amount(self.day))  # Pre-fill with existing value

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

        # Destroy the current window
        self.destroy()

        # Create a new instance of the Day_Input window for the same day
        self.master.open_day_Input(self.day)
        
class EditInput(ctk.CTkToplevel):
    def __init__(self, parent, day, order):
        super().__init__(parent)
        self.day = day
        self.order = order

        self.title(f"Edit Order - Day {day}")
        self.geometry("510x530")

        # Customer Label
        self.customerLabel = ctk.CTkLabel(self, text="Customer Name")
        self.customerLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Customer Textbox
        self.name = ctk.CTkEntry(self, placeholder_text="eg. ithuba ccc")
        self.name.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        self.name.insert(0, order.get("Customer Name", ""))  # Pre-fill with existing value

        # Amount Label
        self.amountLabel = ctk.CTkLabel(self, text="Amount")
        self.amountLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # Amount Textbox
        self.amount = ctk.CTkEntry(self, placeholder_text="1375")
        self.amount.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        self.amount.insert(0, order.get("Amount", ""))  # Pre-fill with existing value

        # Product Label
        self.productLabel = ctk.CTkLabel(self, text="Product")
        self.productLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # Product Textbox
        self.product = ctk.CTkEntry(self, placeholder_text="eg. T8 C MD")
        self.product.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        self.product.insert(0, order.get("Product", ""))  # Pre-fill with existing value

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

        # Pre-select the existing priority value
        self.priorityVar.set(str(order.get("Priority Level", "1")))
        
        # Day Picker Label
        self.moveDayLabel = ctk.CTkLabel(self, text="Move to Day")
        self.moveDayLabel.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        # Day Picker Dropdown
        self.moveDayVar = tk.StringVar()
        self.moveDayVar.set(str(day))
        self.moveDayPicker = ctk.CTkComboBox(
            self,
            values=[str(i) for i in range(1, 21)]
        )
        self.moveDayPicker.set(str(day))  # Set the initial value
        self.moveDayPicker.grid(row=6, column=1, padx=20, pady=20, sticky="ew")

        # Add a button to apply changes
        self.applyChangesButton = ctk.CTkButton(
            self, text="Apply Changes", command=self.apply_changes
        )
        self.applyChangesButton.grid(
            row=7, column=1, columnspan=1, padx=20, pady=20, sticky="ew"
        )
        
        # Add a button to delete the order
        self.deleteOrderButton = ctk.CTkButton(
            self, text="Delete Order", command=self.delete_order
        )
        self.deleteOrderButton.grid(
            row=7, column=0, columnspan=1, padx=20, pady=20, sticky="ew"
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

        # Get the selected day from the dropdown
        target_day = int(self.moveDayPicker.get())

        # Move the order to the selected day
        self.move_order_to_day(target_day)

        # Refresh the day_window
        self.master.update_day_schedule(self.day)

        # Update the output
        self.master.update_Schedule()

        # Close the edit window
        self.destroy()
        
    def move_order_to_day(self, target_day):
        # Remove the order from the current day
        self.master.orderList[f'day{self.day}'].remove(self.order)

        # Add the order to the selected day
        day_key = f'day{target_day}'
        self.master.orderList.setdefault(day_key, []).append(self.order)
        
        # Set the selected value in the combobox
        self.moveDayPicker.set(str(target_day))
        
    def delete_order(self):
        # Remove the order from the order list
        self.master.orderList[f'day{self.day}'].remove(self.order)

        # Refresh the day_window
        self.master.update_day_schedule(self.day)

        # Update the output
        self.master.update_Schedule()

        # Close the edit window
        self.destroy()

if __name__ == "__main__":
    app = Output()
    app.mainloop()
