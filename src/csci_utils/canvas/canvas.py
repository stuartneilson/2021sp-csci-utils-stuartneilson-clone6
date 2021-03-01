"""Utils for accessing and submitting to Canvas"""

import canvasapi
from canvasapi import Canvas
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from environs import Env
import json
from git import Repo
from contextlib import contextmanager
from typing import List, Dict, ContextManager, Union
import os


def get_assignment(course, assignment_name):
    """
    assignment from canvas API

    :param course:
    :param assignment_name: title of assignment
    :return: canvas assignment object
    """

    assignments = course.get_assignments()

    # find current assigment, given assigment name
    assignment = None
    for a in assignments:
        if assignment_name == a.name:
            assignment = a

    return assignment


def get_quiz(course, quiz_title):
    """
    provides the canvas quiz based on the title

    :param course: canvas object
    :param quiz_title: title of quiz
    :return: course object
    """
    quizzes = course.get_quizzes()
    quiz = None
    for q in quizzes:
        if quiz_title == q.title:
            quiz = q
    return quiz


def get_submission_comments(repo: Repo, qsubmission: QuizSubmission) -> Dict:
    """Provides some info about the submission, to pass to Canvas"""
    return dict(
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(),
        quiz_submission_id=qsubmission.id,
        quiz_attempt=qsubmission.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
    )


@contextmanager
def pset_submission(
    canvas_url,
    canvas_token,
    course_id,
    assignment_name,
    quiz_name,
    repo,
    url,
    do_submit=True,
):
    """Creates and yields a canvas submission object - the recieving context is responsible for filling in the answers component of the submission,
       this function will then submit those answers

    :the first five parameters are part of the canvas api setup
    :the url parameter should be populated with the url of the executing device (e.g. CI/CD platform url), for providing as metadata to Canvas
    """

    canvas = canvasapi.Canvas(canvas_url, canvas_token)
    course = canvas.get_course(course_id)
    assignment = get_assignment(course, assignment_name)
    quiz = get_quiz(course, quiz_name)

    try:
        qsubmission = quiz.create_submission()
        yield qsubmission

    finally:
        if do_submit:
            print("Submission to be attempted")
            if qsubmission is not None:
                print("Completing Submission")
                completed = qsubmission.complete()

                submission = assignment.submit(
                    dict(
                        submission_type="online_url",
                        url=url,
                    ),
                    comment=dict(
                        text_comment=json.dumps(
                            get_submission_comments(repo, qsubmission)
                        )
                    ),
                )
        else:
            print("Not submitting")
