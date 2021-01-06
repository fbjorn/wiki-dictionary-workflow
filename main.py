# encoding: UTF-8

import sys

sys.path.append("lib")  # noqa

from lib.workflow import Workflow3, Workflow, ICON_WARNING
from dictionary import find_definitions


def err(wf, title, subtitle=""):
    # type: (Workflow, unicode, unicode) -> int
    """
    Show error text and exit
    :param wf: Workflow instance
    :param title: Error message title
    :param subtitle: Error description
    :return: Exit code
    """
    wf.add_item(title=title, subtitle=subtitle, icon=ICON_WARNING)
    wf.send_feedback()
    return 0


def main(wf):
    # type: (Workflow) -> int

    full_text = u""
    definitions = find_definitions("_".join(wf.args))
    for definition in definitions:
        if definition.synonyms or definition.antonyms:
            if definition.synonyms:
                full_text += u"Синонимы: {}\n".format(u",".join(definition.synonyms))
            if definition.antonyms:
                full_text += u"Антонимы: {}\n".format(u",".join(definition.antonyms))
            full_text += u"{}\n".format(u"-" * 64)
        for i, meaning in enumerate(definition.meanings):
            full_text += u"{}. {}\n".format(i + 1, meaning.value)
            if meaning.examples:
                full_text += u"\n"
            for example in meaning.examples:
                full_text += u"   > {}\n".format(example)
            full_text += u"{}\n".format(u"-" * 64)
    for definition in definitions:
        for meaning in definition.meanings:
            wf.add_item(
                title=meaning.value,
                subtitle=u"; ".join(meaning.examples),
                valid=True,
                arg=full_text
            )
        for syn in definition.synonyms:
            wf.add_item(
                title=syn,
                subtitle=u"Синоним",
                valid=True,
                arg=full_text
            )
        for ant in definition.antonyms:
            wf.add_item(
                title=ant,
                subtitle=u"Антоним",
                valid=True,
                arg=full_text
            )
    wf.send_feedback()


if __name__ == "__main__":
    workflow = Workflow3()
    sys.exit(workflow.run(main))
