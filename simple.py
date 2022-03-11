
from tkinter.constants import CENTER, LEFT, RIDGE, RIGHT, WORD

import requests
from requests.auth import HTTPBasicAuth
import base64

import PySimpleGUI as sg
import os

#релиз 2
from flask import Flask
import queue
import threading
import requests
from flask import request
from waitress import serve
#-

from cryptography.fernet import Fernet


sg.set_options(enable_treeview_869_patch=False)

import json
import configparser
import winsound

#from flask import Flask
#import threading
import pyttsx3

import random
import string

import PIL.Image
import io
from pynput import keyboard
from datetime import datetime
import queue

gui_queue = queue.Queue()
gui_queue_key = queue.Queue()

#релиз 2
popup_queue = queue.Queue()
showscreen_queue = queue.Queue()

#-

oldwindow_screen =None
window_screen =None
window = None
url=''
username=''
password=''
code=''
fullscreen=False
window_height=400
window_width=600
BarcodeVar=''
noScroll=False

barcode=''
current_time  = None
now_time = datetime.now()


showscreen_process=""

MAGIC_USERNAME_KEY = 'SIMPLEUI_key'
service_id = 'SIMPLEUI'

# currinputxml=None
# currscreenname=""
# curroperation_name=""


sg.theme('DarkAmber') 

def get_firstname(inputxml):
     for elem in inputxml['Operations']:
        if elem.get('type')=='Operation':
            return elem.get('Name')

def tts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate',120)  #120 words per minute
    engine.setProperty('volume',1.0) 

    engine.runAndWait()
    engine.stop()

def ss(t):
    global root
    process_xml  = get_process(root,t)
    screen_xml  = get_screen(process_xml)
    show_screen(screen_xml,get_firstname(process_xml),t)



hashMap = list()
list_table_var = []

list_wrapped = []
list_wrapped_vertical = []

textview_keys=0
ErrorMessage = ""
ErrorMessageOpen=""

#релиз 2
#Запускаем сервер
app = Flask(__name__)

@app.route("/popup/<text>", methods=['GET'])
def index(text):
    popup_queue.put(text) 
    return "ok" 

@app.route("/show_screen/<process>/<screen>", methods=['GET','POST'])
def index_ask(process,screen):
    
    show_screen_web(request,process, screen)

    
    return "ok" 

@app.route("/set_screenshot", methods=['GET','POST'])
def index_ask_screenshot():
    
    
    global showscreen_process
    

    

    request.encoding='utf-8'

    jresponse = json.loads(request.json) 

    if "hashmap" in jresponse:   
        jHashMap = jresponse["hashmap"]
        for valpair in jHashMap:
           hashMap.append({"key":valpair['key'],"value":valpair['value']})



    showscreen_process = "Scanner monitoring"
    showscreen_queue.put("Scanner monitoring")

    


    
    return "ok"     

def show_screen_web(request,process, screen):
    global showscreen_process

    showscreen_process = process
    showscreen_queue.put(screen)

    request.encoding='utf-8'

    jresponse = json.loads(request.text.encode("utf-8")) 


    if "hashmap" in jresponse:   
        jHashMap = jresponse["hashmap"]
        for valpair in jHashMap:
           hashMap.append({"key":valpair['key'],"value":valpair['value']})

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    

@app.route('/shutdown', methods=['POST'])
def shutdown():
    
    shutdown_server()
    return 'Server shutting down...'
web_thr=None
server =None
if __name__ == '__main__':
    
  web_thr =  threading.Thread(target=app.run,kwargs=dict(host='0.0.0.0', port=5000, debug=False)).start() 
  



table_rows = list()

def get_screen(inputxml,screenname=""):
     global BarcodeVar
     global noScroll
     result = None
     BarcodeVar=''
     noScroll=False
     for elem in inputxml['Operations']:
        if elem.get('type')=='Operation' and elem.get('Name')== screenname or (screenname==""):
            if elem.get('noScroll')=='false':
                noScroll=False
            else:
                noScroll=True    

            for pr in elem['Elements']:
                if pr.get('type') == 'LinearLayout':
                    if result==None:
                        result = pr
                elif  pr.get('type') == 'barcode' and BarcodeVar=='':
                    BarcodeVar = pr.get('Variable')
     return result

                    

