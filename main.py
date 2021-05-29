try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass
import math, random
from pygame.locals import *
from players import *
from settings import *


pygame.init()
screen=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()

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
all_rects=[]
def update_all_rect():
	global all_rects
	all_rects=(env_list+[p]+bullets+bombs+bomb_rect+enemies+supporters+gun_container+mines+mines_rect+[health] if health else [])
def draw_all_rects(rects,cam,p):
	global rmain
	ox=-cam.centerx+screenX/2
	oy=-cam.centery+screenY/2
	for obj in rects:
		#if rmain.colliderect(obj.rect.move(ox,oy)):
			if isinstance(obj,pygame.Rect):
				if not distance(obj.center,p.rect.center) < 20:
					pygame.draw.rect(screen,(255,255,0),obj.move(ox,oy))
				else:
					pygame.draw.rect(screen,(0,150,25),obj.move(ox,oy),5)
				
			else:
				obj.showrect(screen,ox,oy)
	return -p.rect.centerx+screenX/2,-p.rect.centery+screenY/2
		

#Environment
environment=pygame.sprite.Group()
env_list=[
	Envx(0,0,1400),
	Envx(0,2800,1400),
	Envy(0,0,2800),
	Envy(1400,0,2800+40),
	Envy(700,0,600),
	Envx(0,200,500),
	Envx(500,700,700),
	Envy(500,700,500),
	Envy(800,1100,600),
	Envx(800,1700,400),
	Envx(1100,1200,1400-1100),
	Envx(350,1400,800-350),
	Envy(500,1800,2200-1800),
	Envx(0,2200,900),
	Envx(1100,2200,1400-1100),
	Envy(700,2400,400)

]


#player
p=Player((100,50))
p.gun=gun["slr"]()
all_rects.append(p)
move_speed=move_angle=0
fire_speed=fire_angle=0
p.angle=270-fire_angle
p.lives=float("inf")
update_x=update_y=True

#bullets
bullets=[]

#bomb
bombs=[]
bomb_rect=[]
damaged=[]

#mines
mines=[]
mines_rect=[]
x,y=300,400

for i in range(0):
		mines.append(Mines((random.randint(500,1400),random.randint(500,2400))))

#joysticks and buttons
j1=Joystick((150,150))
j2=Joystick((150,screenY-150),25)
bomb_btn=Button((600,400),text="bomb")
bomb_btn.size=100
reload_btn=Button((660,screenY-60),text="reload")
reload_btn.size=70
shield_btn=Button((100,screenY-600),text="shield")
shield_btn.size=70
scroll_but=Button((screenX-100,600),text="Scroll")
scroll_but.size=40
show_joystick=False

#shield
shield=None
shield_st=time.time()
shield_time=10

#my stuffs
for i in env_list:
	#environment.add(i)
	all_rects.append(i)
	pass
fingerJoy1=fingerJoy2=None

def collide(p,q,pos=True):
	if not pos:
		a,b=p.center
	else:
		a,b=p.pos
	x,y=q.pos
	if math.sqrt((a-x)**2+(b-y)**2)<20:
		return True
def distance(pos1,pos2):
	x,y=pos1
	a,b=pos2
	
	return math.sqrt((x-a)**2+(y-b)**2)
# Enemy
enemies = []
noOfEnemies = 35
enemyFireTime = 0.5
enemyst=time.time()
def genEn(i,max_x,max_y):
	while i > 0:
		s = Enemy((random.randint(20, max_x), random.randint(250, max_y)))
		#for env in environment:
		for env in env_list:
			if env.rect.colliderect(s.rect):
				continue
		i -= 1
		enemies.append(s)
		all_rects.append(s)
#player supporter
supporters=[]
noOfSup=0
def genSup(i,max_x,max_y):
	while i > 0:
		s = Enemy((random.randint(20, max_x), random.randint(250, max_y)),color=(0,0,150))
		#for env in environment:
		for env in env_list:
			if env.rect.colliderect(s.rect):
				continue
		i -= 1
		s.pehchan="player"
		supporters.append(s)
		all_rects.append(s)

