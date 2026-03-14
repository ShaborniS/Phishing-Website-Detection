import tkinter as tk
import math
from detection.detector_services import analyze_url


class RiskMeter(tk.Canvas):

    def __init__(self, parent, width=500, height=300):

        super().__init__(parent, width=width, height=height, bg="#121212", highlightthickness=0)

        self.width = width
        self.height = height

        self.center_x = width/2
        self.center_y = height*0.9
        self.radius = 170

        self.current_angle = 180
        self.target_angle = 180

        self.draw_meter()

    def draw_segment(self, start, extent, color):

        self.create_arc(
            self.center_x-self.radius,
            self.center_y-self.radius,
            self.center_x+self.radius,
            self.center_y+self.radius,
            start=start,
            extent=extent,
            fill=color,
            outline="#121212",
            width=6
        )

    def draw_labels(self):

        labels = [
            ("VERY LOW", 162),
            ("LOW", 126),
            ("MEDIUM", 90),
            ("HIGH", 54),
            ("CRITICAL", 18)
        ]

        for text, angle in labels:

            rad = math.radians(angle)

            x = self.center_x + (self.radius+35) * math.cos(rad)
            y = self.center_y - (self.radius+35) * math.sin(rad)

            self.create_text(
                x,
                y,
                text=text,
                font=("Segoe UI",11,"bold"),
                fill="#e0e0e0"
            )

    def draw_needle(self):

        rad = math.radians(self.current_angle)

        x = self.center_x + (self.radius-35) * math.cos(rad)
        y = self.center_y - (self.radius-35) * math.sin(rad)

        self.create_line(
            self.center_x,
            self.center_y,
            x,
            y,
            width=5,
            fill="#ffffff"
        )

        self.create_oval(
            self.center_x-10,
            self.center_y-10,
            self.center_x+10,
            self.center_y+10,
            fill="#ffffff"
        )

    def draw_meter(self):

        self.delete("all")

        segment = 36

        self.draw_segment(180, segment, "#00e676")
        self.draw_segment(180-segment, segment, "#76ff03")
        self.draw_segment(180-2*segment, segment, "#ffd740")
        self.draw_segment(180-3*segment, segment, "#ff9100")
        self.draw_segment(180-4*segment, segment, "#ff1744")

        self.draw_labels()
        self.draw_needle()

    def animate(self):

        if abs(self.current_angle - self.target_angle) < 1:
            return

        if self.current_angle > self.target_angle:
            self.current_angle -= 1
        else:
            self.current_angle += 1

        self.draw_meter()

        self.after(8, self.animate)

    def update_meter(self, risk_score):

        self.target_angle = 180 - (risk_score * 1.8)

        self.animate()


class PhishingGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Phishing Website Detector")
        self.root.geometry("700x550")
        self.root.configure(bg="#121212")

        title = tk.Label(
            root,
            text="PHISHING WEBSITE DETECTOR",
            font=("Segoe UI",22,"bold"),
            fg="#00e5ff",
            bg="#121212"
        )
        title.pack(pady=20)

        self.url_entry = tk.Entry(
            root,
            width=60,
            font=("Segoe UI",12),
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.url_entry.pack(pady=10, ipady=8)

        scan_btn = tk.Button(
            root,
            text="SCAN URL",
            font=("Segoe UI",12,"bold"),
            bg="#00e5ff",
            fg="black",
            command=self.scan_url
        )
        scan_btn.pack(pady=10)

        self.result_label = tk.Label(
            root,
            text="Enter a URL and scan",
            font=("Segoe UI",13),
            fg="white",
            bg="#121212"
        )
        self.result_label.pack(pady=15)

        self.meter = RiskMeter(root)
        self.meter.pack()

    # ----------------------
    # Animation for LEGIT
    # ----------------------

    def animate_legitimate(self):

        colors = ["#1b5e20","#2e7d32","#388e3c","#43a047","#4caf50","#66bb6a"]

        def step(i=0):
            if i >= len(colors):
                return
            self.result_label.config(fg=colors[i])
            self.root.after(80, step, i+1)

        step()

    # ----------------------
    # Animation for PHISHING
    # ----------------------

    def animate_phishing(self):

        colors = ["#ff0000","#ff5252","#ff0000","#ff5252","#ff0000"]

        def flash(i=0):
            if i >= len(colors):
                return
            self.result_label.config(fg=colors[i])
            self.root.after(120, flash, i+1)

        flash()

        popup = tk.Toplevel(self.root)
        popup.title("⚠ PHISHING ALERT")
        popup.geometry("420x200")
        popup.configure(bg="#1a0000")

        label = tk.Label(
            popup,
            text="⚠ DANGEROUS WEBSITE DETECTED ⚠",
            font=("Segoe UI",16,"bold"),
            fg="red",
            bg="#1a0000"
        )
        label.pack(expand=True)

        popup.after(3500, popup.destroy)

    def scan_url(self):

        url = self.url_entry.get().strip()

        if not url:
            return

        result = analyze_url(url)

        risk = result["risk_score"]
        prediction = result["prediction"]

        text = f"Prediction: {prediction.upper()} | Risk Score: {risk}"

        self.result_label.config(text=text)

        self.meter.update_meter(risk)

        if prediction == "phishing":
            self.animate_phishing()
        else:
            self.animate_legitimate()


if __name__ == "__main__":

    root = tk.Tk()

    app = PhishingGUI(root)

    root.mainloop()