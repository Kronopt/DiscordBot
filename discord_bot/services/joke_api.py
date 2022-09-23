#!python3
# coding: utf-8


"""
JokeApi Joke container
"""


from datetime import datetime


class JokeApiError(Exception):
    """
    JokeAPI error

    Attributes
    ----------
    error_code : int
        JokeAPI error code
    error_message : str or None
        Error message
    caused_by : list[str] or None
        Error causes
    additional_info : str or None
        More information regarding the error
    """

    def __init__(
        self,
        error_code: int | None,
        error_message: str | None,
        caused_by: list[str] | None,
        additional_info: str | None,
    ):
        super().__init__()
        self.error_code = error_code
        self.error_message = error_message
        self.caused_by = "; ".join(caused_by) if caused_by is not None else ""
        self.additional_info = additional_info

    def __str__(self):
        return (
            f"Received JokeAPI error {self.error_code}: {self.error_message}. Caused by: "
            f"{self.caused_by}. Additional info: {self.additional_info}"
        )


class JokeApiJoke:
    """
    JokeApi Joke container

    All properties can be None if the value can't be retrieved from the JokeApi API

    Attributes
    ----------
    id : int or None
        joke id
    category : str or None
        joke category
    type : str or None
        'twopart' or 'single' denoting if the joke is divided in setup/punchline or not
    joke : str or None
        joke (if type == 'single')
    setup : str or None
        setup part of joke (if type == 'twopart')
    delivery : str or None
        punchline part of joke (if type == 'twopart')
    flags : dict{str: bool} or None
        'nsfw', 'religious', 'political', 'racist' and 'sexist'
    lang : str or None
        language
    error : bool or None
        if JokeApi returned an error
    internal_error : bool or None
        if the given error was internal
    error_code : int or None
        JokeApiJoke error code
    error_message : str or None
        Error message
    caused_by : list[str] or None
        Error causes
    additional_info : str or None
        More information regarding the error
    timestamp : datetime.datetime or None
        date when the error occurred
    """

    def __init__(self, response_dict: dict):
        """
        JokeApiJoke init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from JokeApi API
        """
        self.id = response_dict.get("id")
        self.category = response_dict.get("category")
        self.type = response_dict.get("type")
        self.joke = response_dict.get("joke")
        self.setup = response_dict.get("setup")
        self.delivery = response_dict.get("delivery")
        self.flags = response_dict.get("flags")
        self.lang = response_dict.get("lang")

        # error related
        self.error = response_dict.get("error")
        self.internal_error = response_dict.get("internalError")
        self.error_code = response_dict.get("code")
        self.error_message = response_dict.get("message")
        self.caused_by = response_dict.get("causedBy")
        self.additional_info = response_dict.get("additionalInfo")
        self.timestamp = self._parse_unix_timestamp(response_dict.get("timestamp"))

        if self.error is True:
            raise JokeApiError(
                self.error_code,
                self.error_message,
                self.caused_by,
                self.additional_info,
            )

    @staticmethod
    def _parse_unix_timestamp(timestamp: float | None) -> float | datetime | None:
        return datetime.fromtimestamp(timestamp / 1000) if timestamp else timestamp

    def text(self) -> str | None:
        """
        Returns just the joke text

        Returns
        -------
        srt
            joke
        """
        return f"{self.setup}\n{self.delivery}" if self.type == "twopart" else self.joke
