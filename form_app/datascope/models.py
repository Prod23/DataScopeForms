from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    college_name = models.CharField(max_length=100)
    college_type = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    name_nodal_officer = models.CharField(max_length=50, default='')
    mobile_nodal_officer = models.BigIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['college_name']

    def __str__(self):
        return f"{self.university_name} - {self.college_name}"

    def save(self, *args, **kwargs):
        self.username = f"{self.college_name.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '').replace('-', '').replace(',', '')}_{self.university_name.replace(' ', '_').replace('.','')}"

        existing_users = CustomUser.objects.filter(username=self.username)
        if self.pk:  # Check if the instance already exists (updating)
            existing_users = existing_users.exclude(pk=self.pk)

        if existing_users.exists():
            raise ValueError("Username must be unique.")

        super().save(*args, **kwargs)

class Questionnaire(models.Model):
    email = models.EmailField(blank=True)
    university_name = models.CharField(max_length=255, blank=True)
    college_type = models.CharField(max_length=255, blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)
    ICT_facility = models.BooleanField(default=False)
    num_computers_in_ICT_labs = models.PositiveIntegerField(default=0)
    housekeeping = models.BooleanField(default=False)
    total_staffs_housekeeping = models.PositiveIntegerField(default=0)
    video_conf = models.BooleanField(default=False)
    rooms_with_video_conf = models.PositiveIntegerField(default=0)
    biometric = models.BooleanField(default=False)
    biometric_working = models.BooleanField(default=False)
    merged_savings_accounts = models.BooleanField(default=False)
    classrooms = models.PositiveIntegerField(default=0)
    labrooms = models.PositiveIntegerField(default=0)
    library = models.PositiveIntegerField(default=0)
    additionalrooms = models.PositiveIntegerField(default=0)
    toilets_male = models.PositiveIntegerField(default=0)
    toilets_female = models.PositiveIntegerField(default=0)
    num_under_construction = models.PositiveIntegerField(default=0)
    enrolled = models.PositiveIntegerField(default=0)
    present = models.PositiveIntegerField(default=0)
    showcaused = models.PositiveIntegerField(default=0)
    disenrolled = models.PositiveIntegerField(default=0)
    reenrolled = models.PositiveIntegerField(default=0)
    total_teacher = models.PositiveIntegerField(default=0)
    teacher_present = models.PositiveIntegerField(default=0)
    teacher_una_leave = models.PositiveIntegerField(default=0)
    teacher_salary_on_hold = models.PositiveIntegerField(default=0)
    teacher_other_action = models.PositiveIntegerField(default=0)
    non_teaching = models.PositiveIntegerField(default=0)
    non_teaching_salary_on_hold = models.PositiveIntegerField(default=0)
    non_teaching_una_leave = models.PositiveIntegerField(default=0)
    non_teaching_other_action = models.PositiveIntegerField(default=0)
    faculty_more_five = models.PositiveIntegerField(default=0)
    not_faculty_more_five = models.PositiveIntegerField(default=0)
    faculty_less_three = models.PositiveIntegerField(default=0)
    action_faculty_less_five = models.PositiveIntegerField(default=0)
    class_scheduled = models.PositiveIntegerField(default=0)
    class_held = models.PositiveIntegerField(default=0)
    lab_scheduled = models.PositiveIntegerField(default=0)
    lab_held = models.PositiveIntegerField(default=0)
    inspection = models.BooleanField(default=False)
    merged_accounts_two = models.BooleanField(default=False)
    num_bank_accounts_existed_earlier = models.PositiveIntegerField(default=0)
    num_bank_accounts_existed_today = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('email', 'university_name', 'college_name', 'date')

    def __str__(self):
        return f"Questionnaire for {self.college_name} ({self.date})"


