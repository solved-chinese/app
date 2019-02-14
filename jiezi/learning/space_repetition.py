# not used as for now

from heapq import *


class card():
    def __init__(self, index):
        '''
        index: unique index of a character for identification
        appearance: it is about to appear for the ? time
        I: time interval (until the next repetition) (in days)
        '''
        self.index = index #pk
        self.EF = 2.5
        self.appearance = 1
        self.interval = 0

    def update_interval(self, n):
        if n == 1:
            self.interval=1
        elif n == 2:
            self.interval=6
        else:
            self.interval *= self.EF

    def receive_answer(self, answer):
        self.appearance += 1
        if answer == False:
            self.EF -= 0.8
            self.update_interval(1)
        else:
            self.EF += 0.1
            self.update_interval(self.appearance)
        if self.EF < 1.3: self.EF = 1.3

    def __lt__(self, card2):
        return card2


def decrement(card):
    card.I = card.I - 1
    return card


# a priority_queue with key self.interval
class ReviewStack():
    def __init__(self, pr):
        self.stack = []
        self.pr = pr

    def add_card(self, index):
        a = card(index)
        a.I = self.pr
        heappush(self.stack, [self.pr, a])

    def insert_card(self, card):
        heappush(self.stack, [card.I, card])

    def get_card(self):
        c = heappop(self.stack)
        return c[1]

    def update_card(self, card, answer):
        card.receive_answer(answer)
        heappush(self.stack, [card.I, card])


class UserStack():
    def __init__(self, pr=1, t_review=10, t_learn=20, min_pfm=2):
        '''
        t_review: average time taken to review one word (should be based on historical data)
        t_learn: average time taken to learn one word
        min_pfm: minimum number of new words per five minutes of study
        '''
        self.t_review = t_review
        self.t_learn = t_learn
        self.min_pfm = min_pfm
        self.pr = pr
        self.review = ReviewStack(self.pr)

    def n_review(self, time):
        return max(sum(x[0] < self.pr for x in self.review.stack), time // self.t_review)

    def new_learn_stack(self, learn_stack):
        '''
        when the user begins a completely new stack
        '''
        self.learn_stack = learn_stack

    def get_curr_learn_stack(self, time):
        '''
        learn_stack: list of indices of all the characters that need to be learnt
        time: in minutes
        '''
        n_review = self.n_review(time)
        n_learn = round((time * 60 - self.t_review * n_review) / self.t_learn)
        min_learn = int(time / 5) * self.min_pfm
        if n_learn < min_learn:
            n_learn = min_learn
        return self.learn_stack[:n_learn]

    def get_stack(self, time):
        '''
        return list of indices of characters that need to be learnt, and characters that need to be reviewed
        '''
        l1 = self.get_curr_learn_stack(time)
        self.curr_learn_stack = l1
        l2 = []
        l3 = []
        n_review = (time * 60 - len(l1) * self.t_learn) // self.t_review
        for i in range(n_review):
            card = self.review.get_card()
            l2.append(card.index)
            l3.append(card)
        self.curr_review_stack = l3
        return (l1, l2)

    def update_stack(self, n_learnt, answer=[]):
        '''
        n_earnt: the number of characters learnt
        answer: list of answers to l2; 1: correct, 0: incorrect
        '''
        n_answer = len(answer)
        for i in range(n_learnt):
            self.review.add_card(self.curr_learn_stack[i])
        self.learn_stack = self.learn_stack[n_learnt:]

        for i in range(len(answer)):
            self.review.update_card(self.curr_review_stack[i], answer[i])
        for i in range(n_answer, len(self.curr_review_stack)):
            self.review.insert_card(self.curr_review_stack[i])

    def update_date(self):
        '''
        decrement the priority
        '''
        self.review.stack = [[x[0] - 1, decrement(x[1])] for x in self.review.stack]
        heapify(s.review.stack)


s = UserStack()
learn_stack = list(range(60))
learn_stack = ['C00' + str(x) for x in learn_stack]
s.new_learn_stack(learn_stack)
# stacks=s.get_stack(1)

'''
each day
0. (already finished a stack? - yes) s.new_learn_stack(learn_stack)
1. s.get_stack(time = 10 (min))
2. s.update_stack(learnt=[1,1,...], answer=[1,0,0,...])
3. s.update_date()
'''
























