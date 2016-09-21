import pygame as p
import random
import time
import sqlite3
import sys
import eztext
#-----------------IMPORT STATEMENTS-------------------#
black=(0,0,0)
white=(255,255,255)
#----------------INITIALISATION---------------------#




#----------------MAIN CLASS------------------------#
class window():
    #---------------------------------------CLASS CONSTRUCTOR----------------#
    def __init__(self):
        #-------------------------------MATRIX HOLDING THE DATA OF PIXELS------------------#
        self.matrix=[]
        for i in range(20):
            self.matrix.append([])
            for j in range(40):
                self.matrix[i].append((i*32,j*32))


        #-----------------------WINDOW CREATION------------------#
        p.init()
        self.screen=p.display.set_mode((1280,640))
        p.display.set_caption("Snake-420")
        #---------------------GET SPEED CONTROL VARIABLE----------------#
        clock = p.time.Clock()
        #----------------------MUSIC---------------------#
        self.songs=['Blurry.mp3','Jane.mp3']
        k=random.randint(0,1)
        p.mixer.music.load(self.songs[k])
        p.mixer.music.play(-1)
        #---------------------------NAME INPUT CLASS AND CODE------------------#
        txtbx = eztext.Input(maxlength=45, color=white, prompt='Type Your Name: ')
        txtbx.set_pos(800//2,550//2)
        #--------------------------LOOP VARIABLE TO RECEIVE INPUT---------------#
        mainloop=True
        #-------------------------CONNECTING TO DATABSE TO STORE HIGH SCORES--------------------#
        self.db=sqlite3.connect('Snake')
        self.cur=self.db.cursor()
        try:
            self.cur.execute('create table scores(name varchar(30),score integer,length integer);')
        except:
            print "table already exists"
        #--------------------------WAITING TO INPUT NAME AT 30 FPS----------------------#
        while mainloop:
            clock.tick(30)
            e=p.event.get()
            for events in e:
                if events.type==p.QUIT:
                    sys.exit()
                if events.type==p.KEYDOWN and events.key==p.K_RETURN:
                    mainloop=False
                    break

            self.screen.fill(black)
        # update txtbx
            txtbx.update(e)
        # blit txtbx on the sceen
            txtbx.draw(self.screen)
            p.display.flip()
        #----------------------ALL VARIABLES AND SCREEN INITIALISATION------------------------#
        self.name=txtbx.getVal()
        self.score=0
        self.inc_score=1
        self.Bg=p.Surface((1280,640))
        self.Bg.fill(black)
        self.Bg=self.Bg.convert()
        self.screen.blit(self.Bg,(0,0))
        p.display.flip()
        self.body=[]
        self.row=random.randint(1,18)   #THE RANDOM LOCATIONS TO DRAW FOOD AT
        self.col=random.randint(1,38)   #THE RANDOM LOCATIONS TO DRAW FOOD AT
        self.body.append((128,128,1))
        self.length=1
    #--------------------------DRAW FOOD AT RANDOM LOCATIONS--------------------------#
    def draw_food(self):
        self.c=self.matrix[self.row][self.col]
        p.draw.circle(self.Bg,white,(self.c[1]+16,self.c[0]+16),16)
        self.Bg=self.Bg.convert()
        self.screen.blit(self.Bg,(0,0))
        #p.display.flip()
    #---------------------------------THE GAME STARTS HERE--------------------------------#
    def start(self):
        dist=32
        fps=5
        sx=128
        sy=128
        mainloop=True
        dx=dist
        dy=0
        dir=1
        clock = p.time.Clock()
        while mainloop:

            clock.tick(fps)

            for e in p.event.get():
                if e.type==p.QUIT:
                    sys.exit()
                if e.type==p.KEYDOWN and e.key==p.K_DOWN:
                    if dir==0:
                        break
                    dy=dist
                    dx=0
                    dir=2
                    break
                if e.type==p.KEYDOWN and e.key==p.K_UP:
                    if dir==2:
                        break
                    dy=-dist
                    dx=0
                    dir=0
                    break
                if e.type==p.KEYDOWN and e.key==p.K_RIGHT:
                    if dir==3:
                        break
                    dy=0
                    dx=dist
                    dir=1
                    break
                if e.type==p.KEYDOWN and e.key==p.K_LEFT:
                    if dir==1:
                        break
                    dy=0
                    dx=-dist
                    dir=3
                    break
            #self.Bg.fill(black)

            #self.draw_snake()
            sx+=dx
            sy+=dy
            for i in self.body:
                t=(i[0],i[1])
                if t==(sx,sy):
                    mainloop=False
                    self.game_over()
                    sys.exit()

            if sx==self.c[1] and sy==self.c[0]:
                self.length+=1
                self.body=[(sx,sx,dir)]+self.body
                #p.draw.rect(self.Bg,white,(sx,sy,32,32))
                if sx>=1248:
                    dx=-dist
                if sx<=0:
                    dx=dist
                if sy<=0:
                    dy=dist
                if sy>=608:
                    dy=-dist
                sx+=dx
                sy+=dy
                p.draw.rect(self.Bg,black,(self.c[1],self.c[0],32,32))
                if self.score>80:
                    self.row=random.randint(0,19)
                    self.col=random.randint(0,39)
                else:
                    self.row=random.randint(1,18)
                    self.col=random.randint(1,38)
                self.draw_food()
                fps+=1
                self.score+=self.inc_score
                #self.inc_score+=random.randint(1,4)
                self.inc_score+=1
            self.draw_food()
            #for i in range(len(self.body)):
            for i in self.body:
                lx=i[0]
                ly=i[1]
                #print lx,ly
                p.draw.rect(self.Bg,white,(lx,ly,32,32))
                self.screen.blit(self.Bg,(0,0))
                p.display.flip()
            p.draw.rect(self.Bg,white,(sx,sy,32,32))
            self.body.append((sx,sy,dir))
            #print self.body
            t=self.body.pop(0)

            p.draw.rect(self.Bg,black,(t[0],t[1],32,32))
            #p.draw.rect(self.Bg,black,(t[0]+32//2,t[1],32//2,32))
            #p.draw.rect(self.Bg,black,(t[0]+(32//2)*2,t[1],32//2,32))
            self.Bg=self.Bg.convert()
            self.screen.blit(self.Bg,(0,0))
            p.display.flip()
            if sx>=1248:
                dx=-dist
            if sx<=0:
                dx=dist
            if sy<=0:
                dy=dist
            if sy>=608:
                dy=-dist
        #print self.score
    def game_over(self):
        self.Bg.fill(black)
        self.screen.blit(self.Bg,(0,0))
        p.display.flip()
        myfont = p.font.SysFont("None", 32)
        mytext = myfont.render('GAME OVER:SCORE= '+str(self.score), True, (255,255,255))

        mytext = mytext.convert_alpha()
        self.screen.blit(mytext,(800//2,32))
        mytext = myfont.render('HIGH SCORES', True, (255,255,255))
        self.screen.blit(mytext,(800//2,66))
        p.display.flip()
        self.cur.execute('insert into scores values(?,?,?);',(self.name,self.score,self.length))
        self.db.commit()
        res=self.cur.execute('select * from scores order by score desc;')
        mytext = myfont.render('NAME          SCORE         LENGTH', True, (255,255,255))
        self.screen.blit(mytext,(800//2,100))
        p.display.flip()
        i=0
        r=res.fetchall()
        #n_r=r.
        print r[0][0]
        mainloop=True
        dr=True
        while mainloop:
            for e in p.event.get():
                if e.type==p.QUIT:
                    mainloop=False
                    return
            j=0
            if dr:
                for i in r:
                    if j>10:
                        print 'break'
                        break
                    myfont = p.font.SysFont("None", 32)
                    mytext = myfont.render(str(i[0])+' '*(20-len(str(i[0])))+str(i[1])+' '*(20-len(str(i[1])))+str(i[2]), True, (255,255,255))
                    j+=1
                    #print i[0],i[1],i[1]
                    mytext = mytext.convert_alpha()
                    self.screen.blit(mytext,(800//2,135+j*32))
                    p.display.flip()
                dr=False
        b=1
    def win(self):
        b=1
