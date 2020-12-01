#!python3
# coding: utf-8


"""
ICanHazDadJoke Joke container
"""


from DiscordBot.Services.ExternalAPIHandler import HttpError


class DadJoke:
    """
    Dad Joke container

    All properties can be None if the value can't be retrieved from the icanhazdadjoke API

    Attributes
    ----------
    id : str or None
        icanhazdadjoke joke id
    joke : str or None
        joke
    status : int or None
        http status code
    """

    def __init__(self, response_dict):
        """
        DadJoke init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from icanhazdadjoke API
        """
        self.id = response_dict.get('id')
        self.joke = response_dict.get('joke')
        self.status = response_dict.get('status')

        if self.status != 200:
            raise HttpError(self.status, '-')

    def text(self):
        """
        Returns just the joke text

        Returns
        -------
        srt
            joke
        """
        return self.joke
