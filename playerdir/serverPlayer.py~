#John F. Lake, Jr. & James Bowyer
#Final Project
#Shooter Platforming Game

#This is the file that should be run first.  This is the "server" player, who is red. 

import pygame
import math
import sys
from datetime import datetime
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import cPickle as pickle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#Data Protocol
class Data(LineReceiver):
	#Now we can send data:
	def connectionMade(self):
		gs.areConnected()

	#Get and interpret data sent from the other player: 
	def dataReceived(self,data):
		d = pickle.loads(data)	
		if type(d) is pygame.Rect:
			gs.moveEnemy(d)
		else:
			if d['message'] == "makeBullet":
				gs.makeBullet(d)
			elif d['message'] == "deleteBullet":
				gs.deleteBullet(d['b_x'])
			elif d['message'] == "deletePlayer":
				gs.deleteEnemy()

	#Send data along data connection
	def sendData(self,arg):
		self.sendLine(arg)

	

#Factory for Data connection
class DataFactory(Factory):
	def __init__(self):
		self.prot = Data()
	def buildProtocol(self, addr):
		return self.prot
	def getProt(self):
		return self.prot



class Bullet(pygame.sprite.Sprite):
	def __init__(self,gs=None,posX=0,posY=0,fac=0):
		#Initialize the sprite, sound, and images:
		gs.bullet = self
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("laser.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(posX,posY)

		#Laser movement: 
		self.location = self.rect
		self.velX = 7
		if fac:
			self.velX = -7
	def tick(self):
		self.rect = self.rect.move(self.velX,0)
		#code to kill bullet once off screen
		if (self.rect.right > 1000 or self.rect.left < -1000 or self.rect.top > 1000 or self.rect.bottom < -1000):
			del self

class Wall(pygame.sprite.Sprite):
	#We use types of walls to determine collision results
	#left = 1
	#top = 2
	#right = 3
	#down = 4
	#platform = 5
	def __init__(self, gs=None, x_pos=0, y_pos=0,type=5,dir=0):
		#Initialize the sprite, sound, and images:
		gs.wall = self
		self.type = type
		self.dir = dir
		self.yPos = y_pos
		pygame.sprite.Sprite.__init__(self)
		try:
			self.image = pygame.image.load("images/wall.png")
		except:
			print 'An error has occurred while the game was rendering the wall images.'
			raw_input('Press [ENTER] to exit')
			exit(0)
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x_pos, y_pos)
	def tick(self):
		if self.type == 5:
			#move back and forth:
			if self.dir:
				#move left:
				self.rect = self.rect.move(1,0)
			else:
				#move right:
				self.rect = self.rect.move(-1,0)
			if self.rect.right >= SCREEN_WIDTH-self.rect.width:
				self.dir = 0
			elif self.rect.left == self.rect.width:
				self.dir = 1

