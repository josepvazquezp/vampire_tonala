from abc import ABC, abstractmethod

class State(ABC):
    ''' Clase que establece los estados del juego '''

    def __init__(self, maingame, name) -> None:
        self.maingame = maingame #Conexión a la partida
        self.name = name

    @abstractmethod
    def change_to_play(self):
        ''' Estado de jugar '''
        pass

    @abstractmethod
    def change_to_level_up(self):
        ''' Estado de subir de nivel '''
        pass

    @abstractmethod
    def change_to_chest(self):
        ''' Estado de cofre '''
        pass

    @abstractmethod
    def change_to_pause(self):
        ''' Estado de pausa '''
        pass

    @abstractmethod
    def change_to_game_over(self):
        ''' Estado de fin del juego '''
        pass


class PlayState(State):
    ''' Estado de juego principal '''

    def __init__(self, maingame) -> None:
        super().__init__(maingame, "Play")

    def change_to_play(self):
        ''' Estado de jugar '''
        pass

    def change_to_level_up(self):
        ''' Estado de subir de nivel '''
        self.maingame.change_state(LevelUpState(self.maingame))

    def change_to_chest(self):
        ''' Estado de cofre '''
        self.maingame.change_state(ChestState(self.maingame))

    def change_to_pause(self):
        ''' Estado de pausa '''
        self.maingame.change_state(PauseState(self.maingame))

    def change_to_game_over(self):
        ''' Estado de fin del juego '''
        self.maingame.change_state(GameOverState(self.maingame))

class LevelUpState(State):
    ''' Estado de subida de nivel '''

    def __init__(self, maingame) -> None:
        super().__init__(maingame, "Level")

    def change_to_play(self):
        ''' Estado de jugar '''
        self.maingame.change_state(PlayState(self.maingame))


    def change_to_level_up(self):
        ''' Estado de subir de nivel '''
        pass

    def change_to_chest(self):
        ''' Estado de cofre '''
        pass

    def change_to_pause(self):
        ''' Estado de pausa '''
        pass

    def change_to_game_over(self):
        ''' Estado de fin del juego '''
        pass


class ChestState(State):
    ''' Estado de Cofre '''

    def __init__(self, maingame) -> None:
        super().__init__(maingame, "Chest")

    def change_to_play(self):
        ''' Estado de jugar '''
        self.maingame.change_state(PlayState(self.maingame))

    def change_to_level_up(self):
        ''' Estado de subir de nivel '''
        pass

    def change_to_chest(self):
        ''' Estado de cofre '''

    def change_to_pause(self):
        ''' Estado de pausa '''
        pass

    def change_to_game_over(self):
        ''' Estado de fin del juego '''
        pass


class PauseState(State):
    ''' Estado de pausa '''

    def __init__(self, maingame) -> None:
        super().__init__(maingame, "Pause")

    def change_to_play(self):
        ''' Estado de jugar '''
        self.maingame.change_state(PlayState(self.maingame))


    def change_to_level_up(self):
        ''' Estado de subir de nivel '''
        pass

    def change_to_chest(self):
        ''' Estado de cofre '''
        pass

    def change_to_pause(self):
        ''' Estado de pausa '''
        pass

    def change_to_game_over(self):
        ''' Estado de fin del juego '''
        pass


class GameOverState(State):
    ''' Estado de fin del juego '''

    def __init__(self, maingame) -> None:
        super().__init__(maingame, "Over")

    def change_to_play(self):
        ''' Estado de jugar '''
        pass

    def change_to_level_up(self):
        ''' Estado de subir de nivel '''
        pass

    def change_to_chest(self):
        ''' Estado de cofre '''
        pass

    def change_to_pause(self):
        ''' Estado de pausa '''
        pass

    def change_to_game_over(self):
        ''' Estado de fin del juego '''
        pass