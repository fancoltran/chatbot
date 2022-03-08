
# rasa core
import logging
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies import FallbackPolicy
from rasa_core.policies.memoization import MemoizationPolicy


# rasa nlu
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter
import spacy
nlp = spacy.load('en_core_web_sm')
import convert_json_to_data as conv

# import sys
import os

bot_name=conv.botName
# train_rasa_core

def train_dialog(dialog_training_data_file, domain_file, path_to_model):
    logging.basicConfig(level='INFO')
    fallback = FallbackPolicy(fallback_action_name="utter_unclear", core_threshold=0.3, nlu_threshold=0.3)

    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=1), KerasPolicy(epochs=200,
                                                                          batch_size=20), fallback])
    training_data = agent.load_data(dialog_training_data_file)
    agent.train(
        training_data,
        augmentation_factor=50,
        validation_split=0.2)
    agent.persist(path_to_model)
def train_nlu (data, config_file, model_dir,bot_name):
    training_data = load_data(data)
    trainer = Trainer(config.load(config_file))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name = bot_name)
# Train
#--------
def run_train_model():
    try:
        train_nlu('train_bot/{}/data/nlu.md'.format(bot_name), 'config/config.yml',
                  'train_bot/{}/models/nlu'.format(bot_name), '{}'.format(bot_name))
        train_dialog('train_bot/{}/data/stories.md'.format(bot_name),
                     'train_bot/{}/data/domain.yml'.format(bot_name),
                     "train_bot/{}/models/dialogue".format(bot_name))
        with open('train_bot/{}/status.txt'.format(bot_name), 'w') as file:
            file.write('1')
        message = "success"
    except:
        message = "fall"
    print(message)
    return message


run_train_model()

#python train_dialog.py --path_itents [path itents]