"""
    APP manage file
"""

from flask_script import Manager
from app import create_app

APP = create_app()
MANAGER = Manager(APP)

@MANAGER.command
def run():
    """ Command application run """
    APP.run(port=5001)

if __name__ == '__main__':
    MANAGER.run()