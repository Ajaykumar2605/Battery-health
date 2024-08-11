import tkinter as tk
from PIL import Image, ImageTk
import psutil
import threading
import time
import requests
from io import BytesIO

class BatteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battery Health Monitor")
        self.root.geometry("502x483")
        self.root.resizable(False, False)

        # Load and display application logo and system image
        self.load_images()

        # Create a frame for the battery information
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        # Create labels for battery information
        self.capacity_label = tk.Label(self.info_frame, text="Capacity: N/A", font=("Arial", 12))
        self.capacity_label.pack(pady=5)
        self.percentage_label = tk.Label(self.info_frame, text="Percentage: N/A", font=("Arial", 12))
        self.percentage_label.pack(pady=5)
        self.status_label = tk.Label(self.info_frame, text="Status: N/A", font=("Arial", 12))
        self.status_label.pack(pady=5)
        self.time_remaining_label = tk.Label(self.info_frame, text="Time to Full Charge: N/A", font=("Arial", 12))
        self.time_remaining_label.pack(pady=5)

        # Loading animation
        self.loading_text = tk.StringVar()
        self.loading_text.set("Loading...")
        self.loading_label = tk.Label(self.root, textvariable=self.loading_text, font=("Arial bold", 12))

        # Add a copyright label
        self.footer_frame = tk.Frame(self.root, pady=10)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.copyright_label = tk.Label(self.footer_frame, text="© 2024 Ajay Kumar. All rights reserved.", anchor='e', font=("Arial", 10))
        self.copyright_label.pack(side=tk.BOTTOM, padx=10)

        # Pack loading label and logo
        self.app_logo_label.pack(pady=10)
        self.loading_label.pack(pady=10)

        # Start loading animation
        self.loading_animation_thread = threading.Thread(target=self.animate_loading, daemon=True)
        self.loading_animation_thread.start()

        # Initialize with battery information
        self.update_info()

    def load_images(self):
        """ Load and display application logo and system image """
        try:
            app_logo_url = "https://github.com/Ajaykumar2605/Battery-health/blob/main/source%20files/icons/battery.png?raw=true"

            # Download images
            response_logo = requests.get(app_logo_url)
            response_logo.raise_for_status()

            # Load and resize images
            app_logo = Image.open(BytesIO(response_logo.content)).resize((150, 150))

            # Convert image to PhotoImage
            self.app_logo_photo = ImageTk.PhotoImage(app_logo)

            # Create label to display image
            self.app_logo_label = tk.Label(self.root, image=self.app_logo_photo)
            self.app_logo_label.pack(pady=10)

            # Set window icon
            self.root.iconphoto(False, self.app_logo_photo)

        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            # Fallback if image cannot be downloaded
            self.app_logo_label = tk.Label(self.root, text="Logo not found")
            self.app_logo_label.pack(pady=10)

    def animate_loading(self):
        """ Animate the loading text """
        loading_states = ["Loading.", "Loading..", "Loading..."]
        idx = 0
        while True:
            self.loading_text.set(loading_states[idx % len(loading_states)])
            idx += 1
            time.sleep(0.5)

    def update_info(self):
        """ Fetch and update battery information """
        self.loading_label.pack()  # Ensure loading animation is visible
        threading.Thread(target=self.update_info_thread).start()

    def update_info_thread(self):
        """ Thread to fetch and update battery information """
        battery = psutil.sensors_battery()
        time.sleep(2)  # Simulate loading delay

        if battery:
            capacity = battery.percent
            status = "Charging" if battery.power_plugged else "Not Charging"
            if battery.power_plugged and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                time_remaining = f"{battery.secsleft // 60} min {battery.secsleft % 60} sec"
            else:
                time_remaining = "N/A"
            info = f"Capacity: {capacity} mAh\nPercentage: {capacity}%\nStatus: {status}\nTime to Full Charge: {time_remaining}"
        else:
            info = "Battery information not available."

        # Update the UI with battery information
        self.root.after(0, lambda: self.update_labels(info))

    def update_labels(self, info):
        """ Update labels with battery information """
        info_lines = info.split('\n')
        self.capacity_label.config(text=info_lines[0])
        self.percentage_label.config(text=info_lines[1])
        self.status_label.config(text=info_lines[2])
        self.time_remaining_label.config(text=info_lines[3])
        self.loading_label.pack_forget()  # Hide loading animation

if __name__ == "__main__":
    root = tk.Tk()
    app = BatteryApp(root)
    root.mainloop()