genSup(noOfSup,400,400)
#health
def genHealth():
	h=Health((random.randint(1,1290),random.randint(1,2700)))
	all_rects.append(h)
	return h
health=genHealth()
healthDisappTime=25
healthComeTime=5
h_st=time.time()


def genEn(i,max_x,max_y):
	while i > 0:
		s = Enemy((random.randint(20, max_x), random.randint(250, max_y)))
		for env in environment:
			if env.rect.colliderect(s.rect):
				continue
		i -= 1
		enemies.append(s)
		all_rects.append(s)
genEn(noOfEnemies,1200,2600)
camera=pygame.Rect(*p.pos,screenX,screenY)
cx,cy=camera.center
cam_speed=80
rmain=pygame.Rect(0,0,screenX,screenY)
restart=False
#text
fontObj=pygame.font.Font(pygame.font.get_default_font(),30)
#p.lives=noOfEnemies//10
reloading=False
#p.gun.reload_time=3
def showMiniMap(rects):
	padx=550
	pady=10
	global rmain
	#ox=-cam.centerx+screenX/2
#	oy=-cam.centery+screenY/2
	ox=oy=0
	for obj in rects:
		#if rmain.colliderect(obj.rect.move(ox,oy)):
			#print(obj)
			if isinstance(obj,pygame.Rect):
				pass
			else:
				obj.show_min_rect(screen,ox,oy,padx,pady)
shakeright=True
gun_container=[]
g=gun["m416"]()
g.available_bullets=0
gun_container.append(GunContainer((200,500),g))
#gun_container.append(GunContainer((900,500),gun["m762"]()))
#gun_container.append(GunContainer((200,1700),gun["2m249"]()))
#gun_container.append(GunContainer((900,1800),gun["m249"]()))
#gun_container.append(GunContainer((900,2300),gun["slr"]()))
#gun_container.append(GunContainer((200,900),gun["shotgun"]()))
def contain_gun(pos,gun):
	g=GunContainer(pos,gun)
	gun_container.append(g)
	all_rects.append(g)
for ab in gun_container:
	all_rects.append(ab)
	pass
