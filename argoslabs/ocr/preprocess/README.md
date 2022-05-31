# OCR PreProcess

***This plugin try to pre-process for the better OCR.***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item | Value
---|:---:
Icon | ![Icon](icon.png) 
Display Name | **OCR PreProcess**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)
* [github](https://github.com/Jerry-Chae)

## Notification

### Dependent modules
Module | Source Page | License | Version (If specified otherwise using recent version will be used)
---|---|---|---
[numpy](https://pypi.org/project/numpy/) | [numpy/numpy](https://github.com/numpy/numpy) | [BSD 3-Clause "New" or "Revised" License](https://github.com/numpy/numpy/blob/main/LICENSE.txt) | 1.21.1
[opencv-python](https://pypi.org/project/opencv-python/) | [opencv/opencv-python](https://github.com/opencv/opencv-python) | [MIT License](https://github.com/opencv/opencv-python/blob/master/LICENSE.txt) | 4.5.3.56
[scikit-image](https://pypi.org/project/scikit-image/) | [scikit-image/scikit-image](https://github.com/scikit-image/scikit-image) | [Own License](https://github.com/scikit-image/scikit-image/blob/main/LICENSE.txt) | 0.19.2


## Warning 
No potential damage to customer files and data (overwrite risk)

## Helpful links to 3rd party contents
None

## Version Control 
* [4.531.1100](setup.yaml)
* Release Date: `May 31, 2022`

## Input (Required)
Display Name | Input Method | Default Value | Description
---|---|---|---
Image | fileread | | Image file to process

> * If message to translate is too big then use `Text file`

## Input (Optional)

Display Name | Show Default | Input Method | Default Value | Description
---|---|---|---|---
Save Temp Images | False | | False | If this flag is set then next 7 temporary image files are created for debugging purpose: *.01-gray.* *02-blurred.* *03-white.* *04-edged.* *05-contours.* *06-10large-countour.* *07-receit-contour.*
Target Image | Fase | filewrite | | If this target file is not given, default result image file must be `{finename}.result.{ext}`, for example the result for `01.jpg` is `01.result.jpg` otherwise given result image file will be used
> * If Show Default is True then this item is showed at the Properties otherwise hided at Advanced group

## Return Value

Absolute result image file path

## Return Code
Code | Meaning
---|---
0 | Success
1 | Invalid image file to process
98 | Parsing error for Parameters or Options
99 | Else exceptional case

<!-- ## Parameter setting examples (diagrams)
![Parameter setting examples - 1](README-image2021-12-13_10-1-9.png) -->
