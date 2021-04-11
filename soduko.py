import pygame
import numpy as np

pygame.font.init()


clock = pygame.time.Clock()
clock_time = 30
run = True
update_timer = 0

FONT = pygame.font.SysFont("comicsans", 50)

s = """7 9 0 0 0 0 0 0 3 
4 0 0 0 0 0 0 6 0 
8 0 1 0 0 4 0 0 2 
0 0 5 0 0 0 0 0 0 
3 0 0 1 0 0 0 0 0 
0 4 0 0 0 6 2 0 9 
2 0 0 0 3 0 5 0 6 
0 3 0 6 0 5 4 2 1 
0 0 0 0 0 0 3 0 0"""
s = s.replace(" ","")

board = np.array([["123456789" for x in range(9)] for x in range(9)])
draw_board = [[("",0) for x in range(9)] for x in range(9)]

def drawBoard(board,win, depth):
	win.fill([255, 255, 255])
	#pygame.draw.rect(win,(0,0,0),(20,20,20,20))
	pygame.draw.rect(win,(255,255,255),(20,20,20,20))

	# vertical
	pygame.draw.rect(win,(0,0,0),(0,0,8,506))
	pygame.draw.rect(win,(0,0,0),(166,0,8,506))
	pygame.draw.rect(win,(0,0,0),(332,0,8,506))
	pygame.draw.rect(win,(0,0,0),(498,0,8,506))	

	#horizontal
	pygame.draw.rect(win,(0,0,0),(0,166,506,8))
	pygame.draw.rect(win,(0,0,0),(0,332,506,8))
	pygame.draw.rect(win,(0,0,0),(0,498,506,8))
	pygame.draw.rect(win,(0,0,0),(0,0,506,8))	
	
	for i in range(0,3):
		for j in range(0,3):
			pygame.draw.rect(win,(0,0,0),(8+166*i+54*j,0,4,506))
			pygame.draw.rect(win,(0,0,0),(0,8+166*i+54*j,506,4))
	
	for i, row in enumerate(board):
		for j, num in enumerate(row):
			color = (0,0,0)
			#if original_board[i][j] != board[i][j]:
			#	color = (255,0,0)

			if len(num) == 1:
				text = FONT.render(str(num), 10, color)	
			else:
				text = FONT.render("0", 10, (0,0,0))
			#print(text.get_width())
			#print(int(i/3))
			win.blit(text, (8 + 4*int(j/3) + int(text.get_width()) + j*54,8 + 4*int(i/3) + int(text.get_height())/3 + i*54) ) 

	pygame.display.update()

def removeOthers(b,row,col):

	num = b[row][col]
	board = b.copy()
	count = 0

	if len(num) != 1:
		return board
	#print(board)

	for col_i in range(9):
		if board[row][col_i] == num and (row,col_i) != (row,col):
			return False
		if len(board[row][col_i]) != 1:
			board[row][col_i] = board[row][col_i].replace(num,"")
			if len(board[row][col_i]) == 1:
				board = removeOthers(board.copy(),row,col_i)
				if board == False:
					return False
		if board[row][col_i] == num and (row,col_i) != (row,col):
			return False

	for row_i in range(9):
		if board[row_i][col] == num and (row_i,col) != (row,col):
			return False
		if len(board[row_i][col]) != 1:
			board[row_i][col] = board[row_i][col].replace(num,"")
			if len(board[row_i][col]) == 1:
				board = removeOthers(board.copy(),row_i,col)
				if board == False:
					return False

	for row_i in range(int(row/3)*3,int(row/3)*3+3):
		for col_i in range(int(col/3)*3,int(col/3)*3+3):
			if board[row_i][col_i] == num and (row_i,col_i) != (row,col):
				return False
			if len(board[row_i][col_i]) != 1:
				board[row_i][col_i] = board[row_i][col_i].replace(num,"")
				if len(board[row_i][col_i]) == 1:
					board = removeOthers(board.copy(),row_i,col_i)
					if board == False:
						return False
	return board

def elim(row,col):
	pass

def parseSoduko(board):	
	d = s.split("\n")
	#print(d)
	for i, r in enumerate(d):
		for j, num in enumerate(str(r)):
			if num != "0":
				board[i][j] = str(num) 

original_board = board.copy()
#print([x for x in original_board])

def parseDraw(board, dep):
	for i, row in enumerate(board):
		for j, col in enumerate(row):
			w, dep = draw_board[i][j]
			if len(col) == 1 and len(w) != 1:
				draw_board[i][j] = (col, dep)

parseSoduko(board)	
parseSoduko(original_board)	

boards = []
def solve(board, depth):
	global boards	
	solved = True	


	if board is False:
		return False

	#parseDraw(board,depth)
	#drawBoard(board, win, depth)

	minn = "12345678910"
	loc = (1,1)
	for i in range(9):
		for j in range(9):
			if len(board[i][j]) < len(minn) and len(board[i][j]) > 1:
				minn = board[i][j]
				loc = (i,j)
			if len(board[i][j]) > 1:
				solved = False

	i, j = loc
	if solved:
		return board

	res = False
	for d in minn:
		s = solve(newBoard(board.copy(),i,j,d),depth+1)
		if s != False:
			return s
	return res
	#return some(solve(newBoard(board.copy(),i,j,d),depth+1) for d in minn)

def newBoard(board,i,j,s):
	board[i][j] = s
	board = removeOthers(board,i,j)
	return board

def some(seq):
	for e in seq:
		if e != False: 
			return e
	return False



win = pygame.display.set_mode((506, 506))

board = solve(board,0)
while run:
	dt = clock.tick(clock_time)
	for event in pygame.event.get():			
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()	
			quit()
	update_timer += dt
	drawBoard(board,win,0)	
