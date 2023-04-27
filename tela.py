import subprocess
import tkinter as tk
import os

appname='PYeelight'

class YeelightApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title(appname)
        

        self.toggle_button = tk.Button(self.master, text="ON/OFF", command=self.run_toggle_script)
        self.toggle_button.pack()

        self.brightness_scale = tk.Scale(self.master, from_=1, to=100, orient=tk.HORIZONTAL, command=self.run_brightness_script)
        self.brightness_scale.pack()

        self.rgb_frame = tk.Frame(self.master)
        self.rgb_frame.pack()

        self.rgb_label = tk.Label(self.rgb_frame, text="RGB:")
        self.rgb_label.pack(side="left")

        self.icon_label = tk.Label(self.rgb_frame, text="   ", bg="#8a3257")
        self.icon_label.pack(side="left")

        self.color_frame = tk.Frame(self.master)
        self.color_frame.pack()

        self.red_entry = tk.Entry(self.color_frame, width=3)
        self.red_entry.insert(tk.END, "138")
        self.red_entry.bind("<KeyRelease>", self.update_icon)
        self.red_entry.pack(side="left")

        self.green_entry = tk.Entry(self.color_frame, width=3)
        self.green_entry.insert(tk.END, "50")
        self.green_entry.bind("<KeyRelease>", self.update_icon)
        self.green_entry.pack(side="left")

        self.blue_entry = tk.Entry(self.color_frame, width=3)
        self.blue_entry.insert(tk.END, "87")
        self.blue_entry.bind("<KeyRelease>", self.update_icon)
        self.blue_entry.pack(side="left")

        # Cria a label para o título dos cenários
        self.scenes_label = tk.Label(self.master, text="Cenários:", bg="#8a3257")
        self.scenes_label.pack()

        # Cria a lista de opções dos cenários
        self.scenes_options = tk.StringVar(self.master)
        self.scenes_options.set("Selecione um cenário")
        self.scenes_options_menu = tk.OptionMenu(self.master, self.scenes_options, "Sunrise", "Sunset", "Sleep", "Rainbow", "Disco", "Off1Min", "Stop", "Dim", "Warm", command=self.run_scene_script)
        self.scenes_options_menu.pack()

        # Cria a label para o título das temperaturas
        self.temperature_label = tk.Label(self.master, text="Temperatura:", bg="#8a3257")
        self.temperature_label.pack()

        # Cria a lista de opções das temperaturas
        self.temperature_options = tk.StringVar(self.master)
        self.temperature_options.set("Selecione uma temperatura")
        self.temperature_options_menu = tk.OptionMenu(self.master, self.temperature_options, "2700", "4300", "6500", command=self.run_temp_script)
        self.temperature_options_menu.pack()

    def run_temp_script(self, event=None):
        temp = self.temperature_options.get()
        command = f"./yeelight-scene.sh 0 {temp}"
        subprocess.Popen(command.split())


    def run_scene_script(self, event=None):
        scene = self.scenes_options.get()
        command = f"./yeelight-scene.sh 0 {scene}"
        subprocess.Popen(command.split())

    def run_brightness_script(self, value):
        comando = f"./yeelight-brightness.sh 0 {value}"
        print("Executando:", comando)
        os.system(comando)

    def run_toggle_script(self):
        comando = "./yeelight-toggle.sh 0"
        print("Executando:", comando)
        os.system(comando)

    def update_icon(self, event=None):
        r, g, b = self._get_rgb_from_entries()

        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        self.icon_label.configure(bg=hex_color)
        self._run_rgb_script(r, g, b)

    def _get_rgb_from_entries(self):
        r = self.red_entry.get()
        g = self.green_entry.get()
        b = self.blue_entry.get()

        try:
            r = int(r)
            g = int(g)
            b = int(b)
            if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
                raise ValueError("Erro")
        except ValueError:
            r, g, b = 138, 50, 87

        return r, g, b

    def _run_rgb_script(self, r, g, b):
        command = "./yeelight-rgb.sh 0 {},{},{}".format(r, g, b)
        print("Executando:", command)
        os.system(command)


root = tk.Tk()
app = YeelightApp(master=root)
app.mainloop()