def get_process(inputxml,processname):
     for elem in inputxml['ClientConfiguration']['Processes']:
        if elem.get('type')=='Process':
            if elem.get('ProcessName') == processname:
                return elem

def calculateField(val):
    global hashMap

    if val==None: 
        return ''

    if len(val)==0:
        return ''

    if val[0]=='@':
        var = val[1:]

        result = next((item for item in hashMap if item["key"] == var), None)
        if result==None:
            return "Variable has not been initialized :"+var
        else:    
            return result["value"]

    else:
        return val    
        

def get_layouts(inputxml,orientation,level):
   
    global table_rows
    global text
    global textview_keys

    layout_screen=[]
    new_column= list()

    for elem in inputxml['Elements']:
        if orientation=="vertical":
                   new_column = list() 
                   
        if elem.get('type')=='LinearLayout':
            result_layout = get_layouts(elem,elem.get("orientation"),level+1)

    
            if orientation=='horizontal':
                new_column.append(sg.Column(result_layout))
            else:
                
                layout_screen.append(result_layout)   

            
        else:  
            
 
 
            if elem.get('type')=='TextView':
                
                tvkey = elem.get("Variable")
                if tvkey==None or tvkey=='':
                   tvkey = 'tv'+str(textview_keys)
                   textview_keys+=1
               
               

                b_tn = sg.Text(calculateField(elem.get("Value")),key=tvkey)
               
                
                decoration(elem,b_tn)      

                if elem.get("TextSize")!=None:
                    if type(elem.get("TextSize")) == int:
                        b_tn.Font =(None,elem.get("TextSize")) 
                
                set_color(elem, b_tn)   

                set_gravity(elem, b_tn)    


               
                new_column.append(b_tn)
                                       

            if elem.get('type')=='MultilineText':
                
                tvkey = elem.get("Variable")
                if tvkey==None or tvkey=='':
                   tvkey = 'tv'+str(textview_keys)
                   textview_keys+=1

               
                
                b_tn = sg.Multiline(calculateField(elem.get("Value")),key=tvkey)
                decoration(elem, b_tn)
                            
                set_color(elem, b_tn)   
               
                new_column.append(b_tn)

            if elem.get('type')=='Picture':
                
                _data = calculateField(elem.get("Value"))
                
                if "Не задано" not in str(_data):

                    w = None
                    if elem.get("width")!=None:
                        if type(elem.get("width")) == int:
                            w =elem.get("width")
                        

                    h = None
                    if elem.get("height")!=None:
                        if type(elem.get("height")) == int:
                            h =elem.get("height")

                    

                    if w!=None and h!=None:        
                        data = convert_to_bytes(_data,(w,h))
                    else:    
                        data = convert_to_bytes(_data)      

                    b_tn = sg.Image(data=data,key=elem.get("Variable"))
                    decoration(elem, b_tn)
                                
                    set_gravity(elem, b_tn)
                
                    new_column.append(b_tn)



            if elem.get('type')=='Button':
                b_tn = sg.Button(calculateField(elem.get("Value")),size=(50,None),key=elem.get("Variable"))

                decoration(elem, b_tn)  

                set_gravity(elem, b_tn)
                

                new_column.append(b_tn)

            if elem.get('type') == 'CheckBox':    

                tDefaultValue = False
                result = next((item for item in hashMap if item["key"] == elem.get("Variable")), None)
                if  result!=None:
                    if isinstance(result,dict):
                       if result['value'].lower()=='true' or result['value'].lower()=='да':
                        tDefaultValue = True
                       else:
                        tDefaultValue = False 
                    else:    
                        if result.lower()=='true':
                         tDefaultValue = True
                        else:
                         tDefaultValue = False    

                b_tn = sg.Checkbox(calculateField(elem.get("Value")),key=elem.get("Variable"),enable_events=True,default=tDefaultValue )


                set_gravity(elem, b_tn)
               
                decoration(elem, b_tn)

                new_column.append(b_tn)
            if elem.get('type') == 'SpinnerLayout':

                vList = []
                listelems = calculateField(elem.get("Value")).split(";");    

                

                b_tn = sg.InputCombo(listelems,size=(50,None),key=elem.get("Variable"),enable_events=True)

                if len(listelems)>0:
                     

                    result = next((item for item in hashMap if item["key"] == elem.get("Variable")), None)
                    if  result!=None:
                        b_tn.DefaultValue = result['value']
                    else:
                        b_tn.DefaultValue = listelems[0]

                
                set_gravity(elem, b_tn)
                decoration(elem, b_tn)

                new_column.append(b_tn)
                
                

            if elem.get('type')=='EditTextText' or elem.get('type')=='EditTextNumeric':
                b_tn = sg.InputText(elem.get("Value"),size=(50,None),key=elem.get("Variable"))

                set_gravity(elem, b_tn)    


                new_column.append(b_tn)


            if elem.get('type')=='TableLayout':

                table_str = calculateField(elem.get("Value"))

                #data = make_table(table_str)

                data = []


                jval= json.loads(table_str.encode("utf-8")) 

                jcolumns =  jval["columns"]

                mstring = []
                for column in jcolumns:
                    mstring.append(column ['header'])
                data.append(mstring)

                jrows = jval["rows"]
                for row in jrows:
                    mstring = []
                    for column in jcolumns:
                    #print(row[column ['name']])
                        mstring.append(row[column ['name']])
                    data.append(mstring)    


                headings = []

    
                for column in jcolumns:
                    headings.append(column ['header'])

                #headings = make_headers(table_str)


                tablekey = elem.get("Variable")
                if tablekey==None:
                   tablekey = 'selected_line'

                if len(tablekey.lstrip())==0:
                   tablekey = 'selected_line'    

                if not tablekey in list_table_var:
                    list_table_var.append(tablekey)


                table_rows.append({"key":tablekey,"value":jrows})
            #max_col_width=25,
                b_tn = sg.Table(values=data[1:][:], headings=headings, 
                    # background_color='light blue',
                    auto_size_columns=True,
                    display_row_numbers=False,
                    #justification='right',
                    
                   alternating_row_color='gray',
                    key=tablekey,
                    #row_height=35,
                    
                    enable_events=True)


               
               
                if elem.get("width")!=None:
                    if type(elem.get("width")) == int:
                         if elem.get("width")>0:
                            b_tn.RowHeight =elem.get("width")
               
                if elem.get("height")!=None:
                    if type(elem.get("height")) == int:
                        if elem.get("height")>0:
                            b_tn.NumRows =elem.get("height")
        
                new_column.append(b_tn)



        if orientation=="vertical" and len(new_column)>0:
            layout_screen.append(new_column)
    if  orientation=="horizontal":
        return new_column               
    return  layout_screen           

