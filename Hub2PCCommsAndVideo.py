"""
windows
=======

python - 3.11.4

Need to download and install VLC - https://www.videolan.org/

python extensions:
pip install bleak
pip install python-vlc
pip install pillow (probably allready installed)
hub to pc comms example - https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/
video player example - https://www.makeuseof.com/python-video-media-player-how-to-build/

-> simpler example here (but not tested): https://github.com/PaulleDemon/tkVideoPlayer/issues/2 
async tkinter helper - https://pypi.org/project/async-tkinter-loop/

"""


print("Program Start")

import tkinter as tk
import vlc
from tkinter import NE, NW, Button, Label, PhotoImage, filedialog
from PIL import ImageTk, Image  
import time
import asyncio
from bleak import BleakScanner, BleakClient
from async_tkinter_loop import async_handler, async_mainloop

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Replace this with the name of your hub if you changed
# it when installing the Pybricks firmware.
HUB_NAME = "Little Dawg"
app = None

device = None

class MediaPlayerApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.current_video = 1
        self.title("BoardFusion")
        self.geometry("800x600")
        self.configure(bg="black")
        self.initialize_player()  
        self.initialize_event_handler()     

    def VideoFinshed(self):
        app.current_video = 0
        print(app.current_video)
        print("video finished")

    def initialize_player(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.time = 3600
        self.current_file = None
        self.playing_video = False
        self.video_paused = False
        self.create_widgets()
    
    def initialize_event_handler(self):
        events = self.media_player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.VideoFinshed.__func__)


    def fll_play_video(self):
        print(self.current_video)
        if self.current_video == 1:
            self.stop()
            self.current_file = r"Resources/placeholder_video.mp4"
            self.play_video()
        elif self.current_video ==2:
            pass
        elif self.current_video == 3:
            pass
        elif self.current_video == 4:
            pass
    
    

    def create_widgets(self):     
        self.media_canvas = tk.Canvas(self, bg="black", width=800, height=30, highlightthickness=0)
        self.time_label=Label(self, text='60:00', fg='white', bg='black', font=("Arial", 60, "bold"))
        self.time_label.place(relx=0.85, rely=0.02)
        self.configure(bg = 'black')
        self.img = ImageTk.PhotoImage(Image.open(r"Resources/title.png"))  # PIL solution
        self.l=Label(image=self.img, borderwidth=0)
        self.l.pack()
        self.start_button = Button(self, text="BEGIN", command=self.start, fg='white', bg='black', font=("Arial", 60, "bold"), borderwidth=0, pady= 100)
        self.start_button.pack()



   
    def start(self):
       # self.current_video = 1
        self.media_canvas.pack(fill=tk.BOTH, expand=True)
        self.update_label()
        self.fll_play_video()
        self.begin = time.time()
        self.start_button.destroy()

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        if sec < 10:
            return("{0}:0{1}".format(int(mins),int(sec)))
        return("{0}:{1}".format(int(mins),int(sec)))
    
    def update_label(self):
        self.time -= 1
        new_text = self.time_convert(self.time)
        self.time_label.configure(text=new_text)
        self.after(1000, self.update_label)
        self.time_label.place(relx=0.85, rely=0.02)
        print(new_text)


    def play_video(self):
        if not self.playing_video:
            media = self.instance.media_new(self.current_file)
            self.media_player.set_media(media)
            self.media_player.set_hwnd(self.media_canvas.winfo_id())
            self.media_player.play()
            self.playing_video = True

    def stop(self):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False

app = MediaPlayerApp()

print("Running....")
def hub_filter(device, ad):
    return device.name and device.name.lower() == HUB_NAME.lower()


def handle_disconnect(_):
    print("Hub was disconnected.")


def handle_rx(_, data: bytearray):
    print("Received:", data)
    if app.current_video == 0:
        if data.find(b'Play_Video_1') >= 0:
            app.current_video = 1
        elif data.find(b'Play_Video_2') >= 0:
            app.current_video = 2
        elif data.find(b'Play_Video_3') >= 0:
            app.current_video = 3
        elif data.find(b'Play_Video_4') >= 0:
            app.current_video = 4
        app.fll_play_video()


async def connect_to_hub():
    device = await BleakScanner.find_device_by_filter(hub_filter)
    print(device)
    client = BleakClient(device, disconnected_callback=handle_disconnect)
    try:
        # Connect and get services.
        await client.connect()
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        nus = client.services.get_service(UART_SERVICE_UUID)
        rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

        # Tell user to start program on the hub.
        print("Start the program on the hub now with the button.")

        

    except Exception as e:
        print(e)

@async_handler
async def main(app):
    await connect_to_hub()



if __name__ == "__main__":
    app.after(2000, async_handler(main(app)))
    async_mainloop(app)



msg = "Roll a dice"
print(msg)





    