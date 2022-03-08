import os
from distutils.dir_util import copy_tree
import process_message
from fastapi import FastAPI
import timeit
from rasa_nlu.model import Interpreter
from rasa_core.agent import Agent
from rasa_core.interpreter import NaturalLanguageInterpreter
from rasa_core.utils import EndpointConfig
print("readLoad")
import pickle


list_agent=process_message.load_bots()[0]
list_nlu=process_message.load_bots()[1]

app = FastAPI()
@app.get("/chat/")

async def read_item(bot_name:str, mgs: str):
    global list_agent,list_nlu
    check_bot = 0
    a=timeit.default_timer()
    for bot in os.listdir("train_bot"):
        if bot == bot_name:
            with open("train_bot/{}/status.txt".format(bot_name),'r') as file:
                status=file.read()
            
            if status=='1':
               
                interpreter = NaturalLanguageInterpreter.create(
                    'train_bot/{}/models/nlu/default/{}'.format(bot_name, bot_name))
                endpoint = EndpointConfig('http://localhost:5055/webhook')
                list_agent["agent_" + bot_name] = Agent.load('train_bot/{}/models/dialogue'.format(bot_name),
                                                             interpreter=interpreter, action_endpoint=endpoint)
                list_nlu["nlu_" + bot_name] = Interpreter.load(
                    'train_bot/{}/models/nlu/default/{}'.format(bot_name, bot_name))

                messages = process_message.answer_question_user(list_agent, bot_name, mgs)
                extract_info = process_message.extract_info(list_nlu, bot_name, mgs)
                check_bot=1
                copy_tree("train_bot/{}".format(bot_name), "list_bot/{}".format(bot_name))
                with open('train_bot/{}/status.txt'.format(bot_name), 'w') as file:
                    file.write('0')
            else:
                check_bot =0
            break
    if check_bot==0:
        for agent in list_agent:

            if agent =="agent_"+bot_name:
                messages = process_message.answer_question_user(list_agent,bot_name,mgs)
                extract_info = process_message.extract_info(list_nlu,bot_name,mgs)
                break
            else:
                messages = "{} no exist".format(bot_name)
                extract_info = {}

    print(timeit.default_timer()-a)
    return {"message": messages,
            "extract_info":extract_info
            }






# uvicorn main_api:app --host 0.0.0.0 --port 8000 --reload