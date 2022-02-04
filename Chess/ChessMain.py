"""
This is a driver file. Responsible for handling user inputs and displaying GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 #400px is another good option, larger will reduce image quality
DIMENSION = 8 #Dimension of chess board 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}

'''
Initialize global dictionary of images. Called once and ONCE ONLY in the main.
'''
def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note : we can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () # no square selected initially, keep track last click of user (tuple = row,col)
    playerClicks = [] #keep track of player clicks(two tuples : [(6,4),(4,4)]

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #If user click same square twice, typically undo. we want to unselect
                    sqSelected = () #deselect
                    playerClicks = [] #Clear player clicks, player may perform new click
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #append for both 1st(initial) and 2nd click(final)
                #Now that happened, was that the user's second click?
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #Reset user clicks
                    playerClicks = []
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove(move)
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for displaying graphics within current game state.
'''

def drawGameState(screen,gs):
    drawBoard(screen) #draw square on the board
    #Add in piece highlighting/move suggestion (KIV)
    drawPieces(screen,gs.board) #draw pieces on top of the square

'''
Draw the squares on the board. Top-left square is always light. Black/White perspective doesnt matter
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark gray")] #Light squares remainder 0, Dark squares remainder 1
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw pieces on the board/ on the current GameState.board
Order matters, draw board first then draw pieces. Else, we cant see the pieces.
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()




















