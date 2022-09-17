import os
import signal

from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run

################################################################################
# Variable that can be controlled from the environment
BONDY_URL = os.getenv("BONDY_URL", "ws://localhost:18080/ws")
BONDY_REALM = os.getenv("BONDY_REALM", "io.bondy.my")
AUTH_METHOD = os.getenv("AUTH_METHOD", "anonymous")


AUTHENTICATION_CONFIG = {"anonymous": None}


class Connect:

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

    def _on_join(self, session, details):
        print(f"Joined realm {details.realm} from session {details.session}")
        self._session = session

    def _on_leave(self, session, details):
        print(
            f"Left realm {session.realm} from session {session.session_id} "
            f"because {details.message} ({details.reason})"
        )
        self._session = None


################################################################################
# Start of the script when called from prompt

if __name__ == "__main__":

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    connect = Connect()
    connect.start()
