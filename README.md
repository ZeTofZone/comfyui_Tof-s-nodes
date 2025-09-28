# comfyui Tof's nodes
## A set of utility nodes for Comfyui

### ==[Grow Mask HV](#grow_mask)==

<br>

- Grow a mask with different values for the horizontal and vertical sizes.

<br>

### ==[Load Image Random](#Load_Image_Random)==

<br>

- A node to load a random image from a folder.

<br>

### ==[Save <i>xxx</i> every "n" generations](#Save_every_n_generations)==

<br>

- A set of 3 nodes made to work with the <a href="https://github.com/WASasquatch/was-node-suite-comfyui" target="_blank">WAS-nodes-suite</a> "Image Save" node.

<br>

### ==[Random Any](#Random_Any)==

- A node which can choose randomly something.

<br>

### ==[Prompt with variables](#Prompt_with_variables)==

- A node made to run with <a href="https://github.com/adieyal/comfyui-dynamicprompts">dynamic prompt</a> (or any other prompt randomizer), which give the possibility to use the same variable multiple times (note that you can use multiple of this node for, on the same workflow, have different prompt with the same variables).
<br>&nbsp;<br>

<hr>
<h1 id="grow_mask"><b>Grow Mask HV</b></h1>


This node is made to grow a mask with different values for the horizontal and vertical sizes.
<br>&nbsp;<br>
![grow_mask_hv](https://github.com/user-attachments/assets/4d8e36f7-cd81-4fda-84c3-649b988187a5)

<hr>
<h1 id="Load_Image_Random"><b>Load Image Random</b></h1>
A node to load a random image from a folder.
<br>&nbsp;<br>

If the image contain alpha layer, it will output it as a mask.
<br>&nbsp;<br>

![laod_image_random](https://github.com/user-attachments/assets/e69002b4-45ea-4427-9ee1-e9734a77e2ed)


<hr>
<h1 id="Save_every_n_generations"><b>Save <i>xxx</i> every "n" generations</b></h1>
A set of 3 nodes made to work with the <a href="https://github.com/WASasquatch/was-node-suite-comfyui" target="_blank">WAS-nodes-suite</a> "Image Save" node.
<br>&nbsp;<br>
They are saving :
<ul>
  <li>The workflow in json format for the node "Save json every N generations" (useful if you use the WAS node to save in jpg, which doesn't save the embeded workflow). The file is saved in a "workflow" folder.</li>
  <li>The text (present at "text" input) for the node "Save text every N generations" (useful to save the prompt). The file is saved in a "prompt" folder.</li>
  <li>The image in png format with embeded workflow for the node "Save image every N generations".</li>
</ul>
<br>&nbsp;<br>

![save_xxx_n_generations](https://github.com/user-attachments/assets/03ba9b36-d04a-43b0-9f53-5bc8efcc9932)

<hr>
<h1 id="Random_Any"><b>Random Any</b></h1>
A node which can choose randomly something.
<br>&nbsp;<br>

![random_any](https://github.com/user-attachments/assets/8e916620-f792-4ba4-8b06-c939277bfac2)

<br>&nbsp;<br>
When you put something on input, it will add a new empty input automatically :
<br>(Take care to not mix different inputs type)
<br>&nbsp;<br>
![random_any2](https://github.com/user-attachments/assets/1dfaced8-b0b0-4810-9122-519d69a40566)
<br>&nbsp;<br>
<ul>
  <li>The <i>index</i> output is the choosen index (INT) element (start at 0 for "any_1").</li>
  <li>The <i>seed</i> output act as a relay to chain multiple nodes taking the same index (if the seed is the same, the choosen input will be the same. As this, you can switch multiple elements, it will always choose the same input between the connected nodes).</li>
  <li>The <i>seed_INT+n</i> output is to chain some other random node. Adding an INT (n) to the seed, will make it following the seed of this node (useful for reproducing workflows).</li>
</ul>

<hr>
<h1 id="Prompt_with_variables"><b>Prompt with variables</b></h1>
A node made to run with <a href="https://github.com/adieyal/comfyui-dynamicprompts">dynamic prompt</a> (or any other prompt randomizer), which give the possibility to use the same variable multiple times (note that you can use multiple of this node for, on the same workflow, have different prompt with the same variables).
<br>&nbsp;<br>

![prompt_with_var_1](https://github.com/user-attachments/assets/a98e811b-4175-4121-8ce4-d90aaad4ad6a)
<br>&nbsp;<br>
<b>Note1 : the variables format should begin with the variable number, a space, ":", and another space : 

>1 :

and the value after.
<br>The variable is called by #<i>variable_number</i> : 

>#1

</b>
<ul><li>Exemple :</li></ul>

![prompt_with_var_ex](https://github.com/user-attachments/assets/605d308f-ecf8-438d-871d-d8a243229d6c)

<br>&nbsp;<br><b>Note2 : You can also use a semi-colon ";" to separate variables.</b>
<br>exemple : 

> {a cat|a dog};{brown|black}

is the same as :

> 1 : {a cat|a dog}<br>
> 2 : {brown|black}<br>

This is useful if you want multiple variable for one choice.
<br>&nbsp;<br>exemple : <br>&nbsp;<br>
<table><tr><td>variables</td><td>prompt</td><td>possible results</td></td></td></tr>
<tr><td>1 : {smiling;a happy|crying;an unhappy}</td><td>A man #1 with #2 face.</td><td>A man smiling with a happy face.<br>or<br>A man crying with an unhappy face.</td></tr>
</table>
<br>In this case don't forget to jump to the next available variable (3 in this case) as variables #1 and #2 are already used.
<br>&nbsp;<br>
<ul><li>Exemple using semi-colon separators :</li></ul>


![prompt_with_var_ex2](https://github.com/user-attachments/assets/a2e5891b-d6f5-4a31-b6de-6a14a2bcb2c5)

The resulting object will be always blue and shiny if it's round, and always green and mat if its's squared.
<br>
