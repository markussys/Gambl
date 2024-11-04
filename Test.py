import viz
import vizshape
import vizcam
import vizact
import vizinput
import vizfx

# Initialize Vizard environment
viz.go()
viz.window.setFullscreen(True)
viz.phys.enable()

# Set background color
viz.clearcolor(viz.SKYBLUE)
my_model = viz.add("play2.obj")
my_model.setScale(0.1,0.1,0.1)
my_model.setPosition(10, 0, 0)


my_model.collideBox()  # Creates a box collider around the model's bounding box

# Enable physics for the scene to detect collisions
viz.phys.enable()
my_model.disable(viz.DYNAMICS)

# Enable collision detection for the main viewpoint
viz.MainView.collision(viz.ON)

# Create the floor
test_cube = vizshape.addCube(size=1, color=viz.RED)
test_cube.setPosition(0, 1, 5)
test_cube.collideBox()  # Make it static

floor = vizshape.addPlane(size=(20, 20), axis=vizshape.AXIS_Y, cullFace=False)
floor.setPosition(0, 0, 0)
floor.collidePlane()  # Add collision for the floor

# Setup lighting
head_light = viz.MainView.getHeadLight()
head_light.intensity(0.5)

dir_light = viz.addDirectionalLight()
dir_light.direction(0, -1, 0)
dir_light.position(0, 100, 0)
dir_light.intensity(0.8)

# Setup camera with mouse look
tracker = vizcam.addWalkNavigate(moveScale=2.0)


tracker.setPosition(0,0,0)  # Set tracker to the spawn location
viz.link(tracker, viz.MainView)
viz.mouse.setVisible(False)

# Movement control variables
movement_enabled = True
current_move_speed = 2.0  # Adjust the speed of movement

# Create a cube and a sphere for testing
cube = vizshape.addCube(size=1)
cube.setPosition([2, 1, 5])
sphere = vizshape.addSphere(radius=0.5)
sphere.setPosition([-2, 1, 5])

# Add a 3D text object to display the object name near the top of the screen
text2D = viz.addText('', parent=viz.SCREEN, pos=[0.5, 0.9, 0])  # Centered at the top
text2D.alignment(viz.ALIGN_CENTER)  # Align the text to the center
text2D.fontSize(20)  # Set font size
text2D.color(viz.BLACK)

# Function for detecting what object the user is looking at and pressing E
def checkObject():
    # Get the current position and direction (as Euler angles) of the camera
    position = viz.MainView.getPosition()
    euler = viz.MainView.getEuler()

    # Convert the Euler angles to a forward vector
    direction = viz.Vector(0, 0, 1) * viz.Matrix.euler(euler)

    # Perform ray-casting to check for object intersections
    info = viz.intersect(position, [position[0] + direction[0] * 10, position[1] + direction[1] * 10, position[2] + direction[2] * 10])

    # Check if an object was hit by the ray
    if info.object:
        if info.object == cube:
            text2D.message("Cube")
        elif info.object == sphere:
            text2D.message("Sphere")
        else:
            text2D.message('')
    else:
        text2D.message('')

# When the 'E' key is pressed, check what object is being looked at
def onKeyDown(key):
    if key == 'e':
        checkObject()

# Bind the key event to the function
viz.callback(viz.KEYDOWN_EVENT, onKeyDown)

# Movement function for WASD keys
def Wpressed():
    if movement_enabled:  # Check if movement is allowed
        if viz.key.isDown(87):  # W
            viz.MainView.move([0, 0, current_move_speed * viz.elapsed()], viz.HEAD_ORI)
        if viz.key.isDown(83):  # S
            viz.MainView.move([0, 0, -current_move_speed * viz.elapsed()], viz.HEAD_ORI)
        if viz.key.isDown(68):  # D
            viz.MainView.move([-current_move_speed * viz.elapsed(), 0, 0], viz.HEAD_ORI)
        if viz.key.isDown(65):  # A
            viz.MainView.move([current_move_speed * viz.elapsed(), 0, 0], viz.HEAD_ORI)

# Add a timer to constantly check for WASD movement
movement_handle = vizact.ontimer(0, Wpressed)
