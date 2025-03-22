from django.shortcuts import render, redirect
from .forms import FarmerDetailsForm, FarmerFinancialDetailsForm

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