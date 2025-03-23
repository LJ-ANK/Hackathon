import pickle
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FarmerDetailsForm, FarmerFinancialDetailsForm
import pandas as pd
import numpy as np
import os
from django.conf import settings
from .models import Farmer

# Get the absolute path of the current file (views.py)
current_file_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path



def multi_step_form(request):
    if request.method == 'POST' and 'step' not in request.session:
        form1 = FarmerDetailsForm(request.POST)
        if form1.is_valid():
            request.session['farmer_details'] = form1.cleaned_data
            request.session['step'] = 2
            return redirect('multi_step_form')
    elif 'step' in request.session and request.session['step'] == 2:
        if request.method == 'POST':
            form2 = FarmerFinancialDetailsForm(request.POST)
            if form2.is_valid():
                farmer_details = request.session.get('farmer_details')
                financial_details = form2.cleaned_data
                print("Farmer Details:", farmer_details)
                print("Financial Details:", financial_details)
                del request.session['farmer_details']
                del request.session['step']
                return render(request, 'success.html')  
        else:
            form2 = FarmerFinancialDetailsForm()
        return render(request, 'multi_step_form.html', {'form': form2, 'step': 2}) 
    else:
        form1 = FarmerDetailsForm()
        return render(request, 'multi_step_form.html', {'form': form1, 'step': 1}) 
    
from django.http import HttpResponse
from django.shortcuts import render
from .models import Farmer

def apply(request):
    if request.method == "POST":
        try:
            print("POST Data:", request.POST)  # Debug output
            main_model_path = os.path.join(current_file_dir, 'Final_Trained_XGBoost_Model.pkl')
            soil_model_path = os.path.join(current_file_dir, 'Soil_Quality_From_Temp&Humid.pkl')
            weather_model_path = os.path.join(current_file_dir, 'Weather_Condition_From_Temp&Rain&Snow.pkl')

            with open(main_model_path, "rb") as file:
                loaded_main_model = pickle.load(file)
            
            with open(soil_model_path, "rb") as file:
                loaded_soil_model = pickle.load(file)
            
            with open(weather_model_path, "rb") as file:
                loaded_weather_model = pickle.load(file)
            farmer = Farmer(
                farmer_name=request.POST.get("farmer_name", ""),
                land_area=float(request.POST.get("land_area", 0)),
                assets_worth=float(request.POST.get("assets_worth", 0)),
                previous_loans=float(request.POST.get("previous_loans", 0)),
                paid_loans=float(request.POST.get("paid_loans", 0)),
                ongoing_loans=float(request.POST.get("ongoing_loans", 0)),
                assets_insurance_coverage=request.POST.get("assets_insurance_coverage", ""),
                crop_name=request.POST.get("crop_name", ""),
                water_availability=request.POST.get("water_availability", ""),
                land_ownership=request.POST.get("land_ownership", ""),
                latitude=request.POST.get("latitude"),
                longitude=request.POST.get("longitude"),  
                soil_quality=None,  
                credit_score=None  
            )
            farmer.save()
            water_availability = 0
            if farmer.water_availability.lower() == 'high':
                water_availability = 2
            
            if farmer.water_availability.lower() == 'medium':
                water_availability = 1
            else:
                water_availability = 0

            if farmer.land_ownership.lower() == 'owned':
                land_ownership = 2
            else :
                land_ownership = 1
            


            
            data = get_weather_data(lat=farmer.latitude,long=farmer.longitude)

            Soil_quality = loaded_soil_model.predict(pd.DataFrame([
                     [sum(data['hourly']['soil_temperature_6cm']) / len(data['hourly']['soil_temperature_6cm']),
                sum(data['hourly']['soil_moisture_0_to_1cm']) / len(data['hourly']['soil_moisture_0_to_1cm'])]
            ], columns=['Soil Temperature (°C)', 'Soil Humidity (%)']))

            weather = loaded_weather_model.predict(pd.DataFrame([
                [sum(data['hourly']['temperature_2m']) / len(data['hourly']['temperature_2m']),
                sum(data['hourly']['snowfall']) / len(data['hourly']['snowfall']),
                sum(data['hourly']['rain']) / len(data['hourly']['rain'])]
            ], columns=['Temperature (°C)', 'Snowfall (cm)', 'Rainfall (mm)']))

            print(Soil_quality, weather)

            if farmer.assets_insurance_coverage == 'yes':
                assets_insurance_coverage = 1
            else:
                assets_insurance_coverage=0
    # Prepare the input data correctly: a single row of 11 columns
            input_data = pd.DataFrame([[
                farmer.land_area,
                farmer.assets_worth,
                10,  # Annual Income (Lakhs)
                farmer.previous_loans,
                farmer.paid_loans,
                farmer.ongoing_loans,
                assets_insurance_coverage,
                float(Soil_quality),
                water_availability,
                land_ownership,
                float(weather)
                        ]], columns=[
                            'Land Area (acres)', 'Extra Assets Worth (Lakhs)',
                    'Annual Income (Lakhs)', 'Previous Loans', 'Repaid Loans',
                    'Ongoing Loans', 'Assets Insurance Coverage', 'Soil Quality',
                    'Water Availability', 'Land Ownership Status', 'Weather Forecast'
                ])

    # Now use the model to predict
            predicted_score = loaded_main_model.predict(input_data)

            return render(request,'Credit_score.html',{'score':predicted_score})     
        #     return HttpResponse(f"""Application submitted successfully!
        #     Your credit score is {predicted_score, Soil_quality, weather}
        # """)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return render(request, "apply.html")

def landing_page(request):
    return render(request, 'landing.html')

import requests

def get_weather_data(lat, long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,soil_temperature_6cm,rain,soil_moisture_0_to_1cm,snowfall&timezone=auto&forecast_days=1"
    
    # Make the GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()  # Return the response as a JSON object
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
