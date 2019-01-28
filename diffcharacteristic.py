import matplotlib.pyplot as plt
import numpy as np


class L90_2Term:
	"""This class is used to store a GE L90 Line Diff Setting and to call
	functions to describe it
	"""
	def __init__(self, S1=0.3, S2=0.5, BP=8, P=0.2, Sigma=0):
		self.S1 = S1
		self.S2 = S2
		self.BP = BP
		self.P = P
		self.Sigma = Sigma

	def rest(self, Iloc, Irem):
		"""The rest function calculates the restraint current for a line
		differental application using the set characteristic along with the local
		and remote currents. Once the line end currents are calculated, they are
		combined and returned. Inputs:
					Iloc = Local Current
					Irem = Remote Current (this should be set negative to show outflow)
		"""
		if Iloc ** 2 < self.BP ** 2:
			LocRestSq = (2 * self.S1 ** 2 * np.abs(Iloc) ** 2)
		else:
			LocRestSq = (
										2 * ((self.S2 * Iloc)**2 - (self.S2 * self.BP)**2) +
										2 * (self.S1 * self.BP)**2
									)

		if Irem ** 2 < self.BP ** 2:
			RemRestSq = (2 * self.S1 ** 2 * np.abs(Irem) ** 2)
		else:
			RemRestSq = (
										2 * ((self.S2 * Irem)**2 - (self.S2 * self.BP)**2) +
										2 * (self.S1 * self.BP)**2
									)
	
		return np.sqrt(LocRestSq + RemRestSq)

	def trip(self, Iloc, Irem):
		"""The trip decision is made by passing in the differential and restraint
		currents along with the basic pickup. If the Severity calculation is > 0 a
		trip is declared
		"""
		SA = self.diff(Iloc, Irem)**2 - (2 * self.P**2 + self.rest(Iloc, Irem)**2)
		if SA > 0:
			out = 'Trip'
		else:
			out = 'No Op'
		return out

	def diff(self, Iloc, Irem):
		return np.abs(Iloc + Irem)

	def sysvals(self, Irem=-1):
		"""sysvalues are used to calculate the operating point given a characteristic
		and remote outflow current.
			Inputs:
					Irem = Remote Current (this should be set negative to show outflow)
					S1 = Diff characteristic slope 1
					S2 = Diff characteristic slope 2
					BP = Slope 1 to 2 change over
					P  = Pickup
			Output is a dictionary that contains, Local and Remote Currents, Diff and
			Restraint
		"""
	
		Iloc = - Irem
		while self.trip(Iloc, Irem) == 'No Op':
			Iloc += 0.001
		return{
			'Iloc': round(Iloc, 4),
			'Irem': round(Irem, 4),
			'Diff': round(self.diff(Iloc, Irem), 4),
			'Rest': round(self.rest(Iloc, Irem), 4)
			}

	def plotpairs(self, ascending=True, plotrange=10):
		xvals = []
		yvals = []
		diffvals = []
		restvals = []
		for i in range(plotrange * 100):
			Irem = i / 100
			Iloc = - Irem
			while self.trip(Iloc, Irem) == 'No Op':
				if ascending:
					Iloc += 0.01
				else:
					Iloc -= 0.01
			xvals.append(Irem)
			yvals.append(-Iloc)
			diffvals.append(self.diff(Iloc, Irem))
			restvals.append(self.rest(Iloc, Irem))
		return xvals, yvals, diffvals, restvals
	

	def table(self, outflow=1):
		"""the table function returns a table of results that show the resistive
		coverage for different voltages and CT ratios. By changing the outflow value
		from 1.0pu the system can be tested for different sensitivities.
			Inputs:
					outflow = amount of current leaving the remote end 1.0pu default
					S1 = Diff characteristic slope 1
					S2 = Diff characteristic slope 2
					BP = Slope 1 to 2 change over
					P  = Pickup
		"""
		voltages = [11, 22, 33, 66, 110, 132, 220]
		cts = [100, 200, 400, 600, 800, 1200, 2000]
		# Create and print a header row
		hdr = '{:<8}'.format('CT Ratio')
		for ct in cts:
			hdr = hdr + str('{:8d}'.format(ct))
		print(hdr)

		for voltage in voltages:
			vals = '{:<8}'.format(voltage)
			for ct in cts:
				PUDiff = self.sysvals(Irem=-outflow)['Diff']
				Z = 1000 * voltage / (np.sqrt(3) * ct * PUDiff)
				vals = vals + ' ' + str('{:7.2f}'.format(Z))
			print(vals)
		return{
			'Pickup': self.P,
			'S1': self.S1,
			'S2': self.S2,
			'BP': self.BP
			}


