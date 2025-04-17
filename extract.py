from PIL import Image
import os

def extract_gif_frames(gif_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    im = Image.open(gif_path)
    frame_num = 0

    try:
        while True:
            im.seek(frame_num)
            im.save(f"{output_folder}/frame_{frame_num}.png")
            frame_num += 1
    except EOFError:
        pass  # Reached the end of the GIF

# Save frames into a 'frames' folder inside your project
extract_gif_frames('ship1a.gif', 'frames')
