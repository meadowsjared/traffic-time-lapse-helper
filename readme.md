# Traffic Time Lapse Helper

## Description

A script that makes creating time lapses of traffic in Google Maps easy.

![an example time lapse of Traffic clearing up in Atlanta](example.gif)

## Requirements

The script runs on [**Python 3.9**](http://www.python.org/getit/) and [**Pillow**](https://pillow.readthedocs.io/en/stable/installation.html) (`pip3 install Pillow`) and requires [**NodeJs**](https://nodejs.org/en/download/) and [**Puppeteer**](https://developers.google.com/web/tools/puppeteer).  It also requires OpenCV (`pip3 install opencv-python`) if you want to create videos instead of Gifs. But as long as you have Python3, and nodejs, you can just run `npm install` to install the puppeteer dependency.

## Usage

The URL to take a screenshot of, output directory, and interval between screenshots are all located at the top of **main.py**.

Once these variables are set, run the script and it will begin placing formatted 1920x1080 frames in **/output**. Original frames are kept in **/screenshots**.

lastly after you have the output, run `python3 createGifs.py` to create gifs and throw them in the **/videos** folder.
or alternatively:
make videos instead, by running `python3 createVideos.py` to create mp4 files and throw them in the **/videos** folder.

note: to run it in a way that keeps it running after you logout, use nohup like this:

`nohup python3 -u main.py &`

to stop your program later, you can use:

`ps aux | head -n 1 && ps aux | grep -v grep | grep python3\ main.py`

to get the PID, then use the PID with the `kill <yourPID>` command to kill it using it's PID

## New Features
  * GIF creation added
