import viz
import vizshape
import vizcam
import vizact
import random

# Initialize Vizard environment
viz.go()
viz.window.setFullscreen(True)
viz.phys.enable()

# Set background color
viz.clearcolor(viz.SKYBLUE)

# Add directional light
dir_light = viz.addDirectionalLight()
dir_light.direction(0, -1, 0)
dir_light.position(0, 100, 0)
dir_light.intensity(1)

god = viz.add("god.obj")
god.setPosition(20, 0, 9.5)
god.setScale(0.18, 0.18, 0.18)
god.setEuler(90, 0, 0)

# Load models
my_model = viz.add("play.obj")
my_model.setScale(0.1, 0.07, 0.1)
my_model.setPosition(10, 0, 0)

apiks = viz.add("GAMBLE.obj")
apiks.setPosition(15, 0, -0.7)
apiks.setScale(0.25, 0.25, 0.25)
apiks.setEuler(270,0)

# Create colliders for models
my_model.collideBox()  
my_model.disable(viz.DYNAMICS)
viz.MainView.setEuler([180, 0, 0]) 

viz.MainView.setPosition([35, 0, 13])
viz.MainView.collision(viz.ON)

door = vizshape.addBox()
door.setScale(4.3,4.5, 2)
door.setPosition([2.7,1,8.5])

# Setup camera with mouse look
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition(35, 0, 13)
tracker.setEuler([180, 0, 0])   # Set tracker initial position
# Link tracker to MainView to control the view with navigation
viz.link(tracker, viz.MainView)

# Now set the initial position of the view (camera) after linking to the tracker
 
viz.mouse.setVisible(False)

# Add a 3D text object to display the object name
text2D = viz.addText('', parent=viz.SCREEN, pos=[0.5, 0.9, 0])
text2D.alignment(viz.ALIGN_CENTER)
text2D.fontSize(20)
text2D.color(viz.BLACK)

# Create a box to display the video
box = vizshape.addBox()
box.setScale(0.7, 1, 1)
box.setPosition([15, 1.5, -0.7])
box.setEuler(90,0)

phone = viz.add("phone_booth.obj")
phone.setScale(1, 1, 1)
phone.setPosition(15, 0, -5)

naskis = viz.add("naskis05.obj")
naskis.setScale(0.25,0.25,0.25)
naskis.setPosition(-1,0,4)
naskis.setEuler(90, 0, 0)  # Rotate naskis by 90 degrees

# Load the videos
video_avg220 = viz.addVideo("AVG_220.mpg")
video_avg = viz.addVideo("AVG.mpg")
video_brivenes = viz.addVideo("Brivenes.mpg")

# Define the video options with AVG220 appearing more often
videos = [video_avg220, video_avg220, video_avg220, video_avg, video_avg, video_avg, video_brivenes]

# Initialize coin count
coins = 0
selected_video = None  # To keep track of the video being played
is_video_playing = False  # Track if a video is currently playing
phone_interacted = False  # Flag to track if the phone has been interacted with

# Display coin count on screen
coinText = viz.addText(f'Coins: {coins}', parent=viz.SCREEN, pos=[0.1, 0.9, 0])
coinText.fontSize(20)
coinText.color(viz.YELLOW)

# Function to update coin count display
def updateCoins(amount):
    global coins
    coins = round(coins + amount, 2)
    coinText.message(f'Coins: {coins}')

# Function to handle end of video and award coins
def on_video_end(video):
    global selected_video, is_video_playing
    if video.getState() == viz.MEDIA_STOPPED and video == selected_video:
        if selected_video == video_avg:
            viz.playSound('grrr.mp3')
            updateCoins(1.5)
            print("Finished AVG: +1.5 coins")
        elif selected_video == video_avg220:
            updateCoins(2.5)
            viz.playSound('yipe.mp3')
            print("Finished AVG220: +2.5 coins")
        elif selected_video == video_brivenes:
            updateCoins(250) 
            viz.playSound('yipe.mp3')# Fixed to 250 coins
            print("Finished Brivenes: +250 coins")
        selected_video = None  # Reset selected video
        is_video_playing = False  # Reset flag when video finishes
        
def checkVideoStatus():
    if selected_video:
        on_video_end(selected_video)
vizact.ontimer(0, checkVideoStatus)

# Function to select and play a random video, deducting coins upfront
def play_random_video():
    global coins, selected_video, is_video_playing
    if coins < 2:
        displayTemporaryMessage("Not enough coins to play!", viz.RED)
        return

    # Deduct 2 coins for playing
    updateCoins(-2)
    
    selected_video = random.choice(videos)  # Weighted random choice
    box.texture(selected_video)  # Set the video as the box texture
    selected_video.setTime(0)  # Reset video to start
    selected_video.play()  # Play the video
    is_video_playing = True  # Set flag to indicate video is playing

