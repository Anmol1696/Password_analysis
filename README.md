# Password_analysis
Analysis of passwords

# Introduction
For this project the following terminology have been used. These are as follows<br>
* <b>case</b> point to password consisting of lower case(<i>l</i>), upper case(<i>u</i>), numericals(<i>n</i>) or symbols(<i>s</i>). A single password can have a combination of these.
+ <b>case_pos</b>, this is the flag which poins to the rough position where the case was used. These are start(<i>s</i>), middle(<i>m</i>), end(<i>e</i>), start and end(<i>se</i>).<br>

For example :- "password" will have case position <i>se</i> for case <i>l</i>, "@password" will have case position <i>s</i> for case <i>s</i> and case position <i>e</i> for case <i>l</i>

+ <b>group_length</b>, each password is divided into the chunks of cases. That is all the elements that point to a case which are also togther are chunked together. The max length of the chunk is given in group length for a case
+ <b>group_num</b> is the number of elements present in the group for a particular case<br>

For example :- "@!password1234@pass" will be grouped into ['password', 'pass'] for case <i>l</i>, ['@!', '@'] for case <i>s</i> and ['1234'] for case <i>n</i>.<br>
Here <b>group_length</b> is for case <i>l</i> is `len('password')` and <b>group_num</b> for case <i>l</i> is 2 i.e. `len(['password', 'pass'])`<br>

+ <b>frequancy</b> is the leter or symbol or numeric frequancy in all the passwords
+ <b>troubling</b> passwords are the list of all the passwords on which the program was not able to run the analysis code. These passwords are left out of the analysis

# Working
Given a list of passwords, this scirpt will give out some basic analysis.<br> 
Apart from the terms in the Introduction, the analysis also give the results mentioned below<br>

## Rockyou list
The script takes input the rockyou.txt file which have a database of common passwords. It consists of more than 14 million passwords. All the password in the list are seen if they macth directly from the rockyou list.<br>
The output is the number of unique passwords from this list and also the individual passwords with there frequancy in the password list.<br>
In the future it will also include if some part of the password is present in the rockyou list.<br>

## Common word list
If one has some sort of idea of where the password list is derived from, or the source of the list, than one can put some words that they think might be common.<br>
Or one can just put some random words for which he wants to know if it is part of the password.<br>
The script will see if the common word is in the string. This function is case insensitive.The return is a dictionary with the common word vs its frequancy in the password list<br>

## Repetation in the password list
The script will also make another dictionary with the count of the password from password list vs the password if the count is more than one.<br>
Basicaly it will give you the frequancy of repeating passwords.<br>

# Future works
This is just a simple analysis of a password list. The idea is to make this script into more robust and usefull analysis.<br>
The following points will be added in the future
* As of now no parsing is done. So there will be some form parsing
+ use of nlp to give more acurate results
+ machine learning techniques to classify the passwords as week, medium, strong

Some more ideas in much more details are present in `things_to_include.txt` file.<br>

# Tools and Libraries
* json
+ rouckyou.txt (Dictionary)