def set_color(elem, b_tn):
    textColor = None
    backroundcolor = None
    if elem.get("TextColor")!=None and elem.get("TextColor")!='':
     textColor=elem.get("TextColor").upper()
    if elem.get("BackgroundColor")!=None and elem.get("BackgroundColor")!='':
     backroundcolor=elem.get("BackgroundColor").upper()
    if textColor!=None :
     b_tn.TextColor = textColor 
    if backroundcolor!=None :
     b_tn.BackgroundColor = backroundcolor   

def set_gravity(elem, b_tn):
    if elem.get("gravity_horizontal")!=None:
        if elem.get("gravity_horizontal")=="left":
            b_tn.Justification = LEFT
        if elem.get("gravity_horizontal")=="right":
            b_tn.Justification = RIGHT
        if elem.get("gravity_horizontal")=="center":
            b_tn.Justification = CENTER    

def decoration(elem, b_tn):
    global list_wrapped,list_wrapped_vertical
    w = None
    if elem.get("width")!=None:
        if type(elem.get("width")) == int:
            w =elem.get("width")
        if elem.get("width")=='match_parent' and b_tn.Key!='':
            list_wrapped.append(b_tn.Key)    

    h = None
    if elem.get("height")!=None:
        if type(elem.get("height")) == int:
            h =elem.get("height")
        if elem.get("height")=='match_parent' and b_tn.Key!='':
            list_wrapped_vertical.append(b_tn.Key)     

    if w!=None or h!=None:        
        b_tn.Size=(w,h)  

    
               
       


