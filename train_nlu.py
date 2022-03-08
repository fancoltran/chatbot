# Imports
#-----------
# rasa nlu
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter
import spacy
nlp = spacy.load('en_core_web_sm')
# Ham train NLU
#------------
def train (data, config_file, model_dir,bot_name):
    training_data = load_data(data)
    trainer = Trainer(config.load(config_file))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name = bot_name)


# Tien hanh train modul NLU
# Input : File nlu.md
# Output: Model NLU trong thu mục models/nlu
# train('data/nlu.md', 'config/config.yml', 'models/nlu')
train('chatbot_2/data/nlu.md', 'config/config.yml', 'list_bot/chatbot_2/models/nlu', 'chatbot_2')

# Load modul NLU
# interpreter = Interpreter.load('./models/nlu/default/chatbot_1')
interpreter = Interpreter.load('list_bot/chatbot_2/models/nlu/default/chatbot_2')

# Ham test NLU
def ask_question(text):
    a=interpreter.parse(text)
    print(a)
    print(type(a))

#
#
ask_question("email là 12@gmail.com")