toast=None
update_all_rect()
scrolling=False
while True:
	try:
		screen.fill((125,125,125))
		if health:
			if time.time()-health.st>healthDisappTime:
				all_rects.remove(health)
				health=None
				h_st=time.time()
		else:
			if time.time()-h_st>healthComeTime:
				health=genHealth()
		#pygame.draw.rect(screen,BLACK,rmain,5)
		#r.topleft=p.rect.center
		#for i in environment:i.show(screen)
		
		if not scrolling:
			if camera.centerx<p.rect.centerx:
				camera.centerx+=(p.rect.centerx-camera.centerx)/1000*cam_speed
			elif camera.centerx>p.rect.centerx:
				camera.centerx-=-(p.rect.centerx-camera.centerx)/1000*cam_speed
			if camera.centery<p.rect.centery:
				camera.centery+=(p.rect.centery-camera.centery)/1000*cam_speed
			elif camera.centery>p.rect.centery:
				camera.centery-=-(p.rect.centery-camera.centery)/1000*cam_speed
		ofx,ofy=draw_all_rects(all_rects,camera,p)
		for s in bullets:
			s.fire(screen)
		if show_joystick:
			j1.draw(screen)
			j2.draw(screen)
		bomb_btn.show(screen)
		reload_btn.show(screen)
		shield_btn.show(screen)
		scroll_but.show(screen)
		#show_shield()
		
		if shield and time.time()-shield_st>shield_time:
			all_rects.remove(shield)
			shield=None
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit(0)
			if event.type==FINGERDOWN:
				x,y=event.x*screenX,event.y*screenY
				#print(x,y)
				show_joystick=True
				if y<365 and x<500:
					j1.pos=(x,y)
				if y>910 and x<500:
					j2.pos=(x,y)
				if not shield and bomb_btn.clicked(x,y):
					#if not p.bomb_thrown:
						bomb=Bomb(p.rect.center,math.radians(p.angle),'player')
						if len(bombs)<=3:
							bombs.append(bomb)
							all_rects.append(bomb)
							p.bomb_thrown=True
				if reload_btn.clicked(x,y) and not reloading and p.gun.available_bullets!=p.gun.max_bullets:
						reloading=True
						reload_btn.color=(200,0,0)
						p.gun.reload_st=time.time()
				if shield_btn.clicked(x,y) and not shield and time.time()-shield_st>20:
					shield=pygame.Rect(0,0,p.rect.width*3,p.rect.height*3)
					shield.center=p.rect.center
					shield_st=time.time()
					all_rects.append(shield)
				if scroll_but.clicked(x,y):
					scrolling=not scrolling
					if scroll_but.color!=(200,00,0):
						scroll_but.color=(200,0,0)
					else:
						scroll_but.color=(0,0,200)
				#gun change
				for ab in gun_container:
					if ab.collide and ab.btn.clicked(x,y):
						ab.gun,p.gun=p.gun,ab.gun
						ab.gun_changed()
				if j1.clicked(x,y):
					if not fingerJoy1:	#if finger Joy 1 is None
						fingerJoy1=event
				elif j2.clicked(x,y):
					if not fingerJoy2:
						fingerJoy2=event
				
			if event.type==FINGERMOTION:
				x,y=event.x*screenX,event.y*screenY
				if scrolling:
					camera.centerx-=event.dx*screenX
					camera.centery-=event.dy*screenY
					continue
				if fingerJoy2 and fingerJoy2.finger_id==event.finger_id:
					fire_speed,fire_angle=j2.getPos((event.x)*screenX,(event.y)*screenY)
					p.angle=270-fire_angle
				if fingerJoy1 and fingerJoy1.finger_id==event.finger_id:
					move_speed,move_angle=j1.getPos((event.x)*screenX,(event.y)*screenY)
					update_x=update_y=True
				
					
			if event.type==FINGERUP:
				x,y=event.x*screenX,event.y*screenY
				#print("Fingerup",event)
				show_joystick=True
				if fingerJoy1:
					if fingerJoy1.finger_id==event.finger_id:
						fingerJoy1=None
				if fingerJoy2:
					if fingerJoy2.finger_id==event.finger_id:
						fingerJoy2=None
		if not fingerJoy1:
			move_speed=move_angle=0
			j1.reset()
		if not fingerJoy2:
			fire_speed=0
			j2.reset()
		
		#my extra stuffs like harding the level
		if p.rect.bottom>2200 and p.gun.name!="slr":
			contain_gun(p.rect.center,p.gun)
			p.gun=gun["slr"]()
			toast=Toast("Your gun changed to slr",color=(0,200,0))
		
		
		#player fire
		if fire_speed>=60//10:
			if p.gun.available_bullets!=0 and reloading:
				reloading=False
				reload_btn.color=(0,0,200)
			_bullet=p.fire(fire_angle) if not shield else None
			if isinstance(_bullet,Bullet):
				bullets.append(_bullet)
				all_rects.append(_bullet)
			if p.gun.available_bullets==0 and p.gun.name!="hand":
				reloading=True
				reload_btn.color=(200,0,0)
				p.gun.reload_st=time.time()
		#handle mines
		for m in mines:
			for en in enemies+supporters+[p]:
				if distance(m.pos,en.pos)<m.range:
					m.blast()
					for i in all_rects:
						pass
			if m.blasted:
				r=m.blasting(screen,ofx,ofy)
				if r not in mines_rect:
					mines_rect.append(r)
					all_rects.append(r)
				if shakeright:
					camera.centerx+=50
					camera.centery+=30
				else:
					camera.centerx-=30
					camera.centery-=50
				shakeright=not shakeright
				for en in enemies:
					if r.collidepoint(en.pos):
						en.health-=50
						if en.health<=0:
							toast=Toast("Killed in mines:"+str(noOfEnemies-len(enemies))+f",enem-{en.gun.name}")
							contain_gun(en.pos,en.gun)
							enemies.remove(en)
							all_rects.remove(en)
							if len(enemies)<=0:
								genEn(noOfEnemies,1200,2600)
								p.reset(died=False)
								supporters=[]
								genSup(noOfSup,400,400)
				for en in supporters:
					if r.collidepoint(en.pos):
						en.health-=50
						if en.health<=0:
							supporters.remove(en)
							contain_gun(en.pos,en.gun)
							all_rects.remove(en)
				if r.collidepoint(p.pos):
					p.health-=50
					if p.health<=0:
						p.reset()
				if time.time()-m.st>m.blastTime:
					mines.remove(m)
					mines_rect.remove(r)
					all_rects.remove(m)
					all_rects.remove(r)
					print("removed")
					
				
		#handle bombs
		for b in bombs:
			if distance(b.pos,b.to_reach)<30:
				b.blast()
			#for env in environment:
			for env in env_list:
				if env.rect.collidepoint(*b.pos):
					b.blast()
			if b.blasted:
				factor=1
				r=b.blasting(screen,ofx,ofy)
				if r not in bomb_rect:
					bomb_rect.append(r)
					all_rects.append(r)
				if shakeright:
					camera.centerx+=50
					camera.centery+=30
				else:
					camera.centerx-=30
					camera.centery-=50
				shakeright=not shakeright
				for en in enemies:
					if r.collidepoint(en.pos) and en not in b.damaged:
						b.damaged.append(en)
						en.health-=factor*50/distance(en.pos,r.center)+50
						if en.health<=0:
							toast=Toast("Killed:"+str(noOfEnemies-len(enemies))+f",enem-{en.gun.name}")
							contain_gun(en.pos,en.gun)
							enemies.remove(en)
							all_rects.remove(en)
							if len(enemies)<=0:
								genEn(noOfEnemies,1200,2600)
								p.reset(died=False)
								supporters=[]
								genSup(noOfSup,400,400)
				for en in supporters:
					if r.collidepoint(en.pos) and en not in b.damaged:
						b.damaged.append(en)
						en.health-=factor*50/distance(en.pos,r.center)+50
						if en.health<=0:
							supporters.remove(en)
							contain_gun(en.pos,en.gun)
							all_rects.remove(en)
				if r.collidepoint(p.pos) and p not in b.damaged:
					b.damaged.append(p)
					p.health-=factor*50/distance(en.pos,r.center)+50
					if p.health<=0:
						p.reset()
				if time.time()-b.st>b.blastTime:
					bombs.remove(b)
					bomb_rect.remove(r)
					all_rects.remove(b)
					all_rects.remove(r)
					p.bomb_thrown=False
			else:
				b.fire(screen)
		
		#reloading bullets
		if reloading and time.time()-p.gun.reload_st>p.gun.reload_time:
			p.gun.available_bullets=p.gun.max_bullets
			reloading=False
			p.gun.reload_st=time.time()
			reload_btn.color=(0,0,200)
		
		for en in enemies:
			#en.show(screen)
			#if distance(en.pos,p.pos) < 800:
			if True:
				#for env in environment:
				for env in env_list:
					en.move(env)
			if not en.fired:
				if distance(en.pos,p.pos) < 700:
					en_bullet=en.fire(p.pos)
					if en_bullet:
						bullets.append(en_bullet)
						all_rects.append(en_bullet)
						en.fired = True
			if time.time()-en.st>en.gun.fire_time:
				en.fired = False
				en.st=time.time()
		
		#supporters fire
		for en in supporters:
			#for env in environment:
			for env in env_list+enemies+supporters:
				en.move(env)
			
			disp=float("inf")
			for enemy in enemies:
				dist=distance(en.pos,enemy.pos)
				if dist < disp:
					disp=dist
					to_kill=enemy
			if not en.fired:
				if distance(en.pos,to_kill.pos) < 300:
					en_bullet=en.fire(to_kill.pos)
					#en_bullet.pehchan=en.gun.name
					if en_bullet:
						bullets.append(en_bullet)
						all_rects.append(en_bullet)
						en.fired = True
			if time.time()-en.st>en.gun.fire_time:
				en.fired = False
				en.st=time.time()
	
		#collision - bomb and enemy
		for b in bombs:
			for en in enemies:
				if collide(b,en):
					b.blast()
		#collision bomb and supporter
		for b in bombs:
			for en in supporters:
				if collide(b,en):
					b.blast()
		#collision player and health
		if health and p.rect.colliderect(health.rect):
			p.health+=health.value
			if p.health>100:
				p.health=100
			all_rects.remove(health)
			health=None
			h_st=time.time()
			
		#collision gun container and player
		for ab in gun_container:
			if p.rect.colliderect(ab.rect):
				ab.on_collide(screen)
			else:
				ab.collide=False
		
		
		#collision check for bullets and env
		#for env in environment:
		for env in env_list:
			for bullet in bullets:
				if collide_rect(env.rect,bullet.rect):
					bullets.remove(bullet)
					all_rects.remove(bullet)
		
		#collision - bullet and enemy
		for en in enemies:
			for b in bullets:
				if collide(en,b) and b.pehchan=="player":
					bullets.remove(b)
					all_rects.remove(b)
					en.health-=b.damage
					en.bar.dec(b.damage)
					if en.health<0:
						enemies.remove(en)
						toast=Toast("Killed:"+str(noOfEnemies-len(enemies))+f",enem-{en.gun.name}")
						contain_gun(en.pos,en.gun)
						all_rects.remove(en)
					if len(enemies)==0:
						genEn(noOfEnemies,1200,2600)
						p.reset(died=False)
						genSup(noOfSup,400,400)
						supporters=[]
						for obj in all_rects:
							if isinstance(obj,Bullet):
								all_rects.remove(obj)
								pass
		#collision bullet and supporter
		for en in supporters:
			for b in bullets:
				if collide(en,b) and b.pehchan=="enemy":
					bullets.remove(b)
					all_rects.remove(b)
					en.health-=b.damage
					en.bar.dec(b.damage)
					if en.health<0:
						supporters.remove(en)
						contain_gun(en.pos,en.gun)
						all_rects.remove(en)
		
		
		#collision - bullet and player
		if not shield:
			for b in bullets:
				if collide(b,p) and b.pehchan!="player":
					bullets.remove(b)
					all_rects.remove(b)
					p.hit(b.damage)
					if p.health<=0:
						if p.lives<0:
							exit(0)
						p.reset()
						toast=Toast("You were killed by:"+str(b.pehchan),color=(0,160,160))
				#p.reset(b.damage)
		else:
			shield.center=p.rect.center
		
		#collision for player and env
		if move_speed:
			movex,movey=p.get_component(move_speed*100,move_angle)
			#for env in environment:
			for env in env_list:
				if env.rect.collidepoint(p.rect.centerx,p.rect.top):
					if movey<0:movey=0
				elif env.rect.collidepoint(p.rect.centerx,p.rect.bottom):
					if movey>0:movey=0
				elif env.rect.collidepoint(p.rect.left,p.rect.centery):
					if movex<0:movex=0
				elif env.rect.collidepoint(p.rect.right,p.rect.centery):
					if movex>0:movex=0
			p.updateMove(movex,movey)
		screen.blit(fontObj.render("enemies:"+str(len(enemies)),1,BLACK),(10,200))
		screen.blit(fontObj.render("health:"+str(p.health),1,BLACK),(10,100))
		screen.blit(fontObj.render("bullets:"+str(p.gun.available_bullets),1,BLACK),(10,0))
		screen.blit(fontObj.render("deaths:"+str(p.deaths),1,BLACK),(300,0))
		screen.blit(fontObj.render("sup:"+str(len(supporters)),1,BLACK),(400,100))
		
		showMiniMap(all_rects)
	
		#assert len(bullets)<52,"bullet length"
		#clock.tick(30)
		if toast:
			toast.show(screen)
			if toast.destroy:
				toast=None
		pygame.display.flip()
	except ValueError:
		pass
	except Exception as e:
		print(e)
		p.reset(died=False)
		
		

		
		
		