import os
import connexion
from connexion.resolver import RestyResolver

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')  # Provide the app and the directory of the docs
    app.add_api('api_specification.yml', resolver=RestyResolver('resolve'))
    app.run(port = 8080)

