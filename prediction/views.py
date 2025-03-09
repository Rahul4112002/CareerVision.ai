from django.shortcuts import render, redirect
from .models import Roadmap, Question, Choice
import pickle , os
from django.conf import settings
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder




# model = pickle.load(open("prediction/models/best_student_job_role_model.pkl","rb"))
# le = pickle.load(open("prediction/models/label_encoder.pkl", "rb"))
# processor = pickle.load(open("prediction/models/processor.pkl", "rb"))
# Load the new model
# model = pickle.load(open("prediction/models/MLPclassifier_model.pkl", "rb"))
# oe = pickle.load(open("prediction/models/ohe.pkl", "rb"))
# scaler = pickle.load(open("prediction/models/scalar.pkl", "rb"))
# over_sample = pickle.load(open("prediction/models/over_sampling.pkl", "rb"))

# Load the saved model, encoder, and scaler
with open("prediction/models/mlp_model.pkl", 'rb') as file:
    loaded_model = pickle.load(file)

with open("prediction/models/encoder.pkl", 'rb') as file:
    loaded_encoder = pickle.load(file)

with open("prediction/models/scaler.pkl", 'rb') as file:
    loaded_scaler = pickle.load(file)

    
def home(request):
    # Clear any existing quiz session data when returning to home
    if 'logical_quotient_rating' in request.session:
        del request.session['logical_quotient_rating']
    if 'quiz_taken' in request.session:
        del request.session['quiz_taken']
    return render(request, 'index.html')

# Machine learning
# def prediction(request):
#     result = ''
#     show_data = {}
#     roadmap = None
#     if request.method == 'POST':
#         # Get values from the form (ensure these match your HTML form)
#         logical_quotient_rating = request.POST.get('logical_quotient_rating')
#         hackathons = request.POST.get('hackathons')
#         coding_skills = request.POST.get('coding_skills')
#         public_speaking_points = request.POST.get('public_speaking_points')
#         self_learning_capability = request.POST.get('self_learning_capability')
#         extra_courses_did = request.POST.get('extra_courses_did')
#         certifications = request.POST.get('certifications')
#         workshops = request.POST.get('workshops')
#         reading_and_writing_skills = request.POST.get('reading_and_writing_skills')
#         memory_capability_score = request.POST.get('memory_capability_score')
#         interested_subjects = request.POST.get('interested_subjects')
#         interested_career_area = request.POST.get('interested_career_area')
#         company_settle_in = request.POST.get('Type_of_company_want_to_settle_in')
#         book_interest = request.POST.get('Type_of_book')  # Corrected name
#         management_or_technical = request.POST.get('mangement_technical')  # Corrected name
#         hard_smart_work = request.POST.get('worker')  # Corrected name
#         worked_in_teams = request.POST.get('team')  # Corrected name
#         introvert = request.POST.get('introvert')  # Corrected name
        
#         # Prepare input data for prediction
#         input_data_dict = {
#             "Logical quotient rating": logical_quotient_rating,
#             "hackathons": hackathons,
#             "coding skills rating": coding_skills,
#             "public speaking points": public_speaking_points,
#             "self-learning capability?": self_learning_capability,
#             "Extra-courses did": extra_courses_did,
#             "certifications": certifications,
#             "workshops": workshops,
#             "reading and writing skills": reading_and_writing_skills,
#             "memory capability score": memory_capability_score,
#             "Interested subjects": interested_subjects,
#             "interested career area ": interested_career_area,
#             "Type of company want to settle in?": company_settle_in,
#             "Interested Type of Books": book_interest,
#             "Management or Technical": management_or_technical,
#             "hard/smart worker": hard_smart_work,
#             "worked in teams ever?": worked_in_teams,
#             "Introvert": introvert
#         }
        
#         input_df = pd.DataFrame([input_data_dict])
        
#         # Preprocess input data (use processor from your notebook)
#         input_processed = processor.transform(input_df)  # Ensure 'processor' is accessible

#         # Make prediction
#         prediction = model.predict(input_processed)
        
#         # Decode prediction back to original label
#         result = le.inverse_transform(prediction)[0]  # Get the predicted job role
        
