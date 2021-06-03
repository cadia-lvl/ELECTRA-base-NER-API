# Icelandic NER API 

This project is a minor modification to https://github.com/ditadi/ner

A docterized and deployable Named Entity Recognition tool for Icelandic, using a ELECTRA-base Icelandic langauge fined tuned for NER on the MIM-GOLD-NER corpus. 


1) Make sure that Docker is properly installed
2) downlaod [the zipped pytorch model directory](https://drive.google.com/file/d/1LtssB04q-WcJncfEkatt52QSOjTzT8ro/view?usp=sharing) and extract to directory ./src/bert/model
3) make sure that the content of the pytorch directory are directly under the ./src/bert/model directory. (e.g. ./src/bert/pytorch_model.bin needs to be the correct path to the model binary. 
4) run the following commands to deploy locally

```bash
cd src/bertin
make build
make run
```


