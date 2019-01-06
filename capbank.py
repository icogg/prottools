import numpy as np


class DoubleWyeCapBank:
	"""This class is used to store a capacitor bank and provide the calculations
	in accordance with IEEE Std C37.99-2012. The class is for a fused double wye
	bank. The class calls on a subclass CapCan to provide the details of the cans
	used in the bank.
	"""
	def __init__(self, S, Pt, Pa, P, CapCan, Grounded=False):
		self.S = S
		self.Pt = Pt
		self.Pa = Pa
		self.P = P
		if Grounded:
			self.G = 0
		else:
			self.G = 1
		self.CapCan = CapCan
		
	def Cg(self, f):
		"""The capacitance of the group of capacitors that includes the affected
		unit. For all of the units in that group except the affected unit, the
		per-unit capacitance is 1. For the affected unit, the per-unit capacitance
		is Cu.
		"""
		return (self.P - 1 + self.CapCan.Cu(f)) / self.P
	
	def Cs(self, f):
		"""The per-unit capacitance of the string of (parallel groups of) capacitor
		units from phase to neutral that includes the affected capacitor unit. For
		the group including the affected unit, the per-unit capacitance is Cg. For
		all other groups, the per-unit capacitance is 1.
		"""
		return (self.S * self.Cg(f)) / (self.Cg(f) * (self.S - 1) + 1)

	def Cp(self, f):
		"""The per-unit capacitance of the phase (all parallel strings) that includes
		the affected unit. For this calculation the capacitance of the affected
		string is Cs. The capacitance of all the other strings is 1 per-unit.
		"""
		return ((self.Cs(f) * self.P) + self.Pt - self.P) / self.Pt
		
	def Vng(self, f):
		"""The neutral-to-ground voltage. For grounded banks (G = 0), this voltage is
		always 0. For ungrounded wye banks, the calculation assumes the affected
		phase has a capacitance Cp, and the other two phases each have a per-unit
		capacitance of 1.
		"""
		return self.G * ((3 / (2 + self.Cp(f)))-1)
	
	def Vln(self, f):
		"""The voltage line to neutral across the phase that includes the affected
		unit. With fused units, the operation of the fuse reduces the capacitance of
		that phase and increases the voltage across the affected phase; therefore,
		the numbers are always greater than one except before the operation of the
		fuse on a faulted element.
		"""
		return self.Vng(f) + 1

	def Vcu(self, f):
		"""The actual per-unit voltage on the affected capacitor unit, based on the
		capacitance division of the actual voltage on the affected phase (Vln).
		"""
		if self.Cg(f) == 0:
			r = self.Vln(f) * self.S
		else:
			r = (self.Vln(f) * self.Cs(f)) / self.Cg(f)
		return r
	
	def Ve(self, f):
		"""The actual per-unit voltage on the affected elements, basedon the actual
		voltage on the affected unit."""
		return self.Vcu(f) * self.CapCan.Vg(f)
	
	def Iu(self, f):
		"""The current through the affected capacitor unit, per-unit of the value
		with no fuses blown. The value for SE indicates the power frequency current
		available to blow the fuse on a faulted element. This value may be used to
		estimate the maximum clearing time of the fuse (assuming no discharge from
		parallel elements into the faulted one).
		"""
		return self.Vcu(f) * self.CapCan.Cu(f)

	def Ist(self, f):
		"""The per-unit current in the affected string. This value may be useful for
		differential schemes comparing the current in parallel strings.
		"""
		return self.Cs(f) * self.Vln(f)

	def Iph(self, f):
		"""The current in the affected phase. This equation may be useful for setting
		protection based on phase current.
		"""
		return self.Cp(f) * self.Vln(f)
		
	def Ig(self, f):
		"""IgGIph=−×− For use with protective relay schemes utilizing
		neutral-to-ground current, or the voltage across a low-voltage capacitor in
		the neutral or in each phase. The per-unit change in current to ground is the
		per-unit change in voltage across a low-voltage capacitor in the affected
		phase. It is also the per-unit change in voltage across a low-voltage
		capacitor in the neutral-to-ground connection because the other two phase
		currents do not change in a grounded bank.
		"""
		return (1 - self.G) * (1 - self.Iph(f))

	def In(self, f):
		"""Unbalance current for ungrounded wye-wye banks. [The current is calculated
		assuming the neutral-to-ground (zero sequence) voltage is applied at the
		neutral of the unaffected wye, which is half the of the bank].
		"""
		return (3 * self.Vng(f) * self.G * (self.Pt - self.Pa)) / self.Pt
		
	def Id(self, f):
		"""For grounded wye-wye banks where the difference in the neutral current
		between the two equal wyes is used as a basis for protection. Values are
		per-unit of total phase current (Figure 35).
		"""
		if self.Pt != 2 * self.Pa:
			return 'Invalid Arrangement'
		return self.Vln(f) * (1 - self.Cp(f))

	def printelements(self):
		"""Outputs the per unit values for each element for the range of fuses that
		may operate
		"""
		# list all of the functions that are shown in the standard
		functionlist = [
								'CapCan.Ci', 'CapCan.Vg', 'CapCan.Cu',
								'Cg', 'Cs', 'Cp', 'Vng', 'Vln', 'Vcu', 'Ve',
								'Iu', 'Ist', 'Iph', 'Ig', 'In', 'Id'
								]
		# Create a header row
		hdr = '{:<14}'.format('Element')
		for i in range(self.CapCan.N + 1):
			hdr = hdr + str('{:<7}'.format(i))
		print(hdr)
		
		# add all of the per unit values against the element name
		for item in functionlist:
			vals = '{:<10}'.format(item)
			for i in range(self.CapCan.N + 1):
				try:
					vals = vals + ' ' + str('{:1.4f}'.format(_wrapper(eval('self.' + item), i)))
				except:
					vals = vals + ' ' + 'x.xxxx'
			print(vals)
	
	def ubsetting(self, elelim=1.5, unitlim=1.1):
		"""Calcualate the number of fuses that can operate without stressing the
		adjacent elements and cans. The default liimit is 1.1pu, in some cases the
		user can elect to change this by setting the element limit elelim=1.5 or
		unit limit unitlim=1.1 to another value
		"""
		for fuse in range(self.CapCan.N + 1):
			if self.CapCan.Vg(fuse) < elelim and self.Vcu(fuse) < unitlim:
				pass
			else:
				return print(
						'Blown Fuses {}, Element Voltage {:1.3f}, Unit Voltage {:1.3f}'
						.format(fuse - 1, self.CapCan.Vg(fuse - 1), self.Vcu(fuse), sep=' ')
										)
		return print(self.CapCan.N)


