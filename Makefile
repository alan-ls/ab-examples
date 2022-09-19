.PHONY: all
all: connect

VENV?=venv

.PHONY: connect
connect: ${VENV}
	source .venv/${VENV}/bin/activate;\
		python -m connect

.PHONY: publish
publish: ${VENV}
	source .venv/${VENV}/bin/activate;\
		python -m publish

.PHONY: subscribe
subscribe: ${VENV}
	source .venv/${VENV}/bin/activate;\
		python -m subscribe

.PHONY: ${VENV}
${VENV}: .venv/${VENV}/touch-file

.venv/${VENV}/touch-file: requirements.txt
ifeq (,$(shell which python))
	$(error "No python found in PATH.")
endif
	[[ -d .venv/${VENV} ]] || python -m venv .venv/${VENV}
	source .venv/${VENV}/bin/activate;\
		pip install --upgrade pip;\
		pip install -r requirements.txt
	touch .venv/${VENV}/touch-file
