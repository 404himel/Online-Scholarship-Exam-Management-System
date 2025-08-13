from django.shortcuts import render
import joblib
import numpy as np
def performance_home(request):
    return render(request, 'performance_home.html')



def performance_result_view(request):
    if request.method == 'POST':
        try:
            model = joblib.load("model.pkl")
            scaler = joblib.load("scaler.pkl")

            # Collect form data and convert to proper types
            Student_Age = float(request.POST.get('Student_Age'))
            Sex = int(request.POST.get('Sex'))
            High_School_Type = int(request.POST.get('High_School_Type'))
            Scholarship = float(request.POST.get('Scholarship'))
            Additional_Work = int(request.POST.get('Additional_Work'))
            Sports_activity = int(request.POST.get('Sports_activity'))
            Weekly_Study_Hours = float(request.POST.get('Weekly_Study_Hours'))
            Attendance = int(request.POST.get('Attendance'))
            Notes = int(request.POST.get('Notes'))

            # Prepare feature list in model expected order
            features = [
                Student_Age, Sex, High_School_Type, Scholarship,
                Additional_Work, Sports_activity, Weekly_Study_Hours,
                Attendance, Notes
            ]

            # Scale features using the loaded scaler
            features_scaled = scaler.transform([features])

        
            prediction = str(model.predict(features_scaled)[0])
            print("prediction: ",prediction)

       

            return render(request, 'performance_result.html', {
                'prediction': prediction
            })

        except Exception as e:
            return render(request, 'error.html', {'error_message': str(e)})

    # If GET request, render input form
    return render(request, 'performance_home.html')




