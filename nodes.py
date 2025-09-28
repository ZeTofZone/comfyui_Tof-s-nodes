#import glob
from __future__ import annotations
import random
import os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops, ImageFont
import numpy as np
import torch
import hashlib
import re
import torchvision.transforms.functional as F
from PIL.PngImagePlugin import PngInfo
import json
import kornia.filters
from torch import Tensor
import pathlib

import folder_paths





from typing import NamedTuple

from comfy.samplers import KSAMPLER




class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __eq__(self, _) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


#________________________________________________________________
#________________________________________________________________
# Prompt with variables v2
#________________________________________________________________
#________________________________________________________________

def read_wildcards(text: str, seed: int):
    inner = text.count('{')
    outer = text.count('}')
    if inner != outer or inner == 0 or outer == 0: return text
    for a in text.split('{'):
        ws = a.split('}')[0]
        ws2 = ws.split('|')
        random.seed(None)
        index = random.randint(0, len(ws2) - 1)
        text = text.replace('{'+ws+'}', ws2[index])
    return text

class variables_prompt_v2:
    @classmethod
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "variables": ("STRING", {"multiline": False}, {"forceInput": True}),
                "text": ("STRING", {"multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0x7FFFFFFFFFFFFFFF}),
            },
            "optional": {
            }
        }


    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("out", "variables",)
    FUNCTION = "get_prompt"
    CATEGORY = "Tof"



    def get_prompt(self, variables: str, seed: int, text: str) -> tuple[str]:
        """
        Main entrypoint for this node.
        Using the sampling context, generate a new prompt.
        """
        outtext = read_wildcards(text, seed)
        variables = read_wildcards(variables, seed)
        variables = variables.replace(";", "\n")
        varall = variables.split("\n")
        count = 0
        for v in varall:
            vv = v.find(":")
            if vv > 0 and vv < 5:
                v = v[(vv+2):]
                varall[count] = v
            count = count + 1
                
        bc = len(varall)
        for v in reversed(varall):
            nb = "#"+str(bc)
            #print("TOF : "+nb+" => " + v)
            outtext = outtext.replace(nb, v)
            bc = bc - 1
            
        #print("TOF : "+outtext)

        return (outtext, variables,)






#________________________________________________________________
#________________________________________________________________
# LOAD RANDOM IMAGE NODE
#________________________________________________________________
#________________________________________________________________

class load_image_random:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    "images_path": ("STRING", {"default": './ComfyUI/input/*.png', "multiline": False}),
                    "RGBA": (["false","true"],),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                }
            }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filename_text")
    FUNCTION = "load_image"

    CATEGORY = "Tof"

    def load_image(self, images_path, seed, RGBA='false'):

        RGBA = (RGBA == 'true')
        
        search = os.path.basename(images_path)
        path = images_path.replace(search, "")
        extension = os.path.splitext(os.path.basename(images_path))[1]
        print(path)
        # print(search)
        # print(extension)
        

        arr = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            # print(r)
            print(d)
            # print(f)
            # if d!= path:
                # continue
            for file in f:
                if file.endswith(extension):
                    #print(os.path.join(r, file))
                    arr.append(os.path.join(r, file))
        
        
        random.seed(seed)
        index = random.randint(0, len(arr) - 1)
        # print("index:", index)
        image_path = arr[index]
        
        try:
            i = Image.open(image_path)
            i = ImageOps.exif_transpose(i)
        except OSError:
            cstr(f"The image `{image_path.strip()}` specified doesn't exist!").error.print()
            i = Image.new(mode='RGB', size=(512, 512), color=(0, 0, 0))
        if not i:
            return

        image = i
        if not RGBA:
            image = image.convert('RGB')
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        filename = os.path.basename(image_path)

        return (image, mask, filename)

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()



#________________________________________________________________
#________________________________________________________________

# Save json every N generation
#________________________________________________________________
#________________________________________________________________

