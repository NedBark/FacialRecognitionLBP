from guizero import App, Text, PushButton, TextBox, warn, info, Box
import cv2
import pythonreco
import checkText
import pythonAcq
import os
import checkText
import tkinter
import pythontrain
import glob
from functools import partial

id = None
usr = None

def start_reco():
	    pythonreco.main()
	
def record_user():
        id=txtBox1_id.get().strip()
        usr=txtBox2_name.get().strip()
        code=txtBox3_code.get().strip()
        pythonAcq.main(int(id),str(usr),int(code))
        pythontrain.main()
	#os.system('python pythontry.py')
        
def test():
        id=txtBox1_id.get()
        usr=txtBox2_name.get()
        if(checkText.checkUser(id, usr)==True):
                warn("User alread exists!", "You can use the <Register again button>")
                register_again.show()
        
def register_again(usr):
        path = 'dataset'
        usr=txtBox2_name.get()
        id=txtBox1_id.get()
        #for i in os.listdir(path):
                #if os.path.isfile(os.path.join(path,i)) and usr in i:
        
        for filename in glob.glob("dataset/"+str(usr)+"*"):
                print("Removing: "+filename)
                os.remove(filename)
        print("Starting a new capture session...\n")
        pythonAcq.main(int(id),str(usr),0)
        pythontrain.main()

def run_train():
        pythontrain.main()

app = App(title="Smart Interface")


start_message = Text(app, text = "Welcome home", size = 30, font = "Times New Roman")
login_box = Box(app, width="fill", align="top", border=True)
start_recognition = PushButton(login_box, command=start_reco, text = "Sign In", align="left")

txtBox3_code = TextBox(login_box, align="right")
code_txt = Text(login_box, text="Code:", align="right")
txtBox2_name = TextBox(login_box, align="right")
name_txt = Text(login_box, text="Name:", align="right")
txtBox1_id = TextBox(login_box, align="right")
id_txt = Text(login_box, text="ID:", align="right")

record_user = PushButton(app, command=record_user, text = "Record a new user")
register_again = PushButton(app, command=register_again, args=[usr], text = "Register again", visible=False)
test= PushButton(app, command=test, text = "Test")

run_train = PushButton(app, command=run_train, text = "Just Train", visible=True)

app.display()
