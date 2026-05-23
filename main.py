import pygame,random,math as m,os
from pygame.locals import *
os.environ['SDL_VIDEO_CENTERED']='1'
pygame.init()
pygame.mixer.init(frequency=44100,size=-16,channels=2,buffer=2048)
def gsnd(d,ft):
 sr=44100;s=int(d*sr);b=bytearray()
 for i in range(s):t=i/sr;f=ft(t);v=int(127*m.sin(2*m.pi*f*t)*(1-t/d));v=max(-128,min(127,v));b.append(v&0xFF);b.append(v&0xFF)
 return pygame.mixer.Sound(bytes(b))
def gbomb():
 d=0.4;sr=44100;s=int(d*sr);b=bytearray()
 for i in range(s):t=i/sr;f=50+150*(1-t/d);n=random.randint(-50,50);v=int(127*m.sin(2*m.pi*f*t)*(1-t/d)+n*(1-t/d));v=max(-128,min(127,v));b.append(v&0xFF);b.append(v&0xFF)
 return pygame.mixer.Sound(bytes(b))
def gmus():
 d=8;sr=22050;s=int(d*sr);b=bytearray()
 notes=[261,329,392,523,392,329,261,329,392,523,392,329,293,349,440,587,440,349,293,349,440,587,440,349,261,329,392,523,392,329,261,0,0,0]
 nl=s//len(notes)
 for i in range(s):
  ni=i//nl
  if ni<len(notes):
   f=notes[ni]
   if f>0:v=int(63*m.sin(2*m.pi*f*i/sr)+31*m.sin(2*m.pi*f*0.5*i/sr));v=int(v*(1-(i%nl)/nl));v=max(-128,min(127,v));b.append(v&0xFF);b.append(v&0xFF)
   else:b.append(0);b.append(0)
 return pygame.mixer.Sound(bytes(b))
def gpickup():
 d=0.2;sr=44100;s=int(d*sr);b=bytearray()
 for i in range(s):t=i/sr;f=600+t*2000;v=int(127*m.sin(2*m.pi*f*t)*(1-t/d));v=max(-128,min(127,v));b.append(v&0xFF);b.append(v&0xFF)
 return pygame.mixer.Sound(bytes(b))
try:ssnd=gsnd(0.15,lambda t:800+3000*(1-t/0.15));ssnd.set_volume(0.4)
except:ssnd=None
try:bsnd=gbomb();bsnd.set_volume(0.5)
except:bsnd=None
try:csnd=gsnd(0.3,lambda t:600+t*1500);csnd.set_volume(0.5)
except:csnd=None
try:pksnd=gpickup();pksnd.set_volume(0.6)
except:pksnd=None
try:msnd=gmus();mch=pygame.mixer.Channel(0);mch.set_volume(0.12)
except:mch=None
info=pygame.display.Info()
SW=info.current_w if info.current_w>0 else 800
SH=info.current_h if info.current_h>0 else 480
W,H=800,480
gs=pygame.Surface((W,H))
sc=pygame.display.set_mode((SW,SH),FULLSCREEN|SCALED)
pygame.display.set_caption("Fruit Ninja ULTIMATE")
clock=pygame.time.Clock()
font=pygame.font.Font(None,36)
bfont=pygame.font.Font(None,72)
sf=pygame.font.Font(None,20)
tf=pygame.font.Font(None,14)
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,50,50)
GOLD=(255,215,0)
GREEN=(50,255,50)
BLUE=(50,100,255)
CYAN=(0,255,255)
ORANGE=(255,165,0)
PINK=(255,100,200)
SPLASH,MENU,PLAYING,GAMEOVER,SETTINGS,SHOP=-3,-2,-1,0,1,2
state=SPLASH
splash_timer=120
GT=60
DIFF_SETTINGS={0:("Easy",0.6,50),1:("Normal",1.0,60),2:("Hard",1.5,70),3:("Extreme",2.2,90)}
diff_level=1
score=0
bs=0
tfs=0
combo=0
mc=0
ct=0
tl=GT
coins=0
music_on=True
double_score=0
magnet_timer=0
slow_mo=0
try:
 import json
 with open('fnsave.json','r')as f:sd=json.load(f);bs=sd.get('bs',0);coins=sd.get('coins',0);diff_level=sd.get('diff',1)
