# ab-examples
Simple examples about using Autobahn-py

## Prerequisites
### `python`
* Requires python 3.7+
* Recommanded python 3.10

Check your version running:
``` bash
$ python --version
```

### `bondy` router
By default, the scripts connect anonymously to the `io.bondy.my` realm on a bondy router running on `localhost` and accepting websocket connections on port `18080`.

This can however be overriden with the environment variables:
* `BONDY_URL` for the router
* `BONDY_REALM` for the realm
* `AUTH_METHOD` for the authentication method

## Opening a session
`connect.py` gives an example of a script that connects to bondy only.
It logs when a session is opened and closed by the router:
``` bash
% make connect
source .venv/venv/bin/activate;\
	python -m connect
2022-09-16T22:19:29 trying transport 0 ("ws://localhost:18080/ws") using connect delay 0
2022-09-16T22:19:29 connecting once using transport type "websocket" over endpoint "tcp"
Joined realm io.bondy.my from session 3964461691944587
2022-09-16T22:19:41 session leaving 'wamp.close.system_shutdown'
Left realm io.bondy.my from session None because Router is shutting down (wamp.close.system_shutdown)
2022-09-16T22:19:41 wamp.close.system_shutdown: Router is shutting down
2022-09-16T22:19:41 trying transport 0 ("ws://localhost:18080/ws") using connect delay 2.12233472166706
2022-09-16T22:19:43 connecting once using transport type "websocket" over endpoint "tcp"
```

Type Ctrl-C to kill the script.
``` bash
% make connect
source .venv/venv/bin/activate;\
	python -m connect
2022-09-16T22:53:01 trying transport 0 ("ws://localhost:18080/ws") using connect delay 0
2022-09-16T22:53:01 connecting once using transport type "websocket" over endpoint "tcp"
Joined realm io.bondy.my from session 762962482670083
^C2022-09-16T22:53:02 Shutting down due to SIGINT
Done.
```
