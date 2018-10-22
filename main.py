import random
import os
import click
import json
from markov_chain import *


def load_text(path):
    to_remove='\n"‘’'
    with open(path, 'r') as f:
        data = f.read()

    for i in to_remove:
        data = data.replace(i, ' ')
    return data.split()


def load_json(path):
    to_add_space = ".!?:;,"
    with open(path) as json_file:
        text = json_file.read()
    for i in to_add_space:
        text = text.replace(i, i+' ')

    json_data = json.loads(text)

    ret = []
    for i in json_data:
        words = ""
        if '@' not in i['text'] and 'http' not in i['text']:
            words += i['text']
        ret.append(words.split())

    return ret


def generate_words(chain, order, no_sentences=1):
    words = ""
    cur = pick_start(chain)
    for i in range(0, order):
        words += cur[i] + ' '

    while words.count('.') < no_sentences:
        try:
            next_word = chain[cur].pick_at_random()
        except:
            cur = pick_start(chain)
            for i in range(0, order-1):
                words += cur[i] + ' '
            next_word = cur[-1]

        words += next_word + ' '
        cur = cur[1:] + (next_word,)
        
    return words


def build_chain(directory, order, use_json):
    chain = create_chain()
    for filename in os.listdir(directory):
        if not use_json:
            if filename.endswith(".txt"):
                add_to_chain(chain, load_text(os.path.join(directory, filename)), order)
        else:
            if filename.endswith(".json"):
                tweets = load_json(os.path.join(directory, filename))
                for tweet in tweets:
                    add_to_chain(chain, tweet, order)
    return chain


@click.command()
@click.option('-d', '--directory',
                default='texts', show_default=True,
                help='Directory with input texts (.txt or .json file only).')
@click.option('-o', '--order',
                default=2, show_default=True,
                help='Order of Markov chain to use.')
@click.option('-n', '--no-sentences',
                default=1, show_default=True,
                help='Number of sentences to generate')
@click.option('-j', '--use-json',
                default=True, show_default=True,
                help='Search for .json files instead of .txt')
def main(directory, order, no_sentences, use_json):
    """Random text generator based on nth-order Markov chain"""
    chain = build_chain(directory, order, use_json=use_json)
    words = generate_words(chain, order, no_sentences=no_sentences)
    print(words)


if __name__ == '__main__':
    main()
