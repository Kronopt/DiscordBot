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

    Attributes
    ----------
    name : str
        API name
    url : str
        API endpoint url
    headers : list
        Headers to send with http request
    json_parser : class/function
        Class/Function which parses the json response dict
    """

    def __init__(self, api_name, url, headers, json_parser):
        self.name = api_name
        self.url = url
        self.headers = headers
        self.json_parser = json_parser

    async def call_api(self):
        """
        Calls the API endpoint

        Returns
        -------
        Output of json_parser
        """
        response = await self._request()
        parsed_response = await self._parse_response(response)
        return parsed_response

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
        Parses the external API response using the json_parser

        Parameters
        ----------
        response_json : str
            external API json response as str

        Returns
        -------
        Output of json_parser
        """
        return json.loads(response_json, object_hook=self.json_parser)

    def __repr__(self):
        return self.name
