import pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("BattleShip")
myfont = pygame.font.SysFont("fresansttf",100)
font_start = pygame.font.SysFont("fresansttf",70)
font_game = pygame.font.SysFont("fresansttf",50)

from engine import Game

#global variables
SQ_SIZE = 35
H_MARGIN = SQ_SIZE*4
V_MARGIN = SQ_SIZE
WIDTH = SQ_SIZE*10*2+H_MARGIN
HEIGHT = SQ_SIZE*10*2+V_MARGIN
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
INDENT = 10
HUMAN1 = False
HUMAN2 = False

#colors
GREY = (40,50,60)
WHITE = (255,250,250)
GREEN = (50,200,150)
RED = (250,50,100)
ORANGE = (250,140,20)
BLUE = (50,150,200)
COLORS = {"U":GREY,"M":BLUE,"H":ORANGE,"S":RED}

#load img
# background_image = pygame.image.load("img/Carrier.jpg")
# background_screen = pygame.image.load("img/gamebg.png")

#button
pvp_button = pygame.Rect(100,600,140,70)
pve_button = pygame.Rect(600,600,140,70)
quit_button = pygame.Rect(600,600,180,70)
pause_button = pygame.Rect(100,600,180,70)
restart_button = pygame.Rect(350,600,180,70)

#function to draw
def draw_grid(player,left=0,top=0,search = False):
    for  i in range(100):
        x= left+i%10*SQ_SIZE
        y= top+i//10*SQ_SIZE
        square = pygame.Rect(x,y,SQ_SIZE,SQ_SIZE)
        pygame.draw.rect(SCREEN,WHITE,square,width=3)
        if search:
            x+=SQ_SIZE//2
            y+=SQ_SIZE//2
            pygame.draw.circle(SCREEN,COLORS[player.search[i]],(x,y),radius=SQ_SIZE//4)

#function to draw ships 
def draw_ships(player,left = 0, top =0):
    for ship in player.ships:
        x = left + ship.col*SQ_SIZE + INDENT
        y = top + ship.row*SQ_SIZE + INDENT
        if ship.orientation == "h":
            width = ship.size*SQ_SIZE - 2*INDENT
            height = SQ_SIZE - 2*INDENT
        else:
            width = SQ_SIZE - 2*INDENT
            height = ship.size*SQ_SIZE - 2*INDENT
        #rectangle = pygame.Rect(x,y,width,height)
        #pygame.draw.rect(SCREEN, GREEN ,rectangle,border_radius=15)


#game = Game(HUMAN1,HUMAN2)

#draw screen
game = None
def draw_start_screen():
    SCREEN.fill(GREY)
    #SCREEN.blit(background_screen,(0,0))
    pygame.draw.rect(SCREEN,GREEN,pvp_button)
    pygame.draw.rect(SCREEN,RED,pve_button)
    pvp_text = myfont.render("PVP" , True, WHITE)
    pve_text = myfont.render("PVE" , True, WHITE)
    title_text = font_start.render("BATTLE SHIP",True,WHITE)
    SCREEN.blit(title_text,(280,200))
    SCREEN.blit(pvp_text,(100,600))
    SCREEN.blit(pve_text,(600,600))
    
#Loop Scr Start
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if pvp_button.collidepoint(x, y):  # Nút PVP được nhấp
                HUMAN1 = True
                HUMAN2 = True
                game = Game(HUMAN1, HUMAN2)
                running = False
            elif pve_button.collidepoint(x,y): # Nút PVE được nhấp
                HUMAN1 = True
                HUMAN2 = False
                game = Game(HUMAN1, HUMAN2)
                running = False

    if game is None: 
        draw_start_screen()
    pygame.display.flip()
    
#loop
animating = True
pausing=False
click_pause = False

while animating:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
             x,y = pygame.mouse.get_pos()
             if game.player1_turn and x< SQ_SIZE*10 and y < SQ_SIZE*10:
                 row = y//SQ_SIZE
                 col = x//SQ_SIZE
                 index = row*10+col
                 game.make_move(index)
             elif not game.player1_turn and x > WIDTH // 2 and y < HEIGHT // 2:
                 row = y//SQ_SIZE
                 col = (x - SQ_SIZE*10 - H_MARGIN ) // SQ_SIZE
                 index = row * 10 + col
                 game.make_move(index)
             elif restart_button.collidepoint(x, y):
                 game = Game(HUMAN1,HUMAN2)
             elif quit_button.collidepoint(x,y):
                 game = None
             elif pause_button.collidepoint(x,y):
                 pausing = not pausing
                 click_pause = True
                

        
        #user press key  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                animating=False
              
            # if event.key == pygame.K_SPACE:
            #     pausing= not pausing
                
            if event.key  == pygame.K_RETURN:
                    game = Game(HUMAN1,HUMAN2)
    if not pausing:
            #draw background
            SCREEN.fill(GREY)
            #SCREEN.blit(background_screen,(0,0))
            
            #draw grids
            draw_grid(game.player1,search=True)
            #draw_grid(game.player2,left=(WIDTH-H_MARGIN)//2+H_MARGIN,top=(HEIGHT-V_MARGIN)//2+V_MARGIN)
            
            #draw_grid(game.player1,top=(HEIGHT-V_MARGIN)//2+V_MARGIN)
            draw_grid(game.player2,search=True,left=(WIDTH-H_MARGIN)//2+H_MARGIN)
            
            #draw ship
            draw_ships(game.player1,top=(HEIGHT-V_MARGIN)//2+V_MARGIN)
            #draw_ships(game.player2,left=(WIDTH-H_MARGIN)//2+H_MARGIN)
            draw_ships(game.player2,left=(WIDTH-H_MARGIN)//2+H_MARGIN,top=(HEIGHT-V_MARGIN)//2+V_MARGIN)
            
            #button 
            pygame.draw.rect(SCREEN,GREEN,pause_button)
            pygame.draw.rect(SCREEN,GREEN,restart_button)
            pygame.draw.rect(SCREEN,GREEN,quit_button)
            
            pause_text = font_game.render("Pause" , True, WHITE)
            quit_text = font_game.render("Quit" , True, WHITE)
            restart_text = font_game.render("Restart",True,WHITE)
            
            pause_text_rect = pause_text.get_rect(center=pause_button.center)
            quit_text_rect = quit_text.get_rect(center=quit_button.center)
            restart_text_rect = restart_text.get_rect(center=restart_button.center)
            
            SCREEN.blit(quit_text,quit_text_rect)
            SCREEN.blit(pause_text,pause_text_rect)
            SCREEN.blit(restart_text,restart_text_rect)
            
            #computer moves
            if not game.over and game.computer_turn:
                game.basic_ai()
            #game over message
            if game.over:
                text = "Player" + str(game.result) + " wins!"
                textbox = myfont.render(text,False,GREY,WHITE)
                SCREEN.blit(textbox,(WIDTH//2-240,HEIGHT//2-50))
                
            #update screen
            pygame.time.wait(100)
            pygame.display.flip()