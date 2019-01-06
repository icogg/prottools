import matplotlib.pyplot as plt


class Idmt:
	
	def __init__(self, pickup, tms, curve, deftime=20, adder=0, mintime=0):
		"""Create an instance of an IDMT characteristic"""
		self.element_type = 'IDMT'
		self.pickup = pickup
		self.tms = tms
		self.curve = curve
		self.deftime = deftime
		self.adder = adder
		self.mintime = mintime
		if isinstance(curve, type(list())):
			self.alpha = curve[0]
			self.beta = curve[1]
		elif isinstance(curve, type(str())):
			self.alpha = _curvelup(curve)['alpha']
			self.beta = _curvelup(curve)['beta']
		else:
			return print('select a curve type')


	def optime(self, I):
		"""return the operating time for a given current for the IDMT instance, where
		the current is less than the pickup the value returned is No Op """
		if I > self.pickup + 0.000001:
			return max(
				self.tms *
				self.beta /
				(min((I / self.pickup), self.deftime)**self.alpha - 1) +
				self.adder, self.mintime
				)
		else:
			return 'No Op'
			

class Deftime:

	def __init__(self, pickup, delay=0.01):
		self.element_type = 'DT'
		self.pickup = pickup
		self.delay = delay

	def optime(self, I):
		"""return the operating time for a given current for the IDMT instance, where
		the current is less than the pickup the value returned is No Op """
		if I > self.pickup:
			return self.delay
		else:
			return 'No Op'


class Relay:
	
	def __init__(self, relayname=''):
		self.stages = []
		self.relayname = relayname
		return
	
	def add_element(self, stage):
		self.stages.append(stage)
		self.stages.sort(key=lambda x : x.pickup)
	
	def add_fault_range(self, minfault, maxfault):
		self.min = minfault
		self.max = maxfault
	
	def getoptime(self, I):
		operatetime = 1000000
		for stage in self.stages:		
			try:
				if stage.optime(I) < operatetime:
						operatetime = stage.optime(I)
			except:
				pass
		return operatetime
	
	def plotchar(self):
		try:
			Ifault = list(self.min, self.max, 10)
		except:
			Ifault = list(range(10, 100000, 10))
			time = []
			for i in Ifault:
				time.append(self.getoptime(i))
		return Ifault, time, self.relayname, 
				
		



class Pltidmt:
	
	def __init__(self, name=''):
		self.relays = []
		self.name = name
		return

	def add_relay(self, relay):
		self.relays.append(relay)
		return
	

def _curvelup(curve):
	curves = {
		'SI': {'alpha': 0.02, 'beta': 0.14},
		'VI': {'alpha': 1, 'beta': 13.5},
		'EI': {'alpha': 2, 'beta': 80}
		}
	for k, v in curves.items():
		if curve.upper() == k:
			return v
		else:
			pass


def plotcurve(relay):
	fig = plt.figure()
	fig.suptitle('No axes on this figure')  # Add a title so we know which it is
	current = list(range(100,100000,10))
	# t = lambda I : relay.getoptime(I)
	times = []
	for i in current:
		times.append(relay.getoptime(I))
	plt.loglog(current, times);
	x1,x2,y1,y2 = plt.axis()
	plt.axis((100,10000,0.001,10))

	plt.show()
	
	

testrelay = Relay()
testrelay.add_element(Idmt(200,0.2,'SI'))
testrelay.add_element(Idmt(400,0.05,'VI'))
testrelay.add_element(Deftime(20000, 0.02))
testrelay.add_element(Deftime(22000, 0.01))

current = list(range(100,100000,10))
t = lambda I : testrelay.getoptime(I)

times = []
for i in current:
	times.append(t(i))

plt.loglog(current, times);
x1,x2,y1,y2 = plt.axis()
plt.axis((100,10000,0.001,10))

plt.show()

