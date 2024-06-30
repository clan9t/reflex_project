import time
from pathlib import Path
from urllib.request import urlopen
from PIL import Image

import reflex as rx
import reflex_webcam as webcam

from reflex_project import styles
from reflex_project.templates import template

# Identifies a particular webcam component in the DOM
WEBCAM_REF = "webcam"


class WebcamState(rx.State):
    last_screenshot: Image.Image | None = None
    last_screenshot_timestamp: str = ""
    loading: bool = False
    url: str = ""

    def handle_screenshot(self, img_data_uri: str):
        """Webcam screenshot upload handler.
        Args:
            img_data_uri: The data uri of the screenshot (from upload_screenshot).
        """
        self.url = img_data_uri
        if self.loading:
            return
        self.last_screenshot_timestamp = time.strftime("%H:%M:%S")
        with urlopen(img_data_uri) as img:
            self.last_screenshot = Image.open(img)
            self.last_screenshot.load()
            # convert to webp during serialization for smaller size
            self.last_screenshot.format = "WEBP"  # type: ignore


def screenshot(ref: str):
    img_url = rx.call_script(
        f"refs['ref_{ref}'].current.getScreenshot()"
        
    )
    print('aa')
    print(img_url)
    WebcamState.url = img_url


def last_screenshot_widget(ref: str) -> rx.Component:
    """Widget for displaying the last screenshot and timestamp."""
    return rx.box(
        rx.text(f"WebcamState.last_screenshot:{WebcamState.last_screenshot}"),
        rx.text(f"WebcamState.loading:{WebcamState.loading}"),
        rx.text(f"WebcamState.ImageURL:{WebcamState.url}"),
        rx.button(
            'screenshot',
            on_click=screenshot(ref=ref)
        ),
        rx.cond(
            WebcamState.last_screenshot,
            rx.fragment(
                rx.image(src=WebcamState.last_screenshot),
                rx.text(WebcamState.last_screenshot_timestamp),
            ),
            rx.center(
                rx.text("Click image to capture.", size="4"),
                ),
        ),
        height="270px",
    )


def webcam_upload_component(ref: str) -> rx.Component:
    """Component for displaying webcam preview and uploading screenshots.
    Args:
        ref: The ref of the webcam component.
    Returns:
        A reflex component.
    """
    return rx.vstack(
        webcam.webcam(
            id=ref,
            # on_click=webcam.upload_screenshot(
            #     ref=ref,
            #     handler=WebcamState.handle_screenshot,  # type: ignore
            # ),
        ),
        last_screenshot_widget(ref=ref),
        width="320px",
        align="center",
    )


@template(route="/webcam", title="Webcam")
def webcamera() -> rx.Component:
    return rx.vstack(
        rx.heading("Webcam", size="8"),
        webcam_upload_component(WEBCAM_REF),
        padding_top="3em",
    )
