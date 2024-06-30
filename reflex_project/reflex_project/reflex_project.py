"""Welcome to Reflex!."""

# Import all the pages.
from reflex_project.pages import *

import reflex as rx


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""

def index():
    return

# Create the app.
app = rx.App()
