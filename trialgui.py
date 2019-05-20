from tkinter import *
from PIL import Image,ImageTk
from tkinter import filedialog as fd
import subprocess
from ctypes import *

def start():
	global programFrame
	global pages
	global inputPath
	global solutionWindow
	global playableWindow
	homeFrame.pack_forget()
	programFrame = Canvas(window)
	programFrame.create_image(384,384,image=bgOpa)
	pages = []
	inputPath = ""
	solutionWindow = None

	playableWindow = Playable(programFrame)

	# menu bar
	menubar = Menu(window)
	uploadmenu = Menu(menubar,tearoff=0)
	uploadmenu.add_command(label='Upload File...',command=upload)
	uploadmenu.add_command(label='Solve', command=execute)
	menubar.add_cascade(label='File', menu=uploadmenu)

	window.config(menu=menubar)
	programFrame.pack(fill=BOTH, expand=1)

def exit():
    window.destroy()

def goback(aboutFrame):
	aboutFrame.pack_forget()
	homeFrame.pack()


def about():
    homeFrame.pack_forget()
    f2= Canvas(window)
    lbl = Label(f2,image=abtimg)
    lbl.pack()

    btn1 = Button(f2,width=179,height=69,image=goBackImage,command=lambda:goback(f2))
    btn1.place(x=0, y=0, anchor=NW)
    f2.pack()


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
		solutionWindow.vbar.pack_forget()
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
	solutionWindow = SolutionWindow(window, solutions)


def draw_board(canvas, n, board):  
	# draw checkerboard
	for r in range(n-1, -1, -1):
		for c in range(n):
			if c&1 ^ r&1:
				cellType = yellowCell
				disabledCellType = greyCell
			else:
				cellType = brownCell
				disabledCellType = greyCell
			coords = (c*30+4, r*30+4, c*30+30, r*30+30)
			if board[r][c] == 'C' and c&1 ^ r&1:
				cellType = chancyYellowCell
				disabledCellType = chancyYellowCell
			elif board[r][c] == 'C':
				cellType = chancyBrownCell
				disabledCellType = chancyBrownCell

			canvas.create_image(coords[0], coords[1],image=cellType,disabledimage=disabledCellType, anchor=NW, state='normal', tags='c'+str(r)+str(c))



class Pages:
	currentPage = 0


	def __init__(self, n, numOfSolutions, solutions, solutionWindow):
		self.n = n
		self.numOfSolutions = numOfSolutions
		self.solutions = solutions
		self.solutionWindow = solutionWindow
		self.frames = [None]*numOfSolutions


		currentFrame = Frame(solutionWindow)
		currentFrame.grid(row=1, column=1, sticky='news')
		if solutions[0] == '0':
			Label(currentFrame,text='NO SOLUTION').pack()
			self.frames =  [currentFrame]
		else:
			board = solutions[self.currentPage*n:self.currentPage*n+n]
			Button(currentFrame,image=prevImage, text="Previous Page", command=lambda:self.nextPage(-1)).grid(row=1,column=0,sticky='news')
			# draw board
			canvas = Canvas(currentFrame, width=n*31, height=n*31)
			draw_board(canvas, n, board)
			canvas.grid(row=1,column=1,sticky='news')

			Button(currentFrame, image=nextImage, text="Next Page", command=lambda:self.nextPage(1)).grid(row=1,column=2,sticky='news')
			Label(currentFrame, text="Page {}/{}".format(self.currentPage+1, numOfSolutions)).grid(row=0,column=1,sticky='news')
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
			nextFrame.grid(row=1, column=1, sticky='news')
			board = self.solutions[pageNumber*self.n:pageNumber*self.n+self.n]
			Button(nextFrame,image=prevImage, text="Previous Page", command=lambda:self.nextPage(pageNumber-1)).grid(row=1,column=0,sticky='news')
			# draw board
			canvas = Canvas(nextFrame, width=self.n*31, height=self.n*31)
			draw_board(canvas, self.n, board)
			canvas.grid(row=1,column=1,sticky='news')
			Button(nextFrame,image=nextImage, text="Next Page", command=lambda:self.nextPage(pageNumber+1)).grid(row=1,column=2,sticky='news')
			Label(nextFrame, text="Page {}/{}".format(pageNumber+1, self.numOfSolutions)).grid(row=0,column=1,sticky='news')
			self.frames[pageNumber] = nextFrame