class CourseInformation(models.Model):
    email = models.EmailField(blank=True)
    university_name = models.CharField(max_length=255, blank=True)
    college_type = models.CharField(max_length=255, blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    # Postgraduate Arts Courses
    pg_arts_exist = models.BooleanField(default=False)
    pg_arts_sem1_enrolled = models.PositiveIntegerField(default=0)
    pg_arts_sem1_present = models.PositiveIntegerField(default=0)
    pg_arts_sem2_enrolled = models.PositiveIntegerField(default=0)
    pg_arts_sem2_present = models.PositiveIntegerField(default=0)
    pg_arts_sem3_enrolled = models.PositiveIntegerField(default=0)
    pg_arts_sem3_present = models.PositiveIntegerField(default=0)
    pg_arts_sem4_enrolled = models.PositiveIntegerField(default=0)
    pg_arts_sem4_present = models.PositiveIntegerField(default=0)
    
    # Postgraduate Science Courses
    pg_science_exist = models.BooleanField(default=False)
    pg_science_sem1_enrolled = models.PositiveIntegerField(default=0)
    pg_science_sem1_present = models.PositiveIntegerField(default=0)
    pg_science_sem2_enrolled = models.PositiveIntegerField(default=0)
    pg_science_sem2_present = models.PositiveIntegerField(default=0)
    pg_science_sem3_enrolled = models.PositiveIntegerField(default=0)
    pg_science_sem3_present = models.PositiveIntegerField(default=0)
    pg_science_sem4_enrolled = models.PositiveIntegerField(default=0)
    pg_science_sem4_present = models.PositiveIntegerField(default=0)

    # Postgraduate Commerce Courses
    pg_commerce_exist = models.BooleanField(default=False)
    pg_commerce_sem1_enrolled = models.PositiveIntegerField(default=0)
    pg_commerce_sem1_present = models.PositiveIntegerField(default=0)
    pg_commerce_sem2_enrolled = models.PositiveIntegerField(default=0)
    pg_commerce_sem2_present = models.PositiveIntegerField(default=0)
    pg_commerce_sem3_enrolled = models.PositiveIntegerField(default=0)
    pg_commerce_sem3_present = models.PositiveIntegerField(default=0)
    pg_commerce_sem4_enrolled = models.PositiveIntegerField(default=0)
    pg_commerce_sem4_present = models.PositiveIntegerField(default=0)

    # Postgraduate Professional/Other Courses
    pg_professional_exist = models.BooleanField(default=False)
    pg_professional_sem1_enrolled = models.PositiveIntegerField(default=0)
    pg_professional_sem1_present = models.PositiveIntegerField(default=0)
    pg_professional_sem2_enrolled = models.PositiveIntegerField(default=0)
    pg_professional_sem2_present = models.PositiveIntegerField(default=0)
    pg_professional_sem3_enrolled = models.PositiveIntegerField(default=0)
    pg_professional_sem3_present = models.PositiveIntegerField(default=0)
    pg_professional_sem4_enrolled = models.PositiveIntegerField(default=0)
    pg_professional_sem4_present = models.PositiveIntegerField(default=0)

    # Undergraduate Arts Courses
    ug_arts_exist = models.BooleanField(default=False)
    ug_arts_sem1_enrolled = models.PositiveIntegerField(default=0)
    ug_arts_sem1_present = models.PositiveIntegerField(default=0)
    ug_arts_yr2_enrolled = models.PositiveIntegerField(default=0)
    ug_arts_yr2_present = models.PositiveIntegerField(default=0)
    ug_arts_yr3_enrolled = models.PositiveIntegerField(default=0)
    ug_arts_yr3_present = models.PositiveIntegerField(default=0)

    # Undergraduate Science Courses
    ug_science_exist = models.BooleanField(default=False)
    ug_science_sem1_enrolled = models.PositiveIntegerField(default=0)
    ug_science_sem1_present = models.PositiveIntegerField(default=0)
    ug_science_yr2_enrolled = models.PositiveIntegerField(default=0)
    ug_science_yr2_present = models.PositiveIntegerField(default=0)
    ug_science_yr3_enrolled = models.PositiveIntegerField(default=0)
    ug_science_yr3_present = models.PositiveIntegerField(default=0)

    # Undergraduate Commerce Courses
    ug_commerce_exist = models.BooleanField(default=False)
    ug_commerce_sem1_enrolled = models.PositiveIntegerField(default=0)
    ug_commerce_sem1_present = models.PositiveIntegerField(default=0)
    ug_commerce_yr2_enrolled = models.PositiveIntegerField(default=0)
    ug_commerce_yr2_present = models.PositiveIntegerField(default=0)
    ug_commerce_yr3_enrolled = models.PositiveIntegerField(default=0)
    ug_commerce_yr3_present = models.PositiveIntegerField(default=0)

    # Undergraduate Professional/Other Courses
    ug_professional_exist = models.BooleanField(default=False)
    ug_professional_sem1_enrolled = models.PositiveIntegerField(default=0)
    ug_professional_sem1_present = models.PositiveIntegerField(default=0)
    ug_professional_sem2_enrolled = models.PositiveIntegerField(default=0)
    ug_professional_sem2_present = models.PositiveIntegerField(default=0)
    ug_professional_sem3_enrolled = models.PositiveIntegerField(default=0)
    ug_professional_sem3_present = models.PositiveIntegerField(default=0)
    ug_professional_sem4_enrolled = models.PositiveIntegerField(default=0)
    ug_professional_sem4_present = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('email', 'university_name', 'college_name', 'date')

    def __str__(self):
        return f"Course Info for {self.college_name} ({self.date})"
