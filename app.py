from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, redirect, url_for, session
import warnings
import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

model = load_model('model/ConvolutionalNeuralNetwork_model.h5', compile=False)
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

class_labels = ['Glioma', 'Meningioma', 'NoTumor', 'Pituitary']


def predict_label(img_path):
    image = load_img(img_path, grayscale=False,
                     color_mode='rgb', target_size=(224, 224))
    image = img_to_array(image)
    image = image/255.0
    image = np.expand_dims(image, axis=0)
    model_pred = model.predict(image)
    class_name = np.argmax(model_pred[0])
    class_label = class_labels[class_name]
    model_probs = model_pred[0][class_name]
    print(class_name)
    print(class_label)
    print(model_probs)
    return class_name, class_label, model_probs


@app.route("/submit", methods=['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
        img = request.files['image']
        file_path = "static/user_tested/" + img.filename
        img.save(file_path)
        p = predict_label(file_path)

        cls_name = p[0]
        cls_label = p[1]
        pblt = p[2]*100
        pblt = f"{round(pblt, 2)}%"
        print("21", cls_name)
        print("22", cls_label)
        print("23", pblt)

        if cls_label == "Glioma":
            smtms = " Gastrointestinal: Nausea or vomiting "
            smtms1 = " Muscular: Muscle weakness or weakness of one side of the body"
            smtms2 = ""
        elif cls_label == "Meningioma":
            smtms = "  Visual: Double vision or vision loss "
            smtms1 = " Eyes: Swelling of optic disc or unequal pupils and Also "
            smtms2 = " Common: Headache, problems with coordinationseizures: "
        elif cls_label == "Pituitary":
            smtms = " Vision changes or headaches are symptoms."
            smtms1 = "In some cases, harmones can also be affected , interfacing with menstrual cycles and  causing sexual dysfunction."
            smtms2 = ""
        else:
            smtms = " Nothing "
            smtms1 = ""
            smtms2 = ""    

    return render_template("home.html", result=True, prediction=cls_name, label=cls_label, probs=pblt, img_path=file_path, smtms=smtms, smtms1=smtms1, smtms2=smtms2)


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):

                return redirect(url_for('home'))
        else:
            mesg = 'Invalid Login Try Again'
            return render_template('login.html', msg=mesg)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        col_list = ["name", "email", "password"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': password}
        r1 = r1.append(new_row, ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successfull !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('register.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        current_pass = request.form['current']
        new_pass = request.form['new']
        verify_pass = request.form['verify']
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["password"] == str(current_pass):
                if new_pass == verify_pass:
                    r1.replace(to_replace=current_pass,
                               value=verify_pass, inplace=True)
                    r1.to_excel("user.xlsx", index=False)
                    msg1 = 'Password changed successfully'
                    return render_template('home.html', msg1=msg1)
                else:
                    msg2 = 'Re-entered password is not matched'
                    return render_template('home.html', msg2=msg2)
        else:
            msg3 = 'Incorrect password'
            return render_template('home.html', msg3=msg3)
    return render_template('home.html')


@app.route('/graph', methods=['POST', 'GET'])
def graph():
    return render_template('graph.html')


@app.route('/logout')
def logout():
    session.clear()
    msg = 'You are now logged out', 'success'
    return redirect(url_for('login', msg=msg))


if __name__ == '__main__':
    app.run(port="5003", debug=True)
