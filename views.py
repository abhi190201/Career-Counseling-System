import re
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.views import LoginView
from .forms import ProfileUpdateForm
from .forms import (
    CustomUserCreationForm,
    LoginForm as CustomLoginForm,
    ProfileForm,
    CustomPasswordChangeForm
)

from django.contrib.auth.forms import PasswordChangeForm
from .models import DomainQuestion, InterestQuestion
import random

from .models import InterestQuestion
from collections import Counter
from .models import InterestResult
from career.models import Domain
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import DomainQuestion  # ✅ Actual model name

CustomUser = get_user_model()

# -------------------------
# Custom Password Validator
# -------------------------
def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one uppercase letter.')
    if not re.search(r'[0-9]', password):
        errors.append('Password must contain at least one number.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Password must contain at least one special character.')
    if errors:
        raise ValidationError(errors)
    return password

# -------------------------
# Signup View
# -------------------------
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction

@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user object and get the user instance
            user = form.save()

            # Explicitly set the backend for the login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            messages.success(request, 'Signup successful. You are now logged in.')
            return redirect('dashboard')  # Redirect to the desired page after login

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

# -------------------------
# Login View
# -------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, '⚠️ Invalid username or password.')
            return render(request, 'login.html', {'form': CustomLoginForm()})

    return render(request, 'login.html', {'form': CustomLoginForm()})

# -------------------------
# Logout View
# -------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# -------------------------
# Terms View
# -------------------------
def terms_view(request):
    return render(request, 'terms.html')

# -------------------------
# Dashboard View
# -------------------------
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# -------------------------
# Profile View
# -------------------------

@login_required
def profile_view(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            user = form.save(commit=False)

            # Handle "Other" stream case
            selected_stream = request.POST.get('graduation_stream')
            other_stream = request.POST.get('other_graduation_stream')
            if selected_stream == "Other" and other_stream:
                user.graduation_stream = other_stream
            else:
                user.graduation_stream = selected_stream

            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)



# -------------------------
# Section Views (Dynamic Rendering)
# -------------------------
allowed_sections = {'domains', 'assessment', 'result', 'roadmap', 'courses', 'progress'}

def render_section(section_name):
    @login_required
    def view(request):
        if section_name not in allowed_sections:
            return redirect('dashboard')
        return render(request, f'{section_name}.html')
    return view


# Assign dynamic views for sections
domains_view = render_section('domains')
assessment_view = render_section('assessment')
result_view = render_section('result')

@login_required
def interest_result_page(request):
    top_domains = request.session.get('top_domains', [])
    return render(request, 'interest_result.html', {'top_domains': top_domains})









from .models import DomainTestResult, Roadmap

@login_required
def roadmap_view(request, domain_id=None):
    user = request.user

    # If this is called with domain_id, generate & save new roadmap
    if domain_id:
        try:
            test_result = DomainTestResult.objects.get(user=user, domain__DomainID=domain_id)
        except DomainTestResult.DoesNotExist:
            messages.error(request, "No test result for selected domain.")
            return redirect('domain_result_history')

        domain = test_result.domain
        score = test_result.score

        # Determine roadmap level
        # Determine roadmap level
        if user.tenth_percentage and user.twelfth_percentage:
            if user.tenth_percentage >= 60 and user.twelfth_percentage >= 60:
                level = 'expert'
            else:
                level = 'begining'
        else:
            if score > 60:
                level = 'intermediate'
            elif score < 40:
                level = 'begining'
            else:
                level = 'intermediate'  # Or set another fallback

        # Save or update roadmap
        roadmap, created = Roadmap.objects.update_or_create(
            user=user,
            defaults={'domain': domain, 'level': level}
        )

        # Load template based on selected domain & level
        template_path = f"Domains/{domain.DomainName}/{level}.html"
        return render(request, template_path, {'domain_name': domain.DomainName, 'level': level})

    # If no domain_id, just show existing roadmap if exists
    try:
        roadmap = Roadmap.objects.get(user=user)
        template_path = f"Domains/{roadmap.domain.DomainName}/{roadmap.level}.html"
        return render(request, template_path, {
            'domain_name': roadmap.domain.DomainName,
            'level': roadmap.level
        })
    except Roadmap.DoesNotExist:
        return redirect('domain_result_history')