#         # Fetch roadmap related to the predicted job role
#         roadmap = Roadmap.objects.filter(title__icontains=result).first()

#         show_data = {
#             "logical": logical_quotient_rating,
#             "hackathon": hackathons,
#             "coding": coding_skills,
#             "public": public_speaking_points,
#             "self-learning capability?": self_learning_capability,
#             "Extra-courses did": extra_courses_did,
#             "certifications": certifications,
#             "workshops": workshops,
#             "reading and writing skills": reading_and_writing_skills,
#             "memory capability score": memory_capability_score,
#             "Interested subjects": interested_subjects,
#             "interested career area": interested_career_area,
#             "Type of company want to settle in?": company_settle_in,
#             "Interested Type of Books": book_interest,
#             "Management or Technical": management_or_technical,
#             "hard/smart worker": hard_smart_work,
#             "worked in teams ever?": worked_in_teams,
#             "Introvert": introvert,
#             'result':result,
#             'roadmap': roadmap,
#         }
#     return render(request,'prediction.html',show_data)


# Deep Learning Prediction Function
def prediction(request): 
    result = ''
    show_data = {}
    roadmap = None

    # Retrieve the logical quotient rating from session
    # score = request.session.get('logical_quotient_rating', None)
    # # If the page is accessed without taking the quiz, reset the score
    # if not request.session.get('quiz_taken', False):
    #     score = None
    
    if request.session.get('quiz_taken', False):
        score = request.session.get('logical_quotient_rating', None)
    else:
        score = None

    show_data = {
        "logical_quotient_rating": score,  # Show score on prediction page immediately
        "result": result,
        "roadmap": roadmap
    }
    
    if request.method == 'POST':
        if not request.session.get('quiz_taken', False):
            # If quiz hasn't been taken, redirect to quiz page
            return redirect('quiz')
        # logical_quotient_rating = request.session.get('logical_quotient_rating', 0)

        input_data_dict = {
            "Logical quotient rating": [score],
            "hackathons": [int(request.POST.get('hackathons', "0"))],
            "coding skills rating": [int(request.POST.get('coding_skills', "0"))],
            "public speaking points": [int(request.POST.get('public_speaking_points', "0"))],
            "certifications": [request.POST.get('certifications', "Unknown")],
            "workshops": [request.POST.get('workshops', "Unknown")],
            "Interested subjects": [request.POST.get('interested_subjects', "Unknown")],
            "interested career area ": [request.POST.get('interested_career_area', "Unknown")],
            "Type of company want to settle in?": [request.POST.get('Type_of_company_want_to_settle_in', "Unknown")],
            "Management or Technical": [request.POST.get('management_technical', "Unknown")],
            "worked in teams ever?": [request.POST.get('team', "No")],
            "Introvert": [request.POST.get('introvert', "No")]
        }

        input_df = pd.DataFrame.from_dict(input_data_dict)
        input_df = input_df.astype(str)

        new_data_encoded = loaded_encoder.transform(input_df)
        new_data_scaled = loaded_scaler.transform(new_data_encoded)

        prediction = loaded_model.predict(new_data_scaled)
        result = prediction[0]

           
        
        job_roles = {
            'CRM/Managerial Roles': ['CRM Business Analyst', 'CRM Technical Developer', 'Project Manager', 'Information Technology Manager'],
            'Analyst': ['Business Systems Analyst', 'Business Intelligence Analyst', 'E-Commerce Analyst'],
            'Mobile Applications/ Web Development': ['Mobile Applications Developer', 'Web Developer', 'Applications Developer'],
            'QA/Testing': ['Software Quality Assurance (QA) / Testing', 'Quality Assurance Associate'],
            'UX/Design': ['UX Designer', 'Design & UX'],
            'Databases': ['Database Developer', 'Database Administrator', 'Database Manager', 'Portal Administrator'],
            'Programming/ Systems Analyst': ['Programmer Analyst', 'Systems Analyst'],
            'Networks/ Systems': ['Network Security Administrator', 'Network Security Engineer', 'Network Engineer', 'Systems Security Administrator', 'Software Systems Engineer', 'Information Security Analyst'],
            'SE/SDE': ['Software Engineer', 'Software Developer'],
            'Technical Support/Service': ['Technical Engineer', 'Technical Services/Help Desk/Tech Support', 'Technical Support'],
            'others': ['Solutions Architect', 'Data Architect', 'Information Technology Auditor']
        }

        suggested_roles = job_roles.get(result, ['Unknown'])
        
        
        show_data.update({
            "hackathons": request.POST.get('hackathons', "0"),
            "coding_skills_rating": request.POST.get('coding_skills', "0"),
            "public_speaking_points": request.POST.get('public_speaking_points', "0"),
            "certifications": request.POST.get('certifications', "Unknown"),
            "workshops": request.POST.get('workshops', "Unknown"),
            "interested_subjects": request.POST.get('interested_subjects', "Unknown"),
            "interested_career_area": request.POST.get('interested_career_area', "Unknown"),
            "Type_of_company_want_to_settle_in": request.POST.get('Type_of_company_want_to_settle_in', "Unknown"),
            "management_technical": request.POST.get('management_technical', "Unknown"),
            "team": request.POST.get('team', "No"),
            "introvert": request.POST.get('introvert', "No"),
            'score': score,
            'result': result,
            'roadmap': roadmap,
            'suggested_roles': suggested_roles,
            'logical_quotient_rating': score  # Make sure to include this in the updated data
        })
        
        # Store the prediction result in session
        request.session['predicted_role'] = result
        
        return redirect('job')
        

    return render(request, 'prediction.html', show_data)