def save_json(path, filename: str, prompt=None, extra_pnginfo: dict = None):
    path = str(path) + "workflows\\"
    pathlib.Path(path).mkdir(parents=False, exist_ok=True) 
    with open(path + filename.replace("jpg", "json"), 'w') as file:
        if extra_pnginfo is not None:
            for k, v in extra_pnginfo.items():
                if k == "workflow":
                    k = k.replace("workflow", "")
                file.write(k + json.dumps(v))
                # print(k + json.dumps(v))

        # file.write(text)
def save_json2(path, prompt=None, extra_pnginfo: dict = None):
    path = str(path)
    with open('last_workflow.json', 'w') as file:
        if extra_pnginfo is not None:
            for k, v in extra_pnginfo.items():
                file.write(k + json.dumps(v))
                # print(k + json.dumps(v))

        # file.write(text)

def load_json():
    f = open("last_workflow.json", "r")
    print(f.read())
    return f.read()



class save_json_every_n:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    "path": ("STRING", {"forceInput": True}),
                    "every": ("INT", {"default": 1, "min": 1, "max": 0xffffffffffffffff}),
                },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
            }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "saveN_json"

    CATEGORY = "Tof"

    def saveN_json(self, path, every, prompt=None, extra_pnginfo=None):
        path = path[0]
        filename = os.path.basename(path)
        path = path.replace(filename, "")
        # print(path)
        i = int(re.search(r'\d+', filename).group())
        # print(i)
        if every * round(i / every) == i:
            print("\033[94mTof Nodes - Save json every N generations :\033[0m Workflow saved in json format")
            save_json(path, filename, prompt, extra_pnginfo)
        else:
            print("\033[94mTof Nodes - Save json every N generations :\033[0m Nothing to do")
        # read = load_json()
        # if extra_pnginfo == read:
            # print("Same worflow, returning")
            # return()
        # save_json("", prompt, extra_pnginfo)
        return ()


#________________________________________________________________
#________________________________________________________________
# Save text every N generation
#________________________________________________________________
#________________________________________________________________

def save_text(path, filename: str, text: str):
    path = str(path) + "prompts\\"
    pathlib.Path(path).mkdir(parents=False, exist_ok=True) 
    with open(path + filename.replace("jpg", "txt"), 'w') as file:
        if text is not None:
            file.write(text)
            print(text)


class save_text_every_n:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    "path": ("STRING", {"forceInput": True}),
                    "text": ("STRING", {"forceInput": True}),
                    "every": ("INT", {"default": 1, "min": 1, "max": 0xffffffffffffffff}),
                },
            }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "saveN_text"

    CATEGORY = "Tof"

    def saveN_text(self, path, every, text):
        path = path[0]
        filename = os.path.basename(path)
        path = path.replace(filename, "")
        # print(path)
        i = int(re.search(r'\d+', filename).group())
        # print(i)
        if every * round(i / every) == i:
            print("\033[94mTof Nodes - Save text every N generations :\033[0m text saved in txt format")
            save_text(path, filename, text)
        else:
            print("\033[94mTof Nodes - Save text every N generations :\033[0m Nothing to do")
        # read = load_json()
        # if extra_pnginfo == read:
            # print("Same worflow, returning")
            # return()
        # save_json("", prompt, extra_pnginfo)
        return ()


#________________________________________________________________
#________________________________________________________________
# Save png every N generation
#________________________________________________________________
#________________________________________________________________

def save_image(img: torch.Tensor, path, prompt=None, extra_pnginfo: dict = None):
    path = str(path)

    if len(img.shape) != 3:
        raise ValueError(f"can't take image batch as input, got {img.shape[0]} images")

    img = img.permute(2, 0, 1)
    if img.shape[0] not in (3, 4):
        raise ValueError(
            f"image must have 3 or 4 channels, but got {img.shape[0]} channels"
        )

    img = img.clamp(0, 1)
    img = F.to_pil_image(img)

    metadata = PngInfo()

    if prompt is not None:
        metadata.add_text("prompt", json.dumps(prompt))

    if extra_pnginfo is not None:
        for k, v in extra_pnginfo.items():
            metadata.add_text(k, json.dumps(v))

    img.save(path, pnginfo=metadata, compress_level=4)

    subfolder, filename = os.path.split(path)

    return {"filename": filename, "subfolder": subfolder, "type": "output"}


