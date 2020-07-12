from tkinter import *  #framework for window
from tkinter import filedialog  #library for dialogue box browising files
import tkinter.messagebox  #module for messagebox
from pygame import mixer  #library for music
import os    # package to snip the path and get the file name
from mutagen.mp3 import MP3
import time
import threading


root = Tk()   #window opening in the variable called root
mixer.init()   #initializing mixer

#creating menu bar
menubar = Menu(root)
root.config(menu=menubar)

root.geometry('600x300')   # window sizing
root.title("Sangeet")      # window title
root.iconbitmap(r'favicon.ico')  #icon for the window


#adding status bar
status_bar = Label(root, text='Sangeet welcomes you', relief = SUNKEN, anchor = W)
status_bar.pack(side=BOTTOM, fill = X)

#adding left frame
left_frame = Frame(root)
left_frame.pack(side = LEFT)

#adding right frame
right_frame = Frame(root)
right_frame.pack()


#adding three different frames in the right frame
tr_frame = Frame(right_frame)
tr_frame.pack()

mr_frame = Frame(right_frame)
mr_frame.pack()

br_frame = Frame(right_frame)
br_frame.pack()

l_box = Listbox(left_frame)
l_box.pack()

play_list = []


#function to song in playlist
def add_to_playlist(f_name):
    i = 0
    f_name= os.path.basename(f_name)
    l_box.insert(i,f_name)
    play_list.insert(i, path)
    l_box.pack()
    i+=1

#function to delete song
def del_song():
    song_sel = l_box.curselection()
    song_sel = int(song_sel[0])
    l_box.delete(song_sel)
    play_list.pop(song_sel)

#function to show the dialogue box
def about_info():  
    tkinter.messagebox.showinfo('SANGEET', 'Listen and Enjoy Music')

 #function to open path
def browse_file(): 
    global path
    path = filedialog.askopenfilename()
    add_to_playlist(path)


#addition of button add and delete
add_btn = Button(left_frame, text = "ADD", command = browse_file)
add_btn.pack(side = LEFT)

del_btn = Button(left_frame, text = "DELETE" ,command = del_song)
del_btn.pack()

#adding menu and submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File',menu=subMenu) #submenu named file in the menu
subMenu.add_command(label='Browse', command = browse_file)   #cascaded command naming new project in sub menu
subMenu.add_command(label='Exit', command = root.destroy)
subMenu.add_command(label='About', command = about_info) 


#lable for totak time
length_lable = Label(br_frame, text = 'Length : --:--')
length_lable.pack()

#lable for current play time
play_lable = Label(br_frame,text = 'Playing : --:--' )
play_lable.pack()

#function to calculate playing time
def start_count(t):
    global paused
    current_t = 0
    while current_t <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            m,s = divmod(current_t,60)
            m=round(m)
            s=round(s)
            time_format = '{:02d}:{:02d}'.format(m,s)     #to show time of music
            play_lable['text'] = 'Playing : '+ time_format
            time.sleep(1)
            current_t+=1


#function to display total time and song currently played
def show_info(play_song):
    file_data = os.path.splitext(play_song)
    file_name = os.path.basename(play_song)
    file_lable['text'] = "Playing  " + file_name

    if file_data[1] == '.mp3':
        music = MP3(play_song)
        t_length = music.info.length
        #print(t_length)  
    else:  
        song = mixer.Sound(play_song)
        t_length = song.get_length()
        #print(t_length)
        #  
    m,s = divmod(t_length,60)
    m=round(m)
    s=round(s)
    time_format = '{:02d}:{:02d}'.format(m,s)
    #print(t_length)     #to show time of music
    length_lable['text'] = 'Length : '+ time_format
    t1 = threading.Thread(target = start_count, args=(t_length,))
    t1.start()
    #start_count(t_length)
    
#Label for the information widget
file_lable = Label(tr_frame, text = 'Enjoy')   # labeling widget 
file_lable.pack()


#function for the play button
def play_music():  
    global paused

    if paused:
        mixer.music.unpause()   #unpaused
        status_bar['text'] = 'Music Resumed'  # check if the pause is initialize
        paused = FALSE
    else: 
        try:  # perform if pause isn't initiaized
            stop_music()
            time.sleep(1)
            song_sel = l_box.curselection()
            song_sel = int(song_sel[0])
            play_it = play_list[song_sel]
            mixer.music.load(play_it)  #load music
            mixer.music.play()   #play the music
            status_bar['text'] = 'Playing music '+''+ os.path.basename(play_it)
            show_info(play_it)

        except:
           tkinter.messagebox.showerror('File not found', 'Sangeet couldn''t find the file')
           #print("executed")

#addition of play button
play_image = PhotoImage(file ='icons/play.png')    #image for the pause button #change it
play_btn = Button(mr_frame, image = play_image ,command = play_music)  
play_btn.grid(row=1, column = 0)




paused = FALSE
#pause music function
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    status_bar['text'] = 'Music paused'

#adding pause button
pause_image = PhotoImage(file = 'icons/pause.png')  #image for the play buttom:change it
pause_btn = Button(mr_frame, image = pause_image, command = pause_music)
pause_btn.grid(row=1, column = 1)

#stop music function
def stop_music():
    mixer.music.stop()  # stop the music
    status_bar['text'] = 'Music stopped'

#stop music button
stop_image = PhotoImage(file = 'icons/stop.png')  #image for the play buttom:change it
stop_btn = Button(mr_frame, image = stop_image, command = stop_music)
stop_btn.grid(row=1, column = 2)


# volume controller
def volume_control(val):  
    vol = int(val)/100
    mixer.music.set_volume(vol)  
 
#voulume controll label
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=volume_control)
scale.set(50)
mixer.music.set_volume(.5)
scale.pack()

root.mainloop()