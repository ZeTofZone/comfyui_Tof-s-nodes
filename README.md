# comfyui Tof's nodes
A set of utility nodes for Comfyui
<hr>
<hr>

<h1><b>Grow Mask HV</b></h1>


This node is made to grow a mask with different value for the horizontal and vertical size.
<br>&nbsp;<br>
![grow_mask_hv](https://github.com/user-attachments/assets/4d8e36f7-cd81-4fda-84c3-649b988187a5)

<hr>
<h1><b>Laod Image Random</b></h1>
A node to load a random image from a folder.
<br>&nbsp;<br>

If the image contain alpha layer, it will output it as a mask.
<br>&nbsp;<br>

![laod_image_random](https://github.com/user-attachments/assets/e69002b4-45ea-4427-9ee1-e9734a77e2ed)


<hr>
<h1><b>Save <i>xxx</i> every "n" generations</b></h1>
A set of 3 nodes made to work with the WAS suite "Image Save" node.
<br>
<br>&nbsp;<br>
They are saving :
<ul>
  <li>The workflow in json format for the node "Save json every N generations" (useful if you use the WAS node to save in jpg, which doesn't save the embeded workflow). The file is saved in a "workflow" folder.</li>
  <li>The text (present at "text" input) for the node "Save text every N generations" (useful to save the prompt). The file is saved in a "prompt" folder.</li>
</ul>
<br>&nbsp;<br>

![save_xxx_n_generations](https://github.com/user-attachments/assets/03ba9b36-d04a-43b0-9f53-5bc8efcc9932)
