def syschecks(master=True, 
							LineVT=True,
							BusVT=True,
							RemoteStatus='available'):
	""" the syschecks function is intended to configure the MiCOM P543 relay for a
	suitable reclosing method. The inputs for the function are:
		
		master: (Default is True) set True if the end being considered is the master
						set False when used as a slave end
		LineVT: (Default is True) set True when a Line VT is fitted
						set False when  a line VT is not available
		BusVT: (Default is True) set True when a Bus VT is fitted
						set False when  a Bus VT is not available
		RemoteStatus:	set 'available' when a remote status is available
	"""	
	Disabled = 'Disabled'
	Enabled = 'Enabled'
	Unset = 'Not required'

	# for testing --- remove
	
	SystemChecks = Unset
	CS1Status = Unset
	CBSCall = Unset
	CBSCDLLB = Unset
	CBSCLLDB = Unset
	CBSCCS1 = Unset
	CtrlSetgIP35 = Unset  # this bit is used to block remote system check commands
	CtrlSetgIP36 = Unset  # allows closing live line based on remote status
	CtrlSetgIP37 = Unset  # allows closing dead line based on remote status
	CtrlSetgIP38 = Unset  # set when no line VT fitted and bus must be dead
	comment="""-"""
				
	if master:
		if LineVT:
			# dont have to worry about a bus vt being presents as the master close on deadline is OK
			SystemChecks = Enabled
			CS1Status = Disabled
			CBSCall = Enabled
			CBSCDLLB = Enabled
			CBSCLLDB = Disabled
			CBSCDLDB = Enabled
			CBSCCS1 = Disabled
			CtrlSetgIP35 = Enabled
			CtrlSetgIP36 = Disabled
			CtrlSetgIP37 = Disabled
			CtrlSetgIP38 = Disabled
			
			comment = """When a line VT is fitted to the master end reclosing is allowed for any 
			condition that has a dead line (both live and dead bus)."""
				
		elif not LineVT and RemoteStatus == 'available':
			# check with the remote status
			SystemChecks = Enabled
			CS1Status = Disabled
			CBSCall = Disabled
			CBSCDLLB = Unset
			CBSCLLDB = Unset
			CBSCDLDB = Unset
			CBSCCS1 = Unset
			CtrlSetgIP35 = Disabled
			CtrlSetgIP36 = Enabled
			CtrlSetgIP37 = Disabled
			CtrlSetgIP38 = Disabled
		
		elif not LineVT and not RemoteStatus == 'available':
			# where no checks are possible for the master end
			SystemChecks = Disabled
			CS1Status = Unset
			CBSCall = Disabled
			CBSCDLLB = Unset
			CBSCLLDB = Unset
			CBSCDLDB = Unset
			CBSCCS1 = Unset
			CtrlSetgIP35 = Disabled
			CtrlSetgIP36 = Disabled
			CtrlSetgIP37 = Disabled
			CtrlSetgIP38 = Disabled
			
	elif not master:
		if LineVT and BusVT:
			# all close for live line, dead bus and system checks OK
			SystemChecks = Enabled
			CS1Status = Enabled
			CBSCall = Enabled
			CBSCDLLB = Disabled
			CBSCLLDB = Enabled
			CBSCDLDB = Disabled
			CBSCCS1 = Enabled
			CtrlSetgIP35 = Enabled
			CtrlSetgIP36 = Disabled
			CtrlSetgIP37 = Disabled
			CtrlSetgIP38 = Disabled
		
		elif not LineVT and BusVT and RemoteStatus == 'available':
			SystemChecks = Enabled
			CS1Status = Disabled
			CBSCall = Disabled
			CBSCDLLB = Unset
			CBSCLLDB = Unset
			CBSCDLDB = Unset
			CBSCCS1 = Disabled
			CtrlSetgIP35 = Disabled
			CtrlSetgIP36 = Enabled
			CtrlSetgIP37 = Disabled
			CtrlSetgIP38 = Disabled
	
# do we need to block for a live bus when as a slave?
# mesh network no - new network would have VTs
# and would be able to do a dead check, check syn check.
		elif not LineVT and BusVT and not RemoteStatus == 'available':
			pass
	
	return {'System Checks': SystemChecks
						, 'CS1 Status': CS1Status
						, 'CB SC all': CBSCall
						, 'CB SC DLLB': CBSCDLLB
						, 'CB SC LLDB': CBSCLLDB
						, 'CB SC DLDB': CBSCDLDB
						, 'CB SC CS1': CBSCCS1
						, 'Ctrl Setg I/P 35': CtrlSetgIP35
						, 'Ctrl Setg I/P 36': CtrlSetgIP36
						, 'Ctrl Setg I/P 37': CtrlSetgIP37
						, 'Ctrl Setg I/P 38': CtrlSetgIP38
						, 'comment': comment}
