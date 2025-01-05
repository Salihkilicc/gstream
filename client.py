import os
import gi
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gst, Gtk

Gst.init(None)

os.environ["GST_GL_API"] = "opengl"

def view_stream():
    pipeline = Gst.parse_launch(
        "udpsrc port=5000 ! application/x-rtp,media=video,payload=96,clock-rate=90000 ! "
        "rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink"
    )

    window = Gtk.Window()
    window.set_default_size(800, 600)
    window.set_title("Video Stream")
    window.connect("destroy", lambda _: Gtk.main_quit())

    def on_realize(_):
        pipeline.set_state(Gst.State.PLAYING)

    def on_close(_):
        pipeline.set_state(Gst.State.NULL)

    window.connect("realize", on_realize)
    window.connect("delete-event", on_close)
    window.show_all()

    try:
        Gtk.main()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    print("Select option:")
    print("1. Start stream")
    print("2. Stop stream")
    print("3. View stream")

    choice = input("Enter your choice: ")

    if choice == "1":
        import requests
        response = requests.post("http://127.0.0.1:8590/control", json={"action": "start"})
        print(response.json())
    elif choice == "2":
        import requests
        response = requests.post("http://127.0.0.1:8590/control", json={"action": "stop"})
        print(response.json())
    elif choice == "3":
        view_stream()
    else:
        print("Invalid choice.")