class CapCan:
	def __init__(self, N, Su):
		self.N = N
		self.Su = Su
		
	def Ci(self, f):
		"""The per-unit capacitance of the group, based on the number of blown fuses.
		This formula is not explicitly shown in the standard for H-Bridge banks and
		is reduceded out for the CapCan Cu calculation. This reduction is not made in
		this calculator and is kept as an explicit step.
		"""
		return (self.N - f) / self.N
	
	def Vg(self, f):
		"""The voltage that would occur across the affected group of elements where
		the fuses are blowing if there was 1 per-unit voltage on the capacitor unit.
		For the calculation, the capacitance of all groups except the affected group
		is 1 per-unit. The capacitance of the affected group is Ci.
		"""
		return (self.Su * self.N) / ((self.Su - 1) * (self.N - f) + self.N)
	
	def Cu(self, f):
		"""The capacitance of the affected capacitor unit, assuming all groups except
		the affected group have 1 per-unit capacitance and the affected group has
		the capacitance Ci.
		
		The formula used is a slightly different format to that of the standard as it
		does uses the Ci function and not the elemental parts of Ci.
		"""
		return (self.Su * self.Ci(f)) / (self.Ci(f) * (self.Su - 1) + 1)


class HCapbank():
	"""This class is used to store a capacitor bank and provide the calculations
	in accordance with IEEE Std C37.99-2012. The class is for a fused double wye
	bank. The class calls on a subclass CapCan to provide the details of the cans
	used in the bank.
	"""
	def __init__(self, S, St, Pt, Pa, P, CapCan, Grounded=False):
		self.S = S
		self.St = St
		self.Pt = Pt
		self.Pa = Pa
		self.P = P
		if Grounded:
			self.G = 0
		else:
			self.G = 1
		self.CapCan = CapCan
	
	def Chn(self, f):
		"""The capacitance from the H leg to the neutral or reference end on the
		phase, assuming the capacitance of one healthy capacitor unit is 1 per-unit.
		"""
		return (
						(self.CapCan.Cu(f) + self.P - 1) * self.P /
						((self.CapCan.Cu(f) + self.P - 1) * (self.St - 1) + self.P) +
						((self.Pt - self.P)/self.St)
						)

	def Cp(self, f):
		"""The capacitance of the phase from end to end, assuming the capacitance of
		one healthy capacitor unit is 1 per-unit.
		"""
		return self.Chn(f) * self.Pt / (self.Chn(f) * (self.S - self.St) + self.Pt)
	
	def Vln(self, f):
		"""The voltage across the affected phase, that is, 1 for grounded wye or
		delta, where G = 0. For ungrounded wye, this voltage is the per-unit voltage
		across the affected phase including the effect of the neutral shift from
		capacitance unbalance.
		"""
		return 1 + self.G * ((3 / (2 + self.Cp(f) / self.Cp(0))) - 1)

	def Vh(self, f):
		"""The voltage of the H leg, per-unit of the actual voltage on the affected
		phase.
		"""
		return self.Cp(f) / self.Chn(f)
	
	def Ih(self, f):
		"""The current in the H leg, per-unit of the normal total phase current for a
		 wye-connected or single-phase bank or per-unit of total leg current for a
		 delta bank.
		"""
		return (
						- self.Vln(f) *
						((self.St / self.S) - self.Vh(f)) *
						((1 / (self.S - self.St))+(1 / self.St)) *
						(self.S * (self.Pt - self.Pa) / self.Pt)
						)

	def Vcu(self, f):
		"""The voltage across the affected capacitor unit, per-unit of the value with
		no fuses blown.
		"""
		return (
						self.Vln(f) * self.Vh(f) * self.P * self.S /
						(self.P + (self.St - 1) * (self.CapCan.Cu(f) + self.P - 1))
						)
	
	def Ve(self, f):
		"""The voltage across the remaining elements in the affected element group
		(also the voltage across the blown fuses in that group), per-unit of the
		value with no fuses blown.
		"""
		return (
						self.Vcu(f) * self.CapCan.Su * self.CapCan.N /
						(self.CapCan.Su * (self.CapCan.N - f) + f)
						)

	def Iu(self, f):
		"""The current through the affected capacitor unit, per-unit of the value
		with no fuses blown. The value for SE indicates the power frequency current
		available to blow the fuse on a faulted element. This value may be used to
		estimate the maximum clearing time of the fuse (assuming no discharge from
		parallel elements into the faulted one). 
		"""
		return self.Vcu(f) * self.CapCan.Cu(f)
														
	def printelements(self):
		"""Outputs the per unit values for each element for the range of fuses that
		may operate
		"""
		# list all of the functions that are shown in the standard
		functionlist = [
								'CapCan.Ci', 'CapCan.Cu', 'Chn',
								'Cp', 'Vln', 'Vh',
								'Ih', 'Vcu', 'Ve', 'Iu'
								]
		# Create a header row
		hdr = '{:<14}'.format('Element')
		for i in range(self.CapCan.N + 1):
			hdr = hdr + str('{:<7}'.format(i))
		print(hdr)
		
		# add all of the per unit values against the element name
		for item in functionlist:
			vals = '{:<10}'.format(item)
			for i in range(self.CapCan.N + 1):
				try:
					vals = vals + ' ' + str('{:1.4f}'.format(_wrapper(eval('self.' + item), i)))
				except:
					vals = vals + ' ' + 'x.xxxx'
			print(vals)


def _wrapper(funct, *arg):
	"""A function that returns the assumed function and arguments, this is used
	for the print function so that a list of variables can be simply called.
	"""
	return funct(*arg)


def IBank(BankMVAR, BankkV):
	'''Returns the bank full load current, the bank MVAR is the total MVAR at the
	bank voltage.
	'''
	return BankMVAR * 1000 / (np.sqrt(3) * BankkV)



	


