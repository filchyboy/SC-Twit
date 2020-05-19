'''
This initiates the entire setup by calling app.py and
instantiating the class.
'''

from .app import create_app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
