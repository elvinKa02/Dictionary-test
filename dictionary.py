import tkinter as tk
from tkinter import ttk
import csv

window = tk.Tk()
window.geometry('460x350')
window.title("RU-EN")
window.resizable(False, False)


class Main(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.words = {}
        self.main_init()

    # Вид главного окна
    def main_init(self):
        toolbar = tk.Frame(bd=20, bg="#0000FF")
        toolbar.pack(fill=tk.X, side=tk.TOP)

        btn_open_window = tk.Button(toolbar, text='Добавить слово', bd=8, bg='#FF0000', compound=tk.TOP,
                                    command=self.open_window_and_write)
        btn_open_window.pack()

        self.tree = ttk.Treeview(self, column=('Word', 'Translate'), height=15, show='headings')

        self.tree.column('Word', width=230, anchor=tk.CENTER, column=0)
        self.tree.column('Translate', width=230, anchor=tk.CENTER, column=1)

        self.tree.heading('Word', text='Слово')
        self.tree.heading('Translate', text='Перевод')
        self.tree.pack()

    # Открытие окна и запись в столбцы
    def open_window_and_write(self):
        self.words = Writer().show()
        for k, v in self.words.items():
            self.tree.insert("", 0, values=(k, v))


class Writer(tk.Toplevel, Main):
    def __init__(self):
        super().__init__(window)
        self.dct = {}
        self.init_writer()

    # Вид открывающегося окна
    def init_writer(self):
        self.title('RU-EN')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = ttk.Label(self, text='Введите слово')
        label_description.place(x=80, y=50)
        label_select = ttk.Label(self, text='Введите перевод')
        label_select.place(x=80, y=110)

        self.word = tk.StringVar()
        self.trans = tk.StringVar()

        self.entry_word = ttk.Entry(self, textvariable=self.word)
        self.entry_word.place(x=200, y=50)

        self.entry_translate = ttk.Entry(self, textvariable=self.trans)
        self.entry_translate.place(x=200, y=110)

        btn_close = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=300, y=170)

        btn_add = ttk.Button(self, text='Добавить', command=self.close_and_add)
        btn_add.place(x=220, y=170)
        btn_add.bind('<Button-1>')

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.dct

    # Добавление в столбцы и csv файл, закрытие
    def close_and_add(self):
        self.dct[self.word.get()] = self.trans.get()
        self.destroy()
        with open('dict.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([self.word.get(), self.trans.get()])
        csvfile.close()


if __name__ == "__main__":
    root = Main(window)
    root.pack()
    window.mainloop()
