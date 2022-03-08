from rasa_nlu.model import Interpreter
from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
from rasa_core.utils import EndpointConfig
# from rasa.utils.endpoints import EndpointConfig
import os
# list_agent={}
# list_nlu={}

#load all bot
def load_bots():
    list_agent = {}
    list_nlu={}
    for bot_name in os.listdir("list_bot"):
        interpreter = NaturalLanguageInterpreter.create('list_bot/{}/models/nlu/default/{}'.format(bot_name,bot_name))
        endpoint = EndpointConfig('http://localhost:5055/webhook')
        list_agent["agent_" + bot_name]=Agent.load('list_bot/{}/models/dialogue'.format(bot_name), interpreter=interpreter, action_endpoint = endpoint)
        list_nlu["nlu_" + bot_name]=Interpreter.load('list_bot/{}/models/nlu/default/{}'.format(bot_name,bot_name))
    print(list_agent)
    print(list_nlu)
    return list_agent,list_nlu

def load_bot_select(botName):
    for botSelect in os.listdir("list_bot"):
        if botSelect == botName:
            interpreter = NaturalLanguageInterpreter.create(
                'list_bot/{}/models/nlu/default/{}'.format(botName, botName))
            endpoint = EndpointConfig('http://localhost:5055/webhook')
            agent = Agent.load('list_bot/{}/models/dialogue'.format(botName),
                               interpreter=interpreter, action_endpoint=endpoint)
            nlu = Interpreter.load(
                'list_bot/{}/models/nlu/default/{}'.format(botName, botName))
    return agent,nlu



def answer_question_user(list_agent,bot_name,text):
    responses = list_agent["agent_{}".format(bot_name)].handle_text(text)
    message=None
    for response in responses:
        message=response["text"]
    return message

def extract_info(list_nlu,bot_name,text):
    summary={}
    info=list_nlu['nlu_{}'.format(bot_name)].parse(text)
    for entities in info['entities']:
        if entities['value'] is not None:
            summary[entities['entity']] = entities['value']
    return summary

