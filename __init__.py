# -*- coding: utf-8 -*-

"""
This plugin is a password generator.
"""

import pathlib
import secrets
import string
from albert import StandardItem, Action, setClipboardText, PluginInstance, TriggerQueryHandler


__title__ = "PWGen"

md_iid = '2.0'
md_version = "1.8"
md_name = "PW Gen"
md_description = "Create random strong password"
md_license = "BSD-3"
#md_url = "https://github.com/albertlauncher/python/tree/master/pacman"
#md_bin_dependencies = ["pacman", "expac"]


class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        TriggerQueryHandler.__init__(self,
                                     id=md_id,
                                     name=md_name,
                                     description=md_description,
                                     synopsis='<password lenght>',
                                     defaultTrigger='pw ')
        PluginInstance.__init__(self, extensions=[self])
        self.iconUrls = [
            "xdg:pw-logo",
            f"file:{pathlib.Path(__file__).parent}/pw.svg"
        ]

    def genPass(self, length: int):
        # prepare the alphabet
        alphabet = string.ascii_letters + string.digits + string.punctuation
        
        # if lenght less then 6 we cannot include all the possible chars combination for a strong password
        if length < 6:
            # build the password randombly then
            return ''.join(secrets.choice(alphabet) for i in range(length))
        # else, build the password strongly
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if (
                any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.islower() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)
                and sum(c.isalpha() for c in password)
            ):
                return password

    def handleTriggerQuery(self, query):
        # default lenght
        length = 25
        # get password lenght
        try:
            length = int(query.string.strip())
        except:
            pass

        # build password
        pw = self.genPass(length)

        # show password
        query.add(
            StandardItem(
                id=__title__,
                iconUrls=self.iconUrls,
                text=pw,
                subtext="Password length: " + str(length) + ". Click to copy it!",
                actions=[
                    Action(
                        "pw-cp", "Copy password to clipboard",
                        lambda: setClipboardText(pw)
                    )
                ]
            )
        )
