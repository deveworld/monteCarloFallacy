import sys
import time
import random
from strategy import *
from settings import *


class Evaluator(object):
	def __init__(self):
		super(Evaluator, self).__init__()
		self.iter = 0
		self.strategies = []
		self.strategies.append(RandomStrategy())
		self.strategies.append(GamblerStrategy())
		self.strategies.append(RegressionStrategy())
		self.strategies.append(MartingaleRandomStrategy())
		self.strategies.append(MartingaleGamblerStrategy())

	def eval(self):
		random.seed(random.randrange(sys.maxsize))
		result = bool(random.getrandbits(1))

		for strategy in self.strategies:
			strategy.make_guess()
			strategy.inform(result)
	
	
	def get_log_text(self) -> str:
		log_text = f"{self.iter}, "
		for strategy in self.strategies:
			log_text += f"{strategy.__class__.__name__}: {strategy.money:.0f}    "
		return log_text

	def run(self):
		for i in range(Iteration):
			self.eval()
			print(self.get_log_text(), end="\r")
			self.iter += 1
			time.sleep(0.01)
		print()


if __name__ == "__main__":
	if Seed == None:
		seed = random.randrange(sys.maxsize)
	else:
		seed = Seed
	random.seed(seed)
	print(f"Loaded. Seed: {seed}")

	evaluator = Evaluator()
	try:
		evaluator.run()
	except KeyboardInterrupt as e:
		print()