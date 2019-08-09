#!/usr/bin/env python3

'''
discord-espnff bot This is the demo.
'''

import argparse
import logging

import discord
import yaml
import sys
import ffespn
import texttable

import discord_helpers

from chatcmds import echo
from chatcmds import scoreboard
from chatcmds import rankings
from chatcmds import matchup
from chatcmds import teams


if __name__ == "__main__":

    # Run the main things
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config Yaml File", required=True)
    # How Verbose more v == more verbose
    parser.add_argument("-v", "--verbose", action='append_const', help="Turn on Verbosity", const=1, default=[])

    args = parser.parse_args()

    VERBOSE = len(args.verbose)

    FORMAT = "%(levelname)s %(asctime)s %(name)s : %(message)s"

    if VERBOSE == 0:
        # Standard Error Logging
        logging.basicConfig(level=logging.ERROR,
                            format=FORMAT)

    elif VERBOSE >= 1:
        if VERBOSE == 1:

            # Standard Debug Logging
            logging.basicConfig(level=logging.INFO,
                                format=FORMAT)

            # Turn down logging to Warning for these
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("pika").setLevel(logging.WARNING)
            logging.getLogger("paramiko").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)

            for botothing in ["boto3", "botocore.session", "botocore.loaders", "botocore.session", \
                              "botocore.hooks", "botocore.auth", "botocore.args", "botocore.endpoint", \
                              "botocore.client", "botocore.vendored.requests.packages.urllib3.connectionpool", \
                              "botocore.parsers", "botocore.retryhandler"]:
                logging.getLogger(botothing).setLevel(logging.WARNING)

        if VERBOSE >= 2:
            logging.basicConfig(level=logging.DEBUG,
                                format=FORMAT)


    logger = logging.getLogger("bot.py")


    with open(args.config, "r") as config_yaml_file:
        try:
            configs = yaml.load(config_yaml_file)
        except yaml.YAMLError as parse_error:
            logger.error("Error parsing config {} with error {}".format(args.config, config_yaml_file))
            sys.exit(1)
        else:
            pass


    client = discord.Client()




    @client.event
    async def on_ready():
        logger.info("The bot is and a connection hs been made to Discord")
        logger.info(configs["command"])

        await client.change_presence(game=discord.Game(name="ESPN FF"))


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        elif message.content == "ff help":
            # Replace this with Static help Message
            await client.send_message(message.channel, "Ha! You think I can Help you! You fool.")

        # This is not a message from me and not the help message
        iscommand, command_array = discord_helpers.splitter_upper(raw_text=message.content, configs=configs)

        if iscommand is True:
            # Build Latest and Greates
            ourleague = ffespn.League(configs["league_id"], configs["season"])
            context_dict = {"espnff" : ourleague, \
                            "configs" : configs, \
                            "dclient" : client, \
                            "channel" : message.channel}

            # Do the integration, macarena

            command = command_array[0]

            if len(command_array) > 1:
                command_args = command_array[1:]
            else:
                command_args = ""

            this_function = globals()[command]

            thismessage, embed = this_function.chataction(arguments=command_args, context=context_dict)

            if thismessage is not False:
                # This is a normal text message return
                await client.send_message(message.channel, str(thismessage), embed=embed)
            else:
                logger.info("Command Failed in Some Unexpected Manner")

        return



    client.run(configs["client_token"])

