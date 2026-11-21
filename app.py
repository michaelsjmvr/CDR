"""Entry point for the local Crônicas do Recomeço prototype."""

import os

from game_app import create_app, socketio


app = create_app()


if __name__ == "__main__":
    socketio.run(
        app,
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=False,
        allow_unsafe_werkzeug=True,
    )
