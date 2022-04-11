# Arcane incantation to print all the other targets, from https://stackoverflow.com/a/26339924
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

conda-update:
	conda env update --prune -f env.yml

pip-tools:
	pip-compile requirements/dev.in && pip-compile requirements/prod.in
	pip-sync requirements/dev.txt && pip-sync requirements/prod.txt


# Recipe for activating the conda environment within the sub-shell as a target, from https://stackoverflow.com/a/55696820/13749426
.ONESHELL:
shell := /bin/$(ps | grep `echo $$` | awk '{ print $4 }')
print:
	ps | grep `echo $$` | awk '{ print $4 }'
	@echo "${shell}";
# Need to specify bash in order for conda activate to work, otherwise it will try to use the default shell, which is "zsh" in this case
SHELL = /bin/zsh

# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH, otherwise it will not work
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

# Create conda env from env.yml and compile and install exact pip packages
conda-pip:
	conda env update --prune -f env.yml
	$(CONDA_ACTIVATE) mentalHealth
	pip-compile requirements/dev.in && pip-compile requirements/prod.in
	pip-sync requirements/dev.txt && pip-sync requirements/prod.txt
