# Icelandic NER API 

This project is a minor modification to https://github.com/ditadi/ner

A dockerized and deployable Named Entity Recognition tool for Icelandic, using the [IceBERT](https://huggingface.co/mideind/IceBERT-igc/tree/main) model, which also offers the possibilty of using a combination of 4 Transformer models that together achieve a better F-Score on the test set for the MIM-GOLD-NER corpus, which all of them were fine tuned on. 


1) Make sure that Docker is properly installed
2) downlaod [the zipped pytorch models directory](https://drive.google.com/file/d/1ymquVvgU1b5sDZRimVRZtEQ1-hAMlz_H/view?usp=sharing) and extract to directory ./src/bert/
<!-- 3) make sure that the content of the pytorch directory are directly under the ./src/bert/model directory. (e.g. ./src/bert/model/pytorch_model.bin needs to be the correct path to the model binary.  -->
3) run the following commands starting in root directory of the project to deploy locally

```bash
cd src/bert
make build
make run
```

[Link to OpenAPI documentation](https://app.swaggerhub.com/apis/asmundur10/Icelandic-NER/1.0.0-oas3)

