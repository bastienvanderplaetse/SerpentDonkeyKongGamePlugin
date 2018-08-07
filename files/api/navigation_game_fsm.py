from fysom import FysomGlobal, FysomGlobalMixin

class NavigationGameFSM(FysomGlobalMixin, object):

	def onNext(e):
		e.fsm.life = 3

	GSM = FysomGlobal(
			initial = 'not_running',
			events = [
				{
					'name': 'run',
					'src': ['not_running', 'lost', 'has_won', 'playing', 'dead'],
					'dst': 'menu',
					'cond': [
						'tautology', {True: 'reset_life', 'else': 'menu'}
					]
				},
				('win', 'playing', 'has_won'),
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

	def tautology(self, event):
		return True

	def reset_life(self, event):
		event.fsm.life = 3
		return True

	def end_party(self, event):
		event.fsm.life = event.fsm.life - 1
		return True

	def is_lost(self, event):
		if (event.fsm.life == 0):
			event.fsm.life = 3
			return True
		return False

	def __init__(self):
		self.state = None
		super(NavigationGameFSM, self).__init__()