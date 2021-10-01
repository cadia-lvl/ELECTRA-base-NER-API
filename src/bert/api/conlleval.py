'''
Copyright (C) 2021 by Ásmundur A. Guðjónsson
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE
'''

import sys,os

# def create_conlleval_output(guess_path, correct_path):
#     """
#     :param guess_path: the string path to the file with the annoted text to be evaluated, a NER tagged text in the CoNNL format
#     :param correct_path: the string path to the correctly annoted text file, a NER tagged text in the CoNNL format
#     :param output_path:the string path to the output_file, a NER tagged text in the CoNNL format
#     """
guess_path = sys.argv[1]
correct_path = sys.argv[2]
# output_path = sys.argv[3]

with open(guess_path, 'r') as f:
    guess_lines = f.readlines()

with open(correct_path, 'r') as f:
    correct_lines = f.readlines()

with open('tmp', 'w') as f:
    for i in range(0, len(correct_lines)):
        correct_parts = (correct_lines[i]).split('\t')
        guess_parts = (guess_lines[i]).split('\t')


        if len(correct_parts) == 2 :
            correct_tag = correct_parts[1].replace('\n', '')
            wrt_str = "{} {} {}".format(correct_parts[0], correct_tag , guess_parts[1])
            f.write(wrt_str)
        else:
            f.write('\n')

os.system('perl conlleval.pl < tmp')
os.system('rm tmp')