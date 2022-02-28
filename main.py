from lib2to3.pgen2 import pgen
import pygame,json

WIDTH,HEIGHT = 1080,720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
TILESIZE = int(HEIGHT/8)
CHUNK = []
MX,MY,MZ = [],[],[]
MX2,MZ2 = [],[]
MX3,MZ3 = [],[]
re1,re2,re3,re4 = [],[],[],[]
pygame.init()
SPEED = 15
try:
    with open("chunk.pmn","r") as CHNK:
        CHUNK = json.load(CHNK)
except:
    for i in range(16):
        MX.append(1)
        MX2.append(0)
        MX3.append(2)
    for i in range(100):
        MY.append(MX2)
    MY.append(MX)
    for i in range(99):
        MY.append(MX3)
    for i in range(16):
        CHUNK.append(MY)
    with open("chunk.pmn","w") as CHNK:
        json.dump(CHUNK,CHNK)
    with open("chunk.pmn","r") as CHNK:
        CHUNK = json.load(CHNK)
grass = pygame.transform.scale(pygame.image.load("assets/grass.png").convert(),(TILESIZE,TILESIZE*2))
dirt = pygame.transform.scale(pygame.image.load("assets/dirt.png").convert(),(TILESIZE,TILESIZE*2))
air = pygame.transform.scale(pygame.image.load("assets/air.png").convert(),(TILESIZE,TILESIZE*2))
pygame.init()

Sprites = ["air",grass,dirt]
CamX, CamY, CamZ = -WIDTH/5,8800,0
PX,PY,PZ = int((CamX + WIDTH/2)/TILESIZE), int(CamY/TILESIZE), int((CamZ + HEIGHT/2)/TILESIZE)
Tiles = [(0,0,0),(255,255,255)]
Clock = pygame.time.Clock()
Speed = 0
SY = PY
JumpSpeed = 0
Jump =0
Jumped = 0
def touching_air(sz,sy,sx):
    try:  
        if CHUNK[sz-1][sy][sx] == 0:
            return True
    except: return True
    try:
        if CHUNK[sz+1][sy][sx] == 0:
            return True
    except: return True
    try:
        if CHUNK[sz][sy+1][sx] == 0: 
            return True    
    except: return True
    try:
        if CHUNK[sz][sy-1][sx] == 0:
            return True
    except: return True
    try:    
        if CHUNK[sz][sy][sx+1] == 0:
            return True
    except: return True
    try:    
        if CHUNK[sz][sy][sx-1] == 0:
            return True
    except:
        pass
    return False
PLHBU = pygame.Rect(WIDTH/2-(TILESIZE*.2),HEIGHT/2-((TILESIZE*3)-TILESIZE*1.6),TILESIZE*.4,TILESIZE*.1)
PLHBL = pygame.Rect(WIDTH/2-(TILESIZE*.4),HEIGHT/2-((TILESIZE*3)-TILESIZE*1.7),TILESIZE*.1,TILESIZE*.05)
PLHBR = pygame.Rect(WIDTH/2+(TILESIZE*.3),HEIGHT/2-((TILESIZE*3)-TILESIZE*1.7),TILESIZE*.1,TILESIZE*.05)
PLHBD = pygame.Rect(WIDTH/2-(TILESIZE*.2),HEIGHT/2-((TILESIZE*3)-TILESIZE*1.7),TILESIZE*.4,TILESIZE*.1)
while True:
    PX,PY,PZ = int((CamX + WIDTH/2)/TILESIZE), int(CamY/TILESIZE), int((CamZ + HEIGHT/2)/TILESIZE)
    Clock.tick(60)
    # print(int(Clock.get_fps()))
    
    # r1 setzen
    re1 = CHUNK
    # bei r1 0 zu r2 aussortieren
    re2,re3,re4 = [],[],[] 
    # r2 nach r3 von hinten nach vorne sortieren

    sx,sy,sz = 0,len(CHUNK[0])-1,0
    # for layer in CHUNK:
    for i in range(16):
        
        layer = CHUNK[i]
        for r in range(len(layer)-1,-1,-1):
            row = layer[-r]
            for tile in row:
                if not Sprites[CHUNK[sz][sy][sx]] == "air":
                    if touching_air(sz,sy,sx):
                        WIN.blit(Sprites[CHUNK[sz][sy][sx]],((sx*TILESIZE)-CamX,((((sy*TILESIZE))+(sz*(TILESIZE)))-CamY)-CamZ))
                    
                #pygame.draw.rect(WIN,(0,0,0),pygame.Rect((sx*TILESIZE)-CamX,((((sy*TILESIZE))+(sz*(TILESIZE/2)))-CamY)-CamZ,TILESIZE,TILESIZE),1)
                sx += 1
            sx = 0
            sy -= 1
        sy = len(layer)-1
        if i == PZ or i == 15:
            for i in range(10000):
                if CHUNK[PZ][PY-i][PX] == 0:
                    pass
                else:
                    INY = CamY-(PY*TILESIZE)
                    pygame.draw.circle(WIN,(255,255,0),(WIDTH/2,HEIGHT/2-INY+i*TILESIZE),10)
                    break
            pygame.draw.rect(WIN,(255,255,255),pygame.Rect(WIDTH/2-(TILESIZE*.4),HEIGHT/2-(TILESIZE*3),TILESIZE*.8,TILESIZE*1.8))
        sz += 1
    CamY += Speed
    
    try:
        if CHUNK[PZ][int(((PY*TILESIZE)-Speed-.001)/TILESIZE)][PX] == 0: 
            Speed += .3
            Jumped = 0
        
        else:
            if Keys[pygame.K_SPACE]:
                Jump = 1
            if Jumped == 0:
                Speed = 0
    except:
        CamY += Speed
        Speed += 2
    #print(PX,PY,PZ,Jump)
    if Jump == 1:
        SY = CamY
        Jump = 0
        Speed = -TILESIZE/7
        Jumped = 1
    
    
    
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_r]:
        with open("chunk.pmn","r") as CHNK:
            CHUNK = json.load(CHNK)

    if Keys[pygame.K_w] and CHUNK[int(((PZ*TILESIZE)-SPEED)/TILESIZE)][PY-2][PX] == 0:
        CamZ -= SPEED
    if Keys[pygame.K_a]:
        CamX -= SPEED
    if Keys[pygame.K_s]:
        CamZ += SPEED
    if Keys[pygame.K_d]:
        CamX += SPEED
    if Keys[pygame.K_LSHIFT]:
        CamY += SPEED
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
    WIN.fill((0,0,0))