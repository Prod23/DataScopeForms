from django.shortcuts import render, redirect
from .forms import RegisterForm, QuestionnaireForm, CoursesInformationForm
from .models import Questionnaire, CustomUser, CourseInformation
from django.contrib import messages
from django.contrib.auth import login
from .forms import QuestionnaireForm
from django.db.models import Sum, Count, F, Q, ExpressionWrapper, FloatField, IntegerField, Case, When
import csv
from django.http import HttpResponse
import pandas as pd



# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print("Hi")
        if form.is_valid():
            print("Hi")
            user = form.save()
            messages.success(
                request, "You can fill the form now")
            # Redirect to a page where the user can verify their email
            return redirect("submit-form", username=f"{user.college_name.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '').replace('-', '').replace(',', '')}_{user.university_name.replace(' ', '_').replace('.','')}")
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, "signup.html", context)


def signin_admin(request):
    if request.method == 'POST':
        university_name = request.POST['university_name'].replace(
            ' ', '').lower()
        college_name = request.POST['college_name'].replace(' ', '').lower()
        username = f"{college_name}_{university_name}"
        print(username)
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(
                request, f"{request.user.username}, Welcome Admin")
            return redirect("submit-form-admin", username=user.username)

        else:
            messages.warning(request, "Wrong Credentials")
            return redirect("signin_admin")

    return render(request, "login_admin.html")


def signin(request):
    if request.method == 'POST':
        university_name = request.POST['university_name']
        college_name = request.POST['college_name']
        college_name = college_name.replace(' ', '_').replace(':', '').replace(
            '(', '').replace(')', '').replace('-', '').replace(',', '')
        university_name = university_name.replace(' ', '_')
        username = f"{college_name}_{university_name.replace('.','')}"
        print(username)
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(
                request, f"{request.user.username}, start filling!")
            return redirect("submit-form", username=user.username)

        else:
            messages.warning(request, "College Doesn't Exist Register Again")
            return redirect("register")

    return render(request, "login.html")


def submit_form(request, username):
    user_instance = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form.instance.email = user_instance.email
            form.instance.college_type = user_instance.college_type
            form.instance.college_name = user_instance.college_name
            form.instance.university_name = user_instance.university_name
            form.save()
            return redirect("submit-form-course", username=username)
    else:
        form = QuestionnaireForm()

    context = {"form": form}
    return render(request, 'index.html', context)

def submit_form_course(request, username):
    user_instance = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        form = CoursesInformationForm(request.POST)
        if form.is_valid():
            form.instance.email = user_instance.email
            form.instance.college_type = user_instance.college_type
            form.instance.college_name = user_instance.college_name
            form.instance.university_name = user_instance.university_name
            form.save()
            return redirect('success_page_url')
    else:
        form = CoursesInformationForm()

    context = {"form": form}
    return render(request, 'course_info.html', context)


def submit_form_admin(request, username):
    user_instance = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form.instance.email = user_instance.email
            form.instance.college_type = user_instance.college_type
            form.instance.college_name = user_instance.college_name
            form.instance.university_name = user_instance.university_name
            form.save()
            # Redirect to a success page or another view
            return redirect("submit-form-course", username=username)
    else:
        form = QuestionnaireForm()

    context = {"form": form}
    return render(request, 'admin_page.html', context)


def success_page(request):
    return render(request, 'success.html')

