import random
from django.utils.translation import gettext_lazy as _


class MessageManager:

    # types of messages
    MESSAGE_TYPE_CONSUMPTION = 0
    MESSAGE_TYPE_CONSUMPTION_CHANGE = 1
    MESSAGE_TYPES = {MESSAGE_TYPE_CONSUMPTION, MESSAGE_TYPE_CONSUMPTION_CHANGE}

    MESSAGES = {
        MESSAGE_TYPE_CONSUMPTION: {
            "empty": [
                _("Use water wisely, every drop counts!"),
                _("By saving water, together we can make a difference."),
                _("Use water, don't waste it."),
            ],
            "best20_": [
                _("This week your consumption is ranked within the top 20%. Keep up the good work to preserve water resources!"),
                _("This week your consumption is ranked within the top 20%. Continue saving water to help the environment."),
            ],
            "avg_best20": [
                _("Keep up the good work and continue to preserving water resources!"),
                _("Well done! Continue saving water to help the environment."),
            ],
            "_avg": [
                _("Try more to reduce your consumption and help addressing climate change!"),
                _("Your peers are saving more. Use water, don’t waste it."),
                _("Try more to save water! Use water wisely, every drop counts!"),
                _("Try more! By saving water, together we can make a difference."),
            ],
        },
        MESSAGE_TYPE_CONSUMPTION_CHANGE: {
            "empty": [
                _("Use water wisely, every drop counts!"),
                _("By saving water, together we can make a difference."),
                _("Use water, don't waste it."),
            ],
            "best20_": [
                _("This week your consumption reduction is ranked within the top 20%. Keep up the good work to preserve water resources!"),
                _("This week your consumption reduction is ranked within the top 20%. Continue saving water to help the environment."),
            ],
            "avg_best20": [
                _("Keep up the good work and continue to preserving water resources!"),
                _("Well done! Continue saving water to help the environment."),
            ],
            "_avg": [
                _("Try more to improve your consumption reduction and help addressing climate change!!"),
                _("Your peers are reducing their consumption more. Use water, don’t waste it."),
                _("Try more to save water! Use water wisely, every drop counts!"),
                _("Try more! By saving water, together we can make a difference and help the environment."),
            ],
        }
    }

    def __init__(self, you_vs_others):
        self.you_vs_others = you_vs_others

        # read average, best 20%, my school
        self.best20 = self._get_you_vs_others_prop(prop="best20")
        self.avg = self._get_you_vs_others_prop(prop="avg")
        self.me = self._get_you_vs_others_prop(prop="me")

        # classify
        if self.best20:
            self.classification = "best20_" if self.me <= self.best20 else (
                "_avg" if self.me > self.avg else
                "avg_best20"
            )
        else:
            self.classification = "empty"

    def _get_you_vs_others_prop(self, prop):
        try:
            return [
                (v["weekly_total"] if "weekly_total" in v else v["change"])
                for v in self.you_vs_others
                if v["id"] == prop
            ][0]
        except IndexError:
            raise MessageManager.YouVsOthersFormatError(
                f"Invalid `you_vs_other` parameter - could not find item with id `{prop}`."
            )

    def get_messages(self, message_type, n_messages=1):
        # validate message type
        if message_type not in self.MESSAGE_TYPES:
            raise self.InvalidMessageTypeError(f"Message type `message_type` is invalid.")

        # get a number of random options from matching messages
        return random.choices(
            self.MESSAGES[message_type][self.classification],
            k=n_messages
        )

    def get_message(self, message_type):
        return self.get_messages(message_type=message_type, n_messages=1)[0]

    class YouVsOthersFormatError(ValueError):
        pass

    class InvalidMessageTypeError(ValueError):
        pass
