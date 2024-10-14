
import viz
import vizshape

viz.go()

# Add a light source
light = viz.addLight()
light.position(0, 5, 5)  # Set light position
light.enable()

# Create a plane to act as the video screen
screen = vizshape.addPlane(size=(2, 1.5))
screen.setPosition(0, 1.5, 3)  # Set screen position

# Load the video
video = viz.addVideo('DURDEN_EDIT.mp4')  # Replace with your video file
video.setLoop(True)  # Optional: Set video to loop

# Apply the video as a texture to the plane
screen.texture(video)

# Play the video
video.play()

# Enable lighting for the screen
screen.enable(viz.LIGHTING)