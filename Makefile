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

.PHONY: register
register: ${VENV}
	source .venv/${VENV}/bin/activate;\
		python -m register

.PHONY: call
call: ${VENV}
	source .venv/${VENV}/bin/activate;\
		python -m call

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

.PHONY: bondy
bondy:
	docker run \
		-e BONDY_ERL_NODENAME=bondy1@127.0.0.1 \
		-e BONDY_ERL_DISTRIBUTED_COOKIE=bondy \
		-p 18080:18080 \
		-p 18081:18081 \
		-p 18082:18082 \
		-p 18086:18086 \
		-u 0:1000 \
		-v "$(PWD)/bondy/etc:/bondy/etc" \
		--name bondy-beta.64 \
		-d leapsight/bondy:1.0.0-beta.64
