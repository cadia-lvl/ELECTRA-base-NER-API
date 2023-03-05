# Create common environment for training and serving BERT
FROM continuumio/miniconda3
WORKDIR /root

# Copy over dependency file to cache (hopefully) core packages
COPY ./api/model/mlflow_env.yml /root/mlflow_env.yml


# Create a conda environment from the specified conda.yaml
RUN conda env create --file /root/mlflow_env.yml

# Add to .bashrc
RUN echo "source activate mlflow-env-bert" >> .bashrc
# RUN apt-get update && apt-get -y --no-install-recommends install docker

COPY ./api/requirements.txt /root/requirements.txt

# Pip install api requirements into the conda env
RUN /bin/bash -c "source activate mlflow-env-bert" && \
	pip install --upgrade pip setuptools && \
	pip install -r /root/requirements.txt --no-cache-dir


# Download trained BERT pytorch model
# RUN wget 'https://aisc-mlops-bert.s3.amazonaws.com/model.pt' -O /root/model.pt -nc

COPY ./model/* /root/model/


# Copy api to root
COPY ./api /root

# link model	
RUN ln -s /root/model.pt ./model/data/pyfunc_data/model.pt

# Make our start script executable
#RUN ["chmod", "+x", "/root/start.sh"]

EXPOSE 8080

# Start the API
ENTRYPOINT [ "/root/start.sh" ]

