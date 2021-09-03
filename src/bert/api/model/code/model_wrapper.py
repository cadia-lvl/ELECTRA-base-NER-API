import os
import time
from typing import List, Any

import torch
import json
# from datasets import load_dataset

import traceback


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""

    for i in range(0, len(lst), n):
        yield lst[i:i + n]


from transformers import AutoTokenizer, AutoModelForTokenClassification


# from tokenizers import ByteLevelBPETokenizer


class ModelWrapper():
    def __init__(self, model, tokenizer, label_dict, max_length):
        self._model = model
        self._tokenizer = tokenizer
        self._label_dict = label_dict
        self._MAX_LENGTH = max_length

    def predict(self, data):
        text = data.iloc[0]['text']
        return self.predict_sent(text)

    def predict_sent(self, text):

        splits = text.split(' ')
        sequences = list(chunks(splits, self._MAX_LENGTH))
        all_tokens = []
        all_predictions = []
        for sequence_splits in sequences:

            sequence = ' '.join(sequence_splits)
            try:

                ids_to_remove = []
                encoded_seq = self._tokenizer(sequence, return_offsets_mapping=True, add_special_tokens=False)
                unique_token_indices = []
                token_indices = encoded_seq['offset_mapping']
                seen = set()
                # clean_offsets = []
                for i in range(len(token_indices)):
                    x = token_indices[i]
                    if x not in seen:
                        seen.add(x)
                        unique_token_indices.append(x)
                        # clean_offsets.append(x)
                    else:
                        ids_to_remove.append(i)
                token_indices = unique_token_indices

                tokens = []

                # a variable that keeps track of the end index in the previous word
                # to correct it when words are split up in the tokenization
                last_end_index = -1

                current_index = 0
                for index in token_indices:
                    token = sequence[index[0]: index[1]]

                    if index[0] == last_end_index:

                        last_list_index = len(tokens) - 1

                        tokens[last_list_index] += token
                        ids_to_remove.append(current_index)
                    else:

                        tokens.append(token)

                    last_end_index = index[1]
                    current_index += 1


            except Exception as e:
                print(4 * '\\o -TOKENIZATION ERROR- o/')
                print('=' * 20)
                print(super(type(e)))
                print('-' * 20)
                # tb = sys.exc_info()[2]
                # print('-'*20)

                traceback.print_tb(e.__traceback__)
                print('-' * 20)

                print(sequence)
                print('=' * 20)

                print(4 * 'o/ -CLOSING- \\o')

            inputs = self._tokenizer.encode(sequence, return_tensors="pt")

            outputs = self._model(inputs)[0]

            predictions = torch.argmax(outputs, dim=2)
            outcomes = [self._label_dict[str(prediction)] for prediction in predictions[0].tolist()]
            outcomes = outcomes[1:-1]
            ids_to_remove.sort(reverse=True)
            # print(ids_to_remove)
            for id in ids_to_remove:
                del outcomes[id]

            all_predictions.extend(outcomes)
            all_tokens.extend(tokens)

        return all_tokens, all_predictions

    # def filter_tokens_tags(self, tokens, tags):
    #   filtered_tokens: List[Any] = []
    #   filtered_tags = []
    #   # print(tokens)
    #   # print(tags)
    #   # temp = list(zip(tokens, tags))
    #   # print(temp)
    #   for token, tag in zip(tokens, tags):
    #     if token in ['[CLS]', '[SEP]']:
    #       continue
    #     elif token[:2] == '##':
    #       if len(filtered_tokens) == 0 or '#' in token[2:] :
    #         filtered_tokens.append(token)
    #         filtered_tags.append(tag)
    #       else:
    #         #ADD VALIDATION HERE THAT TAGS ARE CORRECT
    #         filtered_tokens[len(filtered_tokens) - 1] += token[2:]
    #         print('FILTER_TOKENS')
    #         print(tokens)
    #     else:
    #       filtered_tokens.append(token)
    #       filtered_tags.append(tag)
    #   # print(20 * 'XXXX')
    #   # print(token)
    #   # print(tag)
    #   # print(20*'XXXX')
    #   # print(filtered_tokens)
    #   # print(filtered_tags)
    #   return filtered_tokens, filtered_tags

    def get_token_from_conll_line(self, line):
        return line.split('\t')[0]

    def get_tag_from_conll_line(self, line):
        return line.split('\t')[1]

    def check_if_tag_same_type(self, tag1, tag2):
        if len(tag1) != len(tag2):
            return False
        elif tag1 == tag2:
            return True
        else:
            return tag1[2:] == tag2[2:]

    # def correct_conll_sentence(self, correct_sent, model_sent):
    #     correct_lines = correct_sent.split('\n')
    #     model_lines = model_sent.split('\n')
    #     extra_token_counter = 0
    #     fixed_lines = []
    #     for i in range(len(correct_lines)):
    #         correct_line = correct_lines[i]
    #         correct_token = self.get_token_from_conll_line(correct_line)
    #         try:
    #             model_line = model_lines[i + extra_token_counter]
    #         except Exception as e:
    #             print(4 * '\\o -MODEL LINE INDEX OUT OF RANGE- o/')
    #             print('Correct lines : ')
    #             print(correct_lines)
    #             print('Model Lines : ')
    #             print(model_lines)
    #             print('Index : {}'.format(i))
    #             print('Extra token counter : {}'.format(extra_token_counter))
    #             print(4 * 'o/ -CLOSING- \\o')
    #             return 'get_tag_ERROR\tO'
    #
    #         model_token = self.get_token_from_conll_line(model_line)
    #         if correct_token == model_token:
    #             fixed_lines.append(model_line)
    #         else:
    #             token_to_check = correct_token
    #             try:
    #                 first_guessed_tag = self.get_tag_from_conll_line(model_line)
    #             except Exception as e:
    #                 print(20 * '\\o -GET TAG ERROR- o/')
    #                 print(model_sent)
    #                 print(20 * 'o/ -CLOSING- \\o')
    #                 return 'get_tag_ERROR\tO'
    #
    #             while len(token_to_check) > 0:
    #                 # model_line = model_lines[i + extra_token_counter]
    #                 try:
    #                     model_line = model_lines[i + extra_token_counter]
    #                 except Exception as e:
    #                     print(4 * '\\o -TOKEN MERGING ERROR- o/')
    #                     print('Correct lines : ')
    #                     print(correct_lines)
    #                     print('Model Lines : ')
    #                     print(model_lines)
    #                     print('Index : {}'.format(i))
    #                     print('Extra token counter : {}'.format(extra_token_counter))
    #                     print('token_to_check : {}'.format(token_to_check))
    #                     print(4 * 'o/ -CLOSING- \\o')
    #                     return 'get_tag_ERROR\tO'
    #
    #                 model_token = self.get_token_from_conll_line(model_line)
    #                 if token_to_check[:len(model_token)] != model_token:
    #                     print(4 * '\\o -ERROR- o/')
    #                     return_string = 'Mismatching sents\nMismatching sents\nORIGINAL:\n{}\nMODEL_GUESS\n{}\nEND\n'.format(
    #                         correct_sent, model_sent)
    #                     print('Mismatching sents')
    #                     print('ORIGINAL:')
    #                     print(correct_sent)
    #                     print('MODEL GUESS: ')
    #                     print(model_sent)
    #                     print(4 * 'o/ -CLOSING- \\o')
    #                     return return_string
    #                 else:
    #                     tag = self.get_tag_from_conll_line(model_line)
    #                     if not self.check_if_tag_same_type(first_guessed_tag, tag):
    #                         print(4 * '\\o -TAGGING FAILURE- o/')
    #                         print('Guessed:')
    #                         print(model_sent)
    #                         print('Correct:')
    #                         print(correct_sent)
    #                         print(4 * 'o/ -CLOSING- \\o')
    #
    #                     token_to_check = token_to_check[len(model_token):]
    #                     if token_to_check != '':
    #                         extra_token_counter += 1
    #             fixed_lines.append('{}\t{}'.format(correct_token, first_guessed_tag))
    #     return '\n'.join(fixed_lines)
    #
    # def correct_conll(self, correct_conll_string, model_output_conll_string):
    #     correct_sents = correct_conll_string.split('\n\n')
    #     model_sents = model_output_conll_string.split('\n\n')
    #     fixed_sents = []
    #     if len(correct_sents) != len(model_sents):
    #         print(4 * '-WARNING-')
    #         print('Inconsistent # of sents in input and output')
    #         print('LENGTH RECIEVED : {}'.format(len(correct_sents)))
    #         print('LENGTH EXPECTED : {}'.format(len(model_sents)))
    #         print('MODEL SENTS : ')
    #         print(model_sents)
    #         print('CORRECT SENTS : ')
    #         print(correct_sents)
    #         print(4 * '-WARNING-')
    #         print('\n\n\n')
    #         return 'SENT\tINCONSISTENCY'
    #     for correct_sent, model_sent in zip(correct_sents, model_sents):
    #         fixed_sents.append(self.correct_conll_sentence(correct_sent, model_sent))
    #     return '\n\n'.join(fixed_sents)

    def predict_for_conllfile(self, file, label_all_tokens=True):

        sents = file.split('\n\n')
        text_sents = []
        for sent in sents:
            sent_tokens = []
            token_tag_pairs = sent.split('\n')
            for pair in token_tag_pairs:
                token = pair.split('\t')[0]
                sent_tokens.append(token)
            text_sent = ' '.join(sent_tokens)
            if text_sent != '':
                text_sents.append(text_sent)

        tagged_sents = []
        for sent in text_sents:
            tagged_sent = self.predict_sent(sent)
            tagged_sents.append(tagged_sent)

        conll_strings = []
        for sent in tagged_sents:
            for token, tag in zip(sent[0], sent[1]):
                conll_strings.append('{}\t{}\n'.format(token, tag))
            conll_strings.append('\n')

        return ''.join(conll_strings)


def _load_pyfunc(path):
    # model = AutoModelForTokenClassification.from_pretrained('/root/model/')
    model = AutoModelForTokenClassification.from_pretrained(path)
    # Load in the tokenizer
    print(path)
    # tokenizer = AutoTokenizer.from_pretrained('/root/model/')
    try:
        with open(path + '/config.json', 'r') as f:
            model_type = json.load(f)['model_type']
            if model_type == 'roberta':
                tokenizer = AutoTokenizer.from_pretrained(path)
            else:
                tokenizer = AutoTokenizer.from_pretrained(path)
    except Exception:
        print('Failed to initialize tokenizer. Trying to pull from remote')
        with open(path + '/config.json', 'r') as f:
            name = json.load(f)['_name_or_path']
            tokenizer = AutoTokenizer.from_pretrained(name)

        # continue if file not found

    max_length = 360
    # max_length -= tokenizer.num_special_tokens_to_add()

    # Load in the config file for label mapping
    with open(path + '/config.json', 'r') as f:
        label_dict = json.load(f)['id2label']

    return ModelWrapper(
        model=model,
        tokenizer=tokenizer,
        label_dict=label_dict,
        max_length=max_length
    )