def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)
#--


def make_table(val):

    data = []


    jval= json.loads(val.encode("utf-8")) 

    jcolumns =  jval["columns"]

    mstring = []
    for column in jcolumns:
        mstring.append(column ['header'])
    data.append(mstring)

    jrows = jval["rows"]
    for row in jrows:
        mstring = []
        for column in jcolumns:
            #print(row[column ['name']])
            mstring.append(row[column ['name']])
        data.append(mstring)

    
    return data

def make_headers(val):

    data = []

    jval= json.loads(val.encode("utf-8")) 

    jcolumns =  jval["columns"]

    for column in jcolumns:
         data.append(column ['header'])

    return data

def convert_to_bytes(file_or_bytes, resize=None):

    if isinstance(file_or_bytes, str):
        #img = PIL.Image.open(file_or_bytes)
        img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def show_screen(inputxml,screenname="",operation_name=""):



    global ErrorMessage, ErrorMessageOpen
    global hashMap
    global oldwindow_screen
    global window_screen
    global textview_keys
    global gui_queue
    global gui_queue_key
    global list_wrapped,list_wrapped_vertical




    textview_keys=0

    send_request("OnCreate",screenname,operation_name,"OnCreate")

    layout_screen = list()

    list_wrapped = []
    list_wrapped_vertical = []

    layout_screen = get_layouts(inputxml,"vertical",0)
    
    if ErrorMessage!="":
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 200  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

        new_column = list() 
        b_tn = sg.Text(ErrorMessage,size=(70,None),key="ErrorMessage",font=(None,20),text_color='#ed1a1a'.upper())
        new_column.append(b_tn)
        layout_screen.append(new_column)

    if ErrorMessageOpen!="":
        frequency = 2500  # Set Frequenc
        duration = 200  # Set Duration T
        winsound.Beep(frequency, duration)

        new_column = list() 
        b_tn = sg.Text(ErrorMessageOpen,size=(70,None),key="ErrorMessageOpen",font=(None,20),text_color='#ed1a1a'.upper())
        new_column.append(b_tn)
        layout_screen.append(new_column) 

    


    gui_queue = queue.Queue()
    gui_queue_key = queue.Queue()


    if noScroll:
        window_screen = sg.Window(screenname, layout_screen,size=(window_width,window_height+18), element_justification='center',resizable=True,keep_on_top=True,icon=os.path.dirname(os.path.realpath(__file__))+os.sep+'ic_32.ico').Finalize()
    else:    
        col=[[sg.Column(layout_screen,scrollable=True,vertical_scroll_only=True,expand_y=True,expand_x=True,vertical_alignment='top',size=(window_height,window_width),element_justification='center')]]
        window_screen = sg.Window(screenname, col,size=(window_width,window_height+18), element_justification='center',resizable=True,keep_on_top=True,icon=os.path.dirname(os.path.realpath(__file__))+os.sep+'ic_32.ico').Finalize()
    

    for r in window_screen.Rows:
        for el in r:
            if el.Key!=None:
                if el.Key in list_wrapped or el.Key in list_wrapped_vertical:
                    window_screen[el.Key].expand(el.Key in list_wrapped,el.Key in list_wrapped_vertical,el.Key in list_wrapped_vertical)
                    

    #for key_wr in list_wrapped:
    #    window_screen[key_wr].expand(True,False,False)


    if oldwindow_screen!=None:
        oldwindow_screen.close()

    #window_screen.Refresh()
    
    while True:                             # The Event Loop
        event, values = window_screen.read(timeout=10)
        # print(event, values) #debug
        if event in (None, 'Exit', 'Cancel'):
            break

        #релиз 2    
        try:
            popup_message = popup_queue.get_nowait() 
        except queue.Empty:  
            popup_message = None  
       
        if popup_message is not None:    
            #window.disappear()
            sg.popup(popup_message,     keep_on_top=True)
            #window.reappear()    


        try:
            showscreen_message = showscreen_queue.get_nowait() 
        except queue.Empty:  
            showscreen_message = None  
       
        if showscreen_message is not None:    
            l_process_xml  = get_process(root,showscreen_process)
            screen_xml  = get_screen(l_process_xml,showscreen_message)
            if screen_xml==None:
                    
                    ErrorMessage="Screen does not exist:"+showscreen_message
                    sg.popup(ErrorMessage,     keep_on_top=True)
                    #show_screen(inputxml,screenname,operation_name)
                    #oldwindow_screen.close()          
            else:    
                    show_screen(screen_xml,showscreen_message,showscreen_process)
                    #oldwindow_screen.close()  

    

        #-
        
        message=None
        try:
            message = gui_queue.get_nowait() 
        except queue.Empty:  
            message = None  

        message_key=None
        try:
            message_key = gui_queue_key.get_nowait() 
        except queue.Empty:  
            message_key = None      

       
        if event=='__TIMEOUT__' and message==None and message_key==None:
            continue

        if (message is not None and BarcodeVar=='')  and message_key==None: 
            continue

        isTable =False    

        for key in values:
            #apply_theme_fix()

            table_data = next((item for item in table_rows if item["key"] == key), None)
            if table_data!=None and event in list_table_var:
                set_to_hashmap(hashMap,key,table_data['value'][values[key][0]])
                set_to_hashmap(hashMap,key+"_id",values[key][0])
                isTable=True
                
                
            else:    
                set_to_hashmap(hashMap,key,values[key])
                

               
        set_to_hashmap(hashMap,"event","Input")


        if message is not None and BarcodeVar!='': 
            set_to_hashmap(hashMap,"listener","barcode")
            set_to_hashmap(hashMap,BarcodeVar,message)
        elif message_key is not None : 
            set_to_hashmap(hashMap,"listener","keyboard")
            set_to_hashmap(hashMap,'keyboard',message_key)    
        else:    
            if event in list_table_var:
                set_to_hashmap(hashMap,"listener","TableClick")
            else:    
                set_to_hashmap(hashMap,"listener",event)
            
            

        send_request(event,screenname,operation_name,"OperationData")
        oldwindow_screen = window_screen
        noshow=False
        for item in hashMap:

              if item["key"]=="ShowScreen" and item in hashMap:
                noshow=True  
                screen_xml  = get_screen(process_xml,item["value"])
                if screen_xml==None:
                    ErrorMessage="Screen does not exist: "+item["value"]
                    show_screen(inputxml,screenname,operation_name)
                    oldwindow_screen.close()          
                else:    
                    show_screen(screen_xml,item["value"],operation_name)
                    oldwindow_screen.close()    

                if item in hashMap:
                    hashMap.remove(item)
                #exit

        if noshow!=True:
            show_screen(inputxml,screenname,operation_name)
            oldwindow_screen.close() 
        
        
        
