from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import MeditationForm, NotesForm
from .models import Meditation, User, Notes


# Create your views here.

class CustomLoginView(LoginView):  # Definim clasa corect
    template_name = 'meditatii/login.html'

    def get_success_url(self):
        return 'meditatii/meditations/'


@login_required
def student_details(request, username):
    if request.user.user_type != 'teacher':
        return redirect('home')

    try:
        student = User.objects.get(username=username, user_type='student')
        meditations = Meditation.objects.filter(student=student, teacher=request.user)

        total_meditations = meditations.count()
        paid_meditations = meditations.filter(payment_status='paid').count()
        total_amount = sum(med.payment_amount for med in meditations)
        paid_amount = sum(med.payment_amount for med in meditations.filter(payment_status='paid'))

        context = {
            'student': student,
            'meditations': meditations,
            'total_meditations': total_meditations,
            'paid_meditations': paid_meditations,
            'total_amount': total_amount,
            'paid_amount': paid_amount,
        }

        return render(request, 'meditatii/student_details.html', context)

    except User.DoesNotExist:
        return redirect('meditation_list')

@login_required
def notite_details(request, id_notita):
    if request.user.user_type != 'student':
        return redirect('home')

    note = get_object_or_404(Notes, id=id_notita)

    if request.user != note.student:
        return redirect('student_dashboard')

    return render(request, 'meditatii/notite_details.html', context={'note': note})

@login_required
def mark_note_done(request, id_note):
    if request.user.user_type != 'student':
        return redirect('home')

    note = get_object_or_404(Notes, id=id_note)

    if request.user != note.student:
        return redirect('student_dashboard')

    note.note_type = 'done'
    note.save()
    return redirect('notite_details', id_note)

@login_required(login_url='/login')
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('login')

    meditations = Meditation.objects.filter(student=request.user)

    total_meditations = meditations.count()
    if total_meditations > 0:
        paid_meditations = meditations.filter(payment_status='paid').count()
        progress_percentage = (paid_meditations / total_meditations) * 100
    else:
        progress_percentage = 0

    recent_meditations = meditations.order_by('-date')[:10]

    notes_read = Notes.objects.filter(student=request.user).filter(note_type='done').order_by('-date')
    notes_unread = Notes.objects.filter(student=request.user).filter(note_type='notdone').order_by('-date')
    notes_readc = notes_read.count()
    notes_unreadc = notes_unread.count()

    context = {
        'meditations': recent_meditations,
        'progress_percentage': round(progress_percentage, 1),
        'notes_read': notes_read,
        'notes_unreadc': notes_unreadc,
        'notes_readc': notes_readc,
        'notes_unread': notes_unread,
        'total_meditations': total_meditations,
        'paid_meditations': paid_meditations if total_meditations > 0 else 0,
    }

    return render(request, 'meditatii/student_dashboard.html', context)


@login_required(login_url='/login')
def teacher_dashboard(request):
    if request.user.user_type != 'teacher':
        return redirect('login')

    # Get all meditations for this teacher
    meditations = Meditation.objects.filter(teacher=request.user)

    # Calculate payment statistics
    total_meditations = meditations.count()
    paid_meditations = meditations.filter(payment_status='paid').count()
    progress_percentage = (paid_meditations / total_meditations) * 100 if total_meditations > 0 else 0

    # Get unique students and their statistics
    students_data = {}
    for meditation in meditations:
        student = meditation.student
        if student.id not in students_data:
            students_data[student.id] = {
                'student': student,
                'meditation_count': 0,
                'paid_count': 0,
                'total_amount': 0,
                'paid_amount': 0
            }

        students_data[student.id]['meditation_count'] += 1
        students_data[student.id]['total_amount'] += meditation.payment_amount
        if meditation.payment_status == 'paid':
            students_data[student.id]['paid_count'] += 1
            students_data[student.id]['paid_amount'] += meditation.payment_amount

    # Process student payment status
    students = []
    for student_data in students_data.values():
        student = student_data['student']
        meditation_count = student_data['meditation_count']
        paid_count = student_data['paid_count']

        # Calculate payment status
        if paid_count == meditation_count:
            payment_status = 'all_paid'
            payment_status_display = 'Toate plătite'
        elif paid_count > 0:
            payment_status = 'partially_paid'
            payment_status_display = f'{paid_count}/{meditation_count} plătite'
        else:
            payment_status = 'unpaid'
            payment_status_display = 'Neplătit'

        students.append({
            'nume_real': student.nume_real,
            'email': student.email,
            'meditation_count': meditation_count,
            'payment_status': payment_status,
            'payment_status_display': payment_status_display,
            'total_amount': student_data['total_amount'],
            'paid_amount': student_data['paid_amount']
        })

    # Sort students by meditation count (descending)
    students.sort(key=lambda x: x['meditation_count'], reverse=True)

    context = {
        'total_meditations': total_meditations,
        'paid_meditations': paid_meditations,
        'progress_percentage': round(progress_percentage, 1),
        'students': students,
        'total_earnings': sum(student_data['total_amount'] for student_data in students_data.values()),
        'paid_earnings': sum(student_data['paid_amount'] for student_data in students_data.values())
    }

    return render(request, 'meditatii/teacher_dashboard.html', context)


# mediatii/views.py
@login_required
def mark_as_pending(request, meditation_id):
    meditation = get_object_or_404(Meditation, id=meditation_id, student=request.user)
    meditation.payment_status = 'pending'
    meditation.save()
    return redirect('meditation_list')


@login_required
def mark_as_paid(request, meditation_id):
    meditation = get_object_or_404(Meditation, id=meditation_id, teacher=request.user)
    meditation.payment_status = 'paid'
    meditation.save()
    return redirect('meditation_list')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/meditatii/')  # Sau folosește reverse('home')


@login_required(login_url='/login')
def meditation_list(request):
    if request.user.user_type == 'student':
        meditations = Meditation.objects.filter(student=request.user)
    else:
        meditations = Meditation.objects.filter(teacher=request.user)
    return render(request, 'meditatii/meditation_list.html', {'meditations': meditations})


# mediatii/views.py
def home(request):
    return render(request, 'meditatii/home.html')


@login_required(login_url='/login')
def meditation_create(request):
    if request.user.user_type != 'teacher':
        return redirect('meditation_list')

    meditation_form = MeditationForm()
    notes_form = NotesForm()

    if request.method == 'POST':
        if 'meditation_submit' in request.POST:
            meditation_form = MeditationForm(request.POST)
            if meditation_form.is_valid():
                meditation = meditation_form.save(commit=False)
                meditation.teacher = request.user
                meditation.save()
                return redirect('meditation_list')
        elif 'notes_submit' in request.POST:
            notes_form = NotesForm(request.POST)
            if notes_form.is_valid():
                note = notes_form.save(commit=False)
                note.teacher = request.user
                note.note_type = 'notdone'
                note.save()
                return redirect('meditation_list')

    context = {
        'meditation_form': meditation_form,
        'notes_form': notes_form,
    }

    return render(request, 'meditatii/meditation_create.html', context)
