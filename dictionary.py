import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        toolbar = tk.Frame(bd=30, bg="#0000FF")
        toolbar.pack(fill=tk.X, side=tk.TOP)

        label_word = ttk.Label(toolbar, text='Введите слово:')
        label_word.place(x=-25, y=-25)

        self.write_word = tk.StringVar()

        self.entry_write_word = ttk.Entry(toolbar, textvariable=self.write_word)
        self.entry_write_word.place(x=70, y=-26)

        return_translate = ttk.Label(toolbar, text='Перевод:')
        return_translate.place(x=-10, y=40)

        self.entry_return_translate = ttk.Entry(toolbar)
        self.entry_return_translate.place(x=70, y=40)

        btn_trans = tk.Button(toolbar, text='Перевести', bd=3, bg='lightgreen', command=self.translate_and_check)
        btn_trans.place(x=50, y=5)

        btn_clear = tk.Button(toolbar, text='Очистить', bd=3, bg='yellow', command=self.clear_btn)
        btn_clear.place(x=150, y=5)

        btn_open_window = tk.Button(toolbar, text='Добавить слово', bd=8, bg='#FF0000', compound=tk.LEFT,
                                    command=self.open_window_and_write)
        btn_open_window.pack(side='right')

        self.tree = ttk.Treeview(self, column=('Word', 'Translate'), height=15, show='headings')

        self.tree.column('Word', width=230, anchor=tk.CENTER)
        self.tree.column('Translate', width=230, anchor=tk.CENTER)

        self.tree.heading('Word', text='Слово')
        self.tree.heading('Translate', text='Перевод')
        self.tree.pack()

    # Очистка содержимого в вводе и выводе
    def clear_btn(self):
        self.entry_write_word.delete('0', 'end')
        self.entry_return_translate.delete('0', 'end')

    # Открытие окна и запись в столбцы
    def open_window_and_write(self):
        self.words = Writer().show()
        for k, v in self.words.items():
            self.tree.insert("", 0, values=(k, v))

    # Взятие слов с переводом из csv файла и добавление в tkinter
    def translate_and_check(self):
        get_word = self.write_word.get().lower()
        with open('dict.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            result = {}
            for row in reader:
                word = row['word']
                translate = row['translate']
                result[word] = translate
            if get_word in result:
                self.entry_return_translate.insert(0, result[get_word])
            else:
                messagebox.showerror('Ошибка', 'Введёное слово не на русском языке или отсутствует в словаре')
        csvfile.close()


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

    # Добавление в словарь и закрытие
    def close_and_add(self):
        self.dct[self.word.get()] = self.trans.get()
        self.destroy()


if __name__ == "__main__":
    root = Main(window)
    root.pack()
    window.mainloop()