def set_to_hashmap(hashMap,key,v):
    result = next((item for item in hashMap if item["key"] == key), None)
    if result==None:
        hashMap.append({"key":key,"value":v})
    else:
        result["value"]=v        


    


    
def on_press(key):
    global barcode
    global current_time
   

   
    try:

        """ try:
           print('key='+key.char)
        except:
            print('ne fartanulo') """

 
        if key == keyboard.Key.enter :
                if barcode!=None and barcode!="":
                    #print('barcode='+barcode)

                    gui_queue.put(barcode) 
                 
                barcode=""
                now_time = None

        now_time = datetime.now()
        if current_time==None:
            if key.char!=None:
                barcode+=key.char
                current_time = datetime.now() 
        else:

            delay = (now_time-current_time).microseconds
            if(delay<=1500000):
                if key.char!=None:
                    barcode+=key.char
            else:
                barcode=""
                current_time = None       
            
        
    except Exception:
        #print(Exception)
        
        if key == keyboard.Key.enter :
                
                barcode=""
                now_time = None
                
        if 'ctrl' in key.name or 'alt' in key.name or 'shift' in key.name or key.name in ['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12']:
         gui_queue_key.put(key.name)        
        
        

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


listener = keyboard.Listener(
    on_press=on_press)
listener.start()

    
def settings_window():

    global url,username,password,fullscreen, fullscreen,window_height,window_width,code

    layout = [[sg.Text('Client code : ',size=(30,None)),sg.InputText(code,key='code')],
              [sg.Text('Web service URL : ',size=(30,None)),sg.InputText(url,key='url')],
              [sg.Text('User : ',size=(30,None)),sg.InputText(username,key='username')],
              [sg.Text('Password : ',size=(30,None)),sg.InputText(password,key='password', password_char='*')],
              [sg.Checkbox('Fullscreen',key='fullscreen',default=fullscreen)],
              [sg.Text('Height : ',size=(10,None)),sg.InputText(default_text=window_height,key='height',size=(10,None)),sg.Text('Width : ',size=(10,None)),sg.InputText(default_text=window_width,key='width',size=(10,None))],

              [sg.Button("Save",key='btn_save'),sg.Button("Cancel",key='btn_cancel')]]

    swindow = sg.Window('Settings', layout,icon=os.path.dirname(os.path.realpath(__file__))+os.sep+'ic_32.ico')


    while True:                             # The Event Loop
        event, values = swindow.read()

        if event == 'btn_save':

            config = configparser.RawConfigParser()
            # sURL =""
            # sUsername =""
            # sPassword = ""
            # sFullScreen =None
            # sHeight = 0
            # sWidth =0

            tpassword=""    
            for key in values:
                if key == 'url':
                 url = values["url"]
                elif key == 'username':
                 username = values["username"]
                elif key == 'code':
                 code = values["code"] 
                elif key == 'password':
                 tpassword = values["password"]
                elif key == 'fullscreen':
                 fullscreen = values["fullscreen"]
                elif key == 'height':
                 window_height = values["height"]
                elif key == 'width':
                 window_width = values["width"]

            config.add_section('CONNECTION')
            config.add_section('VIEW')
            config.set('CONNECTION','url', url)
            config.set('CONNECTION','code', code)
            config.set('CONNECTION','username', username)
            key = b'SGwWpBU1gq4OjGUFJv_SdXhlXpgQw9Iv2R92TA3lWvk='
            f = Fernet(key)
            token = f.encrypt(tpassword.encode('utf-8'))
            config.set('CONNECTION','password', token.decode())
            config.set('VIEW','fullscreen', fullscreen)
            config.set('VIEW','height', window_height)
            config.set('VIEW','width', window_width)

            #keyring.set_password(service_id, username, tpassword)

            with open(os.path.dirname(os.path.realpath(__file__))+os.sep+'config.ini', 'w') as configfile:
               
               config.write(configfile)


            swindow.close()
            break
        elif event == 'btn_cancel':    
            swindow.close()
            break
        if event in (None, 'Exit', 'Cancel'):
           break  

