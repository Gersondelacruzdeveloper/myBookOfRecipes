import os
from myonlinerecipes import app
from myonlinerecipes import db


if __name__ == "__main__":
      app.run(
        host = os.environ.get("IP"),
        port = int(os.environ.get("PORT")),
        debug = os.environ.get("DEBUG"),
)