class save_every_n:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    "path": ("STRING", {"forceInput": True}),
                    "image": ("IMAGE", ),
                    "every": ("INT", {"default": 10, "min": 1, "max": 0xffffffffffffffff}),
                },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
            }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "saveN_image"

    CATEGORY = "Tof"

    def saveN_image(self, path, image, every, prompt=None, extra_pnginfo=None):
        path = path[0]
        filename = os.path.basename(path)
        path = path.replace(filename, "")
        # print(path)
        # print(filename)
        i = int(re.search(r'\d+', filename).group())
        # print(i)
        if every * round(i / every) == i:
            f = os.path.splitext(os.path.basename(filename))
            # print(f[0])
            # print(f[1])
            new_f = filename.replace(f[1], ".png")
            save_image(image[0], path + new_f, prompt=prompt, extra_pnginfo=extra_pnginfo,)
            print("\033[94mTof Nodes - Save image every N generations :\033[0m File saved in png format with embeded worflow")
        else:
            print("\033[94mTof Nodes - Save image every N generations :\033[0m Nothing to do")
        return ()


#________________________________________________________________
#________________________________________________________________
#   growMask with W and H
#________________________________________________________________
#________________________________________________________________

def binary_dilation(mask: Tensor, radiusH: int, radiusV: int):
    kernelH = torch.ones(1, radiusH * 2 + 1, device=mask.device)
    kernelV = torch.ones(1, radiusV * 2 + 1, device=mask.device)
    mask = kornia.filters.filter2d_separable(mask, kernelH, kernelV, border_type="constant")
    mask = (mask > 0).to(mask.dtype)
    return mask
    
def mask_unsqueeze(mask: Tensor):
    if len(mask.shape) == 3:  # BHW -> B1HW
        mask = mask.unsqueeze(1)
    elif len(mask.shape) == 2:  # HW -> B1HW
        mask = mask.unsqueeze(0).unsqueeze(0)
    return mask

class grow_maskHV:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "grow_horizontaly": ("INT", {"default": 0, "min": 0, "max": 8096, "step": 1}),
                "grow_vertically": ("INT", {"default": 0, "min": 0, "max": 8096, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    CATEGORY = "Tof"
    FUNCTION = "expand"

    def expand(self, mask: Tensor, grow_horizontaly: int, grow_vertically: int):
        mask = mask_unsqueeze(mask)
        if grow_horizontaly > 0 or grow_vertically > 0:
            mask = binary_dilation(mask, grow_horizontaly, grow_vertically)
        return (mask.squeeze(1),)

#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________
#
#   Random Any
#
#_______________________________________________________________________________________________________
#_______________________________________________________________________________________________________

class RandomAny:
    @classmethod
    def INPUT_TYPES(cls):

        return {
            "required": {
                "any_1": (any, {}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0x7FFFFFFFFFFFFFFF}),
                "n": ("INT", {"default": 0, "min": -0x8000000000000000, "max": 0x7FFFFFFFFFFFFFFF})
                ,
            },
        }

    CATEGORY = "Tof"
    FUNCTION = "switchAny"
    RETURN_TYPES = (any, "INT", "INT", "INT",)
    RETURN_NAMES = ("*", "index", "seed", "seed_INT+n")

    def switchAny(self, seed: int, n: int, **kwargs,):
        _inputs = []
        for _in in kwargs.values():
            _inputs.append(_in)
        numb = len(kwargs)
        random.seed(seed)
        choice = random.randint(0, numb-1)
        # print(choice)

        output = _inputs[choice]
        return (output, choice, seed, (int(choice)+n),)


# NODE MAPPING
NODE_CLASS_MAPPINGS = {
    "Prompt with variables": variables_prompt_v2,
    "Load image random": load_image_random,
    "Save image every N generations": save_every_n,
    "Save json every N generations": save_json_every_n,
    "Save text every N generations": save_text_every_n,
    "Grow Mask HV": grow_maskHV,
    "Random Any": RandomAny,
}