#json_response = response.json()

def send_request(event,screenname,operation_name,operation):
    global hashMap
    global ErrorMessage,ErrorMessageOpen


    result = next((item for item in hashMap if item["key"] == "event"), None)
    if result==None:
        hashMap.append({"key":"event","value":event})
    else:
        result["value"]=event


    
    json_str = {"client":code,"process":operation_name,"operation":screenname,"hashmap":hashMap}

    response  = None

    try:
        response = requests.post(
        url+'/set_input/'+operation,
        data=json.dumps(json_str).encode('utf-8'),
        auth=HTTPBasicAuth(username, password,),
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
        )

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        sg.popup('Backend connection error',  e,   grab_anywhere=True)
        return

    if response.status_code==200:
       response.encoding='utf-8'
       hashMap.clear()
       jresponse = json.loads(response.text.encode("utf-8")) 
       if operation=="OnCreate":
           ErrorMessageOpen = jresponse["ErrorMessage"]
       else:      
           ErrorMessage = jresponse["ErrorMessage"]

       if "hashmap" in jresponse:   
        jHashMap = jresponse["hashmap"]
        for valpair in jHashMap:
           hashMap.append({"key":valpair['key'],"value":valpair['value']})

 

webevent=0

filestr = os.path.dirname(os.path.realpath(__file__))+os.sep+'config.ini'
if(os.path.isfile(filestr)):
    rсonfig = configparser.ConfigParser()
    rсonfig.sections()
    rсonfig.read(filestr)
    rсonfig.sections()
    url = rсonfig['CONNECTION']['url'].strip()
    username = rсonfig['CONNECTION']['username'].strip()
    spassword = rсonfig['CONNECTION']['password'].strip()
    code = rсonfig['CONNECTION']['code'].strip()


    key = b'SGwWpBU1gq4OjGUFJv_SdXhlXpgQw9Iv2R92TA3lWvk='
    f = Fernet(key)
    nopass=False
    try:
        password = f.decrypt(spassword.encode('utf-8')).decode()
    except:
        print('Не удается раскодировать пароль!')
        nopass=True


    #password = keyring.get_password(service_id, username)
    if password==None:
        password=""

    window_height = rсonfig['VIEW'].getint('height',400)
    window_width = rсonfig['VIEW'].getint('width',600)
    fullscreen =rсonfig['VIEW'].getboolean('fullscreen',fallback=False)

