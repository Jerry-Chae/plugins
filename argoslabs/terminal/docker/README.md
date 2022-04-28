# Docker Remote Service

***This plugin try to connect remote host and run docker or docker-compose service.***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item | Value
---|:---:
Icon | ![Icon](icon.png) 
Display Name | **Docker Remote Service**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)
* [github](https://github.com/Jerry-Chae)

## Notification

### Dependent modules
Module | Source Page | License | Version (If specified otherwise using recent version will be used)
---|---|---|---
[paramiko](https://pypi.org/project/paramiko/) | [paramiko/paramiko](https://github.com/paramiko/paramiko) | [LGPL v2.1](https://github.com/paramiko/paramiko/blob/main/LICENSE) | 2.10.4
[paramiko-expect](https://pypi.org/project/paramiko-expect/) | [fgimian/paramiko-expect](https://github.com/fgimian/paramiko-expect) | [MIT](https://github.com/fgimian/paramiko-expect/blob/master/LICENSE) | 0.3.2
[cryptography](https://pypi.org/project/cryptography/) | [pyca/cryptography](https://github.com/pyca/cryptography/) | [Both Apache BSD License](https://github.com/pyca/cryptography/blob/main/LICENSE) | 37.0.0


## Warning 
No potential damage to customer files and data (overwrite risk)

## Helpful links to 3rd party contents
None

## Version Control 
* [4.410.2130](setup.yaml)
* Release Date: `Apr 10, 2022`

## Input (Required)
Display Name | Input Method | Default Value | Description
---|---|---|---
msg | | | message to translate

> * If message to translate is too big then use `Text file`

## Input (Optional)

Display Name | Show Default | Input Method | Default Value | Description
---|---|---|---|---
Text file | True | fileread | | Text file to read message
File Encoding | False | | utf8 | File encoding for text file
Target lang | True | choices | English | Destination language to use
Source lang | False | choices | auto | Destination language to use, if auto is set then try to detect source language automatically
Detect lang | False | Flag | Not selected | f set this flag just guessing the language of message and confidence. The result looks like `ko, 0.778`

> * If Show Default is True then this item is showed at the Properties otherwise hided at Advanced group

## Return Value

### Normal Case
Tranlated message

### When set `Detect lang` advanced property
[language 2-character code](https://www.loc.gov/standards/iso639-2/php/code_list.php), confidence (0 ~ 1)
Example result is 
```sh
ja,0.873
```

## Return Code
Code | Meaning
---|---
0 | Success
1 | Exceptional case

## Parameter setting examples (diagrams)
![Parameter setting examples - 1](README-image2021-12-13_10-1-9.png)
