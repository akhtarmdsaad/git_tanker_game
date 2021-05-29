import pygame, math, time, random
from functools import partial
GREEN=(0,150,0)
BLACK=(0,0,0)
st=time.time()
factor=10
pygame.init()

FOntObj=pygame.font.Font(pygame.font.get_default_font(),50)
class Toast:
	def __init__(self,text,time_max=2,color=(255,0,0)):
		surfObj=FOntObj.render(str(text),1,color)
		self.surfObj=pygame.transform.rotate(surfObj,-90)
		self.surf_rect=self.surfObj.get_rect()
		self.surf_rect.center=50,675
		self.st=time.time()
		self.max_time=time_max
		self.alpha=255
		self.destroy=False
	def show(self,screen):
		screen.blit(self.surfObj,self.surf_rect)
		if time.time()-self.st>self.max_time:
			self.alpha-=3
			self.surfObj.set_alpha(self.alpha)
			if self.alpha<=0:
				self.destroy=True
		

fontObj=pygame.font.Font(pygame.font.get_default_font(),20)


def collide_rect(a,b):
	if a.top<b.top and a.top+a.height>b.top:
		if a.left<b.left and a.left+a.width>b.left:
			#a.left-=1
			#a.top-=1
			return True
		elif b.left<a.left and b.left+b.width>a.left:
			#a.left+=1
			#a.top-=1
			return True
	elif a.bottom>b.bottom and a.bottom-a.height<b.bottom:
		if a.left<b.left and a.left+a.width>b.left:
			#a.bottom+=1
			#a.left-=1
			return True
		elif b.left<a.left and b.left+b.width>a.left:
			#a.bottom+=1
			#a.left+=1
			return True
def distance(p,q):
	return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class Environment(pygame.sprite.Sprite):
	
	def __init__(self,x,y,width,height):
		super().__init__()
		self.rect=pygame.Rect(x,y,width,height)
		self.surf=fontObj.render(f"{x},{y}",1,(0,0,0))
		
	def show(self, screen):
		
		pygame.draw.rect(screen,GREEN,self.rect)
	
	def showrect(self,screen,ox,oy):
		pygame.draw.rect(screen,GREEN,self.rect.move(ox,oy))
		#screen.blit(self.surf,self.rect.move(ox,oy).topleft)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.rect(screen,GREEN,rect.move(ox,oy))
	
	
class Envx(Environment):
	def __init__(self,x,y,length):
		super().__init__(x,y,length,40)

class Envy(Environment):
	def __init__(self,x,y,height):
		super().__init__(x,y,40,height)

