import torch
import json

def chunks(lst, n):
  """Yield successive n-sized chunks from lst."""

  for i in range(0, len(lst), n):
    yield lst[i:i + n]

from transformers import AutoTokenizer, AutoModelForTokenClassification

def post_process(sequence, tokens, offset_mappings, outcomes):
  def remove_index(index, tokens, outcomes):
    assert index > 0
    removed_token = tokens.pop(index)
    tokens[index - 1] += removed_token
    # this code assumes the model is smart enough to classify each token
    # when a word is broken up into smaller tokens, with the same tag.
    # but may require testing, the following code may help with that.
    # TEST CODE BELOW
    # removed_outcome = outcomes.pop(index)
    # assert outcomes[index-1] == removed_outcome
    # ATTENTION, MAKE SURE TO COMMENT OUT outcomes.pop(index) HERE BELOW
    # IF USING THE COMMENTED OUT TEST CODE HERE ABOVE
    outcomes.pop(index)

  def fix_tokens(indices, sequence, tokens, offset_mappings):
    for i in indices:
      lower_bound, upper_bound = offset_mappings[i]
      tokens[i] = sequence[lower_bound:upper_bound]

  # find the indices of the extra tokens, if it begins in the same index as the
  # previous item, (offset_mapping), it's either a punctuation, or, an 'extra-token',
  # and then you distinguish between the two because the length of the extra token
  # is longer than the length of its corresponding offset map.
  indices = [i for i, (a, b) in enumerate(offset_mappings) if
             i > 0 and a == offset_mappings[i - 1][1] and
             offset_mappings[i - 1][1] - offset_mappings[i - 1][0] != 0 and
             len(tokens[i]) != offset_mappings[i][1] - offset_mappings[i][0]]
  fix_tokens(indices, sequence, tokens, offset_mappings)
  # remove indices from list in reversed order
  for i in indices[::-1]:
    remove_index(i, tokens, outcomes)

class ModelWrapper():
  def __init__(self, model, tokenizer, label_dict, max_length):
    self._model = model
    self._tokenizer = tokenizer
    self._label_dict = label_dict
    self._MAX_LENGTH = max_length

  def predict(self, data):
    text = data.iloc[0]['text']
    splits = text.split(' ')
    sequences = list(chunks(splits, self._MAX_LENGTH))
    all_tokens = []
    all_predictions = []
    print(len(sequences))
    for sequence_splits in sequences:

      sequence = ' '.join(sequence_splits)
      tokens = self._tokenizer.tokenize(self._tokenizer.decode(self._tokenizer.encode(sequence)))
      encoded_data = self._tokenizer.encode_plus(sequence, return_tensors="pt", add_special_tokens=True,
                                                 max_length=self._MAX_LENGTH,
                                                 return_offsets_mapping=True)
      inputs = encoded_data['input_ids']

      outputs = self._model(inputs)[0]

      predictions = torch.argmax(outputs, dim=2)
      outcomes = [self._label_dict[str(prediction)] for prediction in predictions[0].tolist()]
      offset_mappings_numpy = encoded_data['offset_mapping'].numpy()
      offset_mappings = [tuple(x) for x in offset_mappings_numpy[0]]
      post_process(sequence, tokens, offset_mappings, outcomes)
      all_predictions.extend(outcomes)
      all_tokens.extend(tokens)


    return all_tokens, all_predictions



def _load_pyfunc(path):
  model = AutoModelForTokenClassification.from_pretrained('/root/model/')

  # Load in the tokenizer
  tokenizer = AutoTokenizer.from_pretrained('/root/model/')

  max_length = 360
  # max_length -= tokenizer.num_special_tokens_to_add()

  # Load in the config file for label mapping
  with open('/root/model/config.json', 'r') as f:
    label_dict = json.load(f)['id2label']


  return ModelWrapper(
      model=model,
      tokenizer=tokenizer,
      label_dict=label_dict,
      max_length=max_length
  )