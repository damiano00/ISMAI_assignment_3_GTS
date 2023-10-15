import abc


class Agent(abc.ABC):

    def __init__(self, params, name):
        self._params = params
        self._name = self._params.get('name', name)

    def name(self):
        """ Return agent's name."""
        return self._name

    def reset(self):
        """ Reset any information kept between play calls. """
        pass

    @abc.abstractmethod
    def play(self, game):
        """ Return a move to play in a given game state. """
        pass
