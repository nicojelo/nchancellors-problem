from tkinter import *
from tkinter import filedialog as fd
from ctypes import *
import subprocess

def raise_frame(pageNumber):
	pages[pageNumber].frame.tkraise()

def upload():
	global inputPath
	inputPath = fd.askopenfilename()


def execute():
	with open('./output.txt', 'w+') as file:
		subprocess.call(["./a.out", inputPath], stdout=file)
		file.seek(0)
		solutions = file.read().splitlines()
	showSolution(solutions)

def showSolution(solutions):
	global pages
	solutionWindow = Toplevel(root)
	pages = []
	n = len(solutions[0])
	numOfSolutions = int(solutions[-1])
	totalPages = numOfSolutions

	for i in range(totalPages):
		currentPage = Page(i, solutionWindow, totalPages, solutions[i*n:i*n+n], numOfSolutions)
		pages.append(currentPage)
	raise_frame(0)

# https://pyinmyeye.blogspot.com/2012/08/tkinter-knights-tour-demo.html
def draw_board(canvas, n, board):  
	# draw checkerboard
	for r in range(n-1, -1, -1):
		for c in range(n):
			if c&1 ^ r&1:
				fill = 'tan3'
				dfill = 'tan4'
			else:
				fill = 'bisque'
				dfill= 'bisque3'
			coords = (c*30+4, r*30+4, c*30+30, r*30+30)
			if board[r][c] == 'C':
				fill = 'black'
				dfill = 'black'
				# canvas.create_text(((c*30+4)+(c*30+30))/2, ((r*30+4) + (r*30+30))/2, text="C")
			canvas.create_rectangle(coords, fill=fill, disabledfill=dfill, 
				width=2, state='disabled')



class Page:
	nextPage = None
	frame = None

	def __init__(self, pageNumber, window, totalPages, board, numOfSolutions):
		n = len(board[0])
		self.nextPage = 0 if (pageNumber == (totalPages-1)) else (pageNumber+1)
		self.frame = Frame(window)
		self.frame.grid(row=0, column=0, sticky='news')

		# draw board
		canvas = Canvas(self.frame, width=n*31, height=n*31)
		draw_board(canvas, n, board)
		canvas.pack()

		Label(self.frame, text="Page {}/{}".format(pageNumber+1, numOfSolutions)).pack()
		Button(self.frame, text="Next Page", command=lambda:raise_frame(self.nextPage)).pack()



root = Tk()


pages = []
inputPath = ""
Button(root, text="Open Input File", command=upload).pack()
Button(root, text="Execute", command=execute).pack()




root.mainloop()