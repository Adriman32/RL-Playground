import pygame as pg
import random
import cv2 as cv
from player import Player
from ball import Ball 

class Game():
	def __init__(self,screen_size,verbose=False):
		'''
		Initializes the screen and creates players/ball

		Inputs:
			screen_size
				- Type: Tuple (WIDTH,HEIGHT)
			verbose
				- Type: Boolean
					* Optional argument that toggles output to console
		'''
		pg.init()
		self.SCREEN_WIDTH = screen_size[0]
		self.SCREEN_HEIGHT = screen_size[1]
		self.SCREEN = pg.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
		self.ICON = pg.image.load('assets\A_ICON.png')
		pg.display.set_icon(self.ICON)
		pg.display.set_caption("Adrian's Game")
		self.font = pg.font.Font('freesansbold.ttf', 32)
		self.background_color = (255,255,255)

		self.PLAYER_1 = Player((20,screen_size[1]/2 - 100/2),(self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
		self.PLAYER_1_POS = self.PLAYER_1.get_pos()
		self.PLAYER_2 = Player((screen_size[0]-20*2,screen_size[1]/2 - 100/2),(self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
		self.PLAYER_2_POS = self.PLAYER_2.get_pos()

		self.BALL = Ball((screen_size[0]/2 - 20/2,screen_size[1]/2 - 20/2),(self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
		self.BALL_POS = self.BALL.get_pos()

		self.done = False
		self.action_space = self.PLAYER_1.action_space
		self.verbose = verbose

	def render(self):
		'''
		Updates the contents of the screen
		'''
		screen_color = (255,255,255)
		# Updates scores
		self.P1_SCORE = self.font.render(str(self.BALL.score[0]),True,(0,0,0))
		self.P1_SCORE_POS = self.P1_SCORE.get_rect()
		self.P1_SCORE_POS.left = self.SCREEN_WIDTH/4
		self.P2_SCORE = self.font.render(str(self.BALL.score[1]),False,(0,0,0))
		self.P2_SCORE_POS = self.P2_SCORE.get_rect()
		self.P2_SCORE_POS.left = self.SCREEN_WIDTH - self.SCREEN_WIDTH/4

		# Updates player and ball positions
		self.SCREEN.fill(screen_color)
		self.SCREEN.blit(self.P1_SCORE,self.P1_SCORE_POS)
		self.SCREEN.blit(self.P2_SCORE,self.P2_SCORE_POS)
		self.SCREEN.blit(self.BALL.image,self.BALL_POS)
		self.SCREEN.blit(self.PLAYER_1.image,self.PLAYER_1_POS)
		self.SCREEN.blit(self.PLAYER_2.image,self.PLAYER_2_POS)
		pg.display.flip()

	def getFrame(self):
		screen = pg.display.get_surface()
		capture = pg.surfarray.pixels3d(screen)
		capture = capture.transpose([1,0,2])
		capture_bgr = cv.cvtColor(capture,cv.COLOR_RGB2BGR)
		return capture_bgr

	

	def reset(self):
		self.PLAYER_1_POS = self.PLAYER_1.reset()
		self.PLAYER_2_POS = self.PLAYER_2.reset()
		self.BALL_POS = self.BALL.reset()
		self.done = False
		return (self.PLAYER_1_POS, self.PLAYER_2_POS, self.BALL_POS, self.BALL.score,self.done)


	def step(self,P1_ACTION,P2_ACTION,vel=0.35):
		'''
		Takes one step forward in the game and returns observations

		Inputs:
			P1_ACTION
				- Type: int
				- Action_Space: [-1,0,1]
					* -1: Move player up
					*  0: Do not move player
					*  1: Move player down
			P2_ACTION
				- Type: int
				- Action_Space: [-1,0,1]
					* -1: Move player up
					*  0: Do not move player
					*  1: Move player down
			vel
				- Type: float
				- Optional argument that determines velocity of players

		Outputs:
			PLAYER_1_POS
				- Type: Tuple
				- Observation_Space [int, float, int, int]
					* int: X position
					* float: Y position
					* int: width
					* int: height
			PLAYER_2_POS
				- Type: Tuple
				- Observation_Space [int, float, int, int]
					* int: X position
					* float: Y position
					* int: width
					* int: height
			BALL_POS
				- Type: Tuple
				- Observation_Space [int, float, int, int]
					* int: X position
					* float: Y position
					* int: width
					* int: height
			Done
				- Type: Boolean
				- Returns true if game has finished
		'''
		pg.event.get()
		if(P1_ACTION == 1):
			# Move player up
			self.PLAYER_1_POS = self.PLAYER_1.move([0,-vel])
		if(P1_ACTION == -1):
			# Move player down
			self.PLAYER_1_POS = self.PLAYER_1.move([0,vel])
		if(P2_ACTION == 1):
			# Move player up
			self.PLAYER_2_POS = self.PLAYER_2.move([0,-vel])
		if(P2_ACTION == -1):
			# Move player down
			self.PLAYER_2_POS = self.PLAYER_2.move([0,vel])

		# Checks for player collisions
		player_rects = (self.PLAYER_1.rect, self.PLAYER_2.rect)
		if(self.BALL.collide_check(player_rects)):
			self.BALL.hit()

		# Displays score, winner, and ends the game
		if(self.BALL.done):
			if(self.verbose):
				print("WINNER: {}".format(self.BALL.winner))
				print("SCORE: {}".format(self.BALL.score))
			self.done = True

		self.BALL_POS = self.BALL.cont_move()
		return (self.PLAYER_1_POS, self.PLAYER_2_POS, self.BALL_POS, self.BALL.score,self.done)

	def sample_action(self):
		'''
		Selects a random action from the action space

		Outputs:
			- Random action from environment's action space
		'''

		num_actions = len(self.action_space) -1
		rand_action = random.randint(0,num_actions)
		
		return (self.action_space[rand_action])

	def pre_trained(self,model):
		'''
		Pre-Trained Models returning actions

		Inputs:
			model
				- Type: string
				- Selects the model to use
					* MODELS:
						Follow: Follows the position of the ball
		
		Outputs:
			action
				-Type: int
				- Returns action to take based on selected model
		'''
		if(model == 'follow'):
			if(self.PLAYER_1_POS[1] > self.BALL_POS[1]):
				return(1)
			if(self.PLAYER_1_POS[1] < self.BALL_POS[1]):
				return(-1)