except:sd={}
def sv():
 try:
  import json
  data={'bs':bs,'coins':coins,'bi':cbi,'bu':bu,'diff':diff_level}
  with open('fnsave.json','w')as f:json.dump(data,f)
 except:pass
BLADES=[
 {"name":"Classic","tc":[(255,255,255),(200,200,200)],"price":0,"eff":"normal","desc":"Standart"},
 {"name":"Fire","tc":[(255,200,0),(255,50,0),(255,150,0)],"price":100,"eff":"fire","desc":"Burn!"},
 {"name":"Ice","tc":[(200,230,255),(100,180,255),(50,150,255)],"price":150,"eff":"ice","desc":"Freeze"},
 {"name":"Rainbow","tc":[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)],"price":250,"eff":"rainbow","desc":"Colors!"},
 {"name":"Shadow","tc":[(80,0,150),(40,0,80),(20,0,40)],"price":200,"eff":"shadow","desc":"Dark"},
 {"name":"Lightning","tc":[(255,255,100),(200,200,0),(255,255,255)],"price":300,"eff":"lightning","desc":"Electric"},
 {"name":"Blood","tc":[(255,0,0),(150,0,0),(100,0,0)],"price":350,"eff":"blood","desc":"Blood"},
 {"name":"Gold","tc":[(255,255,100),(255,215,0),(200,170,0)],"price":500,"eff":"gold","desc":"+2 coins"},
 {"name":"Neon","tc":[(0,255,100),(0,200,255),(100,0,255)],"price":400,"eff":"neon","desc":"Bright"},
 {"name":"Space","tc":[(100,50,200),(50,0,150),(200,100,255),(255,255,255)],"price":600,"eff":"space","desc":"Stars"}
]
bu=[True]+[False]*9
cbi=0
try:cbi=sd.get('bi',0);bu=sd.get('bu',[True]+[False]*9)
except:pass
blade=BLADES[cbi]
particles=[]
SPARKS=[]
ss=0
dbtimer=0
fruits=[]
powerups=[]
fst=0
FT=[
 {"name":"Watermelon","color":(255,60,60),"radius":35,"points":1},
 {"name":"Orange","color":(255,180,0),"radius":28,"points":2},
 {"name":"Lemon","color":(255,255,50),"radius":24,"points":2},
 {"name":"Apple","color":(255,30,30),"radius":30,"points":1},
 {"name":"Banana","color":(255,255,120),"radius":34,"points":3},
 {"name":"Peach","color":(255,200,180),"radius":28,"points":2},
 {"name":"Strawberry","color":(255,40,100),"radius":22,"points":3},
 {"name":"Kiwi","color":(120,220,70),"radius":26,"points":3},
 {"name":"Grape","color":(200,20,220),"radius":30,"points":4},
 {"name":"Pineapple","color":(255,220,70),"radius":36,"points":5},
 {"name":"Coconut","color":(160,110,60),"radius":32,"points":4},
 {"name":"Mango","color":(255,170,60),"radius":29,"points":3},
 {"name":"Bomb","color":(60,60,60),"radius":30,"points":-1},
]
class PowerUp:
    def __init__(self):
        self.type=random.choice(["double","slow","magnet","coin"])
        self.x=random.randint(100,W-100);self.y=H+random.randint(50,200)
        self.vy=random.uniform(-8,-5);self.vx=random.uniform(-2,2)
        self.gravity=0.2;self.life=300;self.glow=0
        if self.type=="double":self.color=(255,215,0);self.symbol="x2"
        elif self.type=="slow":self.color=(100,200,255);self.symbol="~"
        elif self.type=="magnet":self.color=(255,100,255);self.symbol="M"
        else:self.color=(255,255,100);self.symbol="$"
    def update(self):
        self.vy+=self.gravity;self.x+=self.vx;self.y+=self.vy;self.life-=1;self.glow=(self.glow+0.1)%(2*m.pi)
    def draw(self,s):
        ga=max(0,min(255,int(40+m.sin(self.glow)*30)))
        gs2=pygame.Surface((40,40),SRCALPHA)
        pygame.draw.circle(gs2,(*self.color,ga),(20,20),18)
        s.blit(gs2,(int(self.x-20),int(self.y-20)))
        pygame.draw.circle(s,self.color,(int(self.x),int(self.y)),16)
        pygame.draw.circle(s,WHITE,(int(self.x),int(self.y)),16,2)
        txt=sf.render(self.symbol,True,BLACK)
        s.blit(txt,(int(self.x)-txt.get_width()//2,int(self.y)-txt.get_height()//2))
    def collect(self):
        global double_score,magnet_timer,slow_mo,coins
        if self.type=="double":double_score=300
        elif self.type=="slow":slow_mo=180
        elif self.type=="magnet":magnet_timer=240
        else:coins+=5
trail=[]
MT=20
swiping=False
lm=(0,0)
sls=0
def sp(mx,my):return mx*W/SW,my*H/SH
class Fruit:
    def __init__(self,sm=1.0):
        self.type=random.choice(FT)
        if self.type["name"]=="Bomb" and random.random()>0.12:self.type=random.choice(FT[:-1])
        self.x=random.randint(100,W-100);self.y=H+random.randint(50,250);self.radius=self.type["radius"]
        a=random.uniform(-m.pi*0.65,-m.pi*0.35);s=random.uniform(8,16)*sm
        self.vx=m.cos(a)*s;self.vy=m.sin(a)*s;self.gravity=0.35
        self.rot=random.uniform(0,2*m.pi);self.rs=random.uniform(-0.25,0.25)
        self.sliced=False;self.sp=[];self.glow=0;self.tp=[];self.frozen=False;self.ft=0
        self.wobble=random.uniform(0,2*m.pi)
    def update(self,mt=0):
        if self.frozen:self.ft-=1
        if self.frozen and self.ft<=0:self.frozen=False;return
        if self.frozen:return
        if mt>0 and not self.sliced:
            dx=W//2-self.x;dy=H//2-self.y;dist=m.sqrt(dx*dx+dy*dy)
            if dist>0:self.vx+=dx/dist*0.5;self.vy+=dy/dist*0.3
        if not self.sliced:
            self.vy+=self.gravity;self.x+=self.vx;self.y+=self.vy;self.rot+=self.rs
            self.wobble=(self.wobble+0.05)%(2*m.pi)
            self.glow=(self.glow+0.1)%(2*m.pi)
            if random.random()<0.4:self.tp.append({"x":self.x+random.uniform(-12,12),"y":self.y+random.uniform(-12,12),"life":12,"color":self.type["color"],"size":random.uniform(1,3)})
        else:
            for p in self.sp:p["vy"]+=self.gravity;p["x"]+=p["vx"];p["y"]+=p["vy"];p["rot"]+=p["rs"];p["life"]-=1
        for p in self.tp[:]:p["life"]-=1
        self.tp=[p for p in self.tp if p["life"]>0]
    def draw(self,s):
        if self.frozen:pygame.draw.circle(s,(150,200,255),(int(self.x),int(self.y)),self.radius+3)
        if not self.sliced:
            ga=max(0,min(255,int(30+m.sin(self.glow)*25)))
            wobble_offset=m.sin(self.wobble)*3
            gs2=pygame.Surface((self.radius*2+10,self.radius*2+10),SRCALPHA)
            c=self.type["color"]
            shadow_c=(max(0,c[0]-80),max(0,c[1]-80),max(0,c[2]-80))
            pygame.draw.circle(gs2,(*shadow_c,100),(self.radius+5,int(self.radius+5+wobble_offset)),self.radius+2)
            pygame.draw.circle(gs2,(c[0],c[1],c[2],ga),(self.radius+5,int(self.radius+5+wobble_offset)),self.radius)
            s.blit(gs2,(int(self.x-self.radius-5),int(self.y-self.radius-5)))
            pygame.draw.circle(s,c,(int(self.x),int(self.y)),self.radius)
            pygame.draw.circle(s,WHITE,(int(self.x),int(self.y)),self.radius,2)
            hl=(min(255,c[0]+80),min(255,c[1]+80),min(255,c[2]+80))
            pygame.draw.circle(s,hl,(int(self.x-self.radius*0.3),int(self.y-self.radius*0.3)),max(1,self.radius//3))
            if self.type["name"]=="Bomb":
                pygame.draw.circle(s,(80,80,80),(int(self.x),int(self.y)),self.radius)
                pygame.draw.circle(s,(150,30,30),(int(self.x),int(self.y)),self.radius-5)
                pygame.draw.line(s,(200,150,50),(int(self.x),int(self.y-self.radius)),(int(self.x+8),int(self.y-self.radius-12)),3)
                sc2=(255,200,0)if random.random()>0.5 else(255,100,0)
                pygame.draw.circle(s,sc2,(int(self.x+8),int(self.y-self.radius-12)),4)
        for p in self.sp:
            sf2=pygame.Surface((self.radius*2,self.radius*2),SRCALPHA)
            c=self.type["color"]
            if p["side"]=="left":
                pygame.draw.arc(sf2,c,(0,0,self.radius*2,self.radius*2),m.pi/2,3*m.pi/2,self.radius)
                pygame.draw.line(sf2,(200,50,50,200),(self.radius,0),(self.radius,self.radius*2),2)
            else:
                pygame.draw.arc(sf2,c,(0,0,self.radius*2,self.radius*2),-m.pi/2,m.pi/2,self.radius)
                pygame.draw.line(sf2,(200,50,50,200),(self.radius,0),(self.radius,self.radius*2),2)
            rt=pygame.transform.rotate(sf2,m.degrees(p["rot"]))
            s.blit(rt,(int(p["x"]-self.radius),int(p["y"]-self.radius)))
        for p in self.tp:
            alpha=max(0,min(255,int(p["life"]*21)));c=p["color"];sz=max(1,int(p["size"]))
            pygame.draw.circle(s,(c[0],c[1],c[2],alpha),(int(p["x"]),int(p["y"])),sz)
    def slice(self,mx,my):
        if not self.sliced and not self.frozen:
            dist=m.sqrt((self.x-mx)**2+(self.y-my)**2)
            if dist<self.radius+12:
                self.sliced=True
                for side,vm in[("left",-1),("right",1)]:self.sp.append({"x":self.x,"y":self.y,"vx":self.vx+vm*random.uniform(2,5),"vy":self.vy-random.uniform(3,7),"rot":self.rot,"rs":vm*random.uniform(0.15,0.5),"side":side,"life":50})
                eff=blade["eff"];pc=30 if eff!="normal"else 20
                for _ in range(pc):
                    a=random.uniform(0,2*m.pi);spd=random.uniform(3,10)
                    if eff=="fire":color=random.choice([(255,200,0),(255,100,0),(255,50,0)])
                    elif eff=="ice":color=random.choice([(150,220,255),(200,240,255),(255,255,255)])
                    elif eff=="rainbow":color=random.choice([(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)])
                    elif eff=="shadow":color=random.choice([(80,0,150),(40,0,80),(20,0,40)])
                    elif eff=="lightning":color=random.choice([(255,255,200),(255,255,0),(200,200,255)])
                    elif eff=="blood":color=random.choice([(200,0,0),(150,0,0),(100,0,0)])
                    elif eff=="gold":color=random.choice([(255,215,0),(255,255,100),(200,170,0)])
                    elif eff=="neon":color=random.choice([(0,255,100),(0,200,255),(100,0,255)])
                    elif eff=="space":color=random.choice([(100,50,200),(200,100,255),(255,255,255)])
                    else:color=random.choice([self.type["color"],WHITE,(255,200,100)])
                    particles.append({"x":self.x,"y":self.y,"vx":m.cos(a)*spd,"vy":m.sin(a)*spd,"life":random.randint(20,40),"color":color,"size":random.uniform(2,5)})
                return self.type["points"]
        return 0 
class Spark:
    def __init__(self,x,y,eff="normal"):self.x=x;self.y=y;self.vx=random.uniform(-4,4);self.vy=random.uniform(-4,4);self.life=random.randint(8,20);self.eff=eff
    def update(self):self.x+=self.vx;self.y+=self.vy;self.vy+=0.1;self.life-=1
    def draw(self,s):
        alpha=max(0,min(255,int(self.life*12)))
        if self.eff=="fire":color=(255,150+random.randint(0,100),random.randint(0,50))
        elif self.eff=="ice":color=(150,200+random.randint(0,55),255)
        elif self.eff=="rainbow":color=random.choice([(255,0,0),(255,255,0),(0,255,0),(0,255,255)])
        else:color=(255,200+random.randint(0,55),random.randint(0,100))
        sz=3 if self.eff!="normal"else 2
        pygame.draw.circle(s,(*color,alpha),(int(self.x),int(self.y)),sz)
def dbg(s):
    for y in range(H):
        t=y/H;r=int(40+t*80);g=int(100+t*100);b=int(150+t*105)
        pygame.draw.line(s,(min(255,r),min(255,g),min(255,b)),(0,y),(W,y))
    for i in range(100):
        x=(i*137+50)%W;y=(i*97+30)%(H//2);br=180+int(m.sin(pygame.time.get_ticks()*0.001+i)*75)
        pygame.draw.circle(s,(min(255,br),min(255,br),min(255,br)),(int(x),int(y)),1)
    for i in range(5):
        cx=random.randint(0,W);cy=random.randint(0,H//3);alpha=random.randint(10,30)
        cs2=pygame.Surface((60,60),SRCALPHA);pygame.draw.circle(cs2,(255,255,255,alpha),(30,30),30)
        s.blit(cs2,(cx-30,cy-30))
def dbt(s):
    if len(trail)>1:
        bc=blade["tc"]
        for i in range(len(trail)-1):
            alpha=int((i/len(trail))*200);th=max(1,int((i/len(trail))*8)+1);ci=i%len(bc);base=bc[ci];color=(base[0],base[1],base[2],alpha)
            if i>0:pygame.draw.line(s,color,trail[i],trail[i+1],th)
            if blade["eff"]!="normal"and random.random()<0.4:SPARKS.append(Spark(trail[i][0]+random.uniform(-8,8),trail[i][1]+random.uniform(-8,8),blade["eff"]))
def cs(x,y,c=8):
    for _ in range(c):SPARKS.append(Spark(x,y,blade["eff"]))
def dt(s):
    bw,bh=300,18;bx,by=W//2-bw//2,12
    pygame.draw.rect(s,(20,20,30),(bx-3,by-3,bw+6,bh+6));pygame.draw.rect(s,(40,40,55),(bx,by,bw,bh))
    fw=int(bw*(tl/GT))
    if tl>GT*0.4:bc=GREEN
    elif tl>GT*0.2:bc=(255,200,0)
    else:bc=RED
    if fw>0:
        for i in range(fw):
            sh=0.7+(i/fw)*0.3;cr=min(255,int(bc[0]*sh));cg=min(255,int(bc[1]*sh));cb=min(255,int(bc[2]*sh))
            pygame.draw.line(s,(cr,cg,cb),(bx+i,by),(bx+i,by+bh))
    pygame.draw.rect(s,WHITE,(bx,by,bw,bh),2)
    tt=font.render("Time: "+str(int(tl)),True,WHITE);s.blit(tt,(W//2-tt.get_width()//2,by+22))
def dsb(s):
    gx,gy=W-45,10;pygame.draw.circle(s,(50,50,65),(gx+15,gy+15),18);pygame.draw.circle(s,(120,120,140),(gx+15,gy+15),18,2)
    gt=font.render("+",True,WHITE);s.blit(gt,(gx+6,gy+2))
def draw_splash(s,timer):
    s.fill((15,5,40))
    for _ in range(200):x=random.randint(0,W);y=random.randint(0,H);br=random.randint(80,255);pygame.draw.circle(s,(br,br,br),(x,y),0)
    t=pygame.time.get_ticks()*0.001
    r1=int(180+m.sin(t)*75);g1=int(120+m.sin(t*1.3)*100);b1=255;color1=(r1,g1,b1)
    r2=255;g2=int(220+m.sin(t*1.5)*35);b2=int(130+m.sin(t*0.9)*80);color2=(r2,g2,b2)
    try:title_font=pygame.font.Font(None,65)
    except:title_font=bfont
    title=title_font.render("FRUIT NINJA",True,color1);title2=title_font.render("FRUIT NINJA",True,color2)
    ox=m.sin(t*2)*3;oy=m.cos(t*1.5)*2
    s.blit(title2,(W//2-title.get_width()//2+ox+2,H//2-60+oy+2));s.blit(title,(W//2-title.get_width()//2+ox,H//2-60+oy))
    try:sub_font=pygame.font.Font(None,46)
    except:sub_font=font
    sub=sub_font.render("ULTIMATE EDITION",True,CYAN);s.blit(sub,(W//2-sub.get_width()//2,H//2-10))
    alpha=max(0,min(255,int(abs(m.sin(t*3))*255)))
    by_surf=pygame.Surface((350,50),SRCALPHA);by_text=font.render("*By ewokas*",True,WHITE)
    by_surf.blit(by_text,(0,0));by_surf.set_alpha(alpha);s.blit(by_surf,(W//2-by_text.get_width()//2,H//2+40))
    tap_text=sf.render("Tap to start",True,WHITE);s.blit(tap_text,(W//2-tap_text.get_width()//2,H-80))
def dm(s):
    s.fill((18,10,45))
    for _ in range(120):x=random.randint(0,W);y=random.randint(0,H);br=random.randint(80,255);pygame.draw.circle(s,(br,br,br),(x,y),0)
    title=bfont.render("FRUIT NINJA",True,GOLD);sub=font.render("ULTIMATE EDITION",True,WHITE)
    s.blit(title,(W//2-title.get_width()//2,H//4-40));s.blit(sub,(W//2-sub.get_width()//2,H//4+20))
    pb=pygame.Rect(W//2-110,H//2-60,220,55)
    diff_btn=pygame.Rect(W//2-110,H//2+10,220,55)
    sb=pygame.Rect(W//2-110,H//2+80,220,55)
    pygame.draw.rect(s,GREEN,pb,border_radius=12);pygame.draw.rect(s,ORANGE,diff_btn,border_radius=12);pygame.draw.rect(s,BLUE,sb,border_radius=12)
    s.blit(font.render("PLAY",True,WHITE),(W//2-45,H//2-47))
    s.blit(font.render("DIFF: "+DIFF_SETTINGS[diff_level][0],True,WHITE),(W//2-65,H//2+23))
    s.blit(font.render("SHOP",True,WHITE),(W//2-40,H//2+93))
    s.blit(font.render("Coins: "+str(coins),True,GOLD),(W//2-55,H//2+145))
    by_text=sf.render("*By ewokas*",True,(200,200,200));s.blit(by_text,(W//2-by_text.get_width()//2,H-30))
    return pb,diff_btn,sb
def dst(s):
    s.fill((25,15,55));s.blit(font.render("SETTINGS",True,WHITE),(W//2-60,20))
    bb=pygame.Rect(20,15,100,35);pygame.draw.rect(s,(100,100,120),bb,border_radius=5);s.blit(sf.render("BACK",True,WHITE),(35,23))
    y=80
    for i,bd in enumerate(BLADES):
        rect=pygame.Rect(50,y,W-100,45)
        if i==cbi:pygame.draw.rect(s,GOLD,rect,border_radius=8);pygame.draw.rect(s,(50,40,85),rect.inflate(-4,-4),border_radius=6)
        else:pygame.draw.rect(s,(50,40,85),rect,border_radius=8)
        pygame.draw.rect(s,WHITE,rect,1,border_radius=8)
        s.blit(sf.render(bd["name"],True,WHITE),(60,y+3));s.blit(tf.render(bd["desc"],True,(200,200,200)),(60,y+23))
        if not bu[i]:s.blit(sf.render("Cost:"+str(bd["price"]),True,GOLD),(W-120,y+12))
        elif i==cbi:s.blit(sf.render("SELECTED",True,GREEN),(W-120,y+12))
        y+=52
    return bb
def dsh(s):
    s.fill((25,15,55));s.blit(font.render("SHOP",True,WHITE),(W//2-50,20))
    bb=pygame.Rect(20,15,100,35);pygame.draw.rect(s,(100,100,120),bb,border_radius=5);s.blit(sf.render("BACK",True,WHITE),(35,23))
    s.blit(font.render("Coins: "+str(coins),True,GOLD),(W//2-70,55))
    y=90;buy_btns=[]
    for i,bd in enumerate(BLADES):
        if bd["price"]==0:continue
        rect=pygame.Rect(50,y,W-100,50);pygame.draw.rect(s,(60,50,95),rect,border_radius=8);pygame.draw.rect(s,WHITE,rect,1,border_radius=8)
        s.blit(sf.render(bd["name"],True,WHITE),(60,y+5));s.blit(tf.render(bd["desc"],True,(200,200,200)),(60,y+25))
        if bu[i]:s.blit(sf.render("OWNED",True,GREEN),(W-150,y+15))
        else:
            bb2=pygame.Rect(W-160,y+10,100,30);pygame.draw.rect(s,GOLD,bb2,border_radius=5)
            s.blit(sf.render("Buy "+str(bd["price"]),True,BLACK),(W-155,y+15));buy_btns.append((bb2,i))
        y+=58
    return bb,buy_btns
running=True
lt=pygame.time.get_ticks()
pb=None
sb=None
diff_btn=None
bb=None
buy_btns=[]
sbr=pygame.Rect(W-45,10,36,36)
mtimer=0
while running:
    ct2=pygame.time.get_ticks();dt2=(ct2-lt)/1000.0;lt=ct2
    if music_on and mch:
        mtimer+=dt2
        if mtimer>8:mch.play(msnd);mtimer=0
    elif not music_on and mch:mch.stop()
    diff_name,diff_mult,diff_time=DIFF_SETTINGS[diff_level]
    GT=diff_time
    for event in pygame.event.get():
        if event.type==QUIT:sv();running=False
        elif event.type==MOUSEBUTTONDOWN:
            mx,my=sp(*event.pos)
            if state==SPLASH:state=MENU
            elif state==MENU:
                if pb and pb.collidepoint(mx,my):
                    state=PLAYING;score=0;combo=0;mc=0;tl=GT;tfs=0;fruits.clear();particles.clear();SPARKS.clear();powerups.clear();double_score=0;magnet_timer=0;slow_mo=0
                elif diff_btn and diff_btn.collidepoint(mx,my):diff_level=(diff_level+1)%4;sv()
                elif sb and sb.collidepoint(mx,my):state=SHOP;buy_btns=[]
            elif state==PLAYING:
                if sbr.collidepoint(mx,my):state=SETTINGS
                else:swiping=True;trail=[];lm=(mx,my)
            elif state==GAMEOVER:state=MENU
            elif state==SETTINGS:
                if bb and bb.collidepoint(mx,my):state=PLAYING
                else:
                    y=80
                    for i in range(len(BLADES)):
                        rect=pygame.Rect(50,y,W-100,45)
                        if rect.collidepoint(mx,my)and bu[i]:cbi=i;blade=BLADES[cbi];sv()
                        y+=52
            elif state==SHOP:
                if bb and bb.collidepoint(mx,my):state=MENU;pb,diff_btn,sb=dm(gs)
                else:
                    for btn,i in buy_btns:
                        if btn.collidepoint(mx,my)and not bu[i]and coins>=BLADES[i]["price"]:coins-=BLADES[i]["price"];bu[i]=True;sv();buy_btns=[]
        elif event.type==MOUSEMOTION:
            mx,my=sp(*event.pos)
            if swiping and state==PLAYING:
                trail.append((mx,my))
                if len(trail)>MT:trail.pop(0)
                sls=m.sqrt((mx-lm[0])**2+(my-lm[1])**2);lm=(mx,my)
                if sls>15:cs(mx,my,4)
                for fruit in fruits[:]:
                    pts=fruit.slice(mx,my)
                    if pts>0:
                        if ssnd:ssnd.play()
                        multiplier=2 if double_score>0 else 1
                        ap=pts*multiplier;score+=ap;tfs+=1;combo+=1;ct=60
                        if combo>mc:mc=combo
                        coins+=1
                        if blade["eff"]=="gold":coins+=2
                        if blade["eff"]=="ice":
                            for f in fruits:
                                if not f.sliced and random.random()<0.3:f.frozen=True;f.ft=30
                        if combo%10==0:ss=12
                        if combo%10==0 and csnd:csnd.play()
                    elif pts<0:
                        if bsnd:bsnd.play()
                        tl=max(0,tl-15);ss=18
        elif event.type==MOUSEBUTTONUP:swiping=False;trail=[]
    if state==SPLASH:
        splash_timer-=1;gs.fill(BLACK);draw_splash(gs,splash_timer)
        if splash_timer<=0:state=MENU
    elif state==PLAYING:
        tl-=dt2
        if tl<=0:tl=0;state=GAMEOVER;sv()
        if double_score>0:double_score-=1
        if magnet_timer>0:magnet_timer-=1
        if slow_mo>0:slow_mo-=1
        game_speed=diff_mult*(0.5 if slow_mo>0 else 1.0)
        prog=1-(tl/GT);sd2=max(6,30-int(prog*24));fst+=1
        if fst>sd2:fst=0;fruits.append(Fruit(game_speed))
        if fst>sd2 and random.random()<prog*0.5:fruits.append(Fruit(game_speed))
        if random.random()<0.003:powerups.append(PowerUp())
        if ct>0:ct-=1
        else:combo=0
        if ss>0:ss-=1
        if dbtimer>0:dbtimer-=1
        for fruit in fruits[:]:
            fruit.update(magnet_timer)
            if not fruit.sliced and fruit.y>H+100:fruits.remove(fruit)
            elif fruit.sliced and all(p["life"]<=0 for p in fruit.sp):fruits.remove(fruit)
        for pu in powerups[:]:
            pu.update()
            if pu.y>H+100 or pu.life<=0:powerups.remove(pu)
            elif swiping and m.sqrt((pu.x-mx)**2+(pu.y-my)**2)<20:
                pu.collect()
                if pksnd:pksnd.play()
                powerups.remove(pu)
        for p in particles[:]:p["life"]-=1;p["x"]+=p["vx"];p["y"]+=p["vy"];p["vy"]+=0.1
        particles=[p for p in particles if p["life"]>0]
        for spk in SPARKS[:]:spk.update()
        SPARKS=[s for s in SPARKS if s.life>0]
        gs.fill(BLACK);dbg(gs)
        for fruit in fruits:fruit.draw(gs)
        for pu in powerups:pu.draw(gs)
        for p in particles:
            alpha=max(0,min(255,int(p["life"]*8)));c=p["color"];sz=max(1,int(p["size"]))
            pygame.draw.circle(gs,(c[0],c[1],c[2],alpha),(int(p["x"]),int(p["y"])),sz)
        for spk in SPARKS:spk.draw(gs)
        dbt(gs);dt(gs);dsb(gs)
        if ss>0:ox=random.randint(-ss,ss);oy=random.randint(-ss,ss);gs2=gs.copy();gs.fill(BLACK);gs.blit(gs2,(ox,oy))
        stxt=font.render("Score: "+str(score),True,WHITE);gs.blit(stxt,(10,10))
        gs.blit(sf.render("Sliced: "+str(tfs),True,WHITE),(10,38))
        gs.blit(sf.render("Coins: "+str(coins),True,GOLD),(10,58))
        if double_score>0:dtxt=sf.render("x2! "+str(int(double_score/60))+"s",True,GOLD);gs.blit(dtxt,(10,78))
        if magnet_timer>0:mtxt=sf.render("Magnet! "+str(int(magnet_timer/60))+"s",True,PINK);gs.blit(mtxt,(10,98))
        if slow_mo>0:stxt2=sf.render("Slow! "+str(int(slow_mo/60))+"s",True,CYAN);gs.blit(stxt2,(10,118))
        gs.blit(sf.render("Diff: "+diff_name,True,ORANGE),(W-120,60))
        if combo>1:
            ctxt=bfont.render("COMBO x"+str(combo)+"!",True,GOLD);ca=max(0,min(255,int((ct/60)*255)))
            cs2=pygame.Surface((ctxt.get_width(),ctxt.get_height()),SRCALPHA);cs2.blit(ctxt,(0,0));cs2.set_alpha(ca)
            gs.blit(cs2,(W//2-ctxt.get_width()//2,H//2))
        if tl<10 and tl>0:wt=bfont.render(str(int(tl))+"!",True,RED);gs.blit(wt,(W//2-wt.get_width()//2,H//2+50))
    elif state==GAMEOVER:
        gs.fill((18,10,45))
        if score>bs:bs=score
        gs.blit(bfont.render("TIME UP!",True,RED),(W//2-120,H//2-120))
        stats=["Score: "+str(score),"Best: "+str(bs),"Sliced: "+str(tfs),"Max combo: x"+str(mc),"Time: "+str(GT)+"s","Diff: "+diff_name]
        for i,t in enumerate(stats):gs.blit(font.render(t,True,WHITE),(W//2-90,H//2-60+i*30))
        gs.blit(font.render("Tap to continue",True,GOLD),(W//2-100,H//2+120))
    elif state==MENU:pb,diff_btn,sb=dm(gs)
    elif state==SETTINGS:bb=dst(gs)
    elif state==SHOP:bb,buy_btns=dsh(gs)
    sc.blit(pygame.transform.scale(gs,(SW,SH)),(0,0))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()