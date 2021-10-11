import pygame as pg

class Player():
	def __init__(self, pos, screen_size, width=20, height=100):
		self.width = width
		self.height = height
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.reset_pos = (self.x_pos,self.y_pos)

		self.image = pg.transform.scale(pg.image.load('assets\PLAYER.png'),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = self.x_pos
		self.rect.y = self.y_pos

		self.screen_width = screen_size[0]
		self.screen_height = screen_size[1]

		self.action_space = (-1,0,1)

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

	def update_rect(self):
		self.rect.x = self.x_pos
		self.rect.y = self.y_pos

	def collide_check(self):
		self.rect.x = self.x_pos
		self.rect.y = self.y_pos

	def reset(self):
		self.x_pos = self.reset_pos[0]
		self.y_pos = self.reset_pos[1]
		self.update_rect()
		return(self.x_pos,self.y_pos,self.width,self.height)