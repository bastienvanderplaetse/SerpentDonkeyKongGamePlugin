from fysom import FysomGlobal, FysomGlobalMixin

class NavigationGameFSM(FysomGlobalMixin, object):

	def onNext(e):
		e.fsm.life = 3
		print("Life : " + str(e.fsm.life))

	GSM = FysomGlobal(
			initial = 'not_running',
			events = [
				{
					'name': 'run',
					'src': ['not_running', 'lost'],
					'dst': 'menu'
				},
				('next', 'menu', 'black_screen'),
				('play', 'black_screen', 'playing'),
				('die', 'playing', 'dead'),
				{
					'name': 'replay',
					'src': 'dead',
					'dst': 'lost',
					'cond': [
						'end_party', {True: 'is_lost', 'else': 'black_screen'}
					]
				}
			],
			state_field = 'state'
		)

	GSM.life = 3

	def end_party(self, event):
		event.fsm.life = event.fsm.life - 1
		print("end_party : " + str(event.fsm.life))
		return True

	def is_lost(self, event):
		print("is_lost : " + str(event.fsm.life))
		if (event.fsm.life == 0):
			event.fsm.life = 3
			return True
		return False

	def __init__(self):
		self.state = None
		super(NavigationGameFSM, self).__init__()