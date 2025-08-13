from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Delete
from Test.models import StudentAnswer, Quiz

User = get_user_model()


from django.core.mail import send_mail
from django.conf import settings

def signuppage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        school = request.POST.get('school')
        contact = request.POST.get('contact')
        roll_no = request.POST.get('roll_no')  

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")

        my_user = User.objects.create_user(
            username=uname,
            email=email,
            password=pass1,
            first_name=first_name,
            last_name=last_name,
            school=school,    
            contact=contact,
            roll_no=roll_no
        )

        user_id = my_user.id  # Database ID

        # Send welcome email with the ID
        send_mail(
            subject="Welcome to Kazi Mofizul Islam Welfare Trust 🎉",
            message=(
                f"""
Welcome to our Website

Hello {first_name},

We’re thrilled to have you on our platform!  
Here, you can:

- View important notices  
- Download your admit card  
- Check results  
- Explore FAQs  
- Access study resources  
- See your performance analysis  
- Chat with our AI Study Assistant  

Your Unique ID is: {user_id}.

Please keep this ID safe — it will help you log in and access your exams.

We look forward to seeing you achieve great things!  


Best wishes,  
— The Exam Portal Team


"""

            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('login')

    return render(request, 'signup.html')

        
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')  

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

def homepage(request):
    return render(request, 'index.html')

def logoutPage(request):
    logout(request)
    return redirect('login')


def user_info(request):
    info = User.objects.all()

    return render(request, 'user_info.html',{'infos':info})


# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('home')  # Replace with your actual user dashboard route
        else:
            messages.error(request, 'Invalid user credentials.')
    
    return render(request, 'user_login.html')



@login_required
def student_dashboard(request):
    user = request.user

    if request.method == "POST":
        # Get the updated form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        user.first_name = first_name
        user.last_name = last_name
        
        if password:
            user.set_password(password)
        
        user.save()

        # Update contact if related model exists
        if hasattr(user, 'studentprofile'):
            user.studentprofile.contact = contact
            user.studentprofile.save()

        if password:
            messages.success(request, "Your password has been updated successfully. Please log in again.")
            return redirect('login')  

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('student_dashboard')  

    # GET: Prepare quiz results
    quizzes_taken_qs = Quiz.objects.filter(
        question__studentanswer__user=user
    ).distinct()

    quiz_results = []
    total_correct = 0
    total_questions = 0

    for quiz in quizzes_taken_qs:
        answers = StudentAnswer.objects.filter(user=user, question__quiz=quiz)
        quiz_total_questions = quiz.question_set.count()
        quiz_correct_answers = sum(1 for ans in answers if ans.selected_choice.is_correct)

        total_correct += quiz_correct_answers
        total_questions += quiz_total_questions

        score = int((quiz_correct_answers / quiz_total_questions) * 100) if quiz_total_questions > 0 else 0

        quiz_results.append({
            'title': quiz.title,
            'score': score,
            'correct': quiz_correct_answers,
            'total': quiz_total_questions,
        })

    avg_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
    quizzes_taken = quizzes_taken_qs.count()

    context = {
        'user': user,
        'quiz_results': quiz_results,
        'total_correct': total_correct,
        'total_questions': total_questions,
        'avg_score': avg_score,
        'quizzes_taken': quizzes_taken,
    }

    return render(request, 'student_dashboard.html', context)

def delete(request):
    
    deleted_users = Delete.objects.all().order_by('-id')
    
    # Default context - no deletion happened
    context = {
        'deleted_users': deleted_users,
        'deletion_successful': False
    }
    
    if request.method == 'POST' and request.POST.get("confirm_delete") == "yes":
        user_id = request.POST.get('user_id')
        
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Create the deleted user record
            deleted_user = Delete.objects.create(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                school=user.school,
                email=user.email,
            )
            
            # Delete the actual user
            user.delete()
            
            # Refresh the list after deletion
            deleted_users = Delete.objects.all().order_by('-id')
            
            # Update context to indicate successful deletion
            context['deleted_users'] = deleted_users
            context['deletion_successful'] = True
            
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')
    
    return render(request, 'delete.html', context)





