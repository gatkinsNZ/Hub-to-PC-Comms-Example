"""
windows
=======

python - 3.11.4

Need to download and install VLC - https://www.videolan.org/

python extensions:
pip install bleak 0.21.1
pip install python-vlc 3.0.20123
pip install async-tkinter-loop 0.9.2
pip install pillow (probably allready installed) 10.1.0???
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
import msvcrt

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Replace this with the name of your hub if you changed
# it when installing the Pybricks firmware.
HUB_NAME = "Little Dawg"
rx_char = None
client = None
mediaCanvasButton = None

class MediaPlayerApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.title("BoardFusion")
        self.geometry("1920x1080")#800x600
        self.configure(bg="black")
        self.initialize_player()  
        self.initialize_event_handler()  

    def VideoFinished(event):
        print("Video " + str(app.current_video) + " finished")
        hubmessage = "video" + str(app.current_video) + "_finished"
        send(str.encode(hubmessage))
        app.current_video = 0
    

    def initialize_player(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media_player.video_set_mouse_input(False)
        self.media_player.video_set_key_input(False)
        self.time = 3600
        self.current_file = None
        self.playing_video = False
        self.video_paused = False
        self.create_widgets()
    
    def initialize_event_handler(self):
        events = self.media_player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.VideoFinished.__func__)

    def fll_play_video(self):
        #print(self.current_video)
        if self.current_video == 1:
            self.stop()
            self.current_file = r"Resources/titlescreen_vid.mp4"
            self.play_video()
        elif self.current_video == 2:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_IntroShort.mp4"
            self.play_video()
            #self.after(3000, self.start_timer)
        elif self.current_video == 3:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_SpinTheWheel.mp4"
            self.play_video()
        elif self.current_video == 4:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_Spun1.mp4"
            self.play_video()
        elif self.current_video == 5:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_Spun2.mp4"
            self.play_video()
        elif self.current_video == 6:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_Spun3.mp4"
            self.play_video()
        elif self.current_video == 7:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_Spun4.mp4"
            self.play_video()
        elif self.current_video == 8:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_Spun5.mp4"
            self.play_video()
        elif self.current_video == 9:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_CardBlue.mp4"
            self.play_video()
        elif self.current_video == 10:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_CardYellow.mp4"
            self.play_video()
        elif self.current_video == 11:
            self.stop()
            self.current_file = r"Resources/New Videos/vid_CardRed.mp4"
            self.play_video() 

    def create_widgets(self):     
        self.media_canvas = tk.Canvas(self, bg="black", width=800, height=30, highlightthickness=0)
        #self.time_label=Label(self, text='60:00', fg='white', bg='black', font=("Arial", 60, "bold"))
        self.configure(bg = 'black')
        self.media_canvas.pack(fill=tk.BOTH, expand=True)
        self.img_two = ImageTk.PhotoImage(Image.open(r"Resources/start_menu.jpg").resize((1182, 664), Image.Resampling.LANCZOS))
        self.start_button = Button(self, command=self.start, borderwidth=0, image= self.img_two)
        self.start_button.pack()
        self.main_screen = False
        self.spin_label = Label(self, borderwidth=0, text='Not spun yet', font=("Arial", 60, "bold"), fg='white', bg='black')

    def start_game(event):
        app.media_canvas.unbind("<Button-1>", mediaCanvasButton)
        app.current_video = 2
        app.fll_play_video()
        

   
    def start(self):
        print('start')
        self.start_button.destroy()
        if self.main_screen == False:        
            mediaCanvasButton = self.media_canvas.bind("<Button-1>", self.start_game.__func__)
            self.current_video = 1
            self.main_screen = True
            #self.frame.pack()
            self.fll_play_video()

    def start_timer(self):
        print("Timer start")
        self.time_label=Label(text='60:00', fg='white', bg='black', font=("Arial", 60, "bold"))
        self.time_label.place(relx=0.82, rely=0.02)
        app.begin = time.time()
        app.update_timer()
    
    def update_timer(self):
        self.time -= 1
        new_text = self.time_convert(self.time)
        self.time_label.configure(text=new_text)
        self.after(1000, self.update_timer)
        self.time_label.place(relx=0.82, rely=0.02)

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        if sec < 10:
            return("{0}:0{1}".format(int(mins),int(sec)))
        return("{0}:{1}".format(int(mins),int(sec)))  
        
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
    #if app.current_video == 0:
    if data.find(b'Play_Video_2') >= 0:
        app.current_video = 2
    elif data.find(b'Play_Video_3') >= 0:
        app.current_video = 3
    elif data.find(b'Play_Video_4') >= 0:
        app.current_video = 4
    elif data.find(b'Play_Video_BlueCard') >= 0:
        app.current_video = 9
    elif data.find(b'Play_Video_YellowCar') >= 0:
        app.current_video = 10
    elif data.find(b'Play_Video_RedCard') >= 0:
        app.current_video = 11
    elif data.find(b'Start_Timer') >= 0:
        app.start_timer()
    else:
        spinNumber = data.decode()
        spinNumber = spinNumber[12]
        app.current_video = (3+int(spinNumber))

        media_canvas = tk.Canvas(bg="black", width=800, height=30, highlightthickness=0)
        app.spin_label=Label(text="You spun a " + str(spinNumber) + "!", fg='white', bg='black', font=("Arial", 60, "bold"))
        app.spin_label.after(1000, showSpinNumber)
        
    app.fll_play_video()
    #print(app.current_video)

def showSpinNumber():
    app.spin_label.place(relx=0.3, rely=0.81)
    app.spin_label.after(6000, app.spin_label.destroy)

def send(data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("Calling send")
    data = loop.run_until_complete(sendAsync(data))
    loop.close


async def sendAsync(data):
    print("Sending to hub: " + str(data))
    await client.write_gatt_char(rx_char, data)


@async_handler
async def main(app):
    
    # Find the device and initialize client.
    global client
    global rx_char
    global mediaCanvasButton

    device = await BleakScanner.find_device_by_filter(hub_filter)
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
        # Handle exceptions.
        print(e)


if __name__ == "__main__":
    app.after(2000, async_handler(main(app)))
    async_mainloop(app)



msg = "Demo finished"
print(msg)





