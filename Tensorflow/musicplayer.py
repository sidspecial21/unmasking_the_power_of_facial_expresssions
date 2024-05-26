from tkinter import *
from PIL import Image, ImageTk  # Importing necessary libraries for image handling
import os
import sys
import vlc
from pathlib import Path
import random

# Initiating VLC
Instance = vlc.Instance()
# Initiating VLC Player
player = Instance.media_player_new()

# Defining MusicPlayer Class
class MusicPlayer(object):
    # Defining Constructor
    def __init__(self, root, emotionStr):
        self.root = root
        # Title of the window
        self.root.title("Music Player")
        
        # Make the window fullscreen
        self.root.attributes('-fullscreen', True)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Create Canvas
        self.canvas = Canvas(self.root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Load and place background image on the canvas
        self.bg_img = ImageTk.PhotoImage(Image.open("assets/frame0/background.jpg").resize((self.screen_width, self.screen_height), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        
     
        # Creating Track Frame for Song label & status label
        trackframe = Frame(self.root, bg='black')
        self.canvas.create_window(20, 20, anchor="nw", window=trackframe, width=800, height=150)

        # Inserting Song Track Label
        songtrack = Label(trackframe, textvariable=self.track, width=50, font=("Helvetica", 24, "bold"), fg="white", bg='black')
        songtrack.pack(pady=10)

        # Inserting Status Label
        trackstatus = Label(trackframe, textvariable=self.status, font=("Helvetica", 18, "bold"), fg="white", bg='black')
        trackstatus.pack(pady=5)
        
        # Creating Button Frame
        buttonframe = LabelFrame(self.root, text="Control Panel", font=("times new roman", 15, "bold"), fg="white", bd=5, relief=GROOVE)
        self.canvas.create_window(0, self.screen_height-100, anchor="nw", window=buttonframe, width=self.screen_width, height=100)
        
        # Load images for control buttons
        self.play_img = ImageTk.PhotoImage(Image.open("assets/frame0/play.png").resize((50, 50), Image.ANTIALIAS))
        self.pause_img = ImageTk.PhotoImage(Image.open("assets/frame0/pause.png").resize((50, 50), Image.ANTIALIAS))
        self.back_img = ImageTk.PhotoImage(Image.open("assets/frame0/back-button.png").resize((50, 50), Image.ANTIALIAS))
        self.next_img = ImageTk.PhotoImage(Image.open("assets/frame0/send.png").resize((50, 50), Image.ANTIALIAS))
        self.vol_up_img = ImageTk.PhotoImage(Image.open("assets/frame0/volume-up.png").resize((50, 50), Image.ANTIALIAS))
        self.vol_down_img = ImageTk.PhotoImage(Image.open("assets/frame0/volume-down.png").resize((50, 50), Image.ANTIALIAS))
        self.shuffle_img = ImageTk.PhotoImage(Image.open("assets/frame0/suffle.png").resize((50, 50), Image.ANTIALIAS))
        self.stop_img = ImageTk.PhotoImage(Image.open("assets/frame0/exit.png").resize((50, 50), Image.ANTIALIAS))

        # Inserting Back Button with image
        backbtn = Button(buttonframe, image=self.back_img, command=self.previoussong, width=50, height=50)
        backbtn.grid(row=0, column=0, padx=10, pady=5)
        
        # Inserting Next Button with image
        nextbtn = Button(buttonframe, image=self.next_img, command=self.nextsong, width=50, height=50)
        nextbtn.grid(row=0, column=1, padx=10, pady=5)

        # Inserting Volume Up Button with image
        volupbtn = Button(buttonframe, image=self.vol_up_img, command=self.volume_up, width=50, height=50)
        volupbtn.grid(row=0, column=2, padx=10, pady=5)
        
        # Inserting Volume Down Button with image
        voldownbtn = Button(buttonframe, image=self.vol_down_img, command=self.volume_down, width=50, height=50)
        voldownbtn.grid(row=0, column=3, padx=10, pady=5)

        # Inserting Play Button with image
        playbtn = Button(buttonframe, image=self.play_img, command=self.playsong, width=50, height=50)
        playbtn.grid(row=0, column=4, padx=10, pady=5)
        
        # Inserting Pause Button with image
        pausebtn = Button(buttonframe, image=self.pause_img, command=self.pausesong, width=50, height=50)
        pausebtn.grid(row=0, column=5, padx=10, pady=5)
        
        # Inserting Shuffle Button with image
        shufflebtn = Button(buttonframe, image=self.shuffle_img, command=self.shufflesong, width=50, height=50)
        shufflebtn.grid(row=0, column=6, padx=10, pady=5)
        
        # Inserting Stop Button with image
        stopbtn = Button(buttonframe, image=self.stop_img, command=self.stopsong, width=50, height=50)
        stopbtn.grid(row=0, column=7, padx=10, pady=5)

        # Creating Playlist Frame
        songsframe = LabelFrame(self.root, text="Song Playlist", font=("times new roman", 15, "bold"), fg="white",bg="black", bd=5, relief=GROOVE)
        self.canvas.create_window(850, 20, anchor="nw", window=songsframe, width=400, height=220)
        
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE, font=("times new roman", 12, "bold"), bg="black", fg="white", bd=5, relief=GROOVE)
        
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        
        # Changing Directory for fetching Songs
        os.chdir(str(Path(__file__).parent.absolute()) + "/songs/" + emotionStr + "/")
        
        songtracks = os.listdir()
        self.songtracks = songtracks
        # Inserting Songs into Playlist
        for track in songtracks:
            self.playlist.insert(END, track)
        if player.is_playing() == 0:
            ranSong = random.choice(self.songtracks)
            self.pos = self.songtracks.index(ranSong)
            self.track.set(ranSong)
            self.status.set("-Playing " + emotionStr)
            Media = Instance.media_new(ranSong)
            player.set_media(Media)
            player.play()
    # Defining Play Song Function
    def playsong(self):
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        Media = Instance.media_new(self.playlist.get(ACTIVE))
        player.set_media(Media)
        player.play()

    def stopsong(self):
        # Displaying Status
        self.status.set("-Stopped")
        # Stopped Song
        player.stop()
        self.root.destroy()
        os.chdir(str(Path(__file__).parent.absolute()))
        os.system("python emotions.py")

    def pausesong(self):
        # Displaying Status
        self.status.set("-Paused")
        # Paused Song
        player.pause()

    def nextsong(self):
        self.pos = (self.pos + 1) % len(self.songtracks)
        nsong = self.songtracks[self.pos]
        player.stop()
        self.track.set(nsong)
        # Loading Selected Song
        Media = Instance.media_new(nsong)
        player.set_media(Media)
        player.play()

    def previoussong(self):
        self.pos = (self.pos - 1) % len(self.songtracks)
        psong = self.songtracks[self.pos]
        player.stop()
        self.track.set(psong)
        # Loading Selected Song
        Media = Instance.media_new(psong)
        player.set_media(Media)
        player.play()

    def shufflesong(self):
        self.status.set("-Shuffle Play")
        song2 = random.choice(self.songtracks)
        self.pos = self.songtracks.index(song2)
        self.track.set(song2)
        player.stop()
        # Loading Selected Song
        Media = Instance.media_new(song2)
        player.set_media(Media)
        player.play()

    def volume_up(self):
        # Increasing the volume by 10 units
        current_volume = player.audio_get_volume()
        player.audio_set_volume(min(current_volume + 10, 100))  # Maximum volume is 100

    def volume_down(self):
        # Decreasing the volume by 10 units
        current_volume = player.audio_get_volume()
        player.audio_set_volume(max(current_volume - 10, 0))  # Minimum volume is 0


