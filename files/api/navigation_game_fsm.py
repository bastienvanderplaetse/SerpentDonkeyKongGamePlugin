from fysom import FysomGlobal, FysomGlobalMixin

class NavigationGameFSM(FysomGlobalMixin, object):

	GSM = FysomGlobal(
			initial = 'not_running',
			events = [
				{
					'name': 'run',
					'src': ['not_running', 'has_won', 'dead'],
					'dst': 'menu'
				},
				('win', 'playing', 'has_won'),
				('next', 'menu', 'black_screen'),
				('play', 'black_screen', 'playing'),
				('die', 'playing', 'dead')
			],
			state_field = 'state'
		)

	def __init__(self):
		self.state = None
		super(NavigationGameFSM, self).__init__()