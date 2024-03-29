#!python3
# coding: utf-8


"""
External API communication handler
"""


import json
from typing import Callable, Mapping, Any
import aiohttp


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

    def __init__(self, status_code: int, message: str):
        super().__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"Received HTTP status code {self.status_code}: {self.message}. Expected 200: OK"


class APICommunicationHandler:
    """
    External API communication handler

    Attributes
    ----------
    name : str
        API name
    base_url : str
        API base url
    headers : list
        Headers to send with http request
    json_parser : class/function
        Class/Function which parses the json response dict
    error_parser : class/function or None
        Class/function which parses the error json response dict.
        If set, it will be called when an http code != 200 occurs and no HttpError will be raised,
        otherwise an HttpError will be raised
    """

    def __init__(
        self,
        api_name: str,
        base_url: str,
        headers: Mapping[str, str],
        json_parser: Callable,
        error_parser: Callable | None = None,
    ):
        self.name = api_name
        self.base_url = base_url if not base_url.endswith("/") else base_url[:-1]
        self.headers = headers
        self.json_parser = json_parser
        self.error_parser = error_parser

    async def call_api(self, endpoint_url: str | None = None) -> Any:
        """
        Calls the API endpoint

        Attributes
        ----------
        endpoint_url : str
            endpoint to add to base_url

        Returns
        -------
        Output of json_parser
        """
        response, http_status_code, http_status_reason = await self._request(
            endpoint_url
        )
        parsed_response = await self._parse_response(
            response, http_status_code, http_status_reason
        )
        return parsed_response

    async def _request(self, endpoint_url: str | None = None) -> tuple[str, int, str]:
        """
        Handles asynchronous http requests with the external API

        Attributes
        ----------
        endpoint_url : str or None
            endpoint to add to base_url

        Returns
        -------
        str
            external API json response as str
        int
            http status code
        str
            http status reason

        Raises
        ------
        aiohttp.ClientResponseError, aiohttp.ClientConnectionError
            If an http error, timeout, etc, occurs
        HttpError
            If an http code different from 200 is returned
        """
        url = self.base_url

        if endpoint_url:
            url += endpoint_url

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                reason = response.reason if response.reason is not None else ""
                if response.status != 200 and not self.error_parser:
                    raise HttpError(response.status, reason)
                response_json = await response.text()

        return response_json, response.status, reason

    async def _parse_response(
        self, response_json: str, http_status_code: int, http_status_reason: str
    ) -> Any:
        """
        Parses the external API response using the json_parser

        Parameters
        ----------
        response_json : str
            external API json response as str
        http_status_code : int
            http status code
        http_status_reason : str
            http status reason

        Returns
        -------
        Output of json_parser
        """
        try:
            response = json.loads(response_json)

        except json.JSONDecodeError as err:
            if http_status_code != 200:
                raise HttpError(http_status_code, http_status_reason) from err
            raise err

        if http_status_code == 200:
            return self.json_parser(response)
        if self.error_parser:
            return self.error_parser(response)

    def __repr__(self):
        return self.name
