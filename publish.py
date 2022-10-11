import os
import signal
import time

from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run
import txaio

################################################################################
# Variable that can be controlled from the environment
BONDY_URL = os.getenv("BONDY_URL", "ws://localhost:18080/ws")
BONDY_REALM = os.getenv("BONDY_REALM", "io.bondy.my")
AUTH_METHOD = os.getenv("AUTH_METHOD", "anonymous")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "io.bondy.news")
PUBSUB_EXIT_MESSAGE = os.getenv("PUBSUB_EXIT_MESSAGE", "Over and Out!")

AUTHENTICATION_CONFIG = {"anonymous": None}


class Publish:

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

    def start(self):

        run([self._component])
        print("Done.")

    ###########################################################################
    # Session handling

    async def _on_join(self, session, details):
        print(f"Joined realm {details.realm} from session {details.session}")
        self._session = session
        print(f"Ready to publish messages to {PUBSUB_TOPIC}")
        self.publish()

    def _on_leave(self, session, details):
        print(
            f"Left realm {session.realm} from session {session.session_id} "
            f"because {details.message} ({details.reason})"
        )
        self._session = None

    ###########################################################################
    # Event handling
    def publish(self):
        """Publishes some message samples then prompt for more messages.
        Exit on Ctrl-D or when "Over and Out!" is entered."""

        print("Publish an empty message")
        self._session.publish(PUBSUB_TOPIC)
        time.sleep(0.5)
        print("Publish a message as a string")
        self._session.publish(PUBSUB_TOPIC, "Hello!")
        time.sleep(0.5)
        print("Publish a message as a list")
        self._session.publish(PUBSUB_TOPIC, ["Here is a list of", 3, "arguments"])
        time.sleep(0.5)
        print("Publish a message with keyword arguments")
        self._session.publish(PUBSUB_TOPIC, n=2, what="keyword args")
        time.sleep(0.5)
        print("Publish a message with some positional and keyword args")
        self._session.publish(PUBSUB_TOPIC, ["a mix", "of"], type=["pos", "kw"])

        message = None
        try:
            while message != PUBSUB_EXIT_MESSAGE:
                message = input(
                    f"Your message ('{PUBSUB_EXIT_MESSAGE}' to publish and exit): "
                )
                self._session.publish(PUBSUB_TOPIC, message)

        except EOFError:
            print("Ctrl-D pressed, leaving.")

        self._session.leave()


################################################################################
# Start of the script when called from prompt

if __name__ == "__main__":

    txaio.use_asyncio()
    txaio.start_logging(level="critical")

    pub = Publish()
    pub.start()
