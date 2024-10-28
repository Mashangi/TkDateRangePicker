from tkinter import ttk
from customtkinter import *
from uiComponents import CenterWindowToDisplay
from tkcalendar import Calendar
from datetime import datetime
from datetime import date, timedelta
import time

class DateRangePicker(CTkToplevel):
    def __init__(self, command, fg_color, bg_color,**kwargs):
        super().__init__(**kwargs)
        self.window = kwargs["master"]
        self.onDate = command
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.geometry(CenterWindowToDisplay(self.window, 700, 500, self.window._get_window_scaling()))
        self.title("Date Range Picker")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        style = ttk.Style(self)
        style.theme_use("default")
        
        self.date_range = CTkLabel(self, text = "Select Date", font = ("arial", 18, "normal"), height= 50)
        self.date_range.pack(side = "top", fill = X, pady =10, padx = 20, expand = False)

        self.cal = Calendar(self, selectmode='day', locale='en_US', disabledforeground='red',
            cursor="hand2",
            selectbackground=self.fg_color,
            background=self.bg_color,
            disabledbackground=self.bg_color, 
            font = "Arial 14 normal",
            weekendbackground = self.lightenColor(self.bg_color,0.01),
            weekendforeground = "white",
            othermonthbackground = self.lightenColor(self.bg_color, -0.1),
            othermonthwebackground = self.lightenColor(self.bg_color, -0.1),
            bordercolor="black", 
            headersbackground=self.bg_color, 
            normalbackground=self.bg_color, 
            foreground="white", 
            normalforeground='white', 
            headersforeground='white'
        )
        self.cal.bind("<<CalendarSelected>>", self.clicked)
        self.cal.pack(fill="both", expand=True, padx=10)

        self.apply_button = CTkButton(self,fg_color = self.fg_color, text = "APPLY",command = self.apply)
        self.apply_button.pack(pady = 20, padx = (20,20),side = "bottom")
        
        self.date1 = self.cal.get_date()
        self.date2 = self.cal.get_date()
        self.highlighted= []

        self.create_highlighter()
        self.update_label()

    def clicked(self,event):
        current_date = self.cal.get_date()
        self.set_date(current_date)

    def has_both(self) -> bool:
        return self.date1 != None and self.date2 != None
    
    def has_none(self) ->bool:
        return self.date1 == None and self.date2 == None

    def is_date_one(self)-> bool:
        return self.has_both() or self.has_none()

    def set_date(self, date):
        if self.is_date_one():
            self.remove_highlighter()
            self.date1 = date
            self.date2 = None
        else: 
            self.date2 = date
            self.create_highlighter()
            self.mark_selection()
        self.update_label()
    
    def update_label(self):
        self.date_range.configure(text = f'{self.date1}\t-to-\t{self.date2}')
    
    def create_highlighter(self):
        self.cal.tag_config("selection", foreground = "white", background = self.lightenColor(self.bg_color,0.2))
    
    def remove_highlighter(self):
        self.cal.tag_delete("selection")
    
    def mark_selection(self):
        dates_between = self.dates_between_generator(self.date1, self.date2)
        for x in range(30):
            try:
                self.highlighted.append(self.cal.calevent_create(next(dates_between), "text", tags=["selection"]))
            except: break
    
    def apply(self):
        self.onDate(self.get_range)
        self.update()
        self.destroy()

    @staticmethod
    def get_range(self,date1, date2):
        return [self.getTimeStamp(date1), self.getTimeStamp(date2)]

    @staticmethod
    def getTimeStamp(s):
        return time.mktime(datetime.strptime(s, "%m/%d/%y").timetuple())
    
    @staticmethod
    def dates_between_generator(date1, date2):
        temp1 = date1.split("/")
        d1 = date(int(f"20{temp1[2]}"), int(temp1[0]), int(temp1[1]))

        temp2 = date2.split("/")
        d2 = date(int(f"20{temp2[2]}"), int(temp2[0]), int(temp2[1]))

        for n in range(int ((d2 - d1).days)):
            yield d1 + timedelta(n)
        
    @staticmethod
    def lightenColor(hex:str,amnt:float):
        hex = hex.removeprefix("#")
        rgb = []

        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        
        rgb= tuple(rgb)
        values =[]
        for x in rgb:
            if amnt <= 0: 
                gap = int(x * (amnt*-1))
                if x -gap > 1:
                    values.append(x-gap)
                else:
                    values.append(1)
            else: 
                gap = int((255 - x) * amnt)
                values.append(x+gap)
        return '#%02x%02x%02x' % tuple(values)

main_window = CTk()
main_window.geometry("1000x600")
calendar = DateRangePicker(master = main_window, fg_color = "#478778",bg_color = "#303030", command = None)

main_window.mainloop()
fg_color = "#478778"