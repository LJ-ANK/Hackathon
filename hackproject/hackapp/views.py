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
file_path = os.path.join(current_file_dir, 'xgb_model.pkl')



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
                latitude=None,  # Not in form
                longitude=None,  # Not in form
                soil_quality=None,  # Not in form
                credit_score=None  # Not in form
            )
            farmer.save()
            return HttpResponse("Application Submitted Successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return render(request, "apply.html")

def landing_page(request):
    return render(request, 'landing.html')


def apply_now(request):
    if request.method == "POST":

        with open(file_path, "rb") as file:
            loaded_model = pickle.load(file)
        
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        farm_name = request.POST.get("farm_name")
        location = request.POST.get("location")
        farm_size = request.POST.get("farm_size")
        annual_income = request.POST.get("annual_income")
        loan_amount = request.POST.get("loan_amount")
        purpose = request.POST.get("purpose")
        random_sample = np.random.rand(1, 30)
        random_sample = pd.DataFrame(random_sample, columns=['Farming_Experience', 'Farm_Size', 'Land_Quality',
       'Proximity_to_Markets', 'Water_Availability', 'Soil_Health_Metrics',
       'Past_Crop_Yields', 'Crop_Rotation_Practices', 'Pest_Disease_Incidence',
       'Income_from_Farming', 'Non_Farming_Income', 'Expenses', 'Debt_History',
       'Savings_Assets', 'Insurance_Coverage', 'Commodity_Prices',
       'Input_Costs', 'Government_Subsidies', 'Climate_Risk_Score',
       'Soil_Risk_Score', 'Market_Risk_Score',
       'Land_Ownership_Status_Leased', 'Land_Ownership_Status_Owned',
       'Land_Ownership_Status_Rented', 'Crop_Market_Demand_High',
       'Crop_Market_Demand_Low', 'Crop_Market_Demand_Medium',
       'Weather_Forecast_Bad', 'Weather_Forecast_Good',
       'Weather_Forecast_Moderate'])

        predicted_score = loaded_model.predict(pd.DataFrame(random_sample))
        
        return HttpResponse(f"""Application submitted successfully!
        Your credit score is {predicted_score}
        """)
    else:
        return render(request, "apply.html")
