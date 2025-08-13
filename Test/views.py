import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Quiz, Question, Choice, StudentAnswer, ExamSetting


@login_required
def start_quiz(request):
    # Clear any previous result to avoid redirecting to result page
    request.session.pop('quiz_result', None)

    # Get the exam start time from admin settings
    exam_setting = ExamSetting.objects.first()
    if not exam_setting or not exam_setting.start_time:
        return render(request, "error.html", {"message": "Exam time has not been set by the admin."})

    now = timezone.now()

    # Debugging (optional)
    print(f"Current UTC Time: {now}")
    print(f"Exam Start Time (UTC): {exam_setting.start_time}")
    print(f"Exam Started?: {now >= exam_setting.start_time}")

    # If the exam hasn't started yet → show waiting page
    if now < exam_setting.start_time:
        return render(request, "waiting.html", {
            "exam_start_time": exam_setting.start_time
        })

    # Get all available questions
    all_questions = list(Question.objects.all())
    if not all_questions:
        return render(request, "error.html", {"message": "No questions are available for the quiz."})

    # Randomly select up to 5 questions
    selected_questions = random.sample(all_questions, min(5, len(all_questions)))

    # Store selected question IDs in session
    request.session['question_ids'] = [q.id for q in selected_questions]

    return render(request, 'quiz_page.html', {
        'questions': selected_questions,
    })


@login_required
def submit_quiz(request):
    if request.method == 'POST':
        question_ids = request.session.get('question_ids', [])
        if not question_ids:
            return redirect('start_quiz')

        questions = Question.objects.filter(id__in=question_ids)

        correct_count = 0
        total = len(question_ids)

        # Clear previous answers for this user & quiz questions
        StudentAnswer.objects.filter(user=request.user, question__in=questions).delete()

        for question in questions:
            choice_id = request.POST.get(str(question.id))
            if choice_id:
                try:
                    selected_choice = Choice.objects.get(id=choice_id, question=question)
                except Choice.DoesNotExist:
                    continue
                StudentAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice
                )
                if selected_choice.is_correct:
                    correct_count += 1

        # Save result in session
        request.session['quiz_result'] = {
            'score': int(correct_count / total * 100),
            'correct': correct_count,
            'total': total
        }
        return redirect('quiz_result')

    return redirect('start_quiz')


@login_required
def quiz_result(request):
    # Pop removes result after showing it once
    result = request.session.pop('quiz_result', None)
    if not result:
        return redirect('start_quiz')

    return render(request, 'quiz_result.html', result)
