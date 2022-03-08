from rasa_core_sdk import Action,Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk import logger

class ActionStoreIntentMessage():
    """Stores the bot use case in a slot"""

    def name(self):
        return "action_store_intent_message"

    def run(self, tracker=Tracker):

        # we grab the whole user utterance here as there are no real entities
        # in the use case
        # message = tracker.get_latest_entity_values('cust_cake')
        message=next(tracker.get_latest_entity_values('cust_cake'), None)

        return [message]

# a=ActionStoreIntentMessage()
# a.run()