# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
import inquirer


def prompt(message: str, choices=list(), multiselect=False, validate=None):
    if not validate:
        validate = True

    questions = []
    if choices:
        if multiselect:
            questions.append(inquirer.Checkbox("res", message=message, choices=choices, validate=validate))
        else:
            questions.append(inquirer.List("res", message=message, choices=choices, validate=validate))
    else:
        questions.append(inquirer.Text("res", message=message, validate=validate))

    answers = inquirer.prompt(questions)

    return answers.get("res")


def confirm(message):
    answers = inquirer.prompt([
        inquirer.Confirm("res", message=message)
    ])

    return answers.get("res")
