import tkinter as tk
import random

green_light_boot = None
green_light_service = None
red_light_boot = None
red_light_service = None

boot_transformer_on = False
service_transformer_on = False
boot_load = 0
service_load = 0
demand = 0

boot_load_label = None
service_load_label = None
demand_label = None

def draw_lines_and_lamps(canvas):
    global green_light_boot, green_light_service, red_light_boot, red_light_service

    canvas.create_line(50, 100, 250, 100, width=2)
    canvas.create_text(150, 85, text="BOOT LINE", font=("Arial", 12))

    canvas.create_line(50, 150, 250, 150, width=2)
    canvas.create_text(150, 135, text="SERVICE LINE", font=("Arial", 12))

    red_light_boot = canvas.create_oval(55, 85, 75, 105, fill="red")
    red_light_service = canvas.create_oval(55, 135, 75, 155, fill="red")

    green_light_boot = canvas.create_oval(30, 85, 50, 105, fill="green")
    green_light_service = canvas.create_oval(30, 135, 50, 155, fill="green")

    canvas.itemconfig(green_light_boot, state="hidden")
    canvas.itemconfig(green_light_service, state="hidden")

def draw_gauges(canvas):
    global boot_load_label, service_load_label, demand_label

    canvas.create_text(75, 30, text="BOOT LOAD", font=("Arial", 12))
    boot_load_label = canvas.create_text(75, 50, text="0 kW", font=("Arial", 12))

    canvas.create_text(200, 30, text="SERVICE LOAD", font=("Arial", 12))
    service_load_label = canvas.create_text(200, 50, text="0 kW", font=("Arial", 12))

    canvas.create_text(150, 180, text="DEMAND", font=("Arial", 12))
    demand_label = canvas.create_text(150, 200, text="0 kW", font=("Arial", 12))

def update_load_labels():
    canvas.itemconfig(boot_load_label, text=f"{boot_load} kW")
    canvas.itemconfig(service_load_label, text=f"{service_load} kW")
    canvas.itemconfig(demand_label, text=f"{demand} kW")

def randomize_demand():
    global demand
    new_demand = random.randint(0, 700)
    demand = new_demand
    update_load_labels()

def boot_transformer():
    global boot_transformer_on, service_transformer_on

    if not boot_transformer_on:
        if service_transformer_on:
            service_transformer_on = False
            canvas.itemconfig(green_light_service, state="hidden")
            canvas.itemconfig(red_light_service, state="normal")
        canvas.itemconfig(green_light_boot, state="normal")
        canvas.itemconfig(red_light_boot, state="hidden")
        boot_transformer_on = True
    else:
        canvas.itemconfig(green_light_boot, state="hidden")
        canvas.itemconfig(red_light_boot, state="normal")
        boot_transformer_on = False

def service_transformer():
    global service_transformer_on, boot_transformer_on

    if not service_transformer_on:
        if boot_transformer_on:
            boot_transformer_on = False
            canvas.itemconfig(green_light_boot, state="hidden")
            canvas.itemconfig(red_light_boot, state="normal")
        canvas.itemconfig(green_light_service, state="normal")
        canvas.itemconfig(red_light_service, state="hidden")
        service_transformer_on = True
    else:
        canvas.itemconfig(green_light_service, state="hidden")
        canvas.itemconfig(red_light_service, state="normal")
        service_transformer_on = False

def isolate():
    global boot_transformer_on, service_transformer_on, boot_load, service_load, demand
    canvas.itemconfig(green_light_boot, state="hidden")
    canvas.itemconfig(red_light_boot, state="normal")
    canvas.itemconfig(green_light_service, state="hidden")
    canvas.itemconfig(red_light_service, state="normal")
    boot_transformer_on = False
    service_transformer_on = False
    boot_load = 0
    service_load = 0
    update_load_labels()

root = tk.Tk()
root.title("Substation Emulator")
main_menu = tk.Menu(root)
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
dev_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Dev", menu=dev_menu)
dev_menu.add_command(label="Randomize Demand", command=randomize_demand)
canvas = tk.Canvas(root, width=300, height=220)
canvas.pack()
draw_lines_and_lamps(canvas)
draw_gauges(canvas)
boot_transformer_button = tk.Button(root, text="BOOT TRANSFORMER", command=boot_transformer, font=("Arial", 16))
boot_transformer_button.pack()
service_transformer_button = tk.Button(root, text="SERVICE TRANSFORMER", command=service_transformer, font=("Arial", 16))
service_transformer_button.pack()
isolate_button = tk.Button(root, text="ISOLATE", command=isolate, font=("Arial", 16))
isolate_button.pack()
root.mainloop()