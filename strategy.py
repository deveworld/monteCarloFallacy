from settings import *
import random


class Strategy():
	def __init__(self):
		super(Strategy, self).__init__()
		self.active = True
		self.last = True
		self.betting = Default_Betting
		self.guess = True
		self.money = Default_Money

	def inform(self, result: bool):
		if not Infinite_Money:
			if not self.active:
				return
		self.last = result
		self.money -= self.betting
		if result == self.guess:
			self.money += self.betting*Reward_Money
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
		self.history = []

	def inform(self, result: bool):
		super(GamblerStrategy, self).inform(result)
		self.history.append(result)
		if len(self.history) > Gambler_Max_History:
			self.history.pop()

	def make_guess(self):
		true_total = 0
		for past in self.history:
			if past:
				true_total += 1
		false_total = len(self.history) - true_total
		diff = abs(true_total - false_total)

		if true_total > false_total:
			self.guess = False
		elif true_total == false_total:
			if bool(random.getrandbits(1)):
				self.guess = not self.last
			else:
				self.guess = bool(random.getrandbits(1))
		else:
			self.guess = True

		self.betting = min(Max_Betting, Default_Betting + (Default_Betting/Gambler_Max_History * diff))


class RegressionStrategy(Strategy):
	def __init__(self):
		super(RegressionStrategy, self).__init__()
		self.iter = 0
		self.true_total = 0

	def inform(self, result: bool):
		super(RegressionStrategy, self).inform(result)
		self.iter += 1
		if result:
			self.true_total += 1

	def make_guess(self):
		ratio = 0.5
		try:
			true_ratio = self.true_total/self.iter
		except ZeroDivisionError:	# First iter
			true_ratio = 0.5
		if true_ratio > 0.5:		# True observed more than False
			self.guess = False
			ratio = true_ratio
		elif true_ratio == 0.5: 	# equal
			self.guess = bool(random.getrandbits(1))
		else:						# False observed more than True
			self.guess = True
			ratio = 1-true_ratio

		self.betting = min(Max_Betting, Default_Betting * (0.5+ratio))


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
		self.history = []

	def inform(self, result: bool):
		super(MartingaleGamblerStrategy, self).inform(result)
		self.history.append(result)
		if len(self.history) > Gambler_Max_History:
			self.history.pop()

	def make_guess(self):
		if self.guess == self.last:
			self.betting = Default_Betting
		else:
			self.betting *= 2
			
		true_total = 0
		for past in self.history:
			if past:
				true_total += 1
		false_total = len(self.history) - true_total
		diff = abs(true_total - false_total)

		if true_total > false_total:
			self.guess = False
		elif true_total == false_total:
			if bool(random.getrandbits(1)):
				self.guess = not self.last
			else:
				self.guess = bool(random.getrandbits(1))
		else:
			self.guess = True
