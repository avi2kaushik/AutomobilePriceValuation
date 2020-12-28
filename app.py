from flask import Flask, render_template, request
from datetime import date
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Engine = int(request.form['Engine'])
        Mileage=float(request.form['Mileage'])
        Max_Power = float(request.form['Max_Power'])
        Seats = int(request.form['Seats'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        if(Owner==0):
            owner_FirstOwner=1
            owner_SecondOwner=0
            owner_ThirdOwner=0
            owner_Fourth_Above=0
            owner_TestDriveCar=0
        elif(Owner==1):
            owner_FirstOwner = 0
            owner_SecondOwner = 1
            owner_ThirdOwner = 0
            owner_Fourth_Above = 0
            owner_TestDriveCar = 0
        elif (Owner == 2):
            owner_FirstOwner = 0
            owner_SecondOwner = 0
            owner_ThirdOwner = 1
            owner_Fourth_Above = 0
            owner_TestDriveCar = 0
        elif (Owner == 3):
            owner_FirstOwner = 0
            owner_SecondOwner = 0
            owner_ThirdOwner = 0
            owner_Fourth_Above = 1
            owner_TestDriveCar = 0
        elif (Owner == 4):
            owner_FirstOwner = 0
            owner_SecondOwner = 0
            owner_ThirdOwner = 0
            owner_Fourth_Above = 0
            owner_TestDriveCar = 1
        else:
            owner_FirstOwner = 1
            owner_SecondOwner = 0
            owner_ThirdOwner = 0
            owner_Fourth_Above = 0
            owner_TestDriveCar = 0

        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        current_date = date.today()
        current_Year=current_date.year
        Year=current_Year-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Dealer=0
            Seller_Type_TrustmarkDealer=0

        elif(Seller_Type_Individual=='Trustmark Dealer'):
            Seller_Type_Individual = 0
            Seller_Type_Dealer = 0
            Seller_Type_TrustmarkDealer = 1
        else:
            Seller_Type_Individual = 0
            Seller_Type_Dealer = 1
            Seller_Type_TrustmarkDealer = 0
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
            Transmission_Automatic=0
        else:
            Transmission_Manual=0
            Transmission_Automatic=1

        prediction = model.predict([[Kms_Driven2, Mileage, Engine, Max_Power, Seats,
       Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Dealer,
       Seller_Type_Individual, Seller_Type_TrustmarkDealer,
       Transmission_Automatic, Transmission_Manual, owner_FirstOwner,
       owner_Fourth_Above, owner_SecondOwner,
       owner_TestDriveCar, owner_ThirdOwner]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)