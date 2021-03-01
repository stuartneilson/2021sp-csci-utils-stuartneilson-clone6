"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcsci_utils` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``csci_utils.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``csci_utils.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import canvasapi
from canvasapi import Canvas
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from environs import Env
import json
from git import Repo
from contextlib import contextmanager
from typing import List, Dict, ContextManager, Union
import os

from csci_utils.canvas.canvas import get_assignment, get_quiz, get_submission_comments, pset_submission
from csci_utils.canvas.canvas_csci_utils import get_answers_pset2

parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
                    help="A name of something.")

def main(args=None):
    args = parser.parse_args(args=args)
    print(args.names)

    repo = Repo(".")
    env = Env()
    url = "https://github.com/csci-e-29/2021sp-csci-utils-stuartneilson".format(
        os.path.basename(repo.working_dir), repo.head.commit.hexsha
    )
    course_id = env.int("CANVAS_COURSE_ID")
    canvas_url = env.str("CANVAS_URL")
    canvas_token = env.str("CANVAS_TOKEN")
    assignment_name = 'CSCI Utils'
    quiz_name = 'CSCI Utils Answers'

    with pset_submission(canvas_url, canvas_token, course_id, assignment_name, quiz_name, repo, url, do_submit=True) as qsubmission:
        questions = qsubmission.get_submission_questions()
        answers = get_answers_pset2(questions,'15+', repo)
        print(answers)
        responses = qsubmission.answer_submission_questions(quiz_questions=answers)

    