class SolutionWindow:
	currentPage = 0
	rootWindow = None
	solutionPages = []

	def __init__(self, root, solutions):
		n = len(solutions[0][0])
		self.rootWindow = Canvas(root, scrollregion=(0,0,n*31,n*31))
		self.vbar = Scrollbar(root, orient=VERTICAL)
		self.vbar.pack(side=RIGHT, fill=Y)
		self.vbar.config(command=self.rootWindow.yview)
		self.rootWindow.config(yscrollcommand=self.vbar.set)

		self.solutionPages = []
		for solution in solutions:
			n = len(solution[0])
			numOfSolutions = int(solution[-1])
			self.solutionPages.append(Pages(n, numOfSolutions, solution, self.rootWindow))
		
		self.solutionPages[0].frames[0].tkraise()
		
		Button(self.rootWindow,image=bnextImage, text="Next Config", command=self.nextPage).grid(row=1, column=2, sticky='news')
		Button(self.rootWindow,image=bprevImage, text="Prev Config", command=self.prevPage).grid(row=1, column=0, sticky='news')
		self.pageLabel = Label(self.rootWindow, text="Config {}/{}".format(self.currentPage+1, len(self.solutionPages)))
		self.pageLabel.grid(row=0, column=1, sticky='news')
		self.rootWindow.pack(side=TOP, expand=YES)

	def nextPage(self):
		if (self.currentPage + 1 >= len(self.solutionPages)):
			self.currentPage = 0
		else:
			self.currentPage +=1
		self.solutionPages[self.currentPage].frames[0].tkraise()
		self.pageLabel['text'] = "Config {}/{}".format(self.currentPage+1, len(self.solutionPages))

	def prevPage(self):
		if self.currentPage < 0:
			self.currentPage = len(self.solutionPages)-2
		else:
			self.currentPage -=1
		self.solutionPages[self.currentPage].frames[0].tkraise()
		self.pageLabel['text'] = "Config {}/{}".format(self.currentPage+1, len(self.solutionPages))

