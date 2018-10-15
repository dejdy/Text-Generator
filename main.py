import random
import os
import click
from markov_chain import *


def load_text(path):
    to_remove='\n"‘’'
    with open(path, 'r') as f:
        data = f.read()

    for i in to_remove:
        data = data.replace(i, ' ')
    return data.split()


def generate_words(chain, order, no_sentences=1):
    words = ""
    cur = pick_start(chain)
    for i in range(0, order):
        words += cur[i] + ' '

    while words.count('.') < no_sentences:
        next_word = chain[cur].pick_at_random()
        words += next_word + ' '
        cur = cur[1:] + (next_word,)
        
    return words


def build_chain(directory, order):
    chain = create_chain()
    for filename in os.listdir(directory):
        add_to_chain(chain, load_text(os.path.join(directory, filename)), order)
    return chain


@click.command()
@click.option('-d', '--directory',
                default='texts', show_default=True,
                help='Directory with input texts (.txt file only).')
@click.option('-o', '--order',
                default=2, show_default=True,
                help='Order of Markov chain to use.')
@click.option('-n', '--no-sentences',
                default=1, show_default=True,
                help='Number of sentences to generate')
def main(directory, order, no_sentences):
    """Random text generator based on nth-order Markov chain"""
    chain = build_chain(directory, order)
    words = generate_words(chain, order, no_sentences=no_sentences)
    print(words)


if __name__ == '__main__':
    main()
