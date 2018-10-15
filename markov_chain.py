import random
import re
import collections
import itertools

class MarkovCounter(collections.Counter):
    def pick_most_common(self):
        (most_common, _), = self.most_common(1)
        return most_common

    def pick_at_random(self):
        i = random.randrange(sum(self.values()))
        return next(itertools.islice(self.elements(), i, None))


def create_chain():
    markov_chain = collections.defaultdict(MarkovCounter)
    return markov_chain

def add_to_chain(markov_chain, l, order):
    arguments = [l[i:] for i in range(1, order+1)]
    for vals in zip(l, *arguments):
        markov_chain[vals[:-1]][vals[-1]] += 1

def pick_start(markov_chain):
    ret = []
    for i in markov_chain.keys():
        if i[0][0].isupper():
            ret.append(i)

    return random.choice(ret)