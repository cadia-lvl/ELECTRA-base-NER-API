# Icelandic NER API 

This project is a minor modification to https://github.com/ditadi/ner

A docterized and deployable Named Entity Recognition tool for Icelandic, using a ELECTRA-base Icelandic langauge fined tuned for NER on the MIM-GOLD-NER corpus. 


1) Make sure that Docker is properly installed
2) downlaod [the zipped pytorch model directory](https://drive.google.com/file/d/1ymquVvgU1b5sDZRimVRZtEQ1-hAMlz_H/view?usp=sharing) and extract to directory ./src/bert/model
3) make sure that the content of the pytorch directory are directly under the ./src/bert/model directory. (e.g. ./src/bert/model/pytorch_model.bin needs to be the correct path to the model binary. 
4) run the following commands starting in root directory of the project to deploy locally

```bash
cd src/bert
make build
make run
```

[Link to OpenAPI documentation](https://app.swaggerhub.com/apis/asmundur10/icelandic-ner-electra/1.0.0)


## API calls
All the API calls use post and input/outputs are in a json format.
Further details about the api calls are automatically generated when the container is run and can be found in /docs or /redoc

| HTTP METHOD | Description |
| ----------- | --------------- |
| /predict | Takes in Icelandic text and returns text with icelandic named entetiy recognition |

# Acknowledgements
[Reykjavik University](https://lvl.ru.is)

This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

