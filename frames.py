import requests as req
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from k import *


class ButtonGroup(tb.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=PM, fill=X, pady=PM)

        self.submit_button = tb.Button(self, text="Submit", bootstyle=SUCCESS)
        self.cancel_button = tb.Button(self, text="Cancel", bootstyle=(OUTLINE, SECONDARY))

        self.submit_button.pack(side=RIGHT, padx=(PM, 0))
        self.cancel_button.pack(side=RIGHT)


class SearchBar(tb.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=PL, fill=BOTH, pady=PL, expand=True)

        self.label_text = tb.StringVar(value="Start Searching!")

        self.search_entry = tb.Entry(self)
        self.search_button = tb.Button(self, text="Search", bootstyle=SUCCESS,
                                       command=self.search_for_record)
        self.result_label = tb.Label(self, textvariable=self.label_text, font=LEAD, justify=CENTER)

        self.result_label.pack(side=BOTTOM, expand=True, padx=PL, pady=PM)
        self.search_entry.pack(fill=X, side=LEFT, expan=True)
        self.search_button.pack(side=LEFT, padx=(PXS, 0))

    def search_for_record(self):
        name = self.search_entry.get()
        if len(name) < 1:
            self.label_text.set(value="ERROR\nNo Query Given")
        else:
            url_string = f"http://10.6.21.76:8000/academics/{name}"
            res = req.get(url_string).json()
            print(res)
            if "msg" in res:
                self.label_text.set(value=res["msg"])
            else:
                self.label_text.set(value=f"Name: {res['name']}\nGrade: {res['grade']}\nGPA: {res['gpa']}\nProfile: {res['profile']}")


class AthleticSearchWindow(tb.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.title_label = tb.Label(self, bootstyle=PRIMARY, text="SMIC Athletic Records", font=H1)
        self.subtitle_label = tb.Label(self,text="A great tool for searching athletic records", font=LEAD)

        self.title_label.pack(anchor=W, pady=PM, padx=PL)
        self.subtitle_label.pack(anchor=W, pady=(0,PM), padx=PM)


class AcademicSearchWindow(tb.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.title_label = tb.Label(self, bootstyle=PRIMARY, text="SMIC RECORDS", font=H1)
        self.subtitle_label = tb.Label(self, text="Get academic records of SMIC students", font=LEAD)

        self.title_label.pack(anchor=NW, padx=PL, pady=(15, 0))
        self.subtitle_label.pack(anchor=NW, padx=PL)
        self.search_bar = SearchBar(self)


class App(tb.Window):

    def __init__(self):
        super().__init__(themename="minty")

        self.title("Frames")
        self.geometry("1280x720")

        self.nav_frame = tb.Frame(self, bootstyle=PRIMARY)
        self.nav_frame.pack(fill=X, ipadx=PXS, ipady=PXS)

        self.container = tb.Frame(self)
        self.container.pack(fill=BOTH, expand=True)

        self.academic_button = tb.Button(self.nav_frame, text="Academic Records", bootstyle=SECONDARY, command=lambda: self.change_frame(name="academic"))
        self.athletic_button = tb.Button(self.nav_frame, text="Athletic Records", bootstyle=SECONDARY, command=lambda: self.change_frame(name="athletic"))

        self.academic_button.pack(side=RIGHT, padx=PXS)
        self.athletic_button.pack(side=RIGHT, padx=PXS)

        self.frames = {
            "academic": AcademicSearchWindow(self.container),
            "athletic": AthleticSearchWindow(self.container)
        }

        self.current_frame = "academic"
        self.set_frame()

    def set_frame(self):
        self.frames[self.current_frame].pack(fill=BOTH, expand=True)

    def remove_frame(self):
        self.frames[self.current_frame].pack_forget()

    def change_frame(self, name):
        self.remove_frame()
        self.current_frame = name
        self.set_frame()


if __name__ == '__main__':
    app = App()
    app.place_window_center()
    app.mainloop()
