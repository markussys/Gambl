import viz
import vizshape
import vizcam
import vizact
import vizinput
import vizfx
import random

# Initialize Vizard environment
viz.go()
viz.window.setFullscreen(True)
viz.phys.enable()

# Set background color
viz.clearcolor(viz.SKYBLUE)

# Load models
my_model = viz.add("play2.obj")
my_model.setScale(0.1, 0.1, 0.1)
my_model.setPosition(10, 0, 0)

apiks = viz.add("GAMBLE.obj")
apiks.setPosition(15, 0, 0)
apiks.setScale(0.25, 0.25, 0.25)

# Create colliders for models
my_model.collideBox()  
viz.phys.enable()
my_model.disable(viz.DYNAMICS)
viz.MainView.collision(viz.ON)

# Setup lighting
head_light = viz.MainView.getHeadLight()
head_light.intensity(0.5)

dir_light = viz.addDirectionalLight()
dir_light.direction(0, -1, 0)
dir_light.position(0, 100, 0)
dir_light.intensity(0.8)

# Setup camera with mouse look
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition(0, 0, 0)
viz.link(tracker, viz.MainView)
viz.mouse.setVisible(False)

# Add a 3D text object to display the object name
text2D = viz.addText('', parent=viz.SCREEN, pos=[0.5, 0.9, 0])
text2D.alignment(viz.ALIGN_CENTER)
text2D.fontSize(20)
text2D.color(viz.BLACK)

# Create a box to display the video
box = vizshape.addBox()
box.setScale(0.8, 1.1, 1.2)
box.setPosition([14.8, 1.5, 0])  # Adjust position as necessary

# Load the videos
video_avg220 = viz.addVideo("AVG_220.mpg")
video_avg = viz.addVideo("AVG.mpg")
video_brivenes = viz.addVideo("Brivenes.mpg")

# Define the video options with AVG220 appearing more often
videos = [video_avg220, video_avg220, video_avg220, video_avg, video_brivenes]

# Initialize coin count
coins = 20
selected_video = None  # To keep track of the video being played
is_video_playing = False  # Track if a video is currently playing

# Display coin count on screen
coinText = viz.addText(f'Coins: {coins}', parent=viz.SCREEN, pos=[0.1, 0.9, 0])
coinText.fontSize(20)
coinText.color(viz.YELLOW)

# Function to update coin count display
def updateCoins(amount):
    global coins
    coins += amount
    coinText.message(f'Coins: {coins}')

# Function to handle end of video and award coins
def on_video_end(video):
    global selected_video, is_video_playing
    if video.getState() == viz.MEDIA_STOPPED and video == selected_video:
        if selected_video == video_avg:
            updateCoins(1.5)
            print("Finished AVG: +1.5 coins")
        elif selected_video == video_avg220:
            updateCoins(2.5)
            print("Finished AVG220: +2.5 coins")
        elif selected_video == video_brivenes:
            updateCoins(207.20)
            print("Finished Brivenes: +250 coins")
        selected_video = None  # Reset selected video
        is_video_playing = False  # Reset flag when video finishes

# Function to select and play a random video, deducting coins upfront
def play_random_video():
    global coins, selected_video, is_video_playing
    if coins < 2:
        print("Not enough coins to play")
        return

    # Deduct 2 coins for playing
    updateCoins(-2)
    
    selected_video = random.choice(videos)  # Weighted random choice
    box.texture(selected_video)  # Set the video as the box texture
    selected_video.setTime(0)  # Reset video to start
    selected_video.play()  # Play the video
    is_video_playing = True  # Set flag to indicate video is playing

# Function to check if the object being looked at is 'apiks'
def checkObject():
    position = viz.MainView.getPosition()
    euler = viz.MainView.getEuler()
    direction = viz.Vector(0, 0, 1) * viz.Matrix.euler(euler)
    info = viz.intersect(position, [position[0] + direction[0] * 10, position[1] + direction[1] * 10, position[2] + direction[2] * 10])

    if info.object == apiks:
        text2D.message("Gamble Object")  # Display apiks name
        return True
    else:
        text2D.message('')
        return False

# Key press function to play a random video when looking at 'apiks'
def onKeyDown(key):
    if key == 'e' and checkObject() and not is_video_playing:  # Play video only if looking at apiks, pressing 'E', and no video is playing
        play_random_video()

# Bind key event
viz.callback(viz.KEYDOWN_EVENT, onKeyDown)

# Monitor video playback state to award coins when video ends
def checkVideoStatus():
    if selected_video:
        on_video_end(selected_video)

# WASD movement function
def Wpressed():
    if viz.key.isDown(87):  # W
        viz.MainView.move([0, 0, 2.0 * viz.elapsed()], viz.HEAD_ORI)
    if viz.key.isDown(83):  # S
        viz.MainView.move([0, 0, -2.0 * viz.elapsed()], viz.HEAD_ORI)
    if viz.key.isDown(68):  # D
        viz.MainView.move([-2.0 * viz.elapsed(), 0, 0], viz.HEAD_ORI)
    if viz.key.isDown(65):  # A
        viz.MainView.move([2.0 * viz.elapsed(), 0, 0], viz.HEAD_ORI)

# Timer to check WASD movement and video status
vizact.ontimer(0, Wpressed)
vizact.ontimer(0, checkVideoStatus)
