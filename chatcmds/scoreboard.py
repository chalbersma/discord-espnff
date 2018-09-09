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
    this is the echo command takes what it's given and returns it.
    '''

    logger = logging.getLogger("chatcmds.scoreboard")
    league = context["espnff"]
    configs = context["configs"]

    embed = None

    if arguments is False or context is False:
        logger.error("Error in Module bad Arguments.")
        final_message = False

    parser = argparse.ArgumentParser(prog="scoreboard")

    parser.add_argument("-w", "--week", help="Override Week", default=False)

    try:
        args = parser.parse_args(arguments)
    except SystemExit as systemerror:
        logger.error("When Parsing System tried to exit: {}".format(systemerror))
        final_message = parser.format_help()
    else:
        # Do Echo

        optional_args = dict()
        if args.week is not False:
            optional_args["week"] = int(args.week)

        logger.debug("Optional Args : \n {}".format(optional_args))

        scoreboard = league.scoreboard(**optional_args)

        scoreboard_url = "http://games.espn.com/ffl/scoreboard?leagueId={}&seasonId={}".format(configs["league_id"], configs["season"])

        final_message = "Scoreboard:"

        optional_args = {}


        myembed = discord.Embed(title="Scoreboard", url=scoreboard_url)

        matchup_index = 1

        for matchup in scoreboard:
            home_team = matchup.home_team
            away_team = matchup.away_team

            name_string = "#{}. {} @ {}".format(matchup_index, away_team.team_abbrev, home_team.team_abbrev)

            if matchup.home_score >= matchup.away_score:
                home_team_name = "**{}**".format(home_team.team_name)
                away_team_name = away_team.team_name
            else:
                away_team_name = "**{}**".format(away_team.team_name)
                home_team_name = home_team.team_name

            matchup_string = "{} ({}-{}) : {} _@_ {} ({}-{}) : {}".format(away_team_name, away_team.wins, away_team.losses, matchup.away_score, \
                                                                               home_team_name, home_team.wins, home_team.losses, matchup.home_score)

            myembed.add_field(name=name_string, value=matchup_string, inline=False)

            matchup_index += 1

        embed = myembed


    return (final_message, embed)
