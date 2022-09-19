import os
import signal

from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run

################################################################################
# Variable that can be controlled from the environment
BONDY_URL = os.getenv("BONDY_URL", "ws://localhost:18080/ws")
BONDY_REALM = os.getenv("BONDY_REALM", "io.bondy.my")
AUTH_METHOD = os.getenv("AUTH_METHOD", "anonymous")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "io.bondy.news")

AUTHENTICATION_CONFIG = {"anonymous": None}


class Subscribe:

    ###########################################################################
    # Creation of the autobahn component and hooking the relevant methods

    def __init__(self):

        # Create the autobahn component
        transport = {
            "type": "websocket",
            "url": BONDY_URL,
            "serializers": ["json"],
        }
        auth_config = AUTHENTICATION_CONFIG[AUTH_METHOD]
        self._component = Component(
            transports=[transport], authentication=auth_config, realm=BONDY_REALM
        )

        # Register the methods that handle the session
        self._component.on("join", self._on_join)
        self._component.on("leave", self._on_leave)

        self._session = None
        self._subscription = None

    def start(self):

        run([self._component])
        print("Done.")

    ###########################################################################
    # Session handling

    async def _on_join(self, session, details):
        print(f"Joined realm {details.realm} from session {details.session}")
        self._session = session
        print(f"Subscribe to {PUBSUB_TOPIC}")
        self._subscription = await session.subscribe(self.on_event, PUBSUB_TOPIC)
        print("Waiting to publications...")

    def _on_leave(self, session, details):
        print(
            f"Left realm {session.realm} from session {session.session_id} "
            f"because {details.message} ({details.reason})"
        )
        self._session = None

    ###########################################################################
    # Event handling
    def on_event(self, *args, **kwargs):
        """Echo any message received until the "Over and Out!".

        The generic argument list allows to receive any kind of inpu.
        The signature can be more restrictive.
        """
        if not args and not kwargs:
            out = "Received an empty message."

        else:
            out = "Received a message "
            if kwargs:
                out += f"with keyword args: {kwargs} "

            if args:
                out += f"with {len(args)} positional args: {args}"

        print(out)
        if "Over and Out!" in args:
            print(f"Received the end of publication message. Unsubscribe and leave")
            self._subscription.unsubscribe()
            self._session.leave()


################################################################################
# Start of the script when called from prompt

if __name__ == "__main__":

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    sub = Subscribe()
    sub.start()