#Player class: 
class Player(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		#Initialize the sprite, and images:
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/redBlock2.png")
		self.gs = gs
		self.bullets = 3
		self.reloadDelay = 0
		self.health = 5
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(50,SCREEN_HEIGHT-self.rect.h)
		self.facing = 0
		self.left = 0
		self.right = 0
		self.up = 0
		self.down = 0
		self.canJump = 1

		#Location/velocity of the red player:
		self.location = self.rect
		self.gravity = 1
		self.velX = 0
		self.velY = 0


	#If you jump, just set your velocity to be 20 upwards
	def jump(self):
		self.velY = -20
		self.canJump = 0

	def containWithinBorder(self):
		l = self.rect
		if l.x <= 0:
			l.x = 0
		if l.y <= 0:
			l.y = 0 
		if l.y >= SCREEN_HEIGHT-self.rect.h:
			l.y = SCREEN_HEIGHT-self.rect.h
		if l.x >= SCREEN_WIDTH-self.rect.w:
			l.x = SCREEN_WIDTH-self.rect.w

	#Move through all of the walls and platforms and check if you collide with any of them
	def collideWalls(self):
		for wall in gs.wall_list:
		    if self.rect.colliderect(wall.rect):	
			#Depending on the type of wall, react accordingly
			if wall.type == 5:
				if self.velY <0:
					self.rect.top = wall.rect.bottom+1
				else:
					self.rect.bottom = wall.rect.top-1
					self.canJump = 1
				self.velY = 0
			elif wall.type == 1:
				self.rect.left = wall.rect.right+1
			elif wall.type == 2:
				self.rect.top = wall.rect.bottom+1
				self.velY = 0
			elif wall.type == 3:
				self.rect.right = wall.rect.left-1
			elif wall.type == 4:
				self.rect.bottom = wall.rect.top-1
				self.velY = 0
				self.canJump = 1


	#Move through all of the bullets and check if you collide with any of them
	def collideBullets(self):
		for b in gs.bullet_list:
			if self.rect.colliderect(b.rect):
				gs.bullet_list.remove(b)
				#remove across server too
				dict = {}
				dict['message'] = "deleteBullet"
				dict['b_x'] = b.rect.x
				d = pickle.dumps(dict)
				df.getProt().sendData(d)
				self.health = self.health - 1
									
			
			
	#Tick (alters movement and rotates the player)
	def tick(self):

		#Reload delay (every 100 you get 1 bullet)
		self.reloadDelay = self.reloadDelay+1
		if self.reloadDelay == 100:
			self.bullets = self.bullets +1
			self.reloadDelay = 0
		#User input: 
		if self.health != 0:
			for event in pygame.event.get():
				#If you press a key, move in that direction
				if event.type is pygame.KEYDOWN:
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.left = 1
						self.facing = 1
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.right = 1
						self.facing = 0
					elif event.key == pygame.K_UP or event.key == pygame.K_w:
						self.up = 1
					elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
						self.down = 1
					#Jump:
					elif event.key == pygame.K_SPACE:
						if self.canJump:
							self.jump()

					#Shoot a bullet (if you have any):
					elif event.key == pygame.K_c:
						if self.bullets >0:
							self.bullets = self.bullets -1
							if self.facing == 0:
								b = Bullet(self.gs,self.rect.right+10,self.rect.y,self.facing)
							if self.facing == 1:
								b = Bullet(self.gs,self.rect.left-20,self.rect.y,self.facing)
							if self.gs.connected:
								dict = {}
								dict['x'] = self.rect.x
								dict['y'] = self.rect.y
								dict['facing'] = self.facing
								dict['message'] = "makeBullet"
								bul = pickle.dumps(dict)
								df.getProt().sendData(bul)
							gs.bullet_list.append(b)
				#if you let up on a key in a direction, stop motion in that direction: 
				elif event.type is pygame.KEYUP:
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.left = 0
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.right = 0
					elif event.key == pygame.K_UP or event.key == pygame.K_w:
						self.up = 0
					elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
						self.down = 0
				elif event.type is pygame.QUIT:
					pygame.quit()
					reactor.stop()

			#Determine the velocity: 
			self.velX = 0
			if self.left:
				self.velX = -5
			elif self.right:
				self.velX = 5

			#Gravity
			self.velY = self.velY + self.gravity
			self.rect = self.rect.move(self.velX,self.velY)
			self.collideWalls()
			self.collideBullets()


		#If you are dead, send that info to the other player
		if self.health == 0:
			dict = {}
			dict['message'] = "deletePlayer"
			d = pickle.dumps(dict)
			df.getProt().sendData(d)


#Main game class: 
class GameSpace:
	def main(self):
		#Initialize everything:
		pygame.init()
		pygame.mixer.init()
		self.size = self.width,self.height=800,800
		self.connected = 0
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("RED VS BLUE")
		self.welcomeImage = pygame.image.load("images/Welcome.png")
		self.welcomeRect = self.welcomeImage.get_rect()
		self.clock = pygame.time.Clock()
		self.player = Player(self)
		self.enemy = Player(self)
		self.wall_list = []
		self.enemy.image = pygame.image.load("images/blueBlock2.png")
		self.redWinsImage = pygame.image.load("images/redWins.png")
		self.blueWinsImage = pygame.image.load("images/blueWins.png")
		self.redWinsRect = self.redWinsImage.get_rect()
		self.blueWinsRect = self.blueWinsImage.get_rect()
		self.enemy.rect.left = -100
		for x in range(0, 80):
			self.wall_list.append(Wall(self, 0, 10*x,1)) 
			self.wall_list.append(Wall(self, 10*x, 790,4)) 
			self.wall_list.append(Wall(self, 790, 10*x,3)) 
			self.wall_list.append(Wall(self, 10*x, 0,2)) 
		for x in range (0, 40):
			if x > 20 and x < 30:
				continue
			self.wall_list.append(Wall(self, 10*x, 100,5,1)) 
			self.wall_list.append(Wall(self, 10*x+400, 200,5,0)) 
			self.wall_list.append(Wall(self, 10*x, 350,5,1))
			self.wall_list.append(Wall(self, 10*x+400, 450,5,0))  
		for x in range (0, 30):
			self.wall_list.append(Wall(self, 10*x, 700,5,1)) 
			self.wall_list.append(Wall(self, 10*x+410, 600,5,0))
		self.bullet_list = []

	#This is the main loop for the game
	def pygame_interior(self):
		self.clock.tick(60)
		self.player.tick()
		if self.connected:
			p = pickle.dumps(self.player.rect)
			df.getProt().sendData(p)
		for bullet in self.bullet_list:
			bullet.tick()
		self.screen.fill(self.black)
		
		if self.enemy.health >0:
			self.screen.blit(self.enemy.image,self.enemy.rect)
		else:
			self.screen.blit(self.redWinsImage,self.redWinsRect)
			self.screen.blit(self.player.image,self.player.rect)
		if self.player.health >0:
			self.screen.blit(self.player.image,self.player.rect)
		else:
			self.screen.blit(self.blueWinsImage,self.blueWinsRect)
			self.screen.blit(self.enemy.image,self.enemy.rect)

		for bullet in self.bullet_list:
			self.screen.blit(bullet.image, bullet.rect)
		for wall in self.wall_list:
			wall.tick()
			self.screen.blit(wall.image, wall.rect)
		pygame.display.flip()



	#Functions for handling results from network messages
	def areConnected(self):
		lc.start(1/FPS)
		self.connected = 1
	def moveEnemy(self,rect):
		self.enemy.rect = rect
	def makeBullet(self,bdict):
		b = Bullet(self,bdict['x'],bdict['y'],bdict['facing'])
		self.bullet_list.append(b)
	def deleteBullet(self,b_x):
		for b in self.bullet_list:
			if abs(b.rect.x-b_x)<100:
				self.bullet_list.remove(b)
	def deleteEnemy(self):
		self.enemy.health = 0



#Run the game 
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
	df = DataFactory()
	reactor.listenTCP(9876,df)
	FPS = 45
	gs.screen.blit(gs.welcomeImage,gs.welcomeRect)
	pygame.display.flip()
	lc = LoopingCall(gs.pygame_interior)
	#lc.start(1/FPS)
	reactor.run()
	sys.exit()
