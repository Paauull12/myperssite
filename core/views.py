from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

# Create your views here.

def home(request):
    context = {
        'name': 'Paul Dobrescu'
    }

    return render(request, 'core/home.html', context=context)

def meditatiimock(request):

    return render(request, 'core/meditatii.html')


def contact(request):
    return render(request, 'core/contact.html')
def cvpage(request):
    context = {
        'name': 'Dobrescu Andrei Paul',
        'contact': {
            'location': 'Cluj-Napoca',
            'email': 'andrei.dobrescu@stud.ubbcluj.ro',
            'phone': '0770 512 879',
            'linkedin': 'Paul Dobrescu',
            'github': 'Paaull12'
        },
        'university': {
            'name': 'Universitatea Babeș-Bolyai',
            'location': 'Cluj-Napoca, Romania',
            'start_year': 2023,
            'end_year': 2026,
            'B_S': 'B.S. in Computer Science',
            'concentration': 'Computer Science',
            'coursework': [
                'Data Structures & Algorithms',
                'Operating systems',
                'Object-Oriented Programming',
                'Computer Systems Architecture'
            ]
        },
        'internships': [
            {
                'name': 'Luminess Groupe',
                'location': 'Romania',
                'position': 'Python Developer Intern',
                'start_date': 'July 2024',
                'end_date': 'Sept 2024',
                'points': [
                    'Designed and developed an internal tool from scratch to automate receipt processing for the accounting department, reducing manual effort and improving efficiency. The tool extracts total amounts from receipts with 92% accuracy in under 20 seconds.',
                    'Collaborated on over five personal and team-based projects, honing skills in web application development, OCR (Optical Character Recognition) optimization, and project management to ensure timely delivery of solutions.'
                ]
            },
            {
                'name': 'Part Time Tutor',
                'location': 'Romania',
                'position': 'Computer Science Tutor',
                'start_date': 'September 2021',
                'end_date': 'Present',
                'points': [
                    'Guided over 40 students to successfully pass the university admission exam for top Computer Science programs in Romania, achieving a 95% admission rate.',
                    'Own, develop, and manage grileinfo.ro, a website offering essential resources for exam preparation.'
                ]
            }
        ],
        'projects': [
            {
                'name': 'SysAdmin Automation Tool',
                'position': 'Main Developer',
                'date': 'July 2023 – September 2023',
                'points': [
                    'Developed a Dockerized credential management system for SysAdmins, incorporating image processing, authentication, and monitoring via Prometheus and Grafana.',
                    'Users upload(Angular UI) images via email, and Python services extract text (username and password), delivering it in text and MP3 format and storing in black-and-white(C++ service) in the DB(PostgreSQL and MinioS3).'
                ]
            },
            {
                'name': 'GitHub ShowCase App',
                'position': 'Main Developer',
                'date': 'June 2024 – July 2024',
                'points': [
                    'Built a web app using Django to showcase my CS50 repository, adaptable for any repository to display work to students and professors(learned how to implement recursive calls on a repository to retrieve data).',
                    'Currently used by 10+ students, the app handles user input via Django and integrates a custom API.'
                ]
            },
            {
                'name': 'Distributed Code Editor',
                'position': 'Main Developer',
                'date': 'February 2024 – March 2024',
                'points': [
                    'Developed a collaborative code editor supporting multi-language compilation (3+ languages), integrated AI-assisted code correction, and JWT-based authentication for enhanced security( real time communication through websockets).',
                    'This tool is meant to be used internally for better communication and faster problem solving between Jr and Sr developers. At this point the application has 17 services dockerized and can be initialized with one command using a PostgreSQL database.'
                ]
            }
        ],
        'activities': [
            {
                'name': 'Babes-Bolyai University',
                'position': 'Scrum master and Developer',
                'date': 'July 2024 - Present',
                'points': [
                    'Led a team of four to build software revolutionizing freelancing, managing development, and project communication.'
                ]
            },
            {
                'name': 'Competitive Programming',
                'date': 'Sept 2020 - Present',
                'points': [
                    'I attended many Olympiads representing my country, Romania. Recently, I participated in the CCC coding contest, ranking in the top 23% for the first time and in the top 11% among all attendees.'
                ]
            }
        ],
        'skills': {
            'programming': ['Python', 'JavaScript', 'HTML/CSS', 'Maple', 'C++', 'C', 'Typescript', 'Java'],
            'tools': ['Android Studio', 'IntelliJ', 'PyCharm', 'UiPath', 'Git', 'Django', 'GitHub', 'Angular', 'Flask', 'Docker'],
            'languages': ['English(C1 Cambridge Diploma)', 'Romanian(native speaker)', 'German(A1)']
        }
    }
    return render(request, 'core/cv.html', context)