from settings import *
import random


class Strategy():
	def __init__(self):
		super(Strategy, self).__init__()
		self.active = True
		self.use_history = False
		self.history = []
		self.last = True
		self.betting = Default_Betting
		self.guess = True
		self.money = Default_Money
		self.correct = 0

	def inform(self, result: bool):
		if not Infinite_Money:
			if not self.active:
				return
		if self.use_history:
			self.history.append(result)
		self.last = result
		self.money -= self.betting
		if result == self.guess:
			self.money += self.betting*Reward_Money
			self.correct += 1
		if self.money <= 0:
			self.active = False

	def make_guess(self):
		self.guess = True


class RandomStrategy(Strategy):
	def __init__(self):
		super(RandomStrategy, self).__init__()
		
	def make_guess(self):
		self.guess = bool(random.getrandbits(1))


class GamblerStrategy(Strategy):
	def __init__(self):
		super(GamblerStrategy, self).__init__()
		
	def make_guess(self):
		self.guess = not self.last


class MartingaleRandomStrategy(Strategy):
	def __init__(self):
		super(MartingaleRandomStrategy, self).__init__()
	
	def make_guess(self):
		if self.guess == self.last:
			self.betting = Default_Betting
		else:
			self.betting *= 2

		self.guess = bool(random.getrandbits(1))


class MartingaleGamblerStrategy(Strategy):
	def __init__(self):
		super(MartingaleGamblerStrategy, self).__init__()
	
	def make_guess(self):
		if self.guess == self.last:
			self.betting = Default_Betting
		else:
			self.betting *= 2

		self.guess = not self.last


class RegressionStrategy(Strategy):
	def __init__(self):
		super(RegressionStrategy, self).__init__()
		self.use_history = True

	def make_guess(self):
		true_total = 0
		for history in self.history:
			if history:
				true_total +=1
		try:
			true_ratio = true_total/len(self.history)
		except ZeroDivisionError:
			true_ratio = 0.5
		if true_ratio > 0.5:
			self.guess = False
		elif true_ratio == 0.5:
			self.guess = bool(random.getrandbits(1))
		else:
			self.guess = True