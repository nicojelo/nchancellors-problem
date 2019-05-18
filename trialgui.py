from tkinter import *
from PIL import Image,ImageTk
window=Tk()
# window.resizable(width=False, height=False)
window.title("N-Chancellor Solver")


# BACKGROUND IMAGE
bg = ImageTk.PhotoImage(Image.open("images/home.jpg"))
menu = Canvas(window, width=768,height=768)
menu.pack()
menu.create_image(384,384,image=bg)


def exit():
    window.destroy()

def about():
    menu.pack_forget()
    f2= Frame(window)
    abtimg = ImageTk.PhotoImage(Image.open("images/aboutpage.jpg"))
    lbl = Label(f2,image=abtimg)
    lbl.pack()

    # btn1 = Button(f2,text="Back To Menu",command=lambda: back(f3))
    # btn1.pack()
    f2.pack()



photo1 = PhotoImage(file="images/start.png")
photo2 = PhotoImage(file="images/abtbtn.png")
photo3 = PhotoImage(file="images/abtbtn.png")

start = Button(menu,width=180,height=60,image=photo1,text="START")
about = Button(menu,width=180,height=60,image=photo2,text="ABOUT",command=about)
exit = Button(menu,width=180,height=60,image=photo3,text="EXIT",command=exit)


# about.pack()
# exit.pack()

start_button_window = menu.create_window(100, 630, anchor='nw', window=start)
about_button_window = menu.create_window(300, 630, anchor='nw', window=about)
quit_button_window = menu.create_window(500, 630, anchor='nw', window=exit)

    



window.mainloop()