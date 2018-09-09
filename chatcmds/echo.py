#!/usr/bin/envconfigs["command"

'''
Docstring, Everthing here is for chataction
'''

import logging
import argparse

import discord_helpers

def chataction(arguments=False, context=False):

    '''
    this is the echo command takes what it's given and returns it.
    '''

    logger = logging.getLogger("chatcmds.echo")
    embed = None

    if arguments is False or context is False:
        logger.error("Error in Module bad Arguments.")
        final_message = False

    parser = argparse.ArgumentParser(prog="echo")

    parser.add_argument("-b", "--bold", action='store_true', help="Bold the Return Message")
    parser.add_argument("phrase", nargs='*', help="Phrase to Echo Back")

    try:
        args = parser.parse_args(arguments)
    except SystemExit as systemerror:
        logger.error("When Parsing System tried to exit: {}".format(systemerror))
        final_message = parser.format_help()
    else:
        # Do Echo
        logger.info("Phrase Arg Object : {}".format(args.phrase))
        combined_phrase = " ".join(args.phrase)
        if args.bold is True:
            final_message = "**{}**".format(combined_phrase)
        else:
            final_message = combined_phrase


    return (final_message, embed)
