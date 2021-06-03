
import torch
import json

def chunks(lst, n):
  """Yield successive n-sized chunks from lst."""

  for i in range(0, len(lst), n):
    yield lst[i:i + n]

from transformers import AutoTokenizer, AutoModelForTokenClassification


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
      inputs = self._tokenizer.encode(sequence, return_tensors="pt")

      outputs = self._model(inputs)[0]

      predictions = torch.argmax(outputs, dim=2)
      outcomes = [self._label_dict[str(prediction)] for prediction in predictions[0].tolist()]
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