from unittest import TestCase
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

class CanvasTests(TestCase):
    def test_canvas_questions(self):
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

        with pset_submission(canvas_url, canvas_token, course_id, assignment_name, quiz_name, repo, url, do_submit=False) as qsubmission:
            assert qsubmission.id > 0
            assert qsubmission.attempt > 0
            questions = qsubmission.get_submission_questions()
            print(questions[0])
            self.assertEqual(questions[0].answer, None)
            self.assertEqual(questions[1].answer, None)
            self.assertEqual(len(questions[4].answers), 4)
            answers = get_answers_pset2(questions,'15+', repo)
            assert answers[0]['id'] > 0
            assert answers[1]['id'] > 0
            self.assertNotEqual(answers[0]['answer'], None)
            self.assertNotEqual(answers[1]['answer'], None)
            responses = qsubmission.answer_submission_questions(quiz_questions=answers)
            print(responses)
            comments = get_submission_comments(repo, qsubmission)            
            assert comments['quiz_submission_id'] > 0
            assert comments['quiz_attempt'] > 0



