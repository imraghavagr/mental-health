.PHONY: clean 

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DATA_URL := 
DATA_DIR := $(PROJECT_DIR)/data/raw/

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
	rm -f data/raw/*.csv

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
SHELL = /bin/zsh

# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH, otherwise it will not work
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


conda-pip:
	@# Help: Create/update conda env and install the exact pip packages into it
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating/updating conda environment."
	conda env update --prune -f env.yml
	$(CONDA_ACTIVATE) mentalHealth
	pip-compile requirements/dev.in && pip-compile requirements/prod.in
	pip-sync requirements/dev.txt && pip-sync requirements/prod.txt
	pip install "pycaret[full]"
else
	@echo ">>> conda not detected, please use a shell configured with conda. Use "Anaconda Prompt" for Windows. Please download and install Anaconda if you don't already have it. Exiting..."
endif

.active:
	@echo "Activating conda environment"
	$(CONDA_ACTIVATE)

data/raw/iris.csv: .active
	@# Help: Download the data from the source and save it to the data/raw/ directory
	python scripts/data/download.py "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data" $@


.DEFAULT_GOAL := help
.PHONY: help
# Arcane incantation to print all the targets along with their descriptions mentioned with "@# Help: <<Description>>", from https://stackoverflow.com/a/65243296/13749426. Check https://stackoverflow.com/a/20983251/13749426 and https://stackoverflow.com/a/28938235/13749426 for coloring terminal outputs.
help:
	@printf "%-20s %s\n" "Target" "Description"
	@printf "%-20s %s\n" "------" "-----------"
	@make -pqR : 2>/dev/null \
		| awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
		| sort \
		| egrep -v -e '^[^[:alnum:]]' -e '^$@$$' \
		| xargs -I _ sh -c 'printf "\033[1;32m%-20s\033[0;33m " _; make _ -nB | (grep -i "^# Help:" || echo "") | tail -1 | sed "s/^# Help: //g"'
