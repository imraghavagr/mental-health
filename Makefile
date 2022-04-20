.PHONY: clean data help

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DATA_URL := faruqui682/mental-health-survey
DATA_DIR := $(PROJECT_DIR)/data/raw/
DATA_INTERIM_DIR := $(PROJECT_DIR)/data/interim/
DATA_PROCESSED_DIR := $(PROJECT_DIR)/data/processed/
SCRIPT_DIR := $(PROJECT_DIR)/scripts/
ARTIFACT_DIR := $(PROJECT_DIR)/artifacts/
MODEL_DIR := $(ARTIFACT_DIR)/pycaretModels/

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

clean:
	@# Help: Clean the data/raw/ directory
	rm -f $(DATA_DIR)*.csv
	rm -f $(DATA_DIR)*.zip

# For windows
conda-update:
	@# Help: Update conda environment
ifeq (True,$(HAS_CONDA))
			@echo ">>> Detected conda, creating/updating conda environment."
			conda env update --prune -f env.yml
else
			@echo ">>> conda not detected, please use a shell configured with conda. Use "Anaconda Prompt" for Windows. Please download and install Anaconda if you don't already have it. Exiting..."
endif

.pip-tools:
	pip-compile requirements/dev.in && pip-compile requirements/prod.in
	pip-sync requirements/dev.txt && pip-sync requirements/prod.txt


# Recipe for activating the conda environment within the sub-shell as a target, from my solution at https://stackoverflow.com/a/71548453/13749426
.ONESHELL:
# Need to specify bash in order for conda activate to work, otherwise it will try to use the default shell, which is "zsh" in this case
SHELL = /bin/bash

# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH, otherwise it will not work
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


conda-pip:
	@# Help: Create/update conda env and install the exact pip packages into it
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating/updating conda environment."
	conda env update --prune -f env.yml
	$(CONDA_ACTIVATE) mentalHealth
	pip-compile requirements/req.in
	pip-sync requirements/req.txt
	pip install "pycaret[full]"
else
	@echo ">>> conda not detected, please use a shell configured with conda. Use "Anaconda Prompt" for Windows. Please download and install Anaconda if you don't already have it. Exiting..."
endif


data:
	@# Help: Download the data from the source and save it to the data/raw/ directory
	$(CONDA_ACTIVATE) mentalHealth
	kaggle datasets download $(DATA_URL) -p $(DATA_DIR)
	unzip $(DATA_DIR)*.zip -d $(DATA_DIR) -A
	rm -f $(DATA_DIR)*.zip
	wget --no-check-certificate --output-document=$(DATA_DIR)survey.csv 'https://docs.google.com/spreadsheets/d/1Zga_eVHZOktbAgTKevxUL_2cQlkQCJjsw4WA_tyHn2w/export?format=csv'

data_merge:
	@# Help: Combine existing data and latest survey data and save it to$(DATA_INTERIM_DIR) directory
	$(CONDA_ACTIVATE) mentalHealth
	python $(SCRIPT_DIR)data/new_data_merge.py $(DATA_DIR) $(DATA_INTERIM_DIR)

preprocess:
	@# Help: Preprocess the data and save it to the $(DATA_PROCESSED_DIR) directory
	$(CONDA_ACTIVATE) mentalHealth
	python $(SCRIPT_DIR)features/preprocess.py $(DATA_INTERIM_DIR) $(DATA_PROCESSED_DIR)

train_model:
	@# Help: Read the final processed data, train the optimal model and save the pkl file to $(MODEL_DIR) directory
	$(CONDA_ACTIVATE) mentalHealth
	python $(SCRIPT_DIR)model/train_model.py $(DATA_PROCESSED_DIR) $(MODEL_DIR)


app:
	@# Help: Run the FastAPI app
	$(CONDA_ACTIVATE) mentalHealth
	python $(SCRIPT_DIR)api/app.py

docker:
	@# Help: Build the docker image
	DOCKER_BUILDKIT=1 docker build -f "Dockerfile" -t mentalhealth .
	docker tag mentalhealth:latest mentalhealth:v1.0.0
	docker run -d -p 8000:8000 mentalhealth

.DEFAULT_GOAL := help
# Arcane incantation to print all the targets along with their descriptions mentioned with "@# Help: <<Description>>", from https://stackoverflow.com/a/65243296/13749426. Check https://stackoverflow.com/a/20983251/13749426 and https://stackoverflow.com/a/28938235/13749426 for coloring terminal outputs.
help:
	@printf "%-20s %s\n" "Target" "Description"
	@printf "%-20s %s\n" "------" "-----------"
	@make -pqR : 2>/dev/null \
		| awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
		| sort \
		| egrep -v -e '^[^[:alnum:]]' -e '^$@$$' \
		| xargs -I _ sh -c 'printf "\033[1;32m%-20s\033[0;33m " _; make _ -nB | (grep -i "^# Help:" || echo "") | tail -1 | sed "s/^# Help: //g"'
