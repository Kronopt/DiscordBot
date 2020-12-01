#!python3
# coding: utf-8


"""
External API communication handler
"""


import aiohttp
import json


class HttpError(Exception):
    """
    HTTP status code received was not 200 OK

    Attributes
    ----------
    status_code : int
        http status code
    message : str
        http text corresponding to status code
    """
    def __init__(self, status_code, message):
        super().__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f'Received HTTP status code {self.status_code}: {self.message}. Expected 200: OK'


class APICommunicationHandler:
    """
    External API communication handler
    """

    def __init__(self, api_name, base_url, headers, joke_container):
        self.name = api_name
        self.url = base_url
        self.headers = headers
        self.joke_container = joke_container

    async def random_joke(self):
        """
        Retrieves a random joke

        Returns
        -------
        self.joke_container
            joke container class
        """
        response = await self._request()
        joke = await self._parse_response(response)
        return joke

    async def _request(self):
        """
        Handles asynchronous http requests with the external API

        Returns
        -------
        str
            external API json response as str

        Raises
        ------
        aiohttp.ClientResponseError, aiohttp.ClientConnectionError
            If an http error, timeout, etc, occurs
        HttpError
            If an http code different from 200 is returned
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.url) as response:
                if response.status != 200:
                    raise HttpError(response.status, response.reason)
                response_json = await response.text()

        return response_json

    async def _parse_response(self, response_json):
        """
        Parses the external API response into a joke container object

        Parameters
        ----------
        response_json : str
            external API json response as str

        Returns
        -------
        self.joke_container
            joke container class
        """
        return json.loads(response_json, object_hook=self.joke_container)

    def __repr__(self):
        return self.name
