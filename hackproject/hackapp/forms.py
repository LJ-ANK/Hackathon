from django import forms

# Form 1: Farmer Details
class FarmerDetailsForm(forms.Form):
    farmer_id = forms.CharField(max_length=50, label="Farmer ID")
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    aadhar_number = forms.CharField(max_length=12, label="Aadhar Number")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    state = forms.CharField(max_length=100, label="State")
    district_city = forms.CharField(max_length=100, label="District/City")
    village = forms.CharField(max_length=100, label="Village")

# Form 2: Farmer Financial Details
class FarmerFinancialDetailsForm(forms.Form):
    annual_income = forms.DecimalField(max_digits=15, decimal_places=2, label="Annual Income")
    loan_amount_required = forms.DecimalField(max_digits=15, decimal_places=2, label="Loan Amount Required")
    existing_loan = forms.DecimalField(max_digits=15, decimal_places=2, label="Existing Loan", required=False)
    credit_score = forms.IntegerField(min_value=300, max_value=900, label="Credit Score")
    bank_name = forms.CharField(max_length=100, label="Bank Name")
    bank_account_number = forms.CharField(max_length=20, label="Bank Account Number")
    ifsc_code = forms.CharField(max_length=11, label="IFSC Code")