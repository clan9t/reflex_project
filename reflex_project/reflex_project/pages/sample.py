"""The home page of the app."""

from reflex_project import styles
from reflex_project.templates import template

import reflex as rx

# @template(route="/", title="Home")
# def index() -> rx.Component:
#     """The home page.

#     Returns:
#         The UI for the home page.
#     """
#     with open("README.md", encoding="utf-8") as readme:
#         content = readme.read()
#     return rx.markdown(content, component_map=styles.markdown_style)

class SampleState(rx.State):
    """Define empty state to allow access to rx.State.router."""
    count: int = 0

    def increment(self):
        self.count += 1


    def decrement(self):
        self.count -= 1

@template(route="/sample", title="Sample")
def sample():
    return rx.hstack(
        rx.button(
            "Decrement",
            color_scheme="ruby",
            on_click=SampleState.decrement,
        ),
        rx.heading(SampleState.count, font_size="2em"),
        rx.button(
            "Increment",
            color_scheme="grass",
            on_click=SampleState.increment,
        ),
        spacing="4",
    )