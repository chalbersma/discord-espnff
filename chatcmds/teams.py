#!/usr/bin/envconfigs["command"

'''
Docstring, Everthing here is for chataction
'''

import logging
import argparse
import texttable

import discord_helpers
import discord

def chataction(arguments=False, context=False):

    '''
    Returns a List of Teams (Numbered)
    '''

    logger = logging.getLogger("chatcmds.scoreboard")
    league = context["espnff"]
    configs = context["configs"]

    embed = None

    if arguments is False or context is False:
        logger.error("Error in Module bad Arguments.")
        final_message = False

    parser = argparse.ArgumentParser(prog="teams")

    try:
        args = parser.parse_args(arguments)
    except SystemExit as systemerror:
        logger.error("When Parsing System tried to exit: {}".format(systemerror))
        final_message = parser.format_help()
    else:
        # Do Echo

        optional_args = dict()

        logger.debug("Optional Args : \n {}".format(optional_args))

        teams = league.teams

        teams_url = "http://games.espn.com/ffl/leaguesetup/ownerinfo?leagueId={}".format(configs["league_id"])

        final_message = "Team List:"

        myembed = discord.Embed(title="Team List", url=teams_url)

        matchup_index = 1

        for team in teams:

            name_string = "#{}. {} ({})".format(matchup_index, team.team_name, team.team_abbrev)

            matchup_string = "Owner: {}".format(team.owner)

            myembed.add_field(name=name_string, value=matchup_string, inline=False)

            matchup_index += 1

        embed = myembed


    return (final_message, embed)
