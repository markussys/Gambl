import viz
import vizshape
import vizcam
import vizact

# Initialize Vizard
viz.go()

# Set up a first-person camera with mouse look functionality
vizcam.PivotNavigate(center=(0,1.8,0), distance=0)
viz.mouse.setVisible(False)  # Hide the cursor
viz.mouse.setTrap(True)      # Lock the mouse to the center

# Create a flat plane for the ground
ground = vizshape.addPlane(size=(50, 50), axis=vizshape.AXIS_Y)
ground.setPosition(0, -0.01, 0)  # Slightly below the user to avoid clipping
ground.color(0.5, 0.5, 0.5)  # Grey colored ground

# Create a vertical plane (wall) for the video
box = vizshape.addBox()
box.setPosition([0,1.5,5])

# Surround the area with walls
wall1 = vizshape.addPlane(size=(50, 5), axis=vizshape.AXIS_Z)  # Wall in front
wall1.setPosition(0, 2.5, 25)
wall1.color(0.7, 0.7, 0.7)

wall2 = vizshape.addPlane(size=(50, 5), axis=vizshape.AXIS_X)  # Left wall
wall2.setPosition(-25, 2.5, 0)
wall2.color(0.7, 0.7, 0.7)

wall3 = vizshape.addPlane(size=(50, 5), axis=vizshape.AXIS_X)  # Right wall
wall3.setPosition(25, 2.5, 0)
wall3.color(0.7, 0.7, 0.7)

# Enable lighting
viz.MainView.getHeadLight().enable()

# Add a primary light source to brighten the scene
light = viz.addLight()
light.position(0, 10, 0)  # Position the light above the scene
light.intensity(5.0)  # Further increased light intensity
light.spread(180)  # Set a large spread for the light to cover more area

# Increase ambient lighting to brighten the whole scene
viz.setOption('viz.dlambient', [0.5, 0.5, 0.5])  # Adjust ambient light for a brighter environment

# Set camera to initial position
viz.MainView.setPosition([0, 1.8, 0])  # Set camera height to eye level

# Set the movement speed
MOVE_SPEED = 5.0

# Movement direction variables
move_forward = False
move_backward = False
move_left = False
move_right = False

# Load video
video = viz.addVideo('gamblee.mpg')
video.pause()  # Pause initially so it doesn't auto-play

# Toggle video texture on the wall with 'v' key
def toggleVideoTexture():
    if box.getTexture() == video:
        box.texture(None)  # Remove the video texture
    else:
        box.texture(video)  # Apply the video texture to the box
        video.setTime(0)   # Reset video to the start
        video.play()       # Play the video

# Function to check if the video has finished playing
def checkVideoStatus():
    if video.getState() == viz.MEDIA_STOPPED:  # Check if the video has stopped
        box.texture(None)  # Remove the texture from the box

# Set a timer to periodically check the video status
vizact.ontimer(0.1, checkVideoStatus)

vizact.onkeydown('v', toggleVideoTexture)

# Update function for handling movement
def updateMovement():
    global move_forward, move_backward, move_left, move_right

    # Move the camera based on the keys being pressed
    if move_forward:
        viz.MainView.move([0, 0, MOVE_SPEED * viz.elapsed()], viz.REL_LOCAL)

    if move_backward:
        viz.MainView.move([0, 0, -MOVE_SPEED * viz.elapsed()], viz.REL_LOCAL)

    if move_left:
        viz.MainView.move([-MOVE_SPEED * viz.elapsed(), 0, 0], viz.REL_LOCAL)

    if move_right:
        viz.MainView.move([MOVE_SPEED * viz.elapsed(), 0, 0], viz.REL_LOCAL)

# Function to handle key presses
def onKeyDown(key):
    global move_forward, move_backward, move_left, move_right

    if key == 'w':  # Move forward
        move_forward = True
    elif key == 's':  # Move backward
        move_backward = True
    elif key == 'a':  # Strafe left
        move_left = True
    elif key == 'd':  # Strafe right
        move_right = True

# Function to handle key releases
def onKeyUp(key):
    global move_forward, move_backward, move_left, move_right

    if key == 'w':
        move_forward = False
    elif key == 's':
        move_backward = False
    elif key == 'a':
        move_left = False
    elif key == 'd':
        move_right = False

# Register the key press and release events
viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.KEYUP_EVENT, onKeyUp)

# Register the update function to be called every frame
vizact.ontimer(0, updateMovement)
