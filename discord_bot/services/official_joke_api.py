#!python3
# coding: utf-8


"""
OfficialJokeApi Joke container
"""


class OfficialJoke:
    """
    OfficialJokeApi Joke container

    All properties can be None if the value can't be retrieved from the OfficialJokeApi API

    Attributes
    ----------
    id : int or None
        OfficialJokeApi joke id
    type : str or None
        joke type/category
    setup : str or None
        joke setup
    punchline : str or None
        joke punchline
    """

    def __init__(self, response_dict: dict):
        """
        OfficialJoke init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from OfficialJokeApi API
        """
        self.id = response_dict.get("id")
        self.type = response_dict.get("type")
        self.setup = response_dict.get("setup")
        self.punchline = response_dict.get("punchline")

    def text(self) -> str:
        """
        Returns just the joke text

        Returns
        -------
        srt
            joke
        """
        return f"{self.setup}\n{self.punchline}"