# Add these imports at the top
import requests
from datetime import datetime
import os
from django.core.cache import cache

def fetch_jobs_from_adzuna(job_category, num_jobs=5):
    """Fetch jobs from Adzuna API with improved category mapping and error handling"""
    # Map the predicted role categories to relevant job search terms
    job_search_mapping = {
        'CRM/Managerial Roles': 'CRM Manager OR Project Manager',
        'Analyst': 'Business Analyst OR Data Analyst',
        'Mobile Applications/ Web Development': 'Web Developer OR Mobile Developer',
        'QA/Testing': 'QA Engineer OR Software Tester',
        'UX/Design': 'UX Designer OR UI Designer',
        'Databases': 'Database Administrator OR Database Developer',
        'Programming/ Systems Analyst': 'Systems Analyst OR Programmer',
        'Networks/ Systems': 'Network Engineer OR Systems Administrator',
        'SE/SDE': 'Software Engineer OR Software Developer',
        'Technical Support/Service': 'Technical Support OR IT Support',
        'others': 'IT Professional'
    }

    # Get the appropriate search term
    search_term = job_search_mapping.get(job_category, job_category)
    
    # Cache key based on search term
    cache_key = f'jobs_{search_term}'
    
    # Try to get cached results first
    cached_results = cache.get(cache_key)
    if cached_results:
        return cached_results

    # Your Adzuna API credentials
    app_id = settings.ADZUNA_APP_ID
    app_key = settings.ADZUNA_APP_KEY
    
    # Base URL for Adzuna API
    base_url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    
    # Parameters for the API request
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': num_jobs,
        'what': search_term,
        'content-type': 'application/json',
        'sort_by': 'date',
        'max_days_old': 30  # Only show jobs posted in last 30 days
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)  # Add timeout
        response.raise_for_status()
        data = response.json()
        
        # Process and format the job listings
        jobs = []
        for job in data.get('results', [])[:num_jobs]:
            # Format the date
            created_at = datetime.strptime(job['created'], "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = created_at.strftime("%B %d, %Y")
            
            # Clean and truncate description
            description = job.get('description', 'No description available')
            if len(description) > 300:
                description = description[:300] + '...'
            
            # Format salary
            salary_min = job.get('salary_min')
            salary_max = job.get('salary_max')
            if salary_min and salary_max:
                salary = f"₹{salary_min/100000:.1f}L - ₹{salary_max/100000:.1f}L"
            elif salary_max:
                salary = f"Up to ₹{salary_max/100000:.1f}L"
            else:
                salary = "Salary not specified"
            
            jobs.append({
                'title': job.get('title'),
                'company': job.get('company', {}).get('display_name', 'Company not specified'),
                'location': job.get('location', {}).get('display_name', 'Location not specified'),
                'description': description,
                'salary': salary,
                'url': job.get('redirect_url'),
                'posted_date': formatted_date
            })
        
        # Cache the results for 1 hour (3600 seconds)
        cache.set(cache_key, jobs, 3600)
        
        return jobs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {str(e)}")
        # Return empty list in case of error
        return []




def job_view(request):
    # Get the prediction result from session
    result = request.session.get('predicted_role', None)
    
    
    # If there's no prediction result, redirect to prediction page
    if result is None:
        return redirect('prediction')
    
    roadmap = Roadmap.objects.filter(title__icontains=result).first()
    
    CRM_Managerial_Roles = ['CRM Business Analyst','CRM Technical Developer','Project Manager','Information Technology Manager']
    Analyst = ['Business Systems Analyst','Business Intelligence Analyst','E-Commerce Analyst']
    Mobile_Applications_Web_Development = ['Mobile Applications Developer','Web Developer','Applications Developer']
    QA_Testing = ['Software Quality Assurance (QA) / Testing','Quality Assurance Associate']
    UX_Design = ['UX Designer','Design & UX']
    Databases = ['Database Developer','Database Administrator','Database Manager','Portal Administrator']
    Programming_Systems_Analyst = ['Programmer Analyst','Systems Analyst']
    Networks_Systems = ['Network Security Administrator','Network Security Engineer','Network Engineer', 'Systems Security Administrator','Software Systems Engineer','Information Security Analyst']
    SE_SDE = ['Software Engineer','Software Developer']
    Technical_Support_Service = ['Technical Engineer','Technical Services/Help Desk/Tech Support','Technical Support']
    others = ['Solutions Architect','Data Architect','Information Technology Auditor']
        
    if result == 'CRM/Managerial Roles':
        cat=CRM_Managerial_Roles
    elif result == 'Analyst':
        cat=Analyst
    elif result == 'Mobile Applications/ Web Development':
        cat=Mobile_Applications_Web_Development
    elif result == 'QA/Testing':
        cat=QA_Testing
    elif result == 'UX/Design':
        cat=UX_Design
    elif result == 'Databases':
        cat=Databases
    elif result == 'Programming/ Systems Analyst':
        cat=Programming_Systems_Analyst
    elif result == 'Networks/ Systems':
        cat=Networks_Systems
    elif result == 'SE/SDE':
        cat=SE_SDE
    elif result == 'Technical Support/Service':
        cat=Technical_Support_Service
    else:
        cat=others
    
    # Fetch job listings with error handling
    try:
        job_listings = fetch_jobs_from_adzuna(result)
    except Exception as e:
        print(f"Error in job_view: {str(e)}")
        job_listings = []
    
    context = {
        'result': result,
        'roadmap': roadmap,
        'cat': cat,  # Make sure 'cat' is defined in your view
        'job_listings': job_listings
    }
        
    return render(request, 'job.html', context)

def roadmap(request):
    roadmaps = Roadmap.objects.all()
    return render(request, 'roadmap.html', {'roadmaps': roadmaps})



def quiz_view(request):
    if 'logical_quotient_rating' in request.session:
        del request.session['logical_quotient_rating']
    if 'quiz_taken' in request.session:
        del request.session['quiz_taken']
    questions = Question.objects.all()
    # score = request.session.get('logical_quotient_rating', None)  # Retrieve score from session
    return render(request, 'quiz.html', {'questions': questions})

# def submit_quiz(request):
#     if request.method == 'POST':
#         score = 0
#         total_questions = 0

#         for question_id, choice_id in request.POST.items():
#             if question_id.startswith('question_'):
#                 total_questions += 1
#                 if Choice.objects.get(pk=choice_id).is_correct:
#                     score += 1

#         # Store score in session
#         request.session['logical_quotient_rating'] = score
#         request.session.modified = True  # ✅ Ensure the session is saved

#         return redirect('prediction')  # Redirect to prediction page
 

def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        for question_id, choice_id in request.POST.items():
            if question_id.startswith('question_'):
                if Choice.objects.get(pk=choice_id).is_correct:
                    score += 1

        # Store score and quiz completion status in session
        request.session['logical_quotient_rating'] = score
        request.session['quiz_taken'] = True
        
        return redirect('prediction')


