docker stop ner_api
docker container rm ner_api
docker build . -t glaciersg/ner_api:v1.0.0
docker run -d -p 8080:8080 --name=ner_api glaciersg/ner_api:v1.0.0