from .models import Course
from django.db.models import Count

@login_required
def courses_view(request):
    # Fetch all courses grouped by domain
    courses = Course.objects.all().order_by('domain', 'title')

    # Group them into a dict { domain: [course, course] }
    domains = {}
    for course in courses:
        domains.setdefault(course.domain, []).append(course)

    return render(request, 'courses.html', {'domains': domains})


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile

@login_required
def progress_view(request):
    profile = UserProfile.objects.get(user=request.user)

    roadmap_done = Roadmap.objects.filter(user=request.user).exists()
    domain_test_done = DomainTestResult.objects.filter(user=request.user).exists()

    context = {
        "profile_complete": profile.is_complete(),
        "test_done": request.user.interestresult_set.exists(),
        "roadmap_done": roadmap_done,
        "domain_test_done": domain_test_done,
    }
    return render(request, "progress.html", context)


# -------------------------
# Default Home Redirect
# -------------------------
def home_view(request):
    return redirect('login')


 
# -------------------------
# test_view
# -------------------------




from django.shortcuts import render, get_object_or_404
from .models import Domain, DomainQuestion
@login_required
def start_test(request, domain_id):
    domain = get_object_or_404(Domain, DomainID=domain_id)

    if 'domain_test_questions' in request.session and request.session.get('domain_test_domain') == domain_id:
        # Reuse questions if already stored for this domain
        question_ids = request.session['domain_test_questions']
        questions = list(DomainQuestion.objects.filter(DomainQuestionID__in=question_ids))
    else:
        # Randomize and store in session
        all_questions = DomainQuestion.objects.filter(Domain=domain)
        questions = random.sample(list(all_questions), min(50, len(all_questions)))

        request.session['domain_test_questions'] = [q.DomainQuestionID for q in questions]
        request.session['domain_test_domain'] = domain_id
        request.session.modified = True

    return render(request, 'domain_test.html', {
        'domain': domain,
        'questions': questions,
    })

@csrf_exempt
@login_required
def submit_test(request, domain_id):
    domain = get_object_or_404(Domain, DomainID=domain_id)
    question_ids = request.session.get('domain_test_questions', [])
    questions = DomainQuestion.objects.filter(DomainQuestionID__in=question_ids)

    try:
        user_answers = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    graded = []
    score = 0

    for question in questions:
        qid = str(question.DomainQuestionID)
        selected = user_answers.get(qid)
        correct = question.CorrectAnswer

        is_correct = (selected == correct)
        if is_correct:
            score += 2

        graded.append({
            "id": qid,
            "text": question.QuestionText,
            "options": {
                "A": question.OptionA,
                "B": question.OptionB,
                "C": question.OptionC,
                "D": question.OptionD,
         },
         "selected": selected,
         "correct": correct,
         "explanation": question.Explanation,
         "is_correct": is_correct,
         })


    # ✅ DELETE existing result if any
    from .models import DomainTestResult
    DomainTestResult.objects.filter(user=request.user, domain=domain).delete()

    # ✅ Save new result
    DomainTestResult.objects.create(
        user=request.user,
        domain=domain,
        score=score
    )

    request.session['graded_result'] = graded
    request.session['domain_test_score'] = score
    request.session['domain_test_domain'] = domain_id

    return JsonResponse({
        "status": "success",
        "redirect_url": f"/domain-result/{domain_id}/"
    })


@login_required
def domain_result_view(request, domain_id):
    domain = get_object_or_404(Domain, DomainID=domain_id)
    graded = request.session.get('graded_result', [])
    score = request.session.get('domain_test_score', 0)

    return render(request, 'domain_result.html', {
        'domain': domain,
        'score': score,
        'graded': graded,
    })


