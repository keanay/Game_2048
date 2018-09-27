'''
2048 game, by MrW01f (fb.com/zakaria.moumen0)

Based on the popular game 2048 [2048](https://github.com/gabrielecirulli/2048) by Gabriele Cirulli


'''
import pygame,random
from pygame.locals import *
pygame.init()
CELLSIZE=100
GAP=int(CELLSIZE/10)
EMPTYCELL='<>'
CELLSANDROWSNUM=4
WINGOAL=2048
MAINFONT=pygame.font.Font('freesansbold.ttf',GAP*4)
FPS=30
FPSCLOCK= pygame.time.Clock()
REVERSEDMOVECOUNTING=-1*(CELLSANDROWSNUM-2)
def initial():
	global CELL_COORD,SHOWWIN,matrix
	CELL_COORD=[]
	matrix = [[EMPTYCELL] * CELLSANDROWSNUM for i in range(CELLSANDROWSNUM)]
	matrix[random.randint(0,CELLSANDROWSNUM-1)][random.randint(0,CELLSANDROWSNUM-1)]=2
	matrix[random.randint(0,CELLSANDROWSNUM-1)][random.randint(0,CELLSANDROWSNUM-1)]=2
	for row in range(CELLSANDROWSNUM):
		if row==0:
			CELL_COORD.append(GAP)
		else:
			CELL_COORD.append(row*(CELLSIZE+GAP)+GAP)
	for row in range(CELLSANDROWSNUM):
		if row==0:
			CELL_COORD.append(GAP)
		else:
			CELL_COORD.append(row*(CELLSIZE+GAP)+GAP)
	SHOWWIN=pygame.display.set_mode((CELL_COORD[-1]+CELLSIZE+GAP,CELL_COORD[-1]+GAP+CELLSIZE))
	pygame.display.set_caption("2048 game")
COLORS_DICT={
'WHITE':(255,255,255),
'BG':(84,84,84),
'BLACK':(0,0,0),
2:(238,228,218),
4:(237,224,200),
8:(242,117,121),
16:(245,149,99),
32:(246,124,95),
64:(246,94,59),
128:(237,207,114),
256:(237,204,97),
512:(237,204,97),
1024:(237,200,80),
2048:(55,228,237),
}
def main():
	initial()
	while True:
		SHOWWIN.fill(COLORS_DICT['WHITE'])
		for row in range(CELLSANDROWSNUM):
			for cell in range(CELLSANDROWSNUM):
				if matrix[row][cell]==EMPTYCELL:
					draw_cell(COLORS_DICT['BG'],row,cell)
				else:
					colored=COLORS_DICT[matrix[row][cell]]
					draw_cell(colored,row,cell)
					write_cell(matrix[row][cell],row,cell)	
		gamestat=state(getemptycells(False))
		if gamestat!='keep going':
			if gamestat=='win':
				menu('you won')
			if gamestat=='lose':
				menu('you lose')
		for event in pygame.event.get():
			if event.type==QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				exit()
			elif event.type==KEYUP:
				handlemovement(event.key)
		pygame.display.update()
		FPSCLOCK.tick(FPS)	
def getemptycells(toappend):
	EMPTYCELLS=[]
	for row in range(CELLSANDROWSNUM):
		for cell in range(CELLSANDROWSNUM):
			if matrix[row][cell]==EMPTYCELL:
				EMPTYCELLS.append([row,cell])
	if EMPTYCELLS==[]:
		return True
	elif toappend:
		rancell=random.choice(EMPTYCELLS)
		matrix[rancell[0]][rancell[1]]=2
def state(full):
	for row in range(CELLSANDROWSNUM):
		for cell in range(CELLSANDROWSNUM):
			statcell=matrix[row][cell]
			if statcell==WINGOAL:
				return 'win'
			elif full:
				if cell!=CELLSANDROWSNUM-1 and row!=CELLSANDROWSNUM-1:
					if statcell==matrix[row][cell+1] or statcell==matrix[row+1][cell]:
						return 'keep going'
				elif row==CELLSANDROWSNUM-1 and cell<CELLSANDROWSNUM-1:
					if statcell==matrix[row][cell+1]:
						return 'keep going'
				elif cell==CELLSANDROWSNUM-1 and row<CELLSANDROWSNUM-1:
					if statcell==matrix[row+1][cell]:
						return 'keep going'
	if full:
		return'lose' 
	return 'keep going'
def draw_cell(color,row,cell):
	pygame.draw.rect(SHOWWIN,color,(CELL_COORD[cell],CELL_COORD[row],CELLSIZE,CELLSIZE))