def generate_data(request):
    # Fetch data from Questionnaire model
    data = Questionnaire.objects.all()
    
    # Create a HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="data.csv"'},
    )
    
    # Create a CSV writer object using the response as its "file"
    writer = csv.writer(response)
    
    # Writing the headers (assuming you have these fields in your model)
    writer.writerow([
        "Date", "Type", "College", "Email Address", "University",
        "No. of College with ICT", "ICT Facility",
        "Number of Computers in ICT Labs", "No. of Coll. with Housekeeping", "Housekeeping",
        "Total No. of Staffs in Housekeeping/Cleaning", "No. of College VC", "Video Conf.",
        "Number of Rooms with Video Conferencing Facility", "Biometric Attendance Facility Available",
        "No of College with Working Biometric", "Is Biometric Machine Working?",
        "No of Colleges Merged Accounts", "Have you merged all the saving accounts of your college?",
        "Total No. of Classrooms/Lecture Halls in your College", "Total No. of Lab Rooms",
        "Total No. of Library Rooms/Halls/Reading Rooms", "No. of Any Additional Rooms in College",
        "Total No. of Toilets for Male in College", "Total No. of Toilets for Female in College",
        "Does the College have any under-construction building, Total No of Under-construction buildings?",
        "Enrolled", "Present",
        "Percentage Present(%)", "Category", "Show-caused", "Dis-Enrolled", "Re-Enrolled",
        "Total Teacher", "Teacher Present", "Teacher on UnA Leave", "Teacher Salary on Hold",
        "Teacher Other Action", "Total Non-Teaching", "Non-Teaching Salary on Hold",
        "Non-Teaching Other Action", "Non-Teaching UnA", "Faculty >5", "Not >5 Faculty",
        "Faculty <3", "Action on Fac. <5", "Class Scheduled", "Class Held", "Lab Scheduled",
        "Lab Held", "No. of Inspection", "Inspection", "AISHE Completed",
        "Have you started process for filling AISHE 2022-2023 form?",
        "Voter Awareness Prog", "Has college conducted Voter Awareness Program today?",
        "The total number of students participated in Voter Awareness Program till date?",
        "College Occupation Status in case of Occupied for Election",
        "Reasons for Colleges Occupied in Election Purposes",
        "Has College Merged all the bank accounts into two accounts?",
        "How many bank accounts existed earlier in the College?",
        "How many bank accounts exists for College today?",
    ])
    
    # Writing data rows
    for row in data:
        writer.writerow([
            row.date,
            row.college_type,
            row.college_name,
            row.university_name,
            1 if row.ICT_facility else 0,
            row.ICT_facility,
            row.num_computers_in_ICT_labs,
            1 if row.housekeeping else 0,
            row.housekeeping,
            row.total_staffs_housekeeping,
            1 if row.video_conf else 0,
            row.video_conf,
            row.rooms_with_video_conf,
            row.biometric,
            1 if row.biometric_working else 0,
            row.biometric_working,
            1 if row.merged_savings_accounts else 0,
            row.merged_savings_accounts,
            row.classrooms,
            row.labrooms,
            row.library,
            row.additionalrooms,
            row.toilets_male,
            row.toilets_female,
            row.num_under_construction,
            row.enrolled,
            row.present,
            100*row.present/row.enrolled,
            'C' if 100*row.present/row.enrolled > 75 else (
                'B' if 100*row.present/row.enrolled > 50 else 'A'),
            row.showcaused,
            row.disenrolled,
            row.reenrolled,
            row.total_teacher,
            row.teacher_present,
            row.teacher_una_leave,
            row.teacher_salary_on_hold,
            row.teacher_other_action,
            row.non_teaching,
            row.non_teaching_salary_on_hold,
            row.non_teaching_una_leave,
            row.faculty_more_five,
            row.not_faculty_more_five,
            row.faculty_less_three,
            row.action_faculty_less_five,
            row.class_scheduled,
            row.class_held,
            row.lab_scheduled,
            row.lab_held,
            1 if row.inspection else 0,
            row.inspection,
            row.aishe,
            1 if row.voter_awareness else 0,
            row.voter_awareness,
            row.num_students_voter_awareness,
            row.college_occupation,
            row.reason_college_occupation,
            row.merged_accounts_two,
            row.num_bank_accounts_existed_earlier,
            row.num_bank_accounts_existed_today,
        ])
    
    return response

