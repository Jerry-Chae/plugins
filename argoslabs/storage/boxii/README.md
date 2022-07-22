# Box II

***This plugin allows generating token from box, show list of files, upload files to box and download files from box.***


## Box II
| Item         |          Value           |
|--------------|:------------------------:|
| Icon         | ![Plugin Name](icon.png) |
| Display Name |        **Box II**        |

## Arun Kumar (ak080495@gmail.com)

Arun Kumar
* [email](mailto:ak080495@gmail.com) 
 
## Version Control 
* [4.721.1450](setup.yaml)
* Release Date: `July 21, 2022`

## Input (Required)
| Display Name          | Selection                | Default Value          |
|-----------------------|--------------------------|------------------------|
| Get Token             | Client ID, Client Secret | Token (str)            |
|                       | Redirect URI             |                        |
|                       | User ID                  |                        |
|                       | Password                 |                        |
| File/Folder Lists     | Client ID, Client Secret | type,id,name           |
|                       | Token                    |                        |
|                       | Folder ID                |                        |
| Upload Files          | Client ID, Client Secret | name,id                |
|                       | Token                    |                        |
|                       | Files to Upload          |                        |
|                       | Folder ID                |                        |
| Download Files/Folder | Client ID, Client Secret | (Downloaded file path) |
|                       | Token                    |                        |
|                       | Folder ID or File ID     |                        |
|                       | Output Path              |                        |


## Return Value

### Normal Case
Description of output result

## Return Code
| Code | Meaning                      |
|------|------------------------------|
| 0    | Success                      |
| 1    | Failure (Invalid Input Type) |
| 99   | Exceptional case             |

##Output Format
You may choose one of 3 output formats below,

<ul>
  <li>String (default)</li>
  <li>CSV</li>
  <li>File</li>
</ul>  


## Parameter setting examples (diagrams)

##Operations
###Get Access Token:
![Box II Input Data](README_Get%20Token%20Access.png)
###File/Folder Lists:
![Box II Input Data](README_Get%20file%20list.png)
###Upload Files:
![Box II Input Data](README_Upload%20file.png)
###Download Files/Folder:
![Box II Input Data](README_Download%20files.png)