class L90_3Term:
	"""This class is used to store a GE L90 Line Diff Setting and to call
	functions to describe it
	"""
	def __init__(self, S1=0.3, S2=0.5, BP=8, P=0.2, Sigma=0):
		self.S1 = S1
		self.S2 = S2
		self.BP = BP
		self.P = P
		self.Sigma = Sigma

	def rest(self, Iloc, Irem):
		"""The rest function calculates the restraint current for a line
		differental application using the set characteristic along with the local
		and remote currents. Once the line end currents are calculated, they are
		combined and returned. Inputs:
					Iloc = Local Current
					Irem = Remote Current (this should be set negative to show outflow)
		"""
		if Iloc ** 2 < self.BP ** 2:
			LocRestSq = (4/3) * (self.S1 ** 2 * np.abs(Iloc) ** 2)
		else:
			LocRestSq = (
										(4/3) * ((self.S2 * Iloc)**2 - (self.S2 * self.BP)**2) +
										(4/3) * (self.S1 * self.BP)**2
									)

		if Irem ** 2 < self.BP ** 2:
			RemRestSq = (4/3) * (self.S1 ** 2 * np.abs(Irem) ** 2)
		else:
			RemRestSq = (
										(4/3) * ((self.S2 * Irem) ** 2 - (self.S2 * self.BP) ** 2) +
										(4/3) * (self.S1 * self.BP) ** 2
									)
	
		return np.sqrt(LocRestSq + RemRestSq)

	def trip(self, Iloc, Irem):
		"""The trip decision is made by passing in the differential and restraint
		currents along with the basic pickup. If the Severity calculation is > 0 a
		trip is declared
		"""
		SA = self.diff(Iloc, Irem)**2 - (2 * self.P**2 + self.rest(Iloc, Irem)**2)
		if SA > 0:
			out = 'Trip'
		else:
			out = 'No Op'
		return out

	def diff(self, Iloc, Irem):
		return np.abs(Iloc + Irem)
		
	def sysvals(self, Irem=-1):
		"""sysvalues are used to calculate the operating point given a characteristic
		and remote outflow current.
			Inputs:
					Irem = Remote Current (this should be set negative to show outflow)
					S1 = Diff characteristic slope 1
					S2 = Diff characteristic slope 2
					BP = Slope 1 to 2 change over
					P  = Pickup
			Output is a dictionary that contains, Local and Remote Currents, Diff and
			Restraint
		"""
	
		Iloc = - Irem
		while self.trip(Iloc, Irem) == 'No Op':
			Iloc += 0.001
		return{
			'Iloc': round(Iloc, 4),
			'Irem': round(Irem, 4),
			'Diff': round(self.diff(Iloc, Irem), 4),
			'Rest': round(self.rest(Iloc, Irem), 4)
			}

	def plotpairs(self, ascending=True, plotrange=10):
		xvals = []
		yvals = []
		diffvals = []
		restvals = []
		for i in range(plotrange * 100):
			Irem = i / 100
			Iloc = - Irem
			while self.trip(Iloc, Irem) == 'No Op':
				if ascending:
					Iloc += 0.01
				else:
					Iloc -= 0.01
			xvals.append(Irem)
			yvals.append(-Iloc)
			diffvals.append(self.diff(Iloc, Irem))
			restvals.append(self.rest(Iloc, Irem))
		return xvals, yvals, diffvals, restvals

	
	def table(self, outflow=1):
		"""the table function returns a table of results that show the resistive
		coverage for different voltages and CT ratios. By changing the outflow value
		from 1.0pu the system can be tested for different sensitivities.
			Inputs:
					outflow = amount of current leaving the remote end 1.0pu default
					S1 = Diff characteristic slope 1
					S2 = Diff characteristic slope 2
					BP = Slope 1 to 2 change over
					P  = Pickup
		"""
		voltages = [11, 22, 33, 66, 110, 132, 220]
		cts = [100, 200, 400, 600, 800, 1200, 2000]
		# Create and print a header row
		hdr = '{:<8}'.format('CT Ratio')
		for ct in cts:
			hdr = hdr + str('{:8d}'.format(ct))
		print(hdr)

		for voltage in voltages:
			vals = '{:<8}'.format(voltage)
			for ct in cts:
				PUDiff = self.sysvals(Irem=-outflow)['Diff']
				Z = 1000 * voltage / (np.sqrt(3) * ct * PUDiff)
				vals = vals + ' ' + str('{:7.2f}'.format(Z))
			print(vals)
		return{
			'Pickup': self.P,
			'S1': self.S1,
			'S2': self.S2,
			'BP': self.BP
			}


