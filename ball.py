import pygame as pg
import numpy as np

STARTING_VELOCITY = 0.15

class Ball():
	def __init__(self, pos, screen_size, width=20, height=20):
		self.width = width
		self.height = height
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.reset_pos = (self.x_pos,self.y_pos)

		self.x_vel = STARTING_VELOCITY
		self.y_vel = STARTING_VELOCITY

		self.image = pg.transform.scale(pg.image.load('assets\BALL.png'),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = self.x_pos
		self.rect.y = self.y_pos

		self.screen_width = screen_size[0]
		self.screen_height = screen_size[1]

		self.done = False
		self.score = [0,0]
		self.winner = "None"

	def get_pos(self):
		return(self.x_pos,self.y_pos,self.width,self.height)


	def move(self, new_pos):

		if(new_pos[0] < 0 and self.x_pos>0):
			self.x_pos = self.x_pos+new_pos[0]
		if(new_pos[0] > 0 and self.x_pos < self.screen_width-self.width):
			self.x_pos = self.x_pos+new_pos[0]


		if(new_pos[1] < 0 and self.y_pos>0):
			self.y_pos = self.y_pos+new_pos[1]
		if(new_pos[1] > 0 and self.y_pos < self.screen_height-self.height):
			self.y_pos = self.y_pos+new_pos[1]


		self.update_rect()
		return(self.x_pos,self.y_pos,self.width,self.height)

	def cont_move(self):

		if(self.x_pos >= self.screen_width-self.width):
			self.done = True
			self.winner = "PLAYER 1"
		if(self.x_pos <= 0):
			self.done = True
			self.winner = "PLAYER 2"


		if(self.y_pos >= self.screen_height-self.height or self.y_pos <= 0):
			self.y_vel *= -1

		return(self.move((self.x_vel,self.y_vel)))

	
	def update_rect(self):
		self.rect.x = self.x_pos
		self.rect.y = self.y_pos

	def collide_check(self, rects):
		returner = False
		for i in rects:
			if(self.rect.colliderect(i)):
				returner = True
		return returner

	def hit(self):
		if(self.x_pos <= 400):
			self.score[0] += 1
			#self.x_vel = np.abs(self.x_vel) 
		else:
			self.score[1] += 1
			#self.x_vel = np.abs(self.x_vel) * -1

		self.x_vel *= -1

	def reset(self):
		self.done = False
		self.x_pos = self.reset_pos[0]
		self.y_pos = self.reset_pos[1]
		self.x_vel = STARTING_VELOCITY
		self.y_vel = STARTING_VELOCITY
		self.update_rect()
		self.score = [0,0]
		return(self.x_pos,self.y_pos,self.width,self.height)
