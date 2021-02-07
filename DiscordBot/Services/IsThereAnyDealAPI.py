#!python3
# coding: utf-8


"""
IsThereAnyDeal API response parsers
"""


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


class SearchEndpoint(IsThereAnyDealErrorResponse):
    """
    IsThereAnyDeal API Search endpoint parser

    All properties can be None if the value can't be retrieved from the IsThereAnyDeal API

    Attributes
    ----------
    id : int or None
        IsThereAnyDeal API game id
    plain : str or None
        IsThereAnyDeal API game identifier
    title : str or None
        Game name
    """

    def __init__(self, response_dict):
        """
        IsThereAnyDeal API Search endpoint init

        Parameters
        ----------
        response_dict : dict
            parsed json obtained from IsThereAnyDeal API Search endpoint
        """
        super().__init__(response_dict)

        self.id = None
        self.plain = None
        self.title = None

        if 'data' in response_dict:
            if 'results' in response_dict['data']:
                result = response_dict['data']['results'][0]  # only the first result is relevant
                self.id = result.get('id')
                self.plain = result.get('plain')
                self.title = result.get('title')


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

        if 'data' in response_dict:
            for game in response_dict['data'].values():  # assumes only one game
                self.title = game.get('title')
                self.image_url = game.get('image')
                self.is_dlc = game.get('is_dlc')

                if 'reviews' in game:
                    self.steam_review = SteamReview(game['reviews'].get('steam'))


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

        if 'shop' in game_shop_dict:
            shop = game_shop_dict['shop']
            self.id = shop.get('id')
            self.name = shop.get('name')

        self.game_url = game_shop_dict.get('url')
        self.price_full = game_shop_dict.get('price_old')
        self.price_discounted = game_shop_dict.get('price_new')
        self.price_percent_discount = game_shop_dict.get('price_cut')

        drm_list = game_shop_dict.get('drm')
        if drm_list is not None:
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

        if 'data' in response_dict:
            for shop_list in response_dict['data'].values():  # assumes only one game
                if 'list' in shop_list:
                    shops = shop_list['list']

                    self.shops = []
                    for shop in shops:
                        self.shops.append(ShopInfo(shop))


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
        self.currency = '€'

        if 'data' in response_dict:
            for shop_info in response_dict['data'].values():  # assumes only one shop
                if 'shop' in shop_info:
                    shop = shop_info['shop']
                    self.id = shop.get('id')
                    self.name = shop.get('name')
                self.price = shop_info.get('price')

