# Video Streaming Project: GStreamer with Flask API

This project demonstrates a simple video streaming setup using GStreamer for video capture and streaming, and Flask for controlling the stream through a RESTful API.

## Overview

The project consists of two main components:

1.  **`server.py`**: A Flask application that provides an API to start and stop a GStreamer video streaming pipeline.
2.  **`client.py`**: A Python script that interacts with the Flask API to control the video stream and displays the received video using GTK.

## Prerequisites

Before you begin, make sure you have the following installed:

*   **Python 3.6+**:  Ensure you have Python installed on your system.
*   **GStreamer**: The GStreamer multimedia framework, along with its essential plugins.
    *   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt update
        sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly python3-gi python3-gst-1.0
        ```
    *   **macOS:** Use `brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly`
    *   **Windows:** Download and install GStreamer from the official website. Then add the path to the GStreamer binaries to your system's environment variables.
*   **Python Libraries:**
    ```bash
    pip install flask flask-restful requests pycairo
    ```
* **macOS only:** install XQuartz to allow video window to show
    * Follow installation instructions for XQuartz here https://www.xquartz.org/
    * Ensure XQuartz is running in the background before executing `client.py`

## Project Structure

*   `README.md`: This file (you're reading it!).
*   `client.py`: Client-side Python script for viewing the stream and interacting with the server API.
*   `server.py`: Server-side Flask application for controlling the GStreamer stream.

## Getting Started

1.  **Clone the Repository (Optional):** If this project is hosted on a repository platform, you can clone the project using git, otherwise download files:
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```
2.  **Run the Server:** Start the Flask server from the directory containing the project:
    ```bash
    python server.py
    ```
    The server will start and listen on `0.0.0.0:8590`. You'll see the following output or similar: `Running on http://0.0.0.0:8590/`
3. **Run the client:** open a new terminal window
    ```bash
    python client.py
    ```
   *   A prompt will appear in terminal asking to select an option.
   *   Select "1" to start the stream and press enter, response will appear in the terminal.
   *   Select "3" to view the stream and press enter, the stream should appear in a new window.
   *   Select "2" to pause the stream.
   *   You can close the video window and continue to use other options if you would like.

## Usage

After starting both server and client scripts, the client terminal will present a menu:

*   **Option 1: Start Stream** Sends a request to the server to start the GStreamer pipeline.
*   **Option 2: Stop Stream** Sends a request to the server to stop the GStreamer pipeline.
*   **Option 3: View Stream** Opens a GTK window displaying the video stream.

Use the keyboard to select the desired option and press enter.

## GStreamer Pipelines Explained

*   **Server (Stream Source):**
    ```
    gst-launch-1.0 avfvideosrc ! videoconvert ! x264enc tune=zerolatency ! rtph264pay config-interval=1 ! udpsink host=127.0.0.1 port=5000
    ```
    *   `avfvideosrc`: Captures video from an Apple video framework device. This is appropriate for macOS. If on linux, use `v4l2src`.
    *   `videoconvert`: Converts the video format to a format that the encoder can understand.
    *  `x264enc tune=zerolatency`: Encodes the video using the H.264 format and optimizing for low latency.
    *   `rtph264pay config-interval=1`: Packages the H.264 encoded video into RTP packets, sending configuration packets every 1 frame.
    *   `udpsink host=127.0.0.1 port=5000`: Sends the RTP packets over UDP to the specified address and port.
*   **Client (Stream Receiver):**

    ```
    udpsrc port=5000 ! application/x-rtp,media=video,payload=96,clock-rate=90000 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
    ```

    *   `udpsrc port=5000`: Receives the UDP stream from port 5000.
    *  `application/x-rtp,media=video,payload=96,clock-rate=90000`: Specifies the stream is video encoded as H.264.
    *   `rtph264depay`: Depayloads the RTP packets, extracting the raw H.264 data.
    *   `h264parse`: Parses the raw H.264 stream for analysis.
    *   `avdec_h264`: Decodes the H.264 data into raw video frames.
    *   `videoconvert`: Converts the raw video to a format the videosink can understand.
    *   `autovideosink`: Selects the appropriate video sink based on your system to display the video.

## Important Considerations

*   **Network:**  Both client and server are configured to use the same machine for testing.
*   **Error Handling:**  More robust error handling (e.g., checking GStreamer pipeline state) should be implemented for production environments.
*   **Code Enhancements:** This can be improved by using argparse for command line arguments, or a better GUI for selection.
* **Performance**: If you find performance is lacking, you can adjust encoding parameters in the server, such as adjusting resolution, bitrate, or using a different encoder.

## Contributing

If you wish to contribute, feel free to fork the repository, make changes, and submit a pull request.

## License

[Add License details here if needed]

## Contact

If you have any questions or comments, please feel free to contact [your email or contact info].
