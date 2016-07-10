# Password_analysis
Analysis of passwords

# Introduction
For this project the following terminology have been used. These are as follows<br>
* `case` point to password consisting of lower case(`l`), upper case(`u`), numericals(`n`) or symbols(`s`). A single password can have a combination of these.
+ `case_pos`, this is the flag which poins to the rough position where the case was used. These are start(`s`), middle(`m`), end(`e`), start and end(`se`).<br>

For example :- "password" will have case position `se` for case `l`, "@password" will have case position `s` for case `s` and case position `e` for case `l`

+ `group_length`, each password is divided into the chunks of cases. That is all the elements that point to a case which are also togther are chunked together. The max length of the chunk is given in group length for a case
+ `group_num` is the number of elements present in the group for a particular case<br>

For example :- "@!password1234@pass" will be grouped into ['password', 'pass'] for case `l`, ['@!', '@'] for case `s` and ['1234'] for case `n`.<br>
Here `group_length` is for case `l` is `len('password')` and `group_num` for case `l` is 2 i.e. `len(['password', 'pass'])`<br>

+ `frequancy` is the leter or symbol or numeric frequancy in all the passwords
+ `troubling` passwords are the list of all the passwords on which the program was not able to run the analysis code. These passwords are left out of the analysis

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
