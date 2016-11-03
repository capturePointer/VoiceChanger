import Queue
import spidev
import time

class Spi:
	
	def __init__(self, ComController):
		self.ComController = ComController
		self.writeQueue = Queue.Queue()
		self.readQueue = Queue.Queue()
		self.spi = spidev.SpiDev()
		self.spi.open(0, 1)
		self.running = True

	def close(self):
		self.spi.close()
		

	def cycle(self):
		output = []
		while not self.writeQueue.empty():
			output.append(self.writeQueue.get())
		if len(output) == 0:
			output.append(0x00)
		input = self.spi.xfer2(output)
		for byte in input:
			self.readQueue.put(byte)


	def write(self, bytes):
		for byte in bytes:
			self.writeQueue.put(byte)


	def readSingleSafe(self):
		result = 0
		while result == 0:
			result = self.readQueue.get()
		return result


	def read(self, amount):
		result = []
		for i in range(amount):
			result.append(self.readQueue.get())
		return result
