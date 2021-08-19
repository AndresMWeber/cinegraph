from cinegraph.images import write_img_to_dir
from cinegraph.utils import Config, SIZE_UNIT, convert_unit, get_filename
import fire
from os.path import getsize
import tkinter as tk
from tkinter import filedialog
from cinegraph.process import process_video


def get_files():
    """Uses Tkinter to interactively generate file list for processing."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilenames()

def create_filename(video_file_path):
    original_filename = get_filename(video_file_path)
    return f"{original_filename}_c{Config.num_colors}_b{Config.blur_x}_r{'x'.join(map(str,Config.resolution))}_f{int(Config.art_frame)}_fm{Config.art_frame_margin}.jpg"


def generate(*files, colors=600, blur=5, resolution=(1920, 1080), no_frame=False, margin=50, write_frames=False):
    Config.blur_x = blur
    Config.blur_y = blur
    Config.resolution = resolution
    Config.num_colors = colors
    Config.art_frame = not no_frame
    Config.art_frame_margin = margin
    Config.write_frames = write_frames

    if not files:
        try:
            files = get_files()
        except:
            files = []
    
    if files:
        for file_name in files:
            print(f"Processing file ({round(convert_unit(getsize(file_name), SIZE_UNIT.MB),2)}) {file_name} ")
            cinegraph = process_video(file_name)
            output = write_img_to_dir(cinegraph, Config.output_dir, create_filename(file_name))
            print(f"Created cinegraph: {output}")
    else:
        return "No files specified...exiting..."


def execute():
    fire.Fire(generate)
