
#!/usr/bin/envconfigs["command"

'''
Rankings
'''

import logging
import argparse
import texttable

import discord_helpers
import discord

def chataction(arguments=False, context=False):

    '''
    Display the current Rankings
    '''

    logger = logging.getLogger("chatcmds.rankings")
    league = context["espnff"]
    configs = context["configs"]

    embed = None

    if arguments is False or context is False:
        logger.error("Error in Module bad Arguments.")
        final_message = False

    parser = argparse.ArgumentParser(prog="scoreboard")

    try:
        args = parser.parse_args(arguments)
    except SystemExit as systemerror:
        logger.error("When Parsing System tried to exit: {}".format(systemerror))
        final_message = parser.format_help()
    else:
        # Do Echo

        standings_url = "http://games.espn.com/ffl/standings?leagueId={}&seasonId={}".format(configs["league_id"], configs["season"])

        myembed = discord.Embed(title="Standings", url=standings_url)

        leaderboard = list()

        for team in league.teams:
            this_wins = team.wins
            this_loss = team.losses

            if this_wins + this_loss == 0:
                wl_percent = 0.00
            else:
                wl_percent = this_wins / (this_wins + this_loss)

            dots_needed = 8 - len(team.team_abbrev)

            standing_string = "`{}{}{}/{}\t\t.{:03d}`".format(team.team_abbrev, "."*dots_needed, this_wins, this_loss, int(wl_percent*1000))

            leaderboard.append(standing_string)

        myembed.add_field(name="Leaderboard:", value="\n".join(leaderboard), inline=False)

        final_message = "Standings:"

        embed = myembed

    return (final_message, embed)