def generate_R1(request):
    user_date = request.GET.get('user_date')
    print(user_date)
    if user_date:
        filtered_data = Questionnaire.objects.filter(date=user_date)
        print('HI')
        grouped_data = filtered_data.values('college_type', 'university_name').annotate(
            colleges_filled=Count('university_name'),
            inspected_colleges=Sum(
                Case(
                    When(inspection=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            present_50=Sum(
                Case(
                    When(Q(present__lt=F('enrolled') * 0.5), then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            present_50_to_75=Sum(
                Case(
                    When(Q(present__gte=F('enrolled') * 0.5) &
                         Q(present__lt=F('enrolled') * 0.75), then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            present_75=Sum(
                Case(
                    When(Q(present__gte=F('enrolled') * 0.75), then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        # Format the filename using the user_date
        filename = f"R3{user_date}.csv"

        # Create a response object for delivering csv data.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'},
        )

        # Create a csv writer object and write the header
        writer = csv.writer(response)
        writer.writerow(['College Type', 'University Name',
                         'Colleges Filled',
                         'Colleges Inspected',
                         'Present less than 50%',
                         'Present between 50% and 75%',
                         'Present more than 75%',
                         ])

        # Write data rows
        for data in grouped_data:
            writer.writerow(
                [data['college_type'], data['university_name'], data['colleges_filled'], data['inspected_colleges'], data['present_50'], data['present_50_to_75'], data['present_75']])

        return response
    else:
        return HttpResponse("No valid date provided", status=400)


def generate_R3(request):
    user_date = request.GET.get('user_date')
    print(user_date)
    if user_date:
        filtered_data = Questionnaire.objects.filter(date=user_date)
        print('HI')
        grouped_data = filtered_data.values('college_type', 'university_name').annotate(
            colleges_filled=Count('university_name'),
            enrollment=Sum('enrolled'),
            present=Sum('present'),
            percent_present=ExpressionWrapper(
                F('present') * 100.0 / F('enrollment'),
                output_field=FloatField()
            ),
            showcaused=Sum('showcaused'),
            disenrolled=Sum('disenrolled'),
            reenrolled=Sum('reenrolled'),
            faculty_more_five=Sum('faculty_more_five'),
            total_teacher=Sum('total_teacher'),
            teacher_una_leave=Sum('teacher_una_leave'),
            teacher_salary_on_hold=Sum('teacher_salary_on_hold'),
            teacher_other_action=Sum('teacher_other_action'),
            non_teaching=Sum('non_teaching'),
            non_teaching_una_leave=Sum('non_teaching_una_leave'),
            non_teaching_salary_on_hold=Sum('non_teaching_salary_on_hold'),
            action_faculty_less_five=Sum('action_faculty_less_five'),
            class_scheduled=Sum('class_scheduled'),
            class_held=Sum('class_held'),
            lab_scheduled=Sum('lab_scheduled'),
            lab_held=Sum('lab_held')
        )
        filename = f"R3{user_date}.csv"

        # Create a response object for delivering csv data.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'},
        )

        # Create a csv writer object and write the header
        writer = csv.writer(response)
        writer.writerow([
            'University Name',
            'College Type',
            'Colleges Filled',
            'Enrollment',
            'Present',
            '% Present',
            'Show-caused',
            'Dis-Enrolled',
            'Re-Enrolled',
            'Teachers taken >5 Class',
            'Total Teacher',
            'No. of Unauthorized Absence (Teachers)',
            'Salary on Hold (Teachers)',
            'Other Actions (Teachers)',
            'Total Non Teaching Staff',
            'No. of Unauthorized Absence (Non-Teaching Staff)',
            'Salary on Hold (Non-Teaching Staff)',
            'Other Actions (Non-Teaching Staff)',
            'Classes Scheduled',
            'Classes Held',
            'Labs-Class Scheduled',
            'Lab-Class Held'
        ])

        # Write data rows
        for data in grouped_data:
            writer.writerow(
                [data['college_type'],
                 data['university_name'],
                 data['colleges_filled'],
                 data['enrollment'],
                 data['present'],
                 data['percent_present'],
                 data['showcaused'],
                 data['disenrolled'],
                 data['reenrolled'],
                 data['faculty_more_five'],
                 data['total_teacher'],
                 data['teacher_una_leave'],
                 data['teacher_salary_on_hold'],
                 data['teacher_other_action'],
                 data['non_teaching'],
                 data['non_teaching_una_leave'],
                 data['non_teaching_salary_on_hold'],
                 data['action_faculty_less_five'],
                 data['class_scheduled'],
                 data['class_held'],
                 data['lab_scheduled'],
                 data['lab_held']
                 ])

        return response
    else:
        return HttpResponse("No valid date provided", status=400)