from .models import InterestQuestion, InterestOption
@login_required
def interest_questions_view(request):
    # Prefetch options related to each question to avoid multiple queries
    questions = InterestQuestion.objects.order_by('?')[:25]  # Random order and limit to 25

    return render(request, 'interest_questions.html', {'questions': questions})





@csrf_exempt
@login_required
def save_interest_answer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            q_id = data.get("question_id")
            answer = data.get("answer")

            # Save logic here - example:
            # question = InterestQuestion.objects.get(id=q_id)
            # response = InterestAnswer.objects.update_or_create(user=request.user, question=question, defaults={"answer": answer})

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import InterestOption, InterestResult, Domain
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
@login_required
def submit_interest_test(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            answers = data.get("answers", {})

            # Tally scores per domain
            domain_scores = {}
            for qid_str, option_label in answers.items():
                try:
                    question_id = int(qid_str)
                    option = InterestOption.objects.get(
                        question_id=question_id,
                        option_label=option_label.upper()
                    )
                    if option.domain:
                        domain_id = str(option.domain.DomainID)  # JSONField stores keys as strings
                        domain_scores[domain_id] = domain_scores.get(domain_id, 0) + 1
                except (InterestOption.DoesNotExist, ValueError):
                    continue

            # Save to InterestResult
            InterestResult.objects.update_or_create(
                user=request.user,
                defaults={'recommended_domains': list(map(int, domain_scores.keys()))}
            )

            # Save to session for later access
            request.session['user_answers'] = answers
            request.session['top_domains'] = list(map(int, domain_scores.keys()))

            return JsonResponse({"status": "success", "redirect_url": "/interest-result/"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


from .models import DomainTestResult

@login_required
def domain_result_history_view(request):
    results = DomainTestResult.objects.filter(user=request.user).select_related('domain').order_by('-submitted_at')
    return render(request, 'domain_result_history.html', {'results': results})




@login_required
def interest_result_view(request):
    top_domain_ids = request.session.get('top_domains', [])

    if not top_domain_ids:
        # Fallback: Get random domains if none from session
        top_domain_ids = list(Domain.objects.order_by('?')[:5].values_list('DomainID', flat=True))

    # Save or update InterestResult for user
    InterestResult.objects.update_or_create(
        user=request.user,
        defaults={'recommended_domains': top_domain_ids}
    )

    domains = Domain.objects.filter(DomainID__in=top_domain_ids)
    return render(request, 'interest_result.html', {'domains': domains})

    
@login_required
def domain_test_view(request, domain_id):
    domain = get_object_or_404(Domain, DomainID=domain_id)

    # Any additional logic to fetch questions related to the domain, if needed
    return render(request, 'domain_test.html', {'domain': domain})


@login_required
def domain_list_view(request):
    domains = Domain.objects.all()
    return render(request, 'domain_list.html', {'domains': domains})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Progress
import json

@login_required
def progress_view(request):
    progress, _ = Progress.objects.get_or_create(user=request.user)

    done_count = sum([
        progress.profile_complete,
        progress.test_complete,
        progress.roadmap_complete,
        progress.courses_complete,
        progress.domain_complete,
    ])

    context = {
        'progress': progress,
        'done_count': done_count
    }
    return render(request, 'progress.html', context)

@csrf_exempt
@login_required
def update_progress_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = data.get('task')
        progress, _ = Progress.objects.get_or_create(user=request.user)

        if task == 'profile':
            progress.profile_complete = True
        elif task == 'test':
            progress.test_complete = True
        elif task == 'roadmap':
            progress.roadmap_complete = True
        elif task == 'courses':
            progress.courses_complete = True
        progress.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
@csrf_exempt
def reset_progress_view(request):
    if request.method == "POST":
        progress, _ = Progress.objects.get_or_create(user=request.user)
        progress.profile_complete = False
        progress.test_complete = False
        progress.roadmap_complete = False
        progress.courses_complete = False
        progress.domain_complete = False
        progress.save()
        return JsonResponse({'status': 'reset'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
