# TOOL ROAD
From a background model to detect the vehicles that pass through the toll, it is sought to obtain the number of the license plate and the city.

Haar classifier
==========
Haar is a cascade classifier that is a system for the recognition of objects using hundreds of samples, these must be positive and negative, use the classifier to recognize the shape of the desired object.

Positive images
--------------------
We need to collect positive images that contain only objects of interest, in our case they were plates, building a positive dataset of 89 images.

<p align="center">
  <img src="https://static.iris.net.co/dinero/upload/images/2009/3/25/75779_151948_1.jpg" width="350"/>
</p>


Negative images
--------------------
We need to collect negative images that do not contain objects of interest, they must contain all kinds of objects, thus avoiding that the classifier does not have enough information about what is not our desired object, this dataset was 2056 images

<p align="center">
  <img src="https://grupoavante.org/media/catalog/product/cache/1/thumbnail/600x/17f82f742ffe127f42dca9de82fb58b1/t/o/toyo_open_country_at2_wo_11.jpg" width="250"/>
</p>



Background & Foreground Extraction
==========

The idea of extracting the foreground is to identify the objects that are not part of the background, i.e., the objects different from those present in the static scene.


Gaussian Mixture-based Background Subtraction
--------------------

<p align="center">
  <img src="https://cstopics.github.io/cstopics/assets/img/vision/7_mog.png" width="350"/>
</p>

Simple Thresholding
==========

Here, the matter is straight forward. If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black). The

<p align="center">
  <img src="https://cstopics.github.io/cstopics/assets/img/vision/4_structures.png" width="650"/>
</p>

Adaptive Gaussian Thresholding
--------------------

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmKpr6K4YhbSKnvY0w1o6EOVX8M8N9w_JjYfOWfafoDgk0lD05" width="350"/>
</p>

Transformations
==========
Geometric transformations modify the spatial relationship between pixels in an image. Suppose an input space $(w, z)$ and an output space (x, y), that are coordinate systems.


<p align="center">
  <img src="https://raw.githubusercontent.com/cstopics/cstopics/6937cd1177395c72b3ccd049293327d8097dc114/assets/notebooks/vision/geo_trans.png" width="450"/>
</p>

Projective transformation
--------------------


<p align="center">
  <img src="https://raw.githubusercontent.com/cstopics/cstopics/6937cd1177395c72b3ccd049293327d8097dc114/assets/notebooks/vision/fig_projective.png" width="250"/>
</p>


Code
==========
The code needs dependencies such as PyQT5, it allows to read the file of the interface, it also needs cv2, with this the processing of the images will be done and finally pytesseract with this the transformation of the image to text will be done, thus obtaining the plate and the city from which it is coming

<p align="center">
  <img src="https://pbs.twimg.com/media/DtLDJWGXcAEkPLG.jpg" width="550"/>
</p>

Interface
==========
The interface is built in qt creator to then read the .ui file in a python program and assign to each widget the function with which it will be activated

<p align="center">
  <img src="Josean11/20182_cstopics_tool_road" width="550"/>
</p>

Results
==========
https://www.youtube.com/watch?time_continue=1&v=GiqK-qqpFHw
