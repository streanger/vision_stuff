'''
vision stuff for generall purpose
version: 0.1.2
date: 03.08.2020
'''
import sys
import os
import time
import math
import numpy as np
import cv2


def script_path():
    '''change dir, to current script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def blank_image(height, width, layers=3, value=255):
    '''create blank image, with specified shape, layers and initial value'''
    img = np.ones((height, width, layers), dtype=np.uint8)*value
    return img
    
    
def save_img(path, img, new_dir='NEW_DIR'):
    '''save img to specified directory'''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        
    path = os.path.join(new_dir, path)
    cv2.imwrite(path, img)
    return True
    
    
def shrink_img(img, width=640, height=640, resize=True):
    '''perform image, to fit frame; width and height are shape of full image
    todo:
        -think of detecting main object and move on x(y) axis to cut it
    '''
    
    out = img.copy()
    if (width < 1) or (height < 1):
        return out
        
    frame_img_height, frame_img_width = out.shape[:2]
    img_frame_ratio = frame_img_width/frame_img_height
    proper_frame_ratio = width/height
    
    # print('img_frame_ratio: {}'.format(img_frame_ratio))
    # print('proper_frame_ratio: {}'.format(proper_frame_ratio))
    
    # calc value to cut; should be 3 cases here
    if img_frame_ratio > proper_frame_ratio:
        new_width = round(frame_img_height*proper_frame_ratio)
        cut_width = round((frame_img_width - new_width)/2)
        out = out[:, cut_width: frame_img_width - cut_width]
        
    elif img_frame_ratio < proper_frame_ratio:
        new_height = round(frame_img_width/proper_frame_ratio)
        cut_height = round((frame_img_height - new_height)/2)
        out = out[cut_height: frame_img_height - cut_height, :]
        
    else:
        # leave format as it is; pass for resize if needed
        pass
        
    if resize:
        out = cv2.resize(out, (width, height))      # resize to frame size
        
    return out
    
    
def shrink_img_dir(directory, width=640, height=640, resize=True, echo=True):
    '''shrink all images from specified directory and store them into new directory named (directory + "_converted")'''
    try:
        dir_path = directory
        if directory in ('.', ''):
            dir_path = ''
        files = [(file, os.path.join(dir_path, file)) for file in os.listdir(directory) if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        files = sorted(files)
    except FileNotFoundError:
        print('no such directory: {}'.format(directory))
        return False
        
    if echo:
        now = time.time()
        total = len(files)
        total_str_len = len(str(total))
        
    converted_images = []
    for key, (file, file_path) in enumerate(files):
        if echo:
            print('{}/{}. {}'.format(str(key+1).zfill(total_str_len), total, file))
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            if echo:
                print('    file is corrupted /\\/\\')
            continue
        converted = shrink_img(img, width, height, resize)
        converted_images.append(converted)
        save_img(file, converted, new_dir='{}_converted'.format(dir_path))
        
    if echo:
        print('elapsed time: {:1.4f}[s]'.format(time.time() - now))
    return None
    
    
def shrink_example():
    # DEBUG
    script_path()
    file = 'example.jpg'
    dir_files = [item for item in os.listdir()]
    if not file in dir_files:
        print('no such file: {}'.format(file))
        return False
        
    resize = False
    
    
    # sizes equal or under sizes of original image
    sizes = [
        (460, 460, 'equal_'),       # 1st case equal size
        (400, 100, 'a_'),           # 2nd case a > b
        (100, 400, 'b_'),           # 3rd case b > a
        ]
        
    for (width, height, prefix) in sizes:
        img = cv2.imread(file, 1)
        out = img.copy()
        
        if (width < 1) or (height < 1):
            return out
            
        frame_img_height, frame_img_width = out.shape[:2]
        img_frame_ratio = frame_img_width/frame_img_height
        proper_frame_ratio = width/height
        
        print('width, height: {}, {}'.format(width, height))
        print('img_frame_ratio: {}'.format(img_frame_ratio))
        print('proper_frame_ratio: {}'.format(proper_frame_ratio))
        print('--------------------------\n')
        
        # calc value to cut; should be 3 cases here
        if img_frame_ratio > proper_frame_ratio:
            new_width = round(frame_img_height*proper_frame_ratio)
            cut_width = round((frame_img_width - new_width)/2)
            out = out[:, cut_width: frame_img_width - cut_width]
            
        elif img_frame_ratio < proper_frame_ratio:
            new_height = round(frame_img_width/proper_frame_ratio)
            cut_height = round((frame_img_height - new_height)/2)
            out = out[cut_height: frame_img_height - cut_height, :]
            
        else:
            # leave format as it is; pass for resize if needed
            pass
            
        if resize:
            # resize to frame size
            out = cv2.resize(out, (width, height))
            
        cv2.imwrite(prefix + file, out)
    return True
    
    
def roll_image(img, x_axis, y_axis):
    '''roll specified img in x_axis(px) and y_axis(px)'''
    img = np.roll(img, y_axis, axis=0)   # axis: 0-up-down, 1-right-left
    img = np.roll(img, x_axis, axis=1)   # axis: 0-up-down, 1-right-left
    return img
    
    
def convert_rotation(deg, radius):
    # R layer
    R_a = math.cos((deg/360)*2*math.pi)*radius
    R_b = math.sin((deg/360)*2*math.pi)*radius
    # G layer
    G_a = math.cos(((deg+120)/360)*2*math.pi)*radius
    G_b = math.sin(((deg+120)/360)*2*math.pi)*radius
    # B layer
    B_a = math.cos(((deg+240)/360)*2*math.pi)*radius
    B_b = math.sin(((deg+240)/360)*2*math.pi)*radius
    dictio = {"R_a":R_a,
              "R_b":R_b,
              "G_a":G_a,
              "G_b":G_b,
              "B_a":B_a,
              "B_b":B_b}
    dictio = dict(zip(dictio.keys(), [round(item) for item in list(dictio.values())]))
    return dictio
    
    
def roll_layers(img, deg, radius):
    '''roll specified img layers with degree and radius'''
    
    dictio = convert_rotation(deg, radius)
    img_copy = img.copy()
    
    b_channel, g_channel, r_channel = cv2.split(img_copy)                  # split to R-G-B
    b_channel = roll_image(b_channel, dictio['B_a'], dictio['B_b'])     # move each one
    g_channel = roll_image(g_channel, dictio['G_a'], dictio['G_b'])
    r_channel = roll_image(r_channel, dictio['R_a'], dictio['R_b'])
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel))             # join layers
    return img_BGRA
    
    
def roll_layers_example():
    script_path()
    file = 'example.jpg'
    img = cv2.imread(file, 1)
    out = roll_layers(img, 60, 5)
    cv2.imwrite('out.jpg', out)
    return True
    
    
def gradient_image(height, width, start_color, stop_color, direction):
    '''
    parameters:
        height      - image height
        width       - image width
        start_color - BGR (0-255) tuple (B, G, R)
        stop_color  - BGR (0-255) tuple (B, G, R)
        direction   - up/down/right/left supported
        
    not used:
        make horizontal or vertical line and use np.repeat
        out = np.repeat(np.repeat(frame, size, axis=0), size, axis=1)
    '''
    
    b_start, g_start, r_start = start_color
    b_stop, g_stop, r_stop = stop_color
    layers = 3
    # img = np.zeros((h, w), dtype=np.uint8)        # without_layers
    img = np.zeros((height, width, layers), dtype=np.uint8)
    
    if direction in ('up', 'down'):
        # make vertical line(s)
        for x in range(height):
            r_value = r_start + round((r_stop - r_start) * ((x+1)/height))
            g_value = g_start + round((g_stop - g_start) * ((x+1)/height))
            b_value = b_start + round((b_stop - b_start) * ((x+1)/height))
            # print((b_value, g_value, r_value))
            img[x, :] = (b_value, g_value, r_value)
            
    elif direction in ('left', 'right'):
        # make horizontal line(s)
        for x in range(width):
            r_value = r_start + round((r_stop - r_start) * ((x+1)/width))
            g_value = g_start + round((g_stop - g_start) * ((x+1)/width))
            b_value = b_start + round((b_stop - b_start) * ((x+1)/width))
            # print((b_value, g_value, r_value))
            img[:, x] = (b_value, g_value, r_value)
            
    else:
        return False
        
    if direction == 'up':
        img = img[::-1, :]
        
    if direction == 'left':
        img = img[:, ::-1]
        
    return img
    
    
def gradient_example():
    '''gradient_example'''
    script_path()
    grad = gradient_image(480, 680, (200, 50, 50), (50, 240, 30), 'down')
    cv2.imwrite('gradient.png', grad)
    return True
    
    
def margin(img, space_size, color=(0, 0, 0)):
    '''space_size -integer; 2 is the lowest value for proper read; try to increase value and look for decoding time'''
    current_h, current_w, layers = img.shape
    new_image = np.ones((current_h+space_size*2, current_w+space_size*2, layers), dtype=np.uint8)*color
    new_image[space_size:-space_size, space_size:-space_size] = img
    return new_image
    
    
def margin_example():
    grad = gradient_image(480, 680, (200, 50, 50), (50, 240, 30), 'down')
    out = margin(grad, 50, (10, 150, 100))
    cv2.imwrite('margin2.png', out)
    return True
    
    
def shrink_img_cli():
    '''shrink single image, cli tool'''
    print(42)
    return True
    
    
def shrink_dir_cli():
    '''shrink directory, cli tool'''
    print(42)
    return True
    
    
if __name__ == "__main__":
    script_path()
    
    # shrink_example()
    shrink_img_dir('example_dir', 2000, 1500)
    
    
'''
functions for use:
    -shrink_image
    -shrink_and_store_images_dir
    
cli tools:
    -shrink_images file <width> <height>        # default 640x640
    -shrink_dir directory <width> <height>      # default 640x640
        -make some progress bar
        
02.08.2020, things done:
    -shrink images fixed (3 cases for now)
    -if width or height is < 1 just return the same image
    -roll_layers added
    -gradient_image added
    -margin added
    
12.09.2020, things_done:
    -shrink_and_store_images_dir renamed to shrink_img_dir
    -echo added in shrink_img_dir
    -shrink_image renamed to shrink_img
    -if img is None, then just continue; when echo print info and then continue
    -sort listed files, before iterating
    -when reading img into memory, cv2.IMREAD_UNCHANGED is used; it prevents windows rotation
    -when specified '.' as directory, files from current dir are converted and stored into '_converted' dir
    
'''
