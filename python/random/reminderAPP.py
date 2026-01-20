import tkinter as tk
from datetime import datetime, timedelta

class ReminderApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.reminders = []
        master.title("Reminder App")

        self.txt = tk.Text(master, height=5, width=30)
        self.txt.pack()

        seconds_frame = tk.Frame(master);   seconds_frame.pack(pady=5, padx=5)
        seconds_label = tk.Label(seconds_frame, text="Seconds:"); seconds_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.seconds_roller = tk.Spinbox(seconds_frame, from_=0, to=59, width=5)
        self.seconds_roller.pack(side=tk.LEFT)

        minutes_frame = tk.Frame(master);   minutes_frame.pack(pady=5, padx=5)
        minutes_label = tk.Label(minutes_frame, text="Minutes:");   minutes_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.minutes_roller = tk.Spinbox(minutes_frame, from_=0, to=59, width=5)
        self.minutes_roller.pack()  

        hours_frame = tk.Frame(master); hours_frame.pack(pady=5, padx=5)
        hours_label = tk.Label(hours_frame, text="Hours:");   hours_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.hours_roller = tk.Spinbox(hours_frame, from_=0, to=23, width=5)
        self.hours_roller.pack()

        self.reminder_button = tk.Button(master, text="Set reminder", command=self.set_reminder)
        self.reminder_button.pack()

        self.check_reminders()  # Check reminders on startup

    def set_reminder(self):
        """Set a reminder with the specified text and time."""
        reminder_text = self.txt.get("1.0", tk.END).strip()
        timestamp = datetime.now() + timedelta(
            hours=int(self.hours_roller.get()),
            minutes=int(self.minutes_roller.get()),
            seconds=int(self.seconds_roller.get())
        )

        if reminder_text:
            self.reminders.append(reminder(reminder_text, timestamp))
            self.txt.delete("1.0", tk.END)

            popup = tk.Toplevel(self.master)
            label = tk.Label(popup, text=f"Reminder set for {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            label.pack(pady=10, padx=10)
        else:
            popup = tk.Toplevel(self.master)
            label = tk.Label(popup, text="Please enter a reminder.")
            label.pack(pady=10, padx=10)
     
    def check_reminders(self):
        """Check if any reminders are due and print them."""
        now = datetime.now()
        for rem in self.reminders:
            if rem.timestamp <= now:
                popup = tk.Toplevel(self.master)
                label = tk.Label(popup, text=f"Reminder: {rem.text} at {rem.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                label.pack(pady=10, padx=10)
                self.reminders.remove(rem)
        self.master.after(1000, self.check_reminders)  # Check every second

class reminder:
    """Class to represent a reminder."""
    def __init__(self, text, timestamp=None):
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return f"Reminder(text={self.text}, timestamp={self.timestamp})"

root = tk.Tk()
root.title("Reminder Application")
root.geometry("500x400")
myApp = ReminderApp(root)
myApp.mainloop()