from tkinter import *
from PIL import Image,ImageTk
window=Tk()
# window.resizable(width=False, height=False)
window.title("N-Chancellor Solver")


# BACKGROUND IMAGE
bg = ImageTk.PhotoImage(Image.open("images/home.jpg"))
abtimg = ImageTk.PhotoImage(Image.open("images/aboutpage.jpg"))
startImage = PhotoImage(file="images/start.png")
aboutImage = PhotoImage(file="images/abtbtn.png")
exitImage = PhotoImage(file="images/abtbtn.png")
goBackImage = PhotoImage(file="images/goback.png")

homeFrame = Frame(window)
homeFrame.grid(row=0, column=0, sticky='news')
menu = Canvas(homeFrame, width=768,height=768)
menu.pack()
menu.create_image(384,384,image=bg)


def exit():
    window.destroy()

def about():
    f2= Frame(window)
    lbl = Label(f2,image=abtimg)
    lbl.pack()

    btn1 = Label(f2,width=266,height=92,image=goBackImage)
    btn1.place(relx=1, x=-2, y=2, anchor=NE)
    f2.grid(row=0, column=0, sticky='news')





startButton = Button(menu,width=180,height=60,image=startImage,text="START")
aboutButton = Button(homeFrame,width=180,height=60,image=aboutImage,text="ABOUT",command=about)
exitButton = Button(menu,width=180,height=60,image=exitImage,text="EXIT",command=exit)


aboutButton.pack()
exitButton.pack()

start_button_window = menu.create_window(100, 630, anchor='nw', window=startButton)
about_button_window = menu.create_window(300, 630, anchor='nw', window=aboutButton)
quit_button_window = menu.create_window(500, 630, anchor='nw', window=exitButton)

    



window.mainloop()