class P543:
	"""This class is used to store a P543 Line Diff Setting and to call
	functions to describe it
	"""
	def __init__(self, IS1=0.2, IS2=2, K1=0.2, K2=1.5):
		self.IS1 = IS1
		self.IS2 = IS2
		self.K1 = K1
		self.K2 = K2

	def rest(self, Iloc, Irem):
		"""The rest function calculates the restraint current for a line
		differental application using the set characteristic along with the local
		and remote currents. Once the line end currents are calculated, they are
		combined and returned. Inputs:
					Iloc = Local Current
					Irem = Remote Current (this should be set negative to show outflow)
		"""
	
		return (np.abs(Iloc) + np.abs(Irem)) / 2

	def diff(self, Iloc, Irem):
		return np.abs(Iloc + Irem)

	def trip(self, Iloc, Irem):
		"""The trip decision is made by passing in the differential and restraint
		currents along with the basic pickup. If the Severity calculation is > 1 a
		trip is declared
		"""
		out = 'No Op'
		if self.rest(Iloc, Irem) < self.IS2:
			if self.diff(Iloc, Irem) > (self.rest(Iloc, Irem) * self.K1 + self.IS1):
				out = 'Trip'
		else:
			restraint = (
									self.K2 * self.rest(Iloc, Irem) + (self.K1 - self.K2) *
									self.IS2 + self.IS1
									)
			if self.diff(Iloc, Irem) > restraint:
				out = 'Trip'
		return out

	def table(self, outflow=1):
		"""the table function returns a table of results that show the resistive
		coverage for different voltages and CT ratios. By changing the outflow value
		from 1.0pu the system can be tested for different sensitivities.
			Inputs:
					outflow = amount of current leaving the remote end 1.0pu default
					K1 = Diff characteristic slope 1
					K2 = Diff characteristic slope 2
					IS2 = Slope 1 to 2 change over
					IS1  = Pickup
		"""
		voltages = [11, 22, 33, 66, 110, 132, 220]
		cts = [100, 200, 400, 600, 800, 1200, 2000]
		# Create and print a header row
		hdr = '{:<8}'.format('CT Ratio')
		for ct in cts:
			hdr = hdr + str('{:8d}'.format(ct))
		print(hdr)

		for voltage in voltages:
			vals = '{:<8}'.format(voltage)
			for ct in cts:
				PUDiff = self.sysvals(Irem=-outflow)['Diff']
				Z = 1000 * voltage / (np.sqrt(3) * ct * PUDiff)
				vals = vals + ' ' + str('{:7.2f}'.format(Z))
			print(vals)
		return{
			'IS1': self.IS1,
			'K1': self.K1,
			'K2': self.K2,
			'IS2': self.IS2
			}

	def sysvals(self, Irem=-1):
		"""sysvalues are used to calculate the operating point given a characteristic
		and remote outflow current.
			Inputs:
					Irem = Remote Current (this should be set negative to show outflow)
			Output is a dictionary that contains, Local and Remote Currents, Diff and
			Restraint
		"""
	
		Iloc = - Irem
		while self.trip(Iloc, Irem) == 'No Op':
			Iloc += 0.001
		return{
			'Iloc': round(Iloc, 4),
			'Irem': round(Irem, 4),
			'Diff': round(self.diff(Iloc, Irem), 4),
			'Rest': round(self.rest(Iloc, Irem), 4)
			}

	def plotpairs(self, ascending=True, plotrange=10):
		xvals = []
		yvals = []
		diffvals = []
		restvals = []
		for i in range(plotrange * 100):
			Irem = i / 100
			Iloc = - Irem
			while self.trip(Iloc, Irem) == 'No Op':
				if ascending:
					Iloc += 0.01
				else:
					Iloc -= 0.01
			xvals.append(Irem)
			yvals.append(-Iloc)
			diffvals.append(self.diff(Iloc, Irem))
			restvals.append(self.rest(Iloc, Irem))
		return xvals, yvals, diffvals, restvals


