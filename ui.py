from tkinter import *
from tkinter import filedialog as fd
from ctypes import *
import subprocess

def upload():
	global inputPath
	inputPath = fd.askopenfilename()
	if playableWindow:
		playableWindow.boardCanvas.pack_forget()

def createInputFile(board):
	global inputPath
	file = open('./customconfig.txt', 'w')
	file.write('1\n')
	file.write(str(len(board)))
	file.write('\n')
	for i in range(0,len(board)):
		for j in range(0,len(board)):
			if board[i][j] == 'C':
				file.write('1')
			else:
				file.write('0')
		file.write('\n')

	file.close()
	inputPath = './customconfig.txt'
	execute()

def execute():
	if solutionWindow:
		solutionWindow.rootWindow.pack_forget()
	with open('./output.txt', 'w+') as file:
		subprocess.call(["./a.out", inputPath], stdout=file)
		file.seek(0)
		solutions = file.read().splitlines()
		# split solutions by configs
		next_indices = [i for i, x in enumerate(solutions) if x == "next config"]
		split_solutions = []
		split_solutions.append(solutions[:next_indices[0]])
		for i in range(1, len(next_indices)):
			split_solutions.append(solutions[next_indices[i-1]+1:next_indices[i]])
		
	showSolution(split_solutions)


def showSolution(solutions):
	global solutionWindow
	solutionWindow = SolutionWindow(root, solutions)


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




class Pages:
	currentPage = 0


	def __init__(self, n, numOfSolutions, solutions, solutionWindow):
		self.n = n
		self.numOfSolutions = numOfSolutions
		self.solutions = solutions
		self.solutionWindow = solutionWindow
		self.frames = [None]*numOfSolutions


		currentFrame = Frame(solutionWindow)
		currentFrame.grid(row=0, column=0, sticky='news')
		if self.n == 1:
			Label(currentFrame,text='NO SOLUTION').pack()
			self.frames =  [currentFrame]
		else:
			board = solutions[self.currentPage*n:self.currentPage*n+n]
			# draw board
			canvas = Canvas(currentFrame, width=n*31, height=n*31)
			draw_board(canvas, n, board)
			canvas.pack()

			Label(currentFrame, text="Page {}/{}".format(self.currentPage+1, numOfSolutions)).pack()
			Button(currentFrame, text="Next Page", command=lambda:self.nextPage(1)).pack()
			Button(currentFrame, text="Previous Page", command=lambda:self.nextPage(-1)).pack()
			self.frames[self.currentPage] =  currentFrame

	def nextPage(self, pageNumber):
		if pageNumber >= self.numOfSolutions:
			pageNumber = 0
			self.currentPage = 0
		elif pageNumber < 0:
			pageNumber = self.numOfSolutions - 1
			self.currentPage = self.numOfSolutions - 1 

		if self.frames[pageNumber] != None:
			self.frames[pageNumber].tkraise()
		else:
			nextFrame = Frame(self.solutionWindow)
			nextFrame.grid(row=0, column=0, sticky='news')
			board = self.solutions[pageNumber*self.n:pageNumber*self.n+self.n]
			# draw board
			canvas = Canvas(nextFrame, width=self.n*31, height=self.n*31)
			draw_board(canvas, self.n, board)
			canvas.pack()
			Label(nextFrame, text="Page {}/{}".format(pageNumber+1, self.numOfSolutions)).pack()
			Button(nextFrame, text="Next Page", command=lambda:self.nextPage(pageNumber+1)).pack()
			Button(nextFrame, text="Previous Page", command=lambda:self.nextPage(pageNumber-1)).pack()
			self.frames[pageNumber] = nextFrame

class SolutionWindow:
	currentPage = 0
	rootWindow = None
	solutionPages = []

	def __init__(self, root, solutions):
		self.rootWindow = Frame(root)
		self.solutionPages = []
		for solution in solutions:
			n = len(solution[0])
			numOfSolutions = int(solution[-1])
			self.solutionPages.append(Pages(n, numOfSolutions, solution, self.rootWindow))
		
		self.solutionPages[0].frames[0].tkraise()
		
		Button(self.rootWindow, text="Next Config", command=self.nextPage).grid(row=1, column=0, sticky='news')
		Button(self.rootWindow, text="Prev Config", command=self.prevPage).grid(row=2, column=0, sticky='news')
		self.pageLabel = Label(self.rootWindow, text="Page {}/{}".format(self.currentPage+1, len(self.solutionPages)))
		self.pageLabel.grid(row=3, column=0, sticky='news')
		self.rootWindow.pack()

	def nextPage(self):
		if (self.currentPage + 1 >= len(self.solutionPages)):
			self.currentPage = 0
		else:
			self.currentPage +=1
		self.solutionPages[self.currentPage].frames[0].tkraise()
		self.pageLabel['text'] = "Page {}/{}".format(self.currentPage+1, len(self.solutionPages))

	def prevPage(self):
		if self.currentPage < 0:
			self.currentPage = len(self.solutionPages)-2
		else:
			self.currentPage -=1
		self.solutionPages[self.currentPage].frames[0].tkraise()
		self.pageLabel['text'] = "Page {}/{}".format(self.currentPage+1, len(self.solutionPages))