class Playable:

	def __init__(self, root):
		self.root = root
		Label(root, text='Enter puzzle size:').pack()
		self.textBox = Entry(root)
		self.textBox.pack()
		self.n = 0
		self.board = ['-'*self.n]*self.n
		self.boardCanvas = Canvas(root, width=self.n*31, height=self.n*31)
		self.boardCanvas.pack()
		self.execButton = None
		self.vbar = Scrollbar(self.root,orient=VERTICAL)
		Button(root, text="Custom Input", command=self.renderBoard).pack()

		self.execButton = Button(self.root, text="Execute", command=lambda:createInputFile(self.board))
		self.execButton.pack()

	def renderBoard(self):
		if solutionWindow:
			solutionWindow.rootWindow.grid_forget()
		self.n = int(self.textBox.get())
		self.boardCanvas.pack_forget()
		if self.vbar:
			self.vbar.pack_forget()

		self.boardCanvas = Canvas(self.root, width=self.n*31, height=self.n*31, scrollregion=(0,0,self.n*31,self.n*31))
		self.vbar.pack(side=RIGHT, fill=Y)
		self.vbar.config(command=self.boardCanvas.yview)
		self.boardCanvas.config(yscrollcommand=self.vbar.set)

		self.board = ['-'*self.n]*self.n
		self.draw_board()
		self.boardCanvas.pack(side=TOP, expand=YES)

		

	# https://pyinmyeye.blogspot.com/2012/08/tkinter-knights-tour-demo.html
	def draw_board(self):  
		# draw checkerboard
		for r in range(self.n-1, -1, -1):
			for c in range(self.n):
				if c&1 ^ r&1:
					cellType = yellowCell
					disabledCellType = greyCell
				else:
					cellType = brownCell
					disabledCellType = greyCell
				coords = (c*30+4, r*30+4, c*30+30, r*30+30)
				if self.board[r][c] == 'C' and c&1 ^ r&1:
					cellType = chancyYellowCell
					disabledCellType = chancyYellowCell
				elif self.board[r][c] == 'C':
					cellType = chancyBrownCell
					disabledCellType = chancyBrownCell

				# rec = self.boardCanvas.create_rectangle(coords, fill=fill, disabledfill=dfill, 
					#width=2, state='normal', tags='c'+str(r)+str(c))
				rec = self.boardCanvas.create_image(coords[0], coords[1],image=cellType,disabledimage=disabledCellType, anchor=NW, state='normal', tags='c'+str(r)+'-'+str(c))

				self.boardCanvas.tag_bind(rec,'<ButtonPress-1>', self.onClickBox)

	def onClickBox(self, event):
		if self.boardCanvas.find_withtag(CURRENT):
			if self.boardCanvas.itemcget(CURRENT, 'state')=="normal":
				
				base = self.boardCanvas.find_withtag(CURRENT)[0]
				row = (self.n-1) - ((base-1)//self.n)
				col =  ((base-1)%self.n)
				self.boardCanvas.itemconfig(CURRENT, state='disabled')
				if col&1 ^ row&1:
					self.boardCanvas.itemconfig(CURRENT, disabledimage=chancyYellowCell)
					self.boardCanvas.itemconfig(CURRENT, image=chancyYellowCell)
				else:
					self.boardCanvas.itemconfig(CURRENT, disabledimage=chancyBrownCell)
					self.boardCanvas.itemconfig(CURRENT, image=chancyBrownCell)
				self.board[row] = self.board[row][:(col)] + 'C' + self.board[row][col+1:self.n]
				self.fillTaken(row,col)

	def fillTaken(self, row,col):
		for i in range(0,self.n):
			self.boardCanvas.itemconfig('c'+str(row)+'-'+str(i), state='disabled')
			self.boardCanvas.itemconfig('c'+str(i)+'-'+str(col), state='disabled')

		if(row-1>=0 and col-2>=0):
			self.boardCanvas.itemconfig('c'+str(row-1)+'-'+str(col-2), state='disabled')
		if(row-2>=0 and col-1>=0):
			self.boardCanvas.itemconfig('c'+str(row-2)+'-'+str(col-1), state='disabled')
		if(row+1<self.n and col+2<self.n):
			self.boardCanvas.itemconfig('c'+str(row+1)+'-'+str(col+2), state='disabled')
		if(row+2<self.n and col+1<self.n):
			self.boardCanvas.itemconfig('c'+str(row+2)+'-'+str(col+1), state='disabled')
		if(row-1>=0 and col+2<self.n):
			self.boardCanvas.itemconfig('c'+str(row-1)+'-'+str(col+2), state='disabled')
		if(row-2>=0 and col+1<self.n):
			self.boardCanvas.itemconfig('c'+str(row-2)+'-'+str(col+1), state='disabled')
		if(row+1<self.n and col-2>=0):
			self.boardCanvas.itemconfig('c'+str(row+1)+'-'+str(col-2), state='disabled')
		if(row+2<self.n and col-1>=0):
			self.boardCanvas.itemconfig('c'+str(row+2)+'-'+str(col-1), state='disabled')

subprocess.call(["gcc", "n_chancellor_problem.c"])

window=Tk()
window.geometry('768x768')

# window.resizable(width=False, height=False)
window.title("N-Chancellor Solver")


# BACKGROUND IMAGE
bg = ImageTk.PhotoImage(Image.open("images/home.jpg"))
abtimg = ImageTk.PhotoImage(Image.open("images/aboutpage.jpg"))
exitImage = ImageTk.PhotoImage(Image.open("images/exit_button.jpg"))
goBackImage = ImageTk.PhotoImage(Image.open("images/goback.jpg"))
bgOpa = ImageTk.PhotoImage(Image.open("images/lowopacity.jpg"))
startImage = PhotoImage(file="images/start.png")
aboutImage = PhotoImage(file="images/abtbtn.png")
# images
brownCell = ImageTk.PhotoImage(Image.open("images/brown.jpg").resize((26, 26)))
yellowCell = ImageTk.PhotoImage(Image.open("images/yellow.jpg").resize((26, 26)))
chancyBrownCell = ImageTk.PhotoImage(Image.open("images/chancybrown.jpg").resize((26, 26)))
chancyYellowCell = ImageTk.PhotoImage(Image.open("images/chancyyellow.jpg").resize((26, 26)))
greyCell = ImageTk.PhotoImage(Image.open("images/gray.jpg").resize((26, 26)))
nextImage = ImageTk.PhotoImage(Image.open("images/next.png").resize((50, 50)))
bnextImage = ImageTk.PhotoImage(Image.open("images/bnext.png").resize((50, 50)))
prevImage = ImageTk.PhotoImage(Image.open("images/prev.png").resize((50, 50)))
bprevImage = ImageTk.PhotoImage(Image.open("images/bprev.png").resize((50, 50)))

homeFrame = Frame(window)
homeFrame.pack()
menu = Canvas(homeFrame, width=768,height=768)
menu.pack()
menu.create_image(384,384,image=bg)



startButton = Button(menu,width=180,height=60,image=startImage,text="START", command=start)
aboutButton = Button(homeFrame,width=180,height=60,image=aboutImage,text="ABOUT",command=about)
exitButton = Button(menu,width=180,height=60,image=exitImage,text="EXIT",command=exit)


aboutButton.pack()
exitButton.pack()

start_button_window = menu.create_window(100, 630, anchor='nw', window=startButton)
about_button_window = menu.create_window(300, 630, anchor='nw', window=aboutButton)
quit_button_window = menu.create_window(500, 630, anchor='nw', window=exitButton)



# 

programFrame = None
pages = []
inputPath = ""
solutionWindow = None

playableWindow = None 



window.mainloop()