#!python3
# coding: utf-8


"""
IsThereAnyDeal API response parsers
"""


import datetime


class IsThereAnyDealError(Exception):
    """
    IsThereAnyDeal error

    Attributes
    ----------
    error : str
    error_description : str or None
    """
    def __init__(self, error, error_description):
        super().__init__()
        self.error = error
        self.error_description = error_description

    def __str__(self):
        return f'Received IsThereAnyDeal error "{self.error}": {self.error_description}'


class IsThereAnyDealErrorResponse:
    """
    IsThereAnyDeal API error response parser

    Attributes
    ----------
    error : str or None
    error_description : str
    """

    def __init__(self, response_dict):
        """
        IsThereAnyDeal API error response init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from IsThereAnyDeal API (any endpoint)
        """
        self.error = response_dict.get('error')
        self.error_description = response_dict.get('error_description', '')

        if self.error:
            raise IsThereAnyDealError(self.error, self.error_description)


class IdentifierEndpoint(IsThereAnyDealErrorResponse):
    """
    IsThereAnyDeal API Identifier endpoint parser

    All properties can be None if the value can't be retrieved from the IsThereAnyDeal API

    Attributes
    ----------
    plain : str or None
        IsThereAnyDeal API game identifier
    """

    def __init__(self, response_dict):
        """
        IsThereAnyDeal API Identifier endpoint init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from IsThereAnyDeal API Identifier endpoint
        """
        super().__init__(response_dict)

        self.plain = None

        if 'data' in response_dict and response_dict['data']:
            self.plain = response_dict['data'].get('plain')


class SteamReview:
    """
    Steam review data

    Attributes
    ----------
    text: str or None
        Review text
    total_reviews: int or None
        Total reviews
    positive_reviews_percent: int or None
        Percentage of all reviews that are positive
    """

    def __init__(self, steam_review_dict):
        """
        SteamReview init

        Parameters
        ----------
        steam_review_dict : dict
            parsed json obtained from IsThereAnyDeal API GetInfoAboutGame endpoint, reviews field
        """
        self.text = steam_review_dict.get('text')
        self.total_reviews = steam_review_dict.get('total')
        self.positive_reviews_percent = steam_review_dict.get('perc_positive')


class GetInfoAboutGameEndpoint(IsThereAnyDealErrorResponse):
    """
    IsThereAnyDeal API GetInfoAboutGame endpoint parser

    All properties can be None if the value can't be retrieved from the IsThereAnyDeal API

    Attributes
    ----------
    title : str or None
        Game name
    image_url : str or None
        Game image url
    is_dlc : bool or None
        If game is a DLC
    steam_review: SteamReview or None
        Steam review data
    """

    def __init__(self, response_dict):
        """
        IsThereAnyDeal API GetInfoAboutGame endpoint init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from IsThereAnyDeal API GetInfoAboutGame endpoint
        """
        super().__init__(response_dict)

        self.title = None
        self.image_url = None
        self.is_dlc = None
        self.steam_review = None

        if 'data' in response_dict and response_dict['data']:
            data = response_dict['data']
            for game in data.values():  # assumes only one game
                self.title = game.get('title')
                self.image_url = game.get('image')
                self.is_dlc = game.get('is_dlc')

                if 'reviews' in game and game['reviews']:
                    self.steam_review = SteamReview(game['reviews'].get('steam'))
                break


class ShopInfo:
    """
    Game shop data

    Attributes
    ----------
    id : str or None
        IsThereAnyDeal API shop id
    name : str or None
        Shop name
    game_url : str or None
        Game url for this store
    price_full : float or None
        Game's full price
    price_discounted : float or None
        Game's price with discount
    price_percent_discount : int or None
        Game's price discount percentage
    drm : list[str]
        DRM for this game in this store
    """

    def __init__(self, game_shop_dict):
        """
        ShopInfo init

        Parameters
        ----------
        game_shop_dict : dict
            parsed json obtained from IsThereAnyDeal API GetCurrentPrices endpoint,
            list field single entry
        """
        self.id = None
        self.name = None
        self.game_url = None
        self.price_full = None
        self.price_discounted = None
        self.price_percent_discount = None
        self.drm = None

        if 'shop' in game_shop_dict and game_shop_dict['shop']:
            shop = game_shop_dict['shop']
            self.id = shop.get('id')
            self.name = shop.get('name')

        self.game_url = game_shop_dict.get('url')
        self.price_percent_discount = game_shop_dict.get('price_cut')

        self.price_full = game_shop_dict.get('price_old')
        if self.price_full:
            self.price_full = round(self.price_full, 2)
        self.price_discounted = game_shop_dict.get('price_new')
        if self.price_discounted:
            self.price_discounted = round(self.price_discounted, 2)

        drm_list = game_shop_dict.get('drm')
        if drm_list:
            self.drm = []
            for drms in drm_list:
                self.drm += drms.split('; ')


class GetCurrentPricesEndpoint(IsThereAnyDealErrorResponse):
    """
    IsThereAnyDeal API GetCurrentPrices endpoint parser

    All properties can be None if the value can't be retrieved from the IsThereAnyDeal API

    Attributes
    ----------
    shops : list[ShopInfo] or None
        Price info per store
    currency : str or None
        Currency of prices
    """

    def __init__(self, response_dict):
        """
        IsThereAnyDeal API GetCurrentPrices endpoint init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from IsThereAnyDeal API GetCurrentPrices endpoint
        """
        super().__init__(response_dict)

        self.shops = None
        self.currency = '€'

        if 'data' in response_dict and response_dict['data']:
            data = response_dict['data']
            for shop_list in data.values():  # assumes only one game
                if 'list' in shop_list and shop_list['list']:
                    shops = shop_list['list']

                    self.shops = []
                    for shop in shops:
                        self.shops.append(ShopInfo(shop))

                break


class GetHistoricalLowEndpoint(IsThereAnyDealErrorResponse):
    """
    IsThereAnyDeal API GetHistoricalLow endpoint parser

    All properties can be None if the value can't be retrieved from the IsThereAnyDeal API

    Attributes
    ----------
    id : str or None
        IsThereAnyDeal API game id
    store : str or None
        Store name
    price : float or None
        Lowest historical price
    date : str or None
        Date of lowest price
    currency : str
        Currency of price
    """

    def __init__(self, response_dict):
        """
        IsThereAnyDeal API GetHistoricalLow endpoint init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from IsThereAnyDeal API GetHistoricalLow endpoint
        """
        super().__init__(response_dict)

        self.id = None
        self.store = None
        self.price = None
        self.date = None
        self.currency = '€'

        if 'data' in response_dict and response_dict['data']:
            data = response_dict['data']
            for shop_info in data.values():  # assumes only one shop
                if 'shop' in shop_info and shop_info['shop']:
                    shop = shop_info['shop']
                    self.id = shop.get('id')
                    self.store = shop.get('name')

                self.price = shop_info.get('price')
                if self.price:
                    self.price = round(self.price, 2)
                self.date = shop_info.get('added')
                if self.date:
                    self.date = datetime.date.fromtimestamp(self.date).isoformat()

                break
