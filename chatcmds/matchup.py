#!/usr/bin/envconfigs["command"

'''
Docstring, Everthing here is for chataction
'''

import logging
import argparse
import texttable

import discord

import discord_helpers

def chataction(arguments=False, context=False):

    '''
    this is the echo command the matchup number and displays info about the matchup
    '''

    logger = logging.getLogger("chatcmds.matchup")
    league = context["espnff"]
    configs = context["configs"]

    embed = None

    if arguments is False or context is False:
        logger.error("Error in Module bad Arguments.")
        final_message = False

    parser = argparse.ArgumentParser(prog="matchup")

    parser.add_argument("-w", "--week", help="Override Week", default=False)
    parser.add_argument("matchup", help="Matchup To Look at.", type=int, default=1)

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

        final_message = "Matchup:"

        matchup = scoreboard[args.matchup-1]

        home_team = matchup.home_team
        away_team = matchup.away_team

        if matchup.home_score >= matchup.away_score:
            home_team_name = "**{}**".format(home_team.team_name)
            away_team_name = away_team.team_name
        else:
            away_team_name = "**{}**".format(away_team.team_name)
            home_team_name = home_team.team_name

        title_string = "{} @ {}".format(away_team_name, home_team_name)

        myembed = discord.Embed(title=title_string, url=scoreboard_url)

        score_string = "{} - {}".format(matchup.away_score, matchup.home_score)

        myembed.add_field(name="Score", value=score_string, inline=False)

        embed = myembed


    return (final_message, embed)
