# Social Distancing 🧍‍♀️🧍‍♂️
--------------------
Detecting with YOLO whether the minimal safe distance between two persons is being kept.

Based on this <a href="https://www.pyimagesearch.com/2020/06/01/opencv-social-distancing-detector/"> great tutorial </a>.

## Examples:
<img src="pedestrians.gif"  width=400>

------------------------------------------------
## TO DO:
- [] Eliminate hard-coded values (DISTANCE). If one person has avg. ~170cm height then look for appropriate scale in pixels (based on bbox ymin and ymax).