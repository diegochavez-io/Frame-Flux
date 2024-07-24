from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip

# Input video and background color
input_video_path = "/Users/agi/Desktop/_VID_H_BG/prep/IMG_4271.mov"
output_video_path = "/Users/agi/Desktop/_VID_H_BG/IMG_4271_v6.mp4"
background_color = (0, 0, 0)  # Black background

def make_horizontal_with_background(input_video_path, output_video_path, background_color):
    # Load the input video
    clip = VideoFileClip(input_video_path)

    # Determine the new dimensions for the output video
    output_width = clip.size[1] * 16 // 9  # Assuming a 16:9 aspect ratio
    output_height = clip.size[1]  # Height remains the same

    # Create a color background clip
    background_clip = ColorClip(size=(output_width, output_height), color=background_color, duration=clip.duration)

    # Position the input video in the center of the background without scaling
    video_position = ('center', 'center')
    final_clip = CompositeVideoClip([background_clip, clip.set_position(video_position).set_start(0).set_duration(clip.duration)], size=(output_width, output_height))

    # Save the final video
    final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', preset='slow', ffmpeg_params=['-profile:v', 'high', '-level', '4.2'])

# Call the function
make_horizontal_with_background(input_video_path, output_video_path, background_color)
