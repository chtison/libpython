.PHONY: jupyter workspace

PWD := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

workspace:
	docker run -it --rm -h docker -v $(PWD):/libpython -w /libpython chtison/workspace

jupyter:
	docker run -d -p 8888:8888 -v $(PWD):/home/jovyan/work jupyter/datascience-notebook start-notebook.sh --NotebookApp.token=''
