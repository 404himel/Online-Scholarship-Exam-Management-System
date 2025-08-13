from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Delete
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from result.models import result 
from notice.models import Notice 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from Test.models import Quiz, Question, Choice

User = get_user_model()
# Admin Login View
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_admin_dashboard')  # ✅ Custom panel
        else:
            messages.error(request, 'Invalid admin credentials.')

    return render(request, 'admin_login.html')


# ✅ Only allow staff/admin users to see the dashboard
@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_admin_dashboard(request):
    return render(request, 'custom_admin_dashboard.html')




@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all()

    # Add user
    if request.method == "POST" and "add_user" in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f"User {new_user.username} created successfully!")
        return redirect('manage_users')

    # Update user
    if request.method == "POST" and "update_user" in request.POST:
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user = get_object_or_404(User, id=user_id)

        # Update username & email
        if username:
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                messages.error(request, "Username already exists.")
                return redirect('manage_users')
            user.username = username

        if email:
            user.email = email

        # Update password if provided
        if password:
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('manage_users')
            user.set_password(password)

        user.save()
        messages.success(request, f"User {user.username} updated successfully!")
        return redirect('manage_users')

    return render(request, 'manage_users.html', {"users": users})



@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user == user:
        messages.error(request, "You cannot delete your own admin account.")
    else:
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully.")

    return redirect('manage_users')

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_results(request):
    sort_order = request.GET.get('sort', 'desc')
    school_filter = request.POST.get('school') if request.method == "POST" and "filter_results" in request.POST else None

    results = result.objects.all()

    if school_filter:
        results = results.filter(school__iexact=school_filter)

    results = results.order_by('umark' if sort_order == 'asc' else '-umark')

    # ✅ Handle adding new result
    if request.method == "POST" and "add_result" in request.POST:
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        school = request.POST.get('school')
        umark = request.POST.get('umark')

        if result.objects.filter(uid=uid).exists():
            messages.error(request, "UID already exists.")
        else:
            result.objects.create(uid=uid, name=name, school=school, umark=umark)
            messages.success(request, f"Result for {name} added successfully.")
            return redirect('manage_results')

    return render(request, 'manage_results.html', {'results': results})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_result(request, result_id):
    res = get_object_or_404(result, id=result_id)
    res.delete()
    messages.success(request, f"Result for {res.name} deleted successfully.")
    return redirect('manage_results')



@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_notices(request):
    notices = Notice.objects.all()

    # ✅ Handle new notice submission
    if request.method == "POST" and "add_notice" in request.POST:
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Notice.objects.create(title=title, content=content, admin_id=request.user.id)
            messages.success(request, "Notice added successfully.")
            return redirect('manage_notices')
        else:
            messages.error(request, "Title and content are required.")

    return render(request, 'manage_notices.html', {'notices': notices})

# ✅ Delete a notice
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    messages.success(request, "Notice deleted successfully.")
    return redirect('manage_notices')

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            notice.title = title
            notice.content = content
            notice.save()
            messages.success(request, "Notice updated successfully.")
            return redirect('manage_notices')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'edit_notice.html', {'notice': notice})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_result(request, result_id):
    res = get_object_or_404(result, id=result_id)

    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        school = request.POST.get('school')
        umark = request.POST.get('umark')

        if uid and name and school and umark:
            res.uid = uid
            res.name = name
            res.school = school
            res.umark = umark
            res.save()
            messages.success(request, "Result updated successfully.")
            return redirect('manage_results')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'edit_result.html', {'res': res})


from Test.models import ExamSetting as Test_examsetting  # your model for exam start time
from django.utils.dateparse import parse_datetime

# your_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse

# --- Timezone related imports ---
from django.utils import timezone
from datetime import datetime

# --- Make sure you import all your models ---
# NOTE: I am using 'ExamSetting'. Please ensure this matches your models.py file.
# If your model is named 'Test_examsetting', change 'ExamSetting' back to that everywhere in this file.
from Test.models import ExamSetting


