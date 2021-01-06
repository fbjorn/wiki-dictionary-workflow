# encoding: utf-8

import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Meaning = namedtuple("Meaning", "value, examples")
Definition = namedtuple("Definition", "meanings, synonyms, antonyms")


def make_url(term):
    # type: (unicode) -> unicode
    return u"https://ru.wiktionary.org/wiki/{}".format(term)


def find_definitions(term):
    definitions = []
    resp = requests.get(make_url(term), headers={})
    bs = BeautifulSoup(resp.text, features="html.parser")

    tag = bs.find(id=u"Русский")
    if tag:
        tag = tag.next_element
    else:
        return []

    kind = "meaning"
    definition = None
    while True:
        if tag is None or tag.name == "h1":
            break

        if tag.name == "span" and tag.attrs.get("id"):
            id_attr = tag.attrs["id"]
            if id_attr.startswith(u"Значение"):
                kind = "meaning"
                if definition is not None:
                    definitions.append(definition)
                definition = Definition(meanings=[], synonyms=[], antonyms=[])
            elif id_attr.startswith(u"Синоним"):
                kind = "synonym"
            elif id_attr.startswith(u"Антоним"):
                kind = "antonym"
            else:
                kind = "unknown"
        if tag.name == "ol":
            if kind == "meaning":
                definition.meanings.extend(get_meanings(tag))
            elif kind == "synonym":
                definition.synonyms.extend(get_synonyms(tag))
            elif kind == "antonym":
                definition.antonyms.extend(get_synonyms(tag))
            tag = tag.next_sibling
        else:
            tag = tag.next_element

    definitions.append(definition)
    return definitions


def get_meanings(tag):
    meanings = []
    for li in tag.find_all("li"):
        text = li.get_text().strip()
        if u"◆" in text:
            parts = text.split(u"◆")
            examples = []
            for full_example in parts[1:]:
                example = full_example.split(".")[0].strip().capitalize()
                if example and u"тсутствует пример" not in example:
                    examples.append(example)
                    break
            meanings.append(Meaning(value=parts[0], examples=examples))
        elif len(text) > 6:
            meanings.append(Meaning(value=text, examples=[]))
    return meanings


def get_synonyms(tag):
    synonyms = []
    for li in tag.find_all("li"):
        text = li.get_text().strip()
        if len(text) > 3:
            synonyms.append(text)
    return synonyms
