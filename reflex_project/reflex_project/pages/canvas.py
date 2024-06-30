from typing import Any
import reflex as rx
from reflex_project.templates import template

box_width = 960
box_height = 640

class ResizeWatcher(rx.Fragment):
    """
    A component that watches the window size and updates the state.

    The only event trigger in `on_resize` which is called once when the component mounts
    and again each time the viewport dimensions change.
    """

    on_resize: rx.EventHandler[lambda width, height: [width, height]]

    def _exclude_props(self) -> list[str]:
        return ["on_resize"]

    def add_imports(self) -> dict[str, str]:
        return {"react": "useEffect"}

    def add_hooks(self) -> list[str]:
        """Register backend on_resize as a handler for the browser window resize event."""
        on_resize = self.event_triggers["on_resize"]
        if isinstance(on_resize, rx.EventChain):
            on_resize = rx.utils.format.wrap(
                rx.utils.format.format_prop(on_resize).strip("{}"),
                "(",
            )
        return [
            """
            useEffect(() => {
                function handleResize() {
                    %s(window.innerWidth, window.innerHeight);
                }

                // Fire initial resize event when the component mounts.
                handleResize();

                // Add the event listener with cleanup.
                window.addEventListener("resize", handleResize);
                return () => window.removeEventListener("resize", handleResize);
            }, []);""" % (
                on_resize,
            )
        ]


class ReactPictureAnnotation(rx.Component):
    """A component that wraps a react-picture-annotation lib."""
    library = "react-picture-annotation"


class ReactPictureAnnotation(ReactPictureAnnotation):
    """React Picture Annotation component."""
    tag = "ReactPictureAnnotation"
    is_default = False

    image: rx.Var[str]
    width: rx.Var[int]
    height: rx.Var[int]

    annotations: rx.Var[list[dict[str, Any]]]
    selected_id: rx.Var[str]

    on_select: rx.EventHandler[lambda e0: [e0]]
    on_change: rx.EventHandler[lambda e0: [e0]]

    scroll_speed: rx.Var[float]

react_picture_annotation = ReactPictureAnnotation.create

initial_annotations = [
    {
        "id":"s4mp1e",    # required,
        "comment":"innitial sample",  # not required
        "mark":{
            "type":"RECT",                # now only support rect

            # The number of pixels in the upper left corner of the image
            "x":0,
            "y":0,

            # The size of tag
            "width":100,
            "height":100
        }
    },
]

initial_selected_id = "s4mp1e"

class ReactPictureAnnotationState(rx.State):
    image: str = "https://cdn.pixabay.com/photo/2017/08/10/05/18/home-2618511_960_720.jpg"
    width: int = 960
    height: int = 640
    watch_width: int = 960
    watch_height: int = 640
    selected_id: str = initial_selected_id
    annotations: list[dict[str, Any]] = initial_annotations
    scroll_speed: float = 0.0

    def set_selected_id(self, select_id: str) -> None:
        self.selected_id = select_id
        print(self.selected_id)

    def on_change_handler(self, data) -> None:
        self.annotations = data
        print(self.annotations)

    def set_windowsize(self, w: int, h: int) -> None:
        self.watch_width = w
        self.watch_height = h
        # self.width = w
        # self.height = h

    def set_width(self, w) -> None:
        self.width  = int(box_width * w[0] / 100)

    def set_height(self, h) -> None:
        self.height = int(box_height * h[0] / 100)

    def reset_size_(self) -> None:
        self.width  = int(box_width * 0.9)
        self.height = int(box_height * 0.9)

    def reset_size(self) -> None:
        self.width  = int(box_width)
        self.height = int(box_height)

class RPAPageState(rx.State):
    text = "Out Area"

    def change_text_mouse_enter(self):
        self.text = "In Area"

    def change_text_mouse_leave(self):
        self.text = "Out Area"


def annotation_canvas() -> rx.Component:
    return rx.box(
                rx.scroll_area(
                    react_picture_annotation(
                        image=ReactPictureAnnotationState.image,
                        width=ReactPictureAnnotationState.width,
                        height=ReactPictureAnnotationState.height,
                        on_select=ReactPictureAnnotationState.set_selected_id,
                        on_change=ReactPictureAnnotationState.on_change_handler,
                        scroll_speed=ReactPictureAnnotationState.scroll_speed,
                    ),
                    type="auto",
                    scrollbars="both",
                ),
                background="green",
                border_radius="2px",
                width=f"{box_width}px",
                height=f"{box_height}px",
                paddin="10px",
                margin="10px",
                on_mouse_enter=RPAPageState.change_text_mouse_enter,
                on_mouse_leave=RPAPageState.change_text_mouse_leave,
                on_mount=ReactPictureAnnotationState.reset_size()
            ),

@template(route="/canvas", title="Canvas", on_load=ReactPictureAnnotationState.reset_size)
def canvas():
    return rx.vstack(
        # ResizeWatcher.create(on_resize=ReactPictureAnnotationState.set_windowsize),
        rx.heading("Canvas", size="8"),
        rx.divider(),
        rx.text("Annotation Picture!", on_mount=ReactPictureAnnotationState.reset_size_()),
        rx.stack(
            rx.badge(RPAPageState.text, size="3", radius="full"),
            rx.text(f"WIDTH:{ReactPictureAnnotationState.width}   HEIGHT:{ReactPictureAnnotationState.height}"),
        ),
        rx.divider(),
        rx.grid(
            rx.box(
                rx.image(
                    src=ReactPictureAnnotationState.image,
                    width="960px",
                    height="640px",
                ),
                background="green",
                border_radius="2px",
                # width="50%",
                # height="auto",
                paddin="10px",
                margin="10px",
            ),
            rx.divider(orientation="vertical"),
            rx.hstack(
                rx.badge(f'HEIGHT:{ReactPictureAnnotationState.height}'),
                rx.slider(
                    default_value=[100],
                    min=1,
                    max=100,
                    on_value_commit=ReactPictureAnnotationState.set_height,
                ),
            ),
            annotation_canvas(),
            # width="auto",
            # height="auto",
            spacing="5",
            justify="center",
        ),

        rx.divider(),
        rx.text("Annotation PicturSe!"),
    )