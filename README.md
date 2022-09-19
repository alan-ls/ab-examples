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
```
Type Ctrl-C to kill the script.

### Example
With logs set to `info` and a restart of the bondy router.
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
Joined realm io.bondy.my from session 762962482670083
^C2022-09-16T22:53:02 Shutting down due to SIGINT
Done.
```

## PubSub
To simulate a pubsub exchange, you need 2 terminals.
1. Launch the subscriber
``` bash
% make subscribe
```
Type Ctrl-C to kill the script or receive an `Over and Out!` message.

2. Launch the publisher
``` bash
% make publish
```
You'll see messages printed on both sides showing the publisher publishing different type of messages and the subscriber echoing them.
You'll then be able to send your own messages.
To exit hit enter `Over and Out!` or hit `Ctrl-D`.

### Example

<table>
<tr>
<th>Subscriber</th>
<th>Publisher</th>
</tr>
<tr>
<td>
<pre>
% make subscribe
source .venv/venv/bin/activate;\
	python -m subscribe
Joined realm com.thing.system from session 4993563508923879
Subscribe to com.thing.system.news
Waiting to publications...
Received an empty message.
Received a message with 1 positional args: ('Hello!',)
Received a message with 1 positional args: (['Here is a list of', 3, 'arguments'],)
Received a message with keyword args: {'n': 2, 'what': 'keyword args'}
Received a message with keyword args: {'type': ['pos', 'kw']} with 1 positional args: (['a mix', 'of'],)
Received a message with 1 positional args: ('This is important!',)
Received a message with 1 positional args: ('Over and Out!',)
Received the end of publication message. Unsubscribe and leave
Left realm com.thing.system from session None because Session closed by client. (wamp.close.goodbye_and_out)
Done.
</pre>
</td>
<td>
<pre>
% make publish
source .venv/venv/bin/activate;\
	python -m publish
Joined realm com.thing.system from session 8778930230711431
Ready to publish messages to com.thing.system.news
Publish an empty message
Publish a message as a string
Publish a message as a list
Publish a message with keyword arguments
Publish a message with some positional and keyword args
Your message: This is important!
Your message: Over and Out!
Left realm com.thing.system from session None because Session closed by client. (wamp.close.goodbye_and_out)
Done.
</pre>
</td>
</tr>
</table>

## RPC
To simulate RPC calls, you need 2 terminals.
1. Register to a URL for RPC
``` bash
% make register
```
Type Ctrl-C to kill the script.

2. Launch the caller
``` bash
% make call
```
Type Ctrl-D to exit.

You'll be prompted to enter 2 numbers. Invalid input will report an error as raised on the registered side and relayed by the router to the caller.

### Example

<table>
<tr>
<th>Caller</th>
<th>Callee</th>
</tr>
<tr>
<td>
<pre>
% make call
source .venv/venv/bin/activate;\
	python -m call
Joined realm com.thing.system from session 7854501446930238
Ready to call com.thing.system.add
Want to add 2 numbers (Ctrl-D to quit)
Enter the 1st number: 12
Enter the 2nd number: -6
12 + -6 = 6.0
Want to add 2 numbers (Ctrl-D to quit)
Enter the 1st number: 3,65
Enter the 2nd number: 7
Got an error: could not convert string to float: '3,65'
Want to add 2 numbers (Ctrl-D to quit)
Enter the 1st number: 3.65
Enter the 2nd number: 7
3.65 + 7 = 10.65
Want to add 2 numbers (Ctrl-D to quit)
Enter the 1st number: Ctrl-D pressed, leaving.
Left realm com.thing.system from session None because Session closed by client. (wamp.close.goodbye_and_out)
Done.
</pre>
</td>
<td>
<pre>
% make register
source .venv/venv/bin/activate;\
	python -m register
Joined realm com.thing.system from session 2073741246722595
Register to com.thing.system.add
Request to add '12' and '-6'
Return 6.0 as result
Request to add '3,65' and '7'
Raise an error for invalid input: could not convert string to float: '3,65'
Request to add '3.65' and '7'
Return 10.65 as result
^CDone.
</pre>
</td>
</tr>
</table>
