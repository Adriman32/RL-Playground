import pygame as pg
from environment import Game

screen_size = (800,600)
env = Game((screen_size),True)
episodes = 3

for ep in range(episodes):

	env.reset()
	is_running = True
	while is_running:
		env.render()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					is_running = False
		
		P1_ACTION = 0
		P2_ACTION = 0

		keys = pg.key.get_pressed()

		if keys[pg.K_r]:
			env.reset()
		if keys[pg.K_w]:
			P1_ACTION = 1
		if keys[pg.K_s]:
			P1_ACTION = -1
		if keys[pg.K_UP]:
			P2_ACTION = 1
		if keys[pg.K_DOWN]:
			P2_ACTION = -1
		
		p1_pos, p2_pos, ball_pos, score, done = env.step(P1_ACTION,P2_ACTION)
		#p1_pos, p2_pos, ball_pos, score, done = env.step(env.sample_action(),env.sample_action())
		#p1_pos, p2_pos, ball_pos, score, done = env.step(env.pre_trained('follow'),env.pre_trained('follow'))
		#p1_pos, p2_pos, ball_pos, score, done = env.step(env.sample_action(),env.pre_trained('follow'))

		'''
		print("\np1_pos:{}".format(p1_pos))
		print("p2_pos:{}".format(p2_pos))
		print("ball_pos:{}".format(ball_pos))
		print("score:{}".format(score))
		print("done:{}\n".format(done))
		'''

		if(done):
			break
