import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'map':
        from kivy.config import Config
        Config.set('graphics', 'fullscreen', False)
        Config.set('graphics', 'width', 1000)
        Config.set('graphics', 'height', 700)
        Config.set('graphics', 'resizable', False)
        Config.write()

        from src import JDMApp
        from mapmaker import MapScreen, MapMaker
        JDMApp("MapMaker", (1000, 700)).run(screen=MapScreen(), widget=MapMaker())
    else:
        from kivy.config import Config
        Config.set('graphics', 'fullscreen', 'auto')
        Config.set('graphics', 'resizable', False)
        Config.write()

        from src import MainField, MainScreen, JDMApp
        from mapmaker import MapScreen
        JDMApp("RPG-Game", None).run(screen_name="main", screen=MainScreen(), widget=MainField())