@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_quiz_questions(request):
    quizzes = Quiz.objects.all()
    selected_quiz = None
    questions = []

    # Get or create the exam setting object. This is a robust way to handle
    # a single settings object for the entire site. It will get the object
    # with id=1, or create it if it doesn't exist yet.
    exam_setting, created = ExamSetting.objects.get_or_create(id=1)

    # Handle GET request for selecting a quiz to view
    quiz_id_get = request.GET.get('quiz')
    if quiz_id_get:
        selected_quiz = get_object_or_404(Quiz, id=quiz_id_get)
        questions = Question.objects.filter(quiz=selected_quiz)
    elif quizzes.exists():
        # Default to the first quiz if none is selected
        selected_quiz = quizzes.first()
        questions = Question.objects.filter(quiz=selected_quiz)

    # Handle all POST requests (form submissions)
    if request.method == "POST":

        # --- ACTION: Update Exam Start Time ---
        if 'update_exam_time' in request.POST:
            time_str = request.POST.get("start_time")
            if time_str:
                try:
                    # 1. Parse the naive datetime string from the form
                    naive_dt = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
                    
                    # 2. Make it timezone-aware using your project's TIME_ZONE from settings.py
                    aware_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
                    
                    # 3. Save it. Django handles the conversion to UTC for storage.
                    exam_setting.start_time = aware_dt
                    exam_setting.save()
                    
                    messages.success(request, "Exam start time updated successfully!")
                except ValueError:
                    messages.error(request, "Invalid date format submitted.")
            else:
                messages.error(request, "Please select a valid date and time.")
            
            # Redirect to avoid form re-submission on refresh
            return redirect(request.path_info)

        # --- ACTION: Add New Quiz ---
        elif 'add_quiz' in request.POST:
            quiz_title = request.POST.get('quiz_title')
            if quiz_title:
                new_quiz = Quiz.objects.create(title=quiz_title)
                messages.success(request, f'Quiz "{quiz_title}" added successfully.')
                return redirect(f"{request.path_info}?quiz={new_quiz.id}")
            else:
                messages.error(request, "Quiz title cannot be empty.")

        # --- ACTION: Delete Quiz ---
        elif 'delete_quiz' in request.POST:
            quiz_id_to_delete = request.POST.get('quiz_id_to_delete')
            quiz_to_delete = get_object_or_404(Quiz, id=quiz_id_to_delete)
            quiz_title = quiz_to_delete.title
            quiz_to_delete.delete()
            messages.success(request, f'Quiz "{quiz_title}" deleted successfully.')
            return redirect(request.path_info)

        # --- ACTION: Add Question ---
        elif 'add_question' in request.POST:
            quiz_id = request.POST.get('quiz_id')
            question_text = request.POST.get('question_text')
            
            # Ensure quiz_id and question_text are provided
            if quiz_id and question_text:
                selected_quiz_for_add = get_object_or_404(Quiz, id=quiz_id)
                question = Question.objects.create(quiz=selected_quiz_for_add, text=question_text)
                
                choice_texts = request.POST.getlist('choice_text')
                # The 'value' of the selected checkbox/radio button for the correct answer
                correct_choice_index = request.POST.get('is_correct')

                for i, text in enumerate(choice_texts):
                    # Only create choice if text is not empty
                    if text:
                        # Check if the current choice's index matches the submitted correct index
                        is_correct = (str(i) == correct_choice_index)
                        Choice.objects.create(question=question, text=text, is_correct=is_correct)

                messages.success(request, "Question added successfully.")
                return redirect(f"{request.path_info}?quiz={quiz_id}")
            else:
                messages.error(request, "Cannot add question. Ensure a quiz is selected and question text is provided.")

    # Prepare context for rendering the template
    context = {
        'quizzes': quizzes,
        'selected_quiz': selected_quiz,
        'questions': questions,
        'exam_setting': exam_setting
    }
    # For a GET request or if a POST action fails validation, render the page
    return render(request, 'manage_quiz_questions.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect(f"/admin/manage-quiz-questions/?quiz={quiz_id}")


from django import forms

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

@login_required
def add_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz added successfully.")
            return redirect('manage_quiz_questions')
    else:
        form = QuizForm()
    
    return render(request, 'add_quiz.html', {'form': form})

from Study_Resources.models import Resource
from Admin.form import ResourceForm

# Only allow staff users (admins)
def is_admin(user):
    return user.is_staff
@login_required
@user_passes_test(is_admin)
def manage_resource(request):
    resources = Resource.objects.all().order_by('-uploaded_at')

    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_resource')
    else:
        form = ResourceForm()

    return render(request, 'manage_resource.html', {
        'resources': resources,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.delete()
    return redirect('manage_resource')