class Playable:

	def __init__(self, root):
		self.root = root
		self.textBox = Entry(root)
		self.textBox.pack()
		self.n = 0
		self.board = ['-'*self.n]*self.n
		self.boardCanvas = Canvas(root, width=self.n*31, height=self.n*31)
		self.boardCanvas.pack()
		self.execButton = None

		Button(root, text="Custom Input", command=self.renderBoard).pack()

	def renderBoard(self):
		if solutionWindow:
			solutionWindow.rootWindow.pack_forget()
		self.n = int(self.textBox.get())
		self.boardCanvas.pack_forget()
		if self.execButton:
			self.execButton.pack_forget()
		self.boardCanvas = Canvas(self.root, width=self.n*31, height=self.n*31)
		self.board = ['-'*self.n]*self.n
		self.draw_board()
		self.boardCanvas.pack()

		self.execButton = Button(self.root, text="Execute", command=lambda:createInputFile(self.board))
		self.execButton.pack()

	# https://pyinmyeye.blogspot.com/2012/08/tkinter-knights-tour-demo.html
	def draw_board(self):  
		# draw checkerboard
		for r in range(self.n-1, -1, -1):
			for c in range(self.n):
				if c&1 ^ r&1:
					fill = 'tan3'
					dfill = 'tan4'
				else:
					fill = 'bisque'
					dfill= 'bisque4'
				coords = (c*30+4, r*30+4, c*30+30, r*30+30)
				if self.board[r][c] == 'C':
					fill = 'black'
					dfill = 'black'
					# canvas.create_text(((c*30+4)+(c*30+30))/2, ((r*30+4) + (r*30+30))/2, text="C")
				rec = self.boardCanvas.create_rectangle(coords, fill=fill, disabledfill=dfill, 
					width=2, state='normal', tags='c'+str(r)+str(c))

				self.boardCanvas.tag_bind(rec,'<ButtonPress-1>', self.onClickBox)

	def onClickBox(self, event):
		if self.boardCanvas.find_withtag(CURRENT):
			if self.boardCanvas.itemcget(CURRENT, 'state')=="normal":
				self.boardCanvas.itemconfig(CURRENT, state='disabled')
				self.boardCanvas.itemconfig(CURRENT, fill='black')
				base = self.boardCanvas.find_withtag(CURRENT)[0]
				row = (self.n-1) - ((base-1)//self.n)
				col =  ((base-1)%self.n)
				self.board[row] = self.board[row][:(col)] + 'C' + self.board[row][col+1:self.n]
				self.fillTaken(row,col)

	def fillTaken(self, row,col):
		for i in range(0,self.n):
			self.boardCanvas.itemconfig('c'+str(row)+str(i), state='disabled')
			self.boardCanvas.itemconfig('c'+str(i)+str(col), state='disabled')

		if(row-1>=0 and col-2>=0):
			self.boardCanvas.itemconfig('c'+str(row-1)+str(col-2), state='disabled')
		if(row-2>=0 and col-1>=0):
			self.boardCanvas.itemconfig('c'+str(row-2)+str(col-1), state='disabled')
		if(row+1<self.n and col+2<self.n):
			self.boardCanvas.itemconfig('c'+str(row+1)+str(col+2), state='disabled')
		if(row+2<self.n and col+1<self.n):
			self.boardCanvas.itemconfig('c'+str(row+2)+str(col+1), state='disabled')
		if(row-1>=0 and col+2<self.n):
			self.boardCanvas.itemconfig('c'+str(row-1)+str(col+2), state='disabled')
		if(row-2>=0 and col+1<self.n):
			self.boardCanvas.itemconfig('c'+str(row-2)+str(col+1), state='disabled')
		if(row+1<self.n and col-2>=0):
			self.boardCanvas.itemconfig('c'+str(row+1)+str(col-2), state='disabled')
		if(row+2<self.n and col-1>=0):
			self.boardCanvas.itemconfig('c'+str(row+2)+str(col-1), state='disabled')


if __name__ == '__main__':
	subprocess.call(["gcc", "n_chancellor_problem.c"])
	root = Tk()
	pages = []
	inputPath = ""
	solutionWindow = None
	Button(root, text="Open Input File", command=upload).pack()
	Button(root, text="Execute", command=execute).pack()

	playableWindow = Playable(root)



	root.mainloop()
