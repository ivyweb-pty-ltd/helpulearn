"""
Created by jacobus on 2024/12/20 
"""

"""This little application tests the concepts that might be used in helpulearn specifically the dependency requirement and random question strategy"""

# List of questions level and answers for numbers from 1 to 12, level is equal to the highest number in the question
import random


class question:
    def __init__(self, question_str, level, answer, probability):
        self.question = question_str
        self.level = level
        self.answer = answer
        self.asked = 0
        self.correct = 0
        self.normalized_prop = 1
        self.probability = probability

    def __str__(self):
        return f'{self.question} = {self.answer}'


def generate_questions(num_range=12):
    questions = []
    for i in range(1, num_range + 1):
        for j in range(1, num_range + 1):
            level=max(i,j)
            questions.append(question(question_str=f'{i} + {j}', level=level, answer=str(i + j),probability=1/pow(10,level)))
    return questions


class question_list:
    def __init__(self, questions):
        self.questions = questions
        self.levels = [1]

    # Calculate chose a question at weighted random based on the probability of the question
    def choose_question(self):
        random_range = self.random_range()
        random_number = random.random() * random_range
        for q in self.questions:
            random_number -= q.probability
            if random_number <= 0:
                return q
        return q

    def random_range(self):
        random_range = 0
        for q in self.questions:
            random_range += q.probability
        return random_range

    def reset_levels(self):
        for i in range(0,len[self.levels]):
            self.levels[i] = 0

    def probability(self, question):
        # Probability is based on the number of correct answers and the number times you have the question right.
        #
        return question.probability


if __name__ == '__main__':
    questions = generate_questions()
    qlist = question_list(questions)
    for i in range(100):
        q = qlist.choose_question()
        q.asked += 1
        q.correct += 1
        q.probability=q.probability/5
        print(q.probability, q)
