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
    Displays the roster of the given team
    '''

    logger = logging.getLogger("chatcmds.matchup")
    league = context["espnff"]
    configs = context["configs"]

    embed = None

    if arguments is False or context is False:
        logger.error("Error in Module bad Arguments.")
        final_message = False

    parser = argparse.ArgumentParser(prog="matchup")

    parser.add_argument("team", help="Team (Number) to Look at", type=int, default=1)

    try:
        args = parser.parse_args(arguments)
    except SystemExit as systemerror:
        logger.error("When Parsing System tried to exit: {}".format(systemerror))
        final_message = parser.format_help()
    else:
        # Do Echo

        logger.debug("Optional Args : \n {}".format(optional_args))

        try:
            team = league.team[args.team]
        except Exception as get_team_error:
            logger.debug("Unable to get team {}, exiting.".format(get_team_error)

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
