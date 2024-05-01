from collections import Counter
import re


def actions(text: str, action_number: int):
    sentences = re.split(r'(?<=[.?!])\s*', text.lower())

    words_in_questions = set()
    words_in_exclamations = set()
    words_in_narratives = set()

    last_questions = [sentence for sentence in sentences if sentence.endswith('?')]
    last_exclamations = [sentence for sentence in sentences if sentence.endswith('!')]
    last_narratives = [sentence for sentence in sentences if sentence.endswith('.')]

    last_question = last_questions[-1] if last_questions else None
    last_exclamation = last_exclamations[-1] if last_exclamations else None
    last_narrative = last_narratives[-1] if last_narratives else None

    last_words_in_question = set(last_question.strip().split()) if last_question else set()
    last_words_in_exclamation = set(last_exclamation.strip().split()) if last_exclamation else set()
    last_words_in_narrative = set(last_narrative.strip().split()) if last_narrative else set()

    for sentence in sentences:
        words = set(sentence[:-1].lower().strip().split())
        if sentence.endswith('?'):
            words_in_questions.update(words)
        elif sentence.endswith('!'):
            words_in_exclamations.update(words)
        else:
            words_in_narratives.update(words)

    actions_dict = {
        1: words_in_questions.difference(words_in_exclamations, words_in_narratives),
        2: words_in_exclamations.difference(words_in_questions, words_in_narratives),
        3: words_in_narratives.difference(words_in_questions, words_in_exclamations),
        4: (words_in_exclamations.union(words_in_narratives)).difference(words_in_questions),
        5: (words_in_questions.union(words_in_exclamations)).difference(words_in_narratives),
        6: (words_in_questions.union(words_in_narratives)).difference(words_in_exclamations),
        7: words_in_questions.intersection(words_in_narratives).difference(words_in_exclamations),
        8: words_in_questions.intersection(words_in_exclamations).difference(words_in_narratives),
        9: words_in_exclamations.difference(words_in_questions.union(words_in_narratives)),
        10: words_in_narratives.difference(words_in_questions.union(words_in_exclamations)),
        11: words_in_questions.difference(words_in_narratives),
        12: words_in_narratives.difference(words_in_exclamations),
        13: words_in_narratives.intersection(words_in_exclamations),
        14: words_in_questions.intersection(words_in_exclamations),
        15: words_in_narratives.intersection(words_in_exclamations).difference(words_in_questions),
        16: words_in_questions.intersection(words_in_narratives).difference(words_in_exclamations),
        17: words_in_questions.intersection(words_in_exclamations).difference(words_in_narratives),
        18: words_in_narratives.union(last_words_in_question).difference(words_in_exclamations,
                                                                         words_in_questions - last_words_in_question),
        19: words_in_questions.union(last_words_in_exclamation).difference(words_in_narratives,
                                                                           words_in_exclamations - last_words_in_exclamation),
        20: words_in_exclamations.union(last_words_in_narrative).difference(words_in_questions,
                                                                            words_in_narratives - last_words_in_narrative),
    }

    result = actions_dict[action_number]

    return result, len(result)


while True:
    print('''В файле "text.txt" задан текст, состоящий из предложений, разделённых знаками препинания из набора «.?!». 
Предложения в свою очередь состоят из слов, отделённых друг от друга пробелами. 
Найти слова (без учёта регистра) и их количество, которые:
1.  встречаются только в вопросительных предложениях.
2.  встречаются только в восклицательных предложениях.
3.  встречаются только в повествовательных предложениях.
4.  не встречаются в вопросительных предложениях.
5.  не встречаются в повествовательных предложениях.
6.  не встречаются в восклицательных предложениях.
7.  встречаются только в повествовательных и вопросительных предложениях.
8.  встречаются только в вопросительных и восклицательных предложениях.
9.  не встречаются ни в повествовательных, ни в вопросительных предложениях.
10. не встречаются ни в вопросительных, ни в восклицательных предложениях.
11. встречаются в вопросительных, но не встречаются в повествовательных предложениях.
12. встречаются в повествовательных, но не встречаются в восклицательных предложениях.
13. встречаются одновременно и в повествовательных, и в восклицательных предложениях.
14. встречаются одновременно и в вопросительных, и в восклицательных предложениях.
15. встречаются одновременно и в повествовательных, и в восклицательных предложениях, но не встречаются в вопросительных.
16. встречаются одновременно и в повествовательных, и в вопросительных предложениях, но не встречаются в восклицательных.
17. встречаются одновременно и в вопросительных, и в восклицательных предложениях, но не встречаются в повествовательных.
18. встречаются только в повествовательных предложениях и возможно в последнем из вопросительных.
19. встречаются только в вопросительных предложениях и возможно в последнем из восклицательных.
20. встречаются только в восклицательных предложениях и возможно в последнем из повествовательных.
21. Завершить работу.''')

    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        with open('text.txt', 'r', encoding='utf-8') as file:
            all_text = ''.join([line.strip('\n') for line in file.readlines()])
        print(actions(all_text, action))
        question = input('Хотите продолжить (да/нет)? ').lower().strip()
        if question == 'да':
            continue
        elif question == 'нет':
            break
        else:
            print('Извините, но вы ввели не "да" и не "нет".')
    elif action == 21:
        break
    else:
        print('Извините, но нет такого действия, попробуйте еще раз.')