class RED615:
	"""This class is used to store a P543 Line Diff Setting and to call
	functions to describe it
	"""
	def __init__(self, ES1=1, ES2=5, Pickup=0.1, S2=0.5, S3=1.5):
		self.ES1 = ES1
		self.ES2 = ES2
		self.S2 = S2
		self.S3 = S3
		self.Pickup = Pickup

	def rest(self, Iloc, Irem):
		"""The rest function calculates the restraint current for a line
		differental application using the set characteristic along with the local
		and remote currents. Once the line end currents are calculated, they are
		combined and returned. Inputs:
					Iloc = Local Current
					Irem = Remote Current (this should be set negative to show outflow)
		"""
	
		return np.abs(Iloc - Irem) / 2

	def diff(self, Iloc, Irem):
		return np.abs(Iloc + Irem)

	def trip(self, Iloc, Irem):
		"""The trip decision is made by passing in the local and remote
		currents.
		"""
		out = 'No Op'
		if self.rest(Iloc, Irem) < self.ES1:
			if self.diff(Iloc, Irem) >= self.Pickup:
				out = 'Trip'
		elif self.rest(Iloc, Irem) < self.ES2:
			Rest = self.rest(Iloc, Irem) * self.S2 - self.S2 * self.ES1 + self.Pickup
			if self.diff(Iloc, Irem) >= Rest:
				out = 'Trip'
		else:
			Rest = self.S3 + self.ES2 * (self.S2 + self.S3) - self.S2 * self.ES1 + self.Pickup
			if self.diff(Iloc, Irem) >= Rest:
				out = ' Trip'
		return out

	def table(self, outflow=1):
		"""the table function returns a table of results that show the resistive
		coverage for different voltages and CT ratios. By changing the outflow value
		from 1.0pu the system can be tested for different sensitivities.
			Inputs:
					outflow = amount of current leaving the remote end 1.0pu default
					K1 = Diff characteristic slope 1
					K2 = Diff characteristic slope 2
					IS2 = Slope 1 to 2 change over
					IS1  = Pickup
		"""
		voltages = [11, 22, 33, 66, 110, 132, 220]
		cts = [100, 200, 400, 600, 800, 1200, 2000]
		# Create and print a header row
		hdr = '{:<8}'.format('CT Ratio')
		for ct in cts:
			hdr = hdr + str('{:8d}'.format(ct))
		print(hdr)

		for voltage in voltages:
			vals = '{:<8}'.format(voltage)
			for ct in cts:
				PUDiff = self.sysvals(Irem=-outflow)['Diff']
				Z = 1000 * voltage / (np.sqrt(3) * ct * PUDiff)
				vals = vals + ' ' + str('{:7.2f}'.format(Z))
			print(vals)
		return{
			'ES1': self.ES1,
			'ES2': self.ES2,
			'S2': self.S2,
			'S3': self.S3,
			'Pickip': self.Pickup
			}

	def sysvals(self, Irem=-1):
		"""sysvalues are used to calculate the operating point given a characteristic
		and remote outflow current.
			Inputs:
					Irem = Remote Current (this should be set negative to show outflow)
			Output is a dictionary that contains, Local and Remote Currents, Diff and
			Restraint
		"""
	
		Iloc = - Irem
		while self.trip(Iloc, Irem) == 'No Op':
			Iloc += 0.001
		return{
			'Iloc': round(Iloc, 4),
			'Irem': round(Irem, 4),
			'Diff': round(self.diff(Iloc, Irem), 4),
			'Rest': round(self.rest(Iloc, Irem), 4)
			}

	def plotpairs(self, ascending=True, plotrange=10):
		xvals = []
		yvals = []
		diffvals = []
		restvals = []
		for i in range(plotrange * 100):
			Irem = i / 100
			Iloc = - Irem
			while self.trip(Iloc, Irem) == 'No Op':
				if ascending:
					Iloc += 0.01
				else:
					Iloc -= 0.01
			xvals.append(Irem)
			yvals.append(-Iloc)
			diffvals.append(self.diff(Iloc, Irem))
			restvals.append(self.rest(Iloc, Irem))
		return xvals, yvals, diffvals, restvals


