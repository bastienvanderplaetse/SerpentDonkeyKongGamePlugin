from serpent.game_api import GameAPI


class DonkeyKongAPI(GameAPI):

    def __init__(self, game=None):
        super().__init__(game=game)

    

    class MyAPINamespace:

        @classmethod
        def my_namespaced_api_function(cls):
            api = DonkeyKongAPI.instance