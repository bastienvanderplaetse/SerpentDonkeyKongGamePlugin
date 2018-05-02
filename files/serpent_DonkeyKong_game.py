from serpent.game import Game

from .api.api import DonkeyKongAPI

from serpent.utilities import Singleton

from xml.dom import minidom


class SerpentDonkeyKongGame(Game, metaclass=Singleton):

    def __init__(self, **kwargs):
        kwargs["platform"] = "executable"

        try:
            doc = minidom.parse('donkeykong_config.xml')

            kwargs["window_name"] = doc.getElementsByTagName("title")[0].firstChild.nodeValue

            kwargs["executable_path"] = doc.getElementsByTagName("emulator")[0].firstChild.nodeValue + " " + doc.getElementsByTagName("game")[0].firstChild.nodeValue

            super().__init__(**kwargs)

            self.api_class = DonkeyKongAPI
            self.api_instance = None

        except FileNotFoundError:
            self._create_config_file()

    def _create_config_file(self):
        print("No config file found.\nCreation of the default config file.")
        doc = minidom.Document()

        config = doc.createElement('config')
        
        title = doc.createElement('title')
        title.appendChild(doc.createTextNode('WINDOW_NAME'))
        config.appendChild(title)

        path = doc.createElement('path')

        emulator = doc.createElement('emulator')
        emulator.appendChild(doc.createTextNode('EMULATOR_PATH'))
        path.appendChild(emulator)

        game = doc.createElement('game')
        game.appendChild(doc.createTextNode('GAME_PATH'))
        path.appendChild(game)

        config.appendChild(path)

        doc.appendChild(config)

        doc.writexml(open('donkeykong_config.xml', 'w'), indent="    ", addindent="  ", newl='\n')

        print("IMPORTANT : donkeykong_config.xml file created. Please change the default values to use the API.")

    @property
    def screen_regions(self):
        regions = {
            "SAMPLE_REGION": (0, 0, 0, 0)
        }

        return regions

    @property
    def ocr_presets(self):
        presets = {
            "SAMPLE_PRESET": {
                "extract": {
                    "gradient_size": 1,
                    "closing_size": 1
                },
                "perform": {
                    "scale": 10,
                    "order": 1,
                    "horizontal_closing": 1,
                    "vertical_closing": 1
                }
            }
        }

        return presets
