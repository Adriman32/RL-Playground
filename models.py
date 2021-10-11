import numpy as np
import random

class simpleQ():

	def __init__(self,state_space,action_space,epsilon=0.2, alpha=0,gamma=0.8):
		'''
		Initializes the action space

		Inputs:
			action_space
				- Type: Tuple

		'''
		self.state_space = state_space		
		self.action_space = action_space
		
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma

		self.last_action = 0
		self.last_state = 0

		self.Q = np.zeros((self.state_space,len(self.action_space)))


	def action(self,state):
		if(random.uniform(0,1) < self.epsilon):
			# Random action
			#print("Random")
			taken_action = self.action_space[random.randint(0,len(self.action_space)-1)]
		else:
			# Predicted action
			#print("Predicted")
			taken_action = self.predict(state)

		self.last_state = state
		self.last_action = taken_action

		print(self.Q[state])

		return(taken_action)


	def predict(self,state):
		best_action = int(self.Q[state,np.argmax(self.Q[state])])-1



	def updateQ(self,state,action,reward):
		print("Updated",state,action,reward)
		print(self.Q[self.last_state,action])
		self.Q[self.last_state,action] = self.Q[self.last_state,action] + self.alpha *(reward+self.gamma*np.max(self.Q[state,:])-self.Q[self.last_state,action])
		print(self.Q[self.last_state,action])