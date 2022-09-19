import os
import signal

from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run
import txaio

################################################################################
# Variable that can be controlled from the environment
BONDY_URL = os.getenv("BONDY_URL", "ws://localhost:18080/ws")
BONDY_REALM = os.getenv("BONDY_REALM", "io.bondy.my")
AUTH_METHOD = os.getenv("AUTH_METHOD", "anonymous")
RPC_URL = os.getenv("RPC_URL", "io.bondy.add")

AUTHENTICATION_CONFIG = {"anonymous": None}


class Call:

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
        print(f"Ready to call {RPC_URL}")
        await self.call()

    def _on_leave(self, session, details):
        print(
            f"Left realm {session.realm} from session {session.session_id} "
            f"because {details.message} ({details.reason})"
        )
        self._session = None

    ###########################################################################
    # Call handling
    async def call(self):
        """Call an RPC to add 2 numbers.
        Ctrl-D to quit."""

        try:
            while True:
                print("Want to add 2 numbers (Ctrl-D to quit)")
                x = input("Enter the 1st number: ")
                y = input("Enter the 2nd number: ")

                try:
                    z = await self._session.call(RPC_URL, x, y)

                except Exception as error:
                    print(f"Got an error: {error.args[0]}")

                else:
                    print(f"{x} + {y} = {z}")

        except EOFError:
            print("Ctrl-D pressed, leaving.")

        self._session.leave()


################################################################################
# Start of the script when called from prompt

if __name__ == "__main__":

    txaio.use_asyncio()
    txaio.start_logging(level="critical")

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    call = Call()
    call.start()
