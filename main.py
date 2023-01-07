"""Main entry point into command line menu."""

import db
from menus import Menu

if __name__ == "__main__":
    db.create_tables()
    menu = Menu()
    menu.get_user_input()
