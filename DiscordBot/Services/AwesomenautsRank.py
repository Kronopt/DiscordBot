#!python3
# coding: utf-8


"""
Awesomenauts ranking information
"""


import discord
import flag
import pycountry


class AwesomenautsRank:
    """
    Awesomenauts ranking information

    Attributes
    ----------
    player_name : str
        player name
    rank : int
        player rank for current season
    games_played_current_season : int
        games played during the current season
    games_played_all_time : int
        total games played
    win_percentage : float
        percentage of games won
    rating : int
        awesomenauts league rating
    league : str
        current league
    league_img_url : str
        current league image url
    favourite_naut : str
        favourite awesomenaut's name
    favourite_naut_img_url : str
        favourite awesomenaut image url
    country : str
        player's country
    country_flag : str
        country flag emoji
    steam_profile_url : str
        player's steam profile url
    """

    def __init__(self, embed_colour, rank_info):
        """
        AwesomenautsRank init

        Parameters
        ----------
        embed_colour : int
            colour of embed
        rank_info : dict
            dictionary containing all attributes as string (except country_flag)
        """
        self.player_name = rank_info.get("player_name", "")
        self.rank = int(rank_info.get("rank", 0))
        self.games_played_current_season = int(
            rank_info.get("games_played_current_season", 0)
        )
        self.games_played_all_time = int(rank_info.get("games_played_all_time", 0))
        self.win_percentage = float(rank_info.get("win_percentage", 0))
        self.rating = int(rank_info.get("rating", 0))
        self.league = rank_info.get("league", "")
        self.league_img_url = rank_info.get("league_img_url", "")
        self.favourite_naut = rank_info.get("favourite_naut", "")
        self.favourite_naut_img_url = rank_info.get("favourite_naut_img_url", "")
        self.country = rank_info.get("country", "")
        self.steam_profile_url = rank_info.get("steam_profile_url", "")

        if self.country:
            country = pycountry.countries.search_fuzzy(self.country)[0]
            self.country_flag = flag.flag(country.alpha_2)
        else:
            self.country_flag = ""

        self.embed = self.create_awesomenauts_rank_embed(embed_colour)

    def create_awesomenauts_rank_embed(self, embed_colour):
        embed = discord.Embed(colour=embed_colour)
        embed.set_author(name=self.player_name, url=self.steam_profile_url)
        embed.set_thumbnail(url=self.league_img_url)
        embed.add_field(name="🥇 RANK", value=f"{self.rank}\u200b")
        embed.add_field(name="🌟 RATING", value=f"{self.rating}\u200b")
        embed.add_field(
            name="📈 GAMES PLAYED",
            value=f"Current Season: {self.games_played_current_season}\n"
            f"Win %: {self.win_percentage}\n"
            f"Total: {self.games_played_all_time}",
        )
        embed.set_footer(
            text=f"{self.favourite_naut} (favourite naut)",
            icon_url=self.favourite_naut_img_url,
        )

        if self.country_flag:
            embed.add_field(name=self.country_flag, value="\u200b")

        return embed
