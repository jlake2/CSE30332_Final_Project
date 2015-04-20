#John F. Lake, Jr. & James Bowyer
#Final Project
#Shooter Platforming Game


#All we need is pygame and some math: 
import pygame
import math

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

#Player class: 
class Player(pygame.sprite.Sprite):
	def __init__(self,gs=None):

		#Initialize the sprite, sound, and images:
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/redBlock.png")
		self.laser = pygame.image.load("laser.png")
		self.rect = self.image.get_rect()

		#Location/velocity of the death star:
		self.location = self.rect
		self.velX = 0
		self.velY = 0

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
			

	#Tick (alters movement and rotates the player)
	def tick(self):
		#User input: 
		for event in pygame.event.get():
			#If you press a key, move in that direction
			if event.type is pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.velX = -5
				elif event.key == pygame.K_RIGHT:
					self.velX = 5
				elif event.key == pygame.K_UP:
					self.velY = -5
				elif event.key == pygame.K_DOWN:
					self.velY = 5
			#if you let up on a key in a direction, stop motion in that direction: 
			elif event.type is pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					self.velX = 0
				elif event.key == pygame.K_RIGHT:
					self.velX = 0
				elif event.key == pygame.K_UP:
					self.velY = 0
				elif event.key == pygame.K_DOWN:
					self.velY = 0

		#Move the death star
		self.rect = self.rect.move(self.velX,self.velY)
		self.containWithinBorder()

			

				

#Main game class: 
class GameSpace:
	def main(self):
		#Initialize everything:
		pygame.init()
		pygame.mixer.init()
		self.size = self.width,self.height=640,480
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		self.player = Player(self)



		#Main game loop;
		while True:
			self.clock.tick(60)
			self.player.tick()
			self.screen.fill(self.black)
			self.screen.blit(self.player.image,self.player.rect)
			pygame.display.flip()



#Run the game 
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