class SEL311L:
	"""This class is used to store a P543 Line Diff Setting and to call
	functions to describe it
	"""
	def __init__(self, ANG87=195, K=6, LPP87=1.2):
		self.K = K
		self.ANG87 = ANG87
		self.LPP87 = LPP87

	def diff(self, Iloc, Irem):
		return np.abs(Iloc + Irem)

	def trip(self, Iloc, Irem):
		"""The trip decision
		"""
		out = 'No Op'
		if self.diff(Iloc, Irem) > self.LPP87:
			if np.abs(Iloc) > 0.05:
				if np.abs(Irem) > 0.05:
					if Iloc / Irem < - self.K:
						out = 'Trip'
					elif Iloc / Irem > - 1 / self.K:
						out = 'Trip'
				else:
					out = 'Trip'
			else:
				out = 'Trip'
		return out

	def table(self, outflow=1):
		"""the table function returns a table of results that show the resistive
		coverage for different voltages and CT ratios. By changing the outflow value
		from 1.0pu the system can be tested for different sensitivities.
			Inputs:
					outflow = amount of current leaving the remote end 1.0pu default
					K1 = Diff characteristic slope 1
					K2 = Diff characteristic slope 2
					IS2 = Slope 1 to 2 change over
					IS1  = Pickup
		"""
		voltages = [11, 22, 33, 66, 110, 132, 220]
		cts = [100, 200, 400, 600, 800, 1200, 2000]
		# Create and print a header row
		hdr = '{:<8}'.format('CT Ratio')
		for ct in cts:
			hdr = hdr + str('{:8d}'.format(ct))
		print(hdr)

		for voltage in voltages:
			vals = '{:<8}'.format(voltage)
			for ct in cts:
				PUDiff = self.sysvals(Irem=-outflow)['Diff']
				Z = 1000 * voltage / (np.sqrt(3) * ct * PUDiff)
				vals = vals + ' ' + str('{:7.2f}'.format(Z))
			print(vals)
		return{
			'87LANG': self.ANG87,
			'K': self.K,
			}

	def sysvals(self, Irem=-1):
		"""sysvalues are used to calculate the operating point given a characteristic
		and remote outflow current.
			Inputs:
					Irem = Remote Current (this should be set negative to show outflow)
			Output is a dictionary that contains, Local and Remote Currents, Diff and
			Restraint
		"""
	
		Iloc = - Irem
		while self.trip(Iloc, Irem) == 'No Op':
			Iloc += 0.01
		return{
			'Iloc': round(Iloc, 4),
			'Irem': round(Irem, 4),
			'Diff': round(self.diff(Iloc, Irem), 4)
			}

	def plotpairs(self, ascending=True, plotrange=10):
		xvals = []
		yvals = []
		diffvals = []
		for i in range(plotrange * 100):
			Irem = i / 100
			Iloc = - Irem
			while self.trip(Iloc, Irem) == 'No Op':
				if ascending:
					Iloc += 0.01
				else:
					Iloc -= 0.01
			xvals.append(Irem)
			yvals.append(-Iloc)
			diffvals.append(self.diff(Iloc, Irem))
		return xvals, yvals, diffvals


def plotcurve(device, plotrange=10):
	fig = plt.figure()
	plt.plot(
		device.plotpairs(
				ascending=False,
				plotrange=plotrange
				)[0],
		device.plotpairs(
				ascending=False,
				plotrange=plotrange
				)[1]
		)
	plt.plot(
		device.plotpairs(
				plotrange=plotrange
				)[0],
				device.plotpairs(
				plotrange=plotrange
				)[1]
				)
	plt.xlim(0, plotrange)
	plt.ylim(0, plotrange)
	plt.grid(True)
	fig.suptitle('Diff Operating Envelope')
	plt.xlabel('Remote Current')
	plt.ylabel('Local Current')
	plt.show()


def printcurves(device, voltage):
	fig = plt.figure()
	cts = [100, 200, 400, 600, 800, 1200, 2000]
	
	for ct in cts:
		xvals = []
		yvals = []
		for i in range(20, 1001):
			xvals.append(i / 1000)
			yvals.append(voltage / (np.sqrt(3) * ct * device.sysvals(-i / 1000)['Diff']))
		plt.plot(xvals, yvals, label=str(ct))
	fig.suptitle('Voltage ' + str(voltage / 1000) + 'kV')
	plt.legend(title='CT Prim')
	plt.xlabel('Per Unit Current')
	plt.ylabel('Resistance (ohms)')
	plt.grid(True)
	plt.show()
