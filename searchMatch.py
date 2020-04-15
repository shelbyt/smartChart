# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright© Shelby Thomas 04/2020


from guizero import App, Text, TextBox, PushButton,Box, ListBox, Window,CheckBox
import re
import csv
from screeninfo import get_monitors
import sys
from dates import date_match
from nltk.tokenize import sent_tokenize

screen_width = 1920
screen_ratio = 1.7
platform = sys.platform

rt = 3
# For Mac need to check this for exceptions
# If it's not win32 assume it's a MAC. Resolution information not
# available.

if (platform == 'win32'):
    for m in get_monitors():
        print(str(m))
        print(m.width)
        screen_width = m.width
        screen_ratio = float(m.width)/m.height
#
    if(screen_width == 1920):
        rt = 1
    elif(screen_ratio < 2):
        rt = 1 
    elif(screen_ratio > 2):
        rt = 2 

resolution = [{

    "app_height":1300,
    "app_width":1000,

    "lbox_height":700,
    "lbox_width":500,

    "fullsen_height":15,
    "fullsen_width":"full",

    "text_box":14,
    "form_box":12,
    "select_box":15,

    "result_box":11,
    "button_pady": 10
},


{
    "app_height":975,
    "app_width":750,

    "lbox_height":225,
    "lbox_width":375,

    "fullsen_height":11,
    "fullsen_width":"full",

    "text_box":11,
    "form_box":10,
    "select_box":12,

    "result_box":12,
    "button_pady":1 

},
{
    "app_height":1075,
    "app_width":750,

    "lbox_height":325,
    "lbox_width":375,

    "fullsen_height":11,
    "fullsen_width":"full",

    "text_box":11,
    "form_box":10,
    "select_box":12,
    "result_box":12,

    "button_pady": 2

},

{
    "app_height":1075,
    "app_width":750,

    "lbox_height":325,
    "lbox_width":375,

    "fullsen_height":11,
    "fullsen_width":"full",

    "text_box":12,
    "form_box":13,
    "select_box":14,
    "result_box":14,

    "button_pady": 2

}
]

app = App(height=resolution[rt]['app_height'],width= resolution[rt]['app_width'] ,title="Search and Match",bg="#ffffff")

term_dict = {}

def dispay_full(value):
   display_str = "\n\n".join(value)
   fullsen.value = display_str
   fullsen.font="Corbel"
   fullsen.text_size = resolution[rt]['result_box']
    

rdict = {}
def pval(val,listbox):
    val_list = rdict[val]
    listbox.value = rdict[val] # This is a list of values for listbox to match

    str_list = []
    for sen_val in val_list:
        subterm_list_raw = term_dict[(sen_val, val)]

        # The subterm list array may have duplicates
        # (TODO)shelby: Clarify why does it have dups?
        subterm_list = list(set(subterm_list_raw))

        for term in subterm_list:
            term_replace = "►"+term+"◄"
            sen_val = sen_val.replace(term, term_replace)
            print (sen_val)

        str_list.append(sen_val)

    display_str = "\n\n".join(str_list)
    fullsen.font="Open Sans"
    fullsen.value = display_str

btn_list = []
lbox_list = []

