#!/usr/bin/env python
import os

from app import create_app
from flask_script import Manager

app_docker = 'docker'
app_default = 'default'

app = create_app(app_docker)
manager = Manager(app)

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host='0.0.0.0')
