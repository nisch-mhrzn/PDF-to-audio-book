import pyttsx3 #text-to-speech conversion
import pikepdf as Pdf #open , read pdf
import pdfplumber #extract text from the PDF file
import tkinter as tk #used to create the GUI.
from tkinter import filedialog #interact with the file system and allows users to browse and select files from their computer.
from tkinter import messagebox

class PDFReader:
    def __init__(self,master):#which is used to refer to the main window of the GUI.
        self.master= master##master is the parent widget, i.e., the window that contains this label.
        master.title("PDF Reader") #sets the title of the window as "PDF Reader

        self.label = tk.Label(master, text='Select PDF File')#Label widget
        self.label.pack(padx=20,pady=20)#pack() -> add widgets to the master widget

        self.select_button=tk.Button(master, text='Select',command=self.select_file)
        self.select_button.pack(padx=5,pady=5)

        self.read_button = tk.Button(master,text='Read',command=self.read_pdf,state="disabled")
        self.read_button.pack(padx=5,pady=5)

        self.quit_button = tk.Button(master,text='Quit',command=master.quit)
        self.quit_button.pack(padx=10,pady=5)
        
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.mainloop()

    def select_file(self):
        file_path =filedialog.askopenfilename(filetypes=[('PDF files','*pdf')])#file dialog module -> askopenfilename(function)
        if file_path:#if selected
            self.file_path = file_path
            self.read_button.config(state='normal')

    def read_pdf(self):
        pdf_book = open(self.file_path,'rb')#creates a file object
        reading_pdf =Pdf.open(pdf_book)# opens the PDF file and returns a Pdf object
        pages = len(reading_pdf.pages)

        with pdfplumber.open(self.file_path) as pdf:
            for i in range(0,pages):
                page = pdf.pages[i]
                pdf_text = page.extract_text()
                print(pdf_text)

                #gfenerte the audio file
                s = pyttsx3.init()
                s.setProperty('rate',400) #set the speech rate
                s.save_to_file(pdf_text,'audio.mp3')
                s.runAndWait()

                #speak the text
                pdf_speaker = pyttsx3.init()
                pdf_speaker.setProperty('rate',400) #set the speech rate
                pdf_speaker.say(pdf_text)
                pdf_speaker.runAndWait()
                pdf_speaker.stop()

        pdf_book.close()
        
    def on_closing(self):
        if messagebox.askyesno(title='Quit?',message='Do you really want to quit?'):
            self.master.destroy()
root = tk.Tk()#craetes a window 
root.geometry('800x500')
my_pdf_reader = PDFReader(root)#calling class 
root.mainloop()# call constructor 