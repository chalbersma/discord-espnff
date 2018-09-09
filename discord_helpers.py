#!/usr/bin/env python3

'''
Helper Functions for Discord
'''

import logging

def splitter_upper(raw_text=False, configs=False):

    '''
    Takes the Raw string from the Command and splits it
    '''

    logger = logging.getLogger("discord_helpers.splitter_upper")

    if raw_text is False or configs is False:
        logger.error("Argument Error")
        return_tuple = (False, "Args Error")
        return return_tuple

    desired_first_token = configs.get("first_token", "ff")

    return_tuple = (False, "Unknown")

    if isinstance(raw_text, str) is False:
        logger.error("Badly Formatted Input")
        return_tuple = (False, "Badly Formatted Input")

    else:

        split_command = raw_text.split()

        if len(split_command) < 2:
            logger.debug("Split Command Too Short")
            return_tuple = (False, "Too Short")
        elif split_command[0] != desired_first_token:
            logger.debug("Not Directed at Me Action.")
            return_tuple = (False, "Not Directed At Me.")
        elif split_command[0] == desired_first_token and split_command[1].isalnum() is True:
            # Success
            logger.debug("Recieved command : {}".format(split_command[1]))
            if split_command[1] in configs["command"]:
                return_tuple = (True, split_command[1:])
            else:
                logger.info("Command not in Whitelist")
                return_tuple = (False, "Not in Whitelist")
        else:
            logger.error("Other Error")
            return_tuple = (False, "Other Error")

    return return_tuple