# Function to check if the object being looked at is a specific target
def checkObject(target):
    position = viz.MainView.getPosition()
    euler = viz.MainView.getEuler()
    direction = viz.Vector(0, 0, 1) * viz.Matrix.euler(euler)
    info = viz.intersect(position, [position[0] + direction[0] * 10, position[1] + direction[1] * 10, position[2] + direction[2] * 10])

    if info.object == target:
        text2D.message("Gamble Object" if target == apiks else "Phone" if target == phone else "god" if target==god else "Naskis" )
        return True
    else:
        text2D.message('')
        return False

promptText = viz.addText('', parent=viz.SCREEN, pos=[0.5, 0.5, 0])  # Define promptText globally
promptText.alignment(viz.ALIGN_CENTER)
promptText.fontSize(24)
promptText.visible(False)

# Function to display a message temporarily on the screen
def displayTemporaryMessage(message, color=viz.WHITE, duration=2.5):
    temp_text = viz.addText(message, parent=viz.SCREEN, pos=[0.5, 0.6, 0])
    temp_text.fontSize(20)
    temp_text.color(color)
    
    # Remove the text after the specified duration
    vizact.ontimer2(duration, 0, temp_text.remove)

# Initialize flags to track which prompt is active
phone_prompt_active = False
naskis_prompt_active = False

# Function to display prompt for phone interaction
def displayPhonePrompt():
    global phone_interacted, phone_prompt_active, naskis_prompt_active
    if not phone_interacted and not promptText.getVisible():
        viz.playSound('Animal.mp3')
        promptText.message("*Mamma: Sveiks dēls, ko vēlējies?:\n1. Vari atsūtīt 50 monētas priekš E-paraksta? \n2. Māt, man ir nepieciešamas 50 monētas, lai nopelnītu 1000000 monētas \n3. Neko")
        promptText.visible(True)
        phone_interacted = True  # Mark that the phone has been interacted with
        phone_prompt_active = True  # Set phone prompt active
        naskis_prompt_active = False  # Ensure naskis prompt is not active

# Function to display prompt for naskis interaction
def displayNaskisPrompt():
    global phone_prompt_active, naskis_prompt_active
    if not promptText.getVisible():
        promptText.message("*Naskis05:Ko gribi nub?:\n1.Kas tu esi?\n2. Es mammai paprasiju naudu priekš E-paraksta!")
        viz.playSound('Animal.mp3')
        promptText.visible(True)
        naskis_prompt_active = True  # Set naskis prompt active
        phone_prompt_active = False  # Ensure phone prompt is not active

# Function to handle answer input based on active prompt
def handleAnswer(choice):
    global phone_prompt_active, naskis_prompt_active
    promptText.visible(False)  # Hide prompt after answering
    
    if phone_prompt_active:
        if choice == 1:
            updateCoins(50)  # Example: Add 50 coins for this choice
            displayTemporaryMessage("Labi dēliņ!", color=viz.GREEN, duration=3)
            viz.playSound('Animal.mp3')
        elif choice == 2:
            updateCoins(50)
            displayTemporaryMessage("NEZVANI MAN VAIRS!", color=viz.RED, duration=3)
            viz.playSound('Animal.mp3')
        elif choice == 3:
            displayTemporaryMessage(".......Ok", color=viz.RED, duration=3)
        phone_prompt_active = False  # Reset phone prompt flag

    elif naskis_prompt_active:
        if choice == 1:
            displayTemporaryMessage("Nav tava darīšana", color=viz.RED, duration=3)
            viz.playSound('Animal.mp3')
        elif choice == 2:
            displayTemporaryMessage("MALACIS MANU PUIS. \n TAGAD TU VARĒSI NOSKAIDROT APARĀTU NOSLĒPUMU", color=viz.GREEN, duration=3)
            viz.playSound('Animal.mp3')
            viz.playSound('explosion.mp3')
            door.remove() 
        naskis_prompt_active = False  # Reset naskis prompt flag
        
def godAudio():
    viz.playSound('jesus.mp3')

# Key press function to handle interactions
def onKeyDown(key):
    global is_video_playing
    
    # If 'E' is pressed while looking at apiks
    if key == 'e' and checkObject(apiks) and not is_video_playing:
        play_random_video()
    
    # If 'E' is pressed while looking at the phone
    elif key == 'e' and checkObject(phone):
        if phone_interacted:
            displayTemporaryMessage("Labāk nezvanīšu viņai vairs", color=viz.RED, duration=2)
        else:
            displayPhonePrompt()

    # If 'E' is pressed while looking at naskis
    elif key == 'e' and checkObject(naskis):
        displayNaskisPrompt()
        
    elif key == 'e' and checkObject(god):
        godAudio()

    # Check if a prompt is visible, then handle answers
    if promptText.getVisible():
        if key == '1':
            handleAnswer(1)
        elif key == '2':
            handleAnswer(2)
        elif key == '3':
            handleAnswer(3)

# Listen for key press events
viz.callback(viz.KEYDOWN_EVENT, onKeyDown)