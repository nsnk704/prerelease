import tkinter

x = ""
tik = tkinter.Tk()
lbl = tkinter.Label(text='Filepath')
txt = tkinter.Entry(width=20)


def main_shaft():
    txt.place(x=90, y=85, width=500)
    lbl.place(x=30, y=85)
    tik.geometry('650x250')
    tik.title('test')
    btn = tkinter.Button(tik, text='処理実行', command=btn_push)
    btn.place(x=290, y=170)
    tik.mainloop()


def btn_push():
    global x
    x = txt.get()
    print(x)
    tik.destroy()


main_shaft()
