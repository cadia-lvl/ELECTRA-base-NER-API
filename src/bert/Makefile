build:
	docker build -t electra_mlflow .
run:
	docker run -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp --gpus all -it --rm --name ner  -p 5000:5000 electra_mlflow
