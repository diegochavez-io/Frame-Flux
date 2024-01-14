import os

input_file = "E:/_OUTPUT/TPPP-liquid-chrome-BLUR.avi"
output_file = "E:/_OUTPUT/TPPP-liquid-chrome-BLUR-mosh.mp4"
start_frame = "40"
end_frame = "90"

# i-frame removal
os.system(f"python C:/Users/diego/repos/_Video-2-Images_Scripts/datamoshing/mosh.py {input_file} -s {start_frame} -e {end_frame} -o {output_file}")
print("i-frame removal completed")

# p-frame duplication
# os.system(f"python C:/Users/diego/repos/_Video-2-Images_Scripts/datamoshing/mosh.py {input_file} -d 5 -s {start_frame} -o {output_file}")
# print("p-frame duplication completed")

# Vector motion
# os.system(f"python C:/Users/diego/repos/_Video-2-Images_Scripts/datamoshing/vector_motion.py {input_file} -s your_script.js -o {output_file}")
# print("Vector motion completed")

# Style transfer
# os.system(f"python C:/Users/diego/repos/_Video-2-Images_Scripts/datamoshing/style_transfer.py -e clouds.mp4 -t trees.mp4 {output_file}")
# print("Style transfer completed")