def analyze():
    ldict = {}
    result = []

    rdict.clear()
    term_dict.clear()

    if(len(btn_list) > 0):
        for btn in btn_list:
            btn.destroy()
        btn_list.clear()

    if(len(lbox_list) > 0):
        for lbox in lbox_list:
            lbox.destroy()
        lbox_list.clear()
    


    with open('conditions.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        
        for line in data:
            #line[1] = line[1].replace(" ","")
            ldict[line[0]] = line[1:][0].split(',')


    data = text_box.value
    data_lower = data.lower()

    if(preprocess_checkbox.value == 0):
        remove_history = re.sub('past medical history.*?drug use',' drug use ',data_lower, flags=re.DOTALL)
        remove_physicala = re.sub('physical exam.*?assessment/plan','. ASSESSMENT',remove_history, flags=re.DOTALL)
        remove_complete = re.sub('physical exam.*?assessment and plan','. ASSESSMENT',remove_physicala, flags=re.DOTALL)
        sentence_list = sent_tokenize(remove_complete)
    else:
        sentence_list = sent_tokenize(data_lower)

    for sentence in sentence_list:
        for (key,terms) in ldict.items():
            for term in terms:
                fixed_word = term.lower()
                # If have a special date character $date$
                # Insert the found dates into the ldict array as a term
                if fixed_word == "$date$":
                    ldict[key].extend(date_match)
                    continue
                if fixed_word in sentence:
                    dup_check = [key,sentence]
                    # If a sub term comes up we save it
                    if (sentence,key) in term_dict:
                        term_dict[(sentence,key)].append(fixed_word)
                    else:
                        term_dict[(sentence,key)] = [fixed_word]
                    if dup_check not in result:
                        result.append([key, sentence])
                        if key in rdict:
                            rdict[key].append(sentence)
                        else:
                            rdict[key] = [sentence]


    lbox_list.append(ListBox(form_box, items=sentence_list, width="fill" ,height= resolution[rt]['lbox_height'],command=dispay_full,multiselect=True,scrollbar=True ))
    lbox_list[0].bg="#C8D7E9"

    counter = 0
    btn = ""

    for(k,vl) in ldict.items():

        if(counter < 4):
            if k in rdict:
                if(platform != 'win32'):
                    btn = PushButton(button_box_r1, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r1, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k, lbox_list[0] ])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r1, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 8):
            if k in rdict:

                if(platform != 'win32'):
                    btn = PushButton(button_box_r2, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r2, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k, lbox_list[0] ])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r2, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 12):

            if k in rdict:

                if(platform != 'win32'):
                    btn = PushButton(button_box_r3, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r3, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k, lbox_list[0] ])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r3, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 16):

            if k in rdict:

                if(platform != 'win32'):
                    btn = PushButton(button_box_r4, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r4, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k, lbox_list[0] ])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r4, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 20):
            if k in rdict:

                if(platform != 'win32'):
                    btn = PushButton(button_box_r5, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r5, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k, lbox_list[0] ])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r5, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 24):
            if k in rdict:
                if(platform != 'win32'):
                    btn = PushButton(button_box_r6, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r6, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k,lbox_list[0]])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r6, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 28):
            if k in rdict:
                if(platform != 'win32'):
                    btn = PushButton(button_box_r7, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r7, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k,lbox_list[0]])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r7, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        elif(counter < 32):
            if k in rdict:
                if(platform != 'win32'):
                    btn = PushButton(button_box_r8, align="left",width="10",text=str("█"+k),command=pval,pady=resolution[rt]['button_pady'] )
                else:
                    btn = PushButton(button_box_r8, align="left",width="10",text=k,command=pval,pady=resolution[rt]['button_pady'] )
                btn.update_command(pval, [k,lbox_list[0]])
                btn.bg ="#9EF844" 
            else:
                btn = PushButton(button_box_r8, align="left",width="10",text=k,pady=resolution[rt]['button_pady'])
                btn.bg ="#F84446" 
        counter += 1
        btn_list.append(btn)
    
title_box = Box(app, width="fill", align="top", border=True)

text_box = TextBox(title_box, text="Copy paste text here and hit ANALYZE",width="100", height="5",multiline='True')
text_box.font = "Corbel"
text_box.text_size =  resolution[rt]['select_box'] 

preprocess_checkbox = CheckBox(app, text="Analyze Raw Data",command=analyze)
analyzebutton = PushButton(title_box, text="Analyze")
analyzebutton.when_clicked = analyze

button_box_r1 = Box(app,  align="top", border=True)
button_box_r2 = Box(app,  align="top", border=True)
button_box_r3 = Box(app,  align="top", border=True)
button_box_r4 = Box(app,  align="top", border=True)
button_box_r5 = Box(app,  align="top", border=True)
button_box_r6 = Box(app,  align="top", border=True)
button_box_r7 = Box(app,  align="top", border=True)
button_box_r8 = Box(app,  align="top", border=True)

form_box = Box(app,width="fill", border=True)
form_box.text_size= resolution[rt]['form_box'] 


select_box = Box(app,width="fill", border=True)
select_box.text_size= resolution[rt]['select_box'] 


fullsen = TextBox(select_box,width="fill",height= resolution[rt]['fullsen_height'] ,text="",multiline=True,scrollbar=True)

app.display()