class Bar:
	def __init__(self,init_pos,length,color,name='',min=0,max=100,orient="horizontal"):
		self.pos=init_pos
		self.length=length
		self.color=color
		self.name=name
		self.max=max
		self.orient=orient
		self.width=5
		self.rect=pygame.Rect(*init_pos,self.length,10)
		self.reverse=None
		self.value=max
		if orient.startswith("v"):
			self.rect.width,self.rect.height=self.rect.height,self.rect.width
	
	def show(self,screen,ox,oy):
		pygame.draw.rect(screen,(0,0,0),(*self.rect.move(ox,oy).topleft,self.width,self.length),self.width//2)
		pygame.draw.rect(screen,self.color,self.rect.move(ox,oy))
	
	def dec(self,value):
		if value<0:
			self.inc(abs(value))
			return
		if self.orient.startswith("h"):
			self.rect.width-=value
			if self.rect.width<0:
				self.rect.width=0
		else:
			self.rect.height-=value
			if self.rect.height<0:
				self.rect.height=0
		self.value-=value
	
	def inc(self,value):
		if self.orient.startswith("h"):
			self.rect.width+=value
			if self.rect.width>self.max:
				self.rect.width=self.max
		else:
			self.rect.height+=value
			if self.rect.height>self.max:
				self.rect.height=self.max
		self.value+=value


class Button:
	def __init__(self,pos,image=None,shape="circle",text=''):
		self.pos=pos
		self.image=pygame.Surface((200,200),pygame.SRCALPHA)
		self.image.fill((0,0,200,150))
		if image:
			self.image=pygame.image.load(image)
		self.shape=shape
		self.color=(0,0,200)
		self.size=200	#or radius
		self.text=text
		self.font=pygame.font.Font(pygame.font.get_default_font(),30)

	def show(self, screen):
		if self.shape == "circle":
			#pygame.draw.circle(screen,(0,00,0),self.pos,self.size,2)
			pygame.draw.circle(screen,self.color,self.pos,self.size)
			screen.blit(pygame.transform.rotate(self.font.render(self.text,1,(0,0,0)),-90),(self.pos[0],self.pos[1]-self.size))
			#screen.blit(self.image,self.pos)
		else:
			pygame.draw.rect(screen,BLACK,(*self.pos,self.size,self.size))
	
	def clicked(self,x,y):
		return distance((x,y),self.pos)<self.size
			
class Health:
	def __init__(self,pos):
		self.image=pygame.image.load("health.png")
		self.pos=pos
		self.rect=self.image.get_rect()
		self.rect.center=self.pos
		self.value=random.randint(10,100)
		self.st=time.time()
	
	def showrect(self, screen,ox,oy):
		screen.blit(self.image,self.rect.move(ox,oy).topleft)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		screen.blit(self.image,rect.move(ox,oy).topleft)
	

class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,color=(0,00,0)):
		self.pos = list(pos)
		self.x,self.y = pos
		self.rect=pygame.Rect(*self.pos,20,20)
		self.fired = False
		self.img=self.rect.copy()
		self.speed=0.3
		self.st=time.time()
		self.mvst=time.time()
		self.xchange=random.choice([1,-1])*self.speed*random.randint(1,3)
		self.ychange=random.choice([1,-1])*self.speed*random.randint(1,3)
		self.health=100
		self.bar=Bar(self.pos,self.health,(200,0,0),name="Health",max=self.health,orient="v")
		_gun=random.choice(list(gun.values()))()
		if self.pos[1]<=1800:
			while _gun.name=="2m249":
				_gun=random.choice(list(gun.values()))()
		self.surf=pygame.transform.rotate(fontObj.render(_gun.name,1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		self.gun=_gun
		self.pehchan=self.gun.name
		self.color=color
		
	def show(self,screen):
		self.bar.show(screen)
		pygame.draw.rect(screen,(0,0,0),self.img)
		

	def showrect(self,screen,ox,oy):
		screen.blit(self.surf,self.surf_rect.move(ox,oy))
		self.bar.show(screen,ox,oy)
		pygame.draw.rect(screen,self.color,self.img.move(ox,oy))

	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.img.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.rect(screen,self.color,rect.move(ox,oy))


	def move(self,env):
		if self==env:
			return
		if time.time()-self.mvst>2:
			self.mvst=time.time()
			self.xchange=random.choice([1,-1])*self.speed*random.randint(0,2)
			self.ychange=random.choice([1,-1])*self.speed*random.randint(0,2)
		self.pos[0]+=self.xchange
		self.pos[1]+=self.ychange
		if env.rect.collidepoint(*self.pos): # or env.rect.collidepoint(*self.rect.bottomleft) or env.rect.collidepoint(*self.rect.topright) or env.rect.collidepoint(*self.rect.bottomright):# or self.pos[0]>700 or self.pos[0]<50 or self.pos[1]>1250 or self.pos[1]<50:
			self.xchange*=-1
			self.ychange*=-1
			self.pos[0]+=self.xchange
			self.pos[1]+=self.ychange
		self.img.topleft=tuple(self.pos
		)
		self.bar.rect.centery=self.img.centery
		self.bar.rect.centerx=self.img.centerx+10
		self.surf_rect.centery=self.img.centery
		self.surf_rect.centerx=self.img.centerx+20

	def fire(self,pos1):
		x,y=pos1
		x-=self.pos[0]
		y-=self.pos[1]
		if x==0:
			x=0.000000001
		angle=math.atan(y/x)
		if x<0:
			angle+=math.radians(180)
		return self.gun.fire(self.pos,math.degrees(angle),self.pehchan if self.pehchan else "enemy")

class GunContainer:
	def __init__(self,pos,gun):
		self.pos=pos
		self.rect=pygame.Rect(*pos,40,40)
		self.gun=gun
		self.surf=pygame.transform.rotate(fontObj.render(self.gun.name,1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		self.surf_rect.center=self.rect.center
		self.btn=Button((50,650),text="change")
		self.btn.size=40
		self.collide=False
	
	def showrect(self,screen,ox,oy):
		pygame.draw.rect(screen,(130,60,0),self.rect.move(ox,oy))
		screen.blit(self.surf,self.surf_rect.move(ox,oy))
	
	def on_collide(self,screen):
		self.btn.show(screen)
		self.collide=True
		return True
	
	def gun_changed(self):
		self.surf=pygame.transform.rotate(fontObj.render(self.gun.name,1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		self.surf_rect.center=self.rect.center
		
		
	def show_min_rect(self,screen,ox,oy,padx,pady):
		pass
	
class Gun:
	def __init__(self,damage,speed,_time,max=30,rd=1,name='',mass=10):
		self.damage=damage
		self.fire_time=_time
		self.max_bullets=max
		self.available_bullets=self.max_bullets
		self.st=time.time()
		self.reload_time=rd
		self.reload_st=time.time()
		self.name=name
		self.bullet_speed=speed
		self.mass=mass
	
	def fire(self,pos,angle,pehchan):
		if self.available_bullets<=0 :
				if not self.reload_st:
					self.reload_st=time.time()
				self.reload()
				return
		if time.time()-self.st>self.fire_time:
			self.st=time.time()
			self.available_bullets-=1
			return Bullet(pos,angle,self.damage,pehchan,speed=self.bullet_speed)
		return None
	
	def reload(self,enemy=True):
		
		if time.time()-self.reload_st>self.reload_time:
			self.available_bullets=self.max_bullets
			self.reload_st=None
		

class Player(pygame.sprite.Sprite):
		
		def __init__(self,pos):
			super().__init__()
			self.pos=list(pos)
			#self.rect=pygame.Rect(*pos,30,20)
			self.image=pygame.transform.scale(pygame.image.load("saad.png"),(40,40))
			self.rect=self.image.get_rect()
			self.rect.topleft=self.pos
			self.st=time.time()
			self.angle=0
			self.gun=gun["hand"]()
			self.bomb_thrown=False
			self.rotatedImage=self.image
			self.health=100
			self.lives=3
			self.deaths=0
			self.mass=70
			
			
		def show(self,screen):
			#pygame.draw.rect(screen,BLACK,self.rect)
			self.rotatedImage=pygame.transform.rotate(self.image,self.angle)
			screen.blit(self.rotatedImage,tuple(self.pos))
			

		def showrect(self,screen,ox,oy):
			self.rotatedImage=pygame.transform.rotate(self.image,self.angle)
			screen.blit(self.rotatedImage,self.rect.move(ox,oy).topleft)
			self.surf=pygame.transform.rotate(fontObj.render(self.gun.name,1,(0,0,0)),-90)
			self.surf_rect=self.surf.get_rect()
			self.surf_rect.center=(self.rect.centerx+20,self.rect.centery)
			screen.blit(self.surf,self.surf_rect.move(ox,oy))
		
		
		def hit(self, damage):
			self.health-=damage
		
		def show_min_rect(self,screen,ox,oy,px,py):
			rect=self.rect.copy()
			rect.width/=factor
			rect.height/=factor
			rect.left/=factor
			rect.top/=factor
			rect.left+=px
			rect.top+=py
			pygame.draw.rect(screen,(0,0,200),rect)
			#screen.blit(self.rotatedImage,rect.move(ox,oy).topleft)

		def updateMove(self,movex,movey):
			self.rect.left+=movex
			self.rect.top+=movey
			self.pos=list(self.rect.topleft)
		
		def get_component(self,force,angle):
			x=force/(self.mass+self.gun.mass)*math.cos(math.radians(angle))
			y=force/(self.mass+self.gun.mass)*math.sin(math.radians(angle))
			return x,y
		
		def fire(self,angle):
			if time.time()-self.st>0.2 and self.gun.available_bullets:
				return self.gun.fire(self.rect.center,angle,"player")
		
		def reset(self,died=True):
			#return	#uncomment in developer mode
			print("You got knocked out")
			self.pos=[100,50]
			self.rect.topleft=self.pos
			if died:
				self.lives-=1
				self.deaths+=1
			self.health=100
			self.gun.available_bullets=self.gun.max_bullets
class Mines:
	def __init__(self,pos):
		self.pos=pos
		self.range=50
		self.radius=10
		self.bombDistance=800
		self.blastlength=self.bombDistance//2
		self.blasted=False
		self.st=None
		self.blastTime=0.5
		self.rect=pygame.Rect(*self.pos,10,10)
	
	def showrect(self,screen,ox,oy):
		pygame.draw.circle(screen,(200,0,0),self.rect.move(ox,oy).topleft,self.radius)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		return
	
	def blasting(self,screen,ox,oy):
		return pygame.Rect(self.pos[0]-self.blastlength//2,self.pos[1]-self.blastlength//2,self.blastlength,self.blastlength)
	
	def blast(self):
		if not self.blasted:
			self.st=time.time()
		self.blasted=True
		

class Bomb:
	
	def __init__(self,pos,angle,name):
		self.pos=list(pos)
		self.angle=angle
		self.thrownBy=name
		self.radius=5
		self.bombDistance=800
		self.st=time.time()
		self.blastlength=self.bombDistance//2
		self.to_reach=[self.pos[0]-self.bombDistance*math.sin(angle),self.pos[1]-self.bombDistance*math.cos(angle)]
		self.blasted=False
		self.diffx=self.to_reach[0]-self.pos[0]
		self.diffy=self.to_reach[1]-self.pos[1]
		self.blastTime=0.5
		self.rect=pygame.Rect(*self.pos,10,10)
	
	def show(self,screen):
		pygame.draw.circle(screen,(0,0,200),self.rect.topleft,self.radius)
	
	def showrect(self,screen,ox,oy):
		pygame.draw.circle(screen,(0,0,200),self.rect.move(ox,oy).topleft,self.radius)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.circle(screen,(0,0,200),rect.move(ox,oy).topleft,self.radius/factor)
	
	
	def fire(self,screen):
		self.diffx=self.to_reach[0]-self.pos[0]
		self.diffy=self.to_reach[1]-self.pos[1]
		self.pos[0]+=self.diffx/100
		self.pos[1]+=self.diffy/100
		self.rect.topleft=self.pos
		self.st=time.time()
		#self.show(screen)
	
	def blasting(self,screen,ox,oy):
		return pygame.Rect(self.pos[0]-self.blastlength//2,self.pos[1]-self.blastlength//2,self.blastlength,self.blastlength)
		pygame.draw.rect(screen,(200,200,0),rect.move(ox,oy))
	
	def blastingoffset(self,screen,ox,oy):
		rect=pygame.Rect(self.pos[0]-self.blastlength//2,self.pos[1]-self.blastlength//2,self.blastlength,self.blastlength)
		pygame.draw.rect(screen,(200,200,0),rect.move(ox,oy))
		return rect
	
	def blast(self):
		self.blasted=True
		self.damaged=[]
	
class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,angle,damage,pehchan='',speed=20):
		super().__init__()
		self.pehchan = pehchan
		self.pos=pos
		self.image=pygame.image.load("bullet.png")
		self.rect=self.image.get_rect()
		self.speed=speed
		self.rotatedImage=self.image
		self.angle=math.radians(270-angle)
		assert type(damage)==type(5),"Damage should be integer"
		self.damage=damage

	def fire(self,screen):
		x,y=self.pos
		x-=self.speed*math.sin(self.angle)
		y-=self.speed*math.cos(self.angle)
		self.rect.topleft=(x,y)
		self.rotatedImage=pygame.transform.rotate(self.image,math.degrees(self.angle))
		self.pos=[x,y]
		#self.show(screen)
		
	def show(self,screen):
		screen.blit(self.rotatedImage,self.rect.center)
	
	def showrect(self,screen,ox,oy):
		screen.blit(self.rotatedImage,self.rect.move(ox,oy).center)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		return
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.rect(screen,GREEN,rect.move(ox,oy))
	
class Joystick:
	
	def __init__(self,pos,size=30):
		self.pos=pos
		self.joypos=pos
		self.size=size
		self.dist=self.size*4
		self.temp_dist=0
		
	def draw(self,screen):
		RED=(255,0,0)
		BLACK=(0,0,0)
		pygame.draw.circle(screen,RED,self.joypos,self.size)
		pygame.draw.circle(screen,BLACK,self.pos,self.size*4,10)
		#print("show",self.joypos)
		
	def getPos(self,x,y):
		''' returns tuple of (distance,direction)
		angle in degrees '''
		l=pygame.mouse.get_pressed()[0]
		a=b=theta=0
		if l==1:
			x-=self.pos[0]
			y-=self.pos[1]
			if x==0:
				x=0.000000001
			self.temp_dist=distance(self.pos,(x+self.pos[0],y+self.pos[1]))
			if self.temp_dist>self.dist:
				self.temp_dist=self.dist
			theta=math.atan(y/x)
			if x<0:
				theta+=math.radians(180)
			a=self.pos[0]+self.temp_dist*math.cos(theta)
			b=self.pos[1]+self.temp_dist*math.sin(theta)
			self.joypos=(a,b)
			#print("func",a,b)
		else:
			self.joypos=self.pos
		return (self.temp_dist//10,math.degrees(theta))
	
	def reset(self):
		self.joypos=self.pos
	
	def clicked(self,x,y):
		return distance((x,y),self.pos)<self.dist

def create_gun(a,b,c,d,e,name,mass):
	assert b<40,"speed less than 30"
	return Gun(a,b,c,d,e,name,mass=mass)
gun={
	#gun parameters - damage, speed, fire time, total bullets, reload time, name to show,mass
	"m249":partial(create_gun,10,25,0.05,100,5,'m249',30),
	"m416":partial(create_gun,15,25,0.1,30,1,"m416",5),
	"shotgun":partial(create_gun,100,15,1,2,2,"shotgun",10),
	"m762":partial(create_gun,20,15,0.1,40,1,"m762",15),
	"slr":partial(create_gun,30,15,0.5,10,2,"slr",7),
	"2m249":partial(create_gun,10,29,0.001,500,20,"2m249",50),
	"hand":partial(create_gun,0,0,0,0,0,"hand",0),
	"saad special":partial(create_gun,30,25,0.001,1000,3,"saad's gun",70)
}