if url==None or url=='':
    settings_window()

else:

    layout = list()
    response = None
    try:
        response = requests.get(
            url+'/get_conf?code='+code,
        params={'code': code},
        auth=HTTPBasicAuth(username, password,)
        )
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        
        sg.popup('Ошибка соединения с бэкендом',  e,   grab_anywhere=True)
            
        raise SystemExit(e)
    

    if response.status_code==200:
        root = json.loads(response.content)
    
        

        menu_def = [['&File', ['&Settings','Info', 'E&xit']],
                 ]

        layout.append([sg.Menu(menu_def, tearoff=False, pad=(200, 1),key='mainmenu')])

        for book in root['ClientConfiguration']['Processes']:
            if book.get('type')=='Process':
                text = book.get('ProcessName',"")
                new_string = list()
                b_tn = sg.Button(text,size=(50,None),key=text)
                    
                new_string.append(b_tn)

    
                layout.append(new_string)
     


        window = sg.Window('Simple UI', layout,size=(window_width,window_height),icon=os.path.dirname(os.path.realpath(__file__))+os.sep+'ic_32.ico').Finalize() 
   
   
        for book in root['ClientConfiguration']['Processes']:
            if book.get('type')=='Process':
                text = book.get('ProcessName',"")
                window[text].expand(True,False,False)
                   

    if fullscreen==True:
       window.maximize()   




    while True:     
    
        # The Event Loop
        event, values = window.read(timeout=10)
        
        #релиз 2
        try:
            popup_message = popup_queue.get_nowait() 
        except queue.Empty:  
            popup_message = None  
       
        if popup_message is not None:    
            #window.disappear()
            sg.popup(popup_message,     keep_on_top=True)
         


        try:
            showscreen_message = showscreen_queue.get_nowait() 
        except queue.Empty:  
            showscreen_message = None  
       
        if showscreen_message is not None:    
            l_process_xml  = get_process(root,showscreen_process)
            screen_xml  = get_screen(l_process_xml,showscreen_message)
            if screen_xml==None:
                    
                    ErrorMessage="Screen does not exist:"+showscreen_message
                    sg.popup(ErrorMessage,     keep_on_top=True)
                    #show_screen(inputxml,screenname,operation_name)
                    #oldwindow_screen.close()          
            else:    
                    show_screen(screen_xml,showscreen_message,showscreen_process)
                    #oldwindow_screen.close()  


        #-

        if event=='__TIMEOUT__':
            continue

        if event == 'Info':
            window.disappear()
            sg.popup('Simple UI (c) Dmitry Vorontsov', 
                     'Version', '1.00',  grab_anywhere=True)
            window.reappear()
   
        if event == 'Settings':
            settings_window()
            continue

        if event in (None, 'Exit', 'Cancel'):


            requests.post('http://127.0.0.1:5000/shutdown')

            #релиз 2
            #pill2kill.set()
            #thr.join()
            #stop_thread=True

            break    
        


        process_xml  = get_process(root,event)
        if process_xml!=None:
            screen_xml  = get_screen(process_xml)
            show_screen(screen_xml,get_firstname(process_xml),event)
        


    window.close()
 