def write_cell(val,row,cell):
	sel_color=COLORS_DICT[val]
	pygame.draw.rect(SHOWWIN,sel_color,(CELL_COORD[cell],CELL_COORD[row],CELLSIZE,CELLSIZE))
	text=MAINFONT.render(str(matrix[row][cell]),True,COLORS_DICT['BLACK'],sel_color)
	text_rect=text.get_rect()
	text_rect.center=(CELL_COORD[cell]+(CELLSIZE/2),CELL_COORD[row]+(CELLSIZE/2))
	SHOWWIN.blit(text,text_rect)
def handlemovement(key):
	addtwo=False
	if key==K_UP:
		vertical(matrix)
		addtwo=up_rearranger(matrix)
	elif key==K_DOWN:
		vertical(matrix)
		addtwo=down_rearranger(matrix)
	elif key==K_RIGHT:
		horizontal(matrix)
		addtwo=right_rearranger(matrix)
	elif key==K_LEFT:
		horizontal(matrix)
		addtwo=left_rearranger(matrix)
	if addtwo==True:
		getemptycells(True)
def menu(message):
	scrninfo=pygame.display.Info()
	message=MAINFONT.render(message,True,COLORS_DICT['BLACK'],COLORS_DICT['WHITE'])
	message_rect=message.get_rect()
	message_rect.center=(scrninfo.current_w/2,scrninfo.current_h/6)
	SHOWWIN.blit(message,message_rect)
	pygame.display.update()
####MOVES LOGIC
def vertical(board):
	lastmove=''
	for row in range(REVERSEDMOVECOUNTING,1):
		row*=-1
		for cell in range(CELLSANDROWSNUM):
			if board[row][cell]!=EMPTYCELL:
				for nxtrow in range(1,(CELLSANDROWSNUM-row)):			
					if board[row+nxtrow][cell]==board[row][cell]:
						if lastmove==[row+1,cell]:
							break
						board[row+nxtrow][cell]+=board[row][cell]
						board[row][cell]=EMPTYCELL
						lastmove=[row,cell]
					if board[row+nxtrow][cell]==EMPTYCELL:
						pass
					else:
						break
def horizontal(board):
	lastmove=''
	addtwo=False
	for cell in range(REVERSEDMOVECOUNTING,1):
		cell*=-1
		for row in range(CELLSANDROWSNUM):
			if board[row][cell]!=EMPTYCELL:
				for nxtcell in range(1,(CELLSANDROWSNUM-cell)):
					if board[row][cell+nxtcell]==board[row][cell]:
						if lastmove==[row,cell+1]:
							break
						board[row][cell+nxtcell]+=board[row][cell]
						board[row][cell]=EMPTYCELL
						lastmove=[row,cell]
					if board[row][cell+nxtcell]==EMPTYCELL:
						pass
					else:
						break
def left_rearranger(board):
	addtwo=False
	for cell in range(CELLSANDROWSNUM):
		for row in range(CELLSANDROWSNUM):
			if board[row][cell]==EMPTYCELL:
				for nxtcell in range(1,(CELLSANDROWSNUM-cell)):
					if board[row][cell+nxtcell]!=EMPTYCELL:
						board[row][cell]=board[row][cell+nxtcell]
						board[row][cell+nxtcell]=EMPTYCELL
						addtwo=True
						break
	return addtwo
def right_rearranger(board):
	addtwo=False
	for cell in range(-1*CELLSANDROWSNUM+1,1):
		cell*=-1
		for row in range(CELLSANDROWSNUM):
			if board[row][cell]==EMPTYCELL:
				for nxtcell in range(1,cell+1):
					if board[row][cell-nxtcell]!=EMPTYCELL:
						board[row][cell]=board[row][cell-nxtcell]
						board[row][cell-nxtcell]=EMPTYCELL
						addtwo=True
						break
	return addtwo
def up_rearranger(board):
	addtwo=False
	for row in range(CELLSANDROWSNUM-1):
		for cell in range(CELLSANDROWSNUM):
			if board[row][cell]==EMPTYCELL:
				for nxtrow in range(1,(CELLSANDROWSNUM-row)):
					if board[row+nxtrow][cell]!=EMPTYCELL:
						board[row][cell]=board[row+nxtrow][cell]
						board[row+nxtrow][cell]=EMPTYCELL
						addtwo=True
						break							
	return addtwo
def down_rearranger(board):
	addtwo=False
	for row in range(-1*CELLSANDROWSNUM+1,1):
		row*=-1
		for cell in range(CELLSANDROWSNUM):
			if board[row][cell]==EMPTYCELL:
				for nxtcell in range(1,row+1):
					if board[row-nxtcell][cell]!=EMPTYCELL:
						board[row][cell]=board[row-nxtcell][cell]
						board[row-nxtcell][cell]=EMPTYCELL
						addtwo=True
						break
	return addtwo	


if __name__=='__main__':
	main()