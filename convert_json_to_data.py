import json
import os
from mdutils import MdUtils
import yaml
import sys
import shutil

fileJson = sys.argv[2]

with open("{}".format(fileJson), mode="r", encoding='utf-8') as j_file:
    data = j_file.read()
intents = json.loads(data)
data_intents = intents["intents"]
data_stories = intents["stories"]
botName = intents["botName"]

if os.path.isdir("train_bot/{}".format(botName)) is not True:
    os.mkdir("train_bot/{}".format(botName))
    os.mkdir("train_bot/{}/data".format(botName, "data"))
shutil.copy2(fileJson, "train_bot/{}".format(botName))


def new_array_stories(array_st):
    new_arrays = []
    for item in array_st:
        new_arrays.append(item)
        new_arrays.append(['- utter_' + item])
    return new_arrays


def create_data_stories(botName):
    mdFile = MdUtils(file_name='train_bot/{}/data/stories.md'.format(botName))
    mdFile.new_header(level=1, title="stories")
    for story in data_stories:
        header = story
        # mdFile.new_header(level=1, title=header)
        mdFile.new_header(level=2, title=header)
        new_arrays = new_array_stories(data_stories["{}".format(story)])
        mdFile.new_list(new_arrays, marked_with='*')
    mdFile.create_md_file()


def create_data_nlu(botName):
    mdFile = MdUtils(file_name='train_bot/{}/data/nlu.md'.format(botName))
    mdFile.new_header(level=1, title="intent")
    for data in data_intents:
        mdFile.new_header(level=2, title="intent:" + data["topic"])
        mdFile.new_list(data['questions'], marked_with='-')
    mdFile.create_md_file()


def set_intents_in_domain():
    topic = {}
    valuesTopic = []
    entities = {}
    valuesEntities = []
    slots = {}
    valuesSlots = {}
    actions = {}
    valuesAction = []
    templates = {}
    valuesTemplates = {}

    def check_values_entities(value):
        check = 0
        for entities in valuesEntities:
            if value == entities:
                check = 1
                break
        return check

    def set_slots(valueEntities):
        valuesSlots.update({"{}".format(valueEntities): {
            "auto_fill": True,
            "type": "text"
        }})

    def set_utter(response):
        valuesUtter = []
        for value in response:
            valuesUtter.append({"text": value})
        return valuesUtter

    for dataTopic in intents["intents"]:
        valuesTopic.append(dataTopic["topic"])
        valuesAction.append("utter_" + dataTopic["topic"])
        valuesUtter = set_utter(dataTopic["responses"])
        valuesTemplates.update({"utter_{}".format(dataTopic["topic"]): valuesUtter})
        for dataEntities in dataTopic["entities"]:
            if check_values_entities(dataEntities) == 0:
                valuesEntities.append(dataEntities)
                set_slots(dataEntities)

    valuesAction.append("utter_unclear")
    valuesUtterUnclear = {
        "utter_unclear": [{"text": "Thưa quý khách, hiện tại em chưa hiểu được yêu cầu của Quý khách."}]}
    valuesTemplates.update(valuesUtterUnclear)
    topic.update({"intents": valuesTopic})
    entities.update({"entities": valuesEntities})
    slots.update({"slots": valuesSlots})
    templates.update({"templates": valuesTemplates})
    actions.update({"actions": valuesAction})

    return topic, entities, slots, actions, templates


topic, entities, slots, templates, actions = set_intents_in_domain()

create_data_nlu(botName)
create_data_stories(botName)


def dump_data(data, botName):
    with open('train_bot/{}/data/domain.yml'.format(botName), 'a', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)


path = 'train_bot/{}/data/domain.yml'.format(botName)
if os.path.isfile(path):
    os.remove(path)
dump_data(topic, botName)
dump_data(entities, botName)
dump_data(slots, botName)
dump_data(templates, botName)
dump_data(actions, botName)
