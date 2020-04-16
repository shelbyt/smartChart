![SM Logo](images/logo-sms.png)
# SmartChart

Search Match (SM) takes in a csv of terms and matches text. 

### Read Before Use

**To Edit Search Terms:**
Windows:
1) Open SearchMatch folder
2) Right click "conditions.csv"
3) Open with Notepad
4) Edit search terms
5) Save when finished

Mac:
1) Right-click SearchMatch app
2) Show package contents
3) Open "Contents" folder
4) Open "conditions.csv"
5) Edit search terms
6) Save when finished

**SC Removes** *Past Medical History* and *Physical Exam* from text by removing everything in between:

a) *Past Medical History* and *Drug Use*

b) *Physical Exam* to *Assessment/Plan*

Example:
> Arise, fair sun, **past medical history**:, and kill the envious moon,
Who is already sick and pale with grief
That thou **drug use**: her maid, art far more fair than she. . . .
The brightness of her cheek would shame those stars
**Physical Exam**: As daylight doth a lamp; her eye in heaven
Would through the airy region stream so bright
**Assessment/Plan**: That birds would sing and think it were not night.

Turns into:

> Arise, fair sun, **drug use**: her maid, art far more fair than she. . . .
The brightness of her cheek would shame those stars
**ASSESSMENT**: That birds would sing and think it were not night.


In the future this will be configurable. For now it can be toggled on and off.
![SC Example](images/example1.PNG)

### The Problem:
Word processors like Word and Google Docs require a user to use complex "regular expressions" to match multiple terms at the same time.


### The Solution:
##### Create a CSV list of terms:

![SM Terms](images/terms-sm.png)


##### Enter text and click buttons to match


![SM Results](images/result-sm.png)

- - -
###### Copyright© Shawn and Shelby Thomas 2020


