import canvasapi
from canvasapi import Canvas
from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from environs import Env
import json
from git import Repo
from typing import List, Dict, ContextManager, Union

def answer_pset2_q0(question: QuizSubmissionQuestion, repo: Repo):
    """returns the answer to question 0, 
    :param question: question number 0, extracted from the qsubmission object
    :param repo: the current repository object
    """
    return int(str(repo.tags[-1]).split('.')[0].replace('v',''))

def answer_pset2_q1(question: QuizSubmissionQuestion, repo: Repo):
    """returns the answer to question 1, 
    :param question: question number 1, extracted from the qsubmission object
    :param repo: the current repository object
    """
    return int(str(repo.tags[-1]).split('.')[1])

def answer_pset2_q2(question: QuizSubmissionQuestion, repo: Repo):
    """returns the answer to question 2, 
    :param question: question number 2, extracted from the qsubmission object
    :param repo: the current repository object
    """
    return int(str(repo.tags[-1]).split('.')[2])

def answer_pset2_q3(question: QuizSubmissionQuestion, repo: Repo):
    """returns the answer to question 3, 
    :param question: question number 3, extracted from the qsubmission object
    :param repo: the current repository object
    """
    true_id = [ans["id"] for ans in question.answers if ans["text"] == "True"][0]
    false_id = [ans["id"] for ans in question.answers if ans["text"] == "False"][0] 
   
    if len(repo.tags) > 0: return true_id 
    else: return false_id

def answer_pset2_q4(question: QuizSubmissionQuestion, repo: Repo, hours_desc: str):
    """returns the answer to question 4, 
    :param question: question number 4, extracted from the qsubmission object
    :param repo: the current repository object
    :param hours_desc: how long the assignment took
    """
    return [ans["id"] for ans in question.answers if ans["text"] == hours_desc][0]

def answer_pset2_q5(question: QuizSubmissionQuestion, repo: Repo):
    """returns the answer to question 5, 
    :param question: question number 5, extracted from the qsubmission object
    :param repo: the current repository object
    """
    return repo.head.commit.hexsha[:8]

def answer_pset2_q6(question: QuizSubmissionQuestion, repo: Repo):
    """returns the answer to question 6, 
    :param question: question number 6, extracted from the qsubmission object
    :param repo: the current repository object
    """
    true_id = [ans["id"] for ans in question.answers if ans["text"] == "True"][0]
    false_id = [ans["id"] for ans in question.answers if ans["text"] == "False"][0] 
   
    if repo.is_dirty(): return false_id 
    else: return true_id

def get_answers_pset2(
    questions: List[QuizSubmissionQuestion], hours_desc: str, repo: Repo
) -> List[Dict]:
    """Creates answers for Canvas quiz questions, specific to CSCI Utils questions
    :param questions: list of questions, extracted from the qsubmission object
    :param hours_desc: string representation of the time taken to complete the problem set
    :param repo: the current repository object
    """

    answer_0 = answer_pset2_q0(questions[0], repo)
    answer_1 = answer_pset2_q1(questions[1], repo)
    answer_2 = answer_pset2_q2(questions[2], repo)
    answer_3 = answer_pset2_q3(questions[3], repo)
    answer_4 = answer_pset2_q4(questions[4], repo, hours_desc)
    answer_5 = answer_pset2_q5(questions[5], repo)  
    answer_6 = answer_pset2_q6(questions[6], repo)  
    
    answers = [answer_0, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6]

    results = []
    for i in range(len(questions)):
        results.append({"id": questions[i].id, "answer": answers[i]})
    return results