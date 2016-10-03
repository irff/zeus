from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import ImageField

import datetime

def seedStudent():
    Student.drop_collection()
    student1 = Student(name='Tri Ahmad Irfan',
                   major='Computer Science',
                   school='University of Indonesia',
                   resume_url='http://google.com',
                   linkedin_url='http://google.com',
                   photo_url='http://google.com',
                   headline='Back-end developer at Quint')
    student1.save()

def seedUserStudent():
    UserStudent.drop_collection()
    user1 = UserStudent(email='genturwt@gmail.com',
                password=generate_password_hash('quint-dev'),
                student=Student.objects.first())
    user1.save()

    user2 = UserStudent(email='kenny@gmail.com',
                password=generate_password_hash('quint-front'),
                student=Student.objects.first())
    user2.save()

    user3 = UserStudent(email='irfan@gmail.com',
                password=generate_password_hash('quint-master'),
                student=Student.objects.first())
    user3.save()

def seedUserCompany():
    UserCompany.drop_collection()
    user1 = UserCompany(email='genturwt@quint.id',
                password=generate_password_hash('quint-dev'),
                company=Company.objects.first())
    user1.save()

    user2 = UserCompany(email='kenny@quint.id',
                password=generate_password_hash('quint-front'),
                company=Company.objects.first())
    user2.save()

    user3 = UserCompany(email='irfan@quint.id',
                password=generate_password_hash('quint-master'),
                company=Company.objects.first())
    user3.save()

def seedOfficeLocation():
    OfficeLocation.drop_collection()
    officeLocation1 = OfficeLocation(name='Quint Tower',
                                    address='Quint Street No. 63',
                                    location=[-60.1523, 63.5125])
    officeLocation1.save()

def seedContactPerson():
    ContactPerson.drop_collection()
    contactPerson1 = ContactPerson(name='Firza Pratama',
                                role='CEO',
                                phone='087835520315',
                                email='firza@quint.dev')
    contactPerson1.save()

def seedJobPost():
    def start():
        return datetime.datetime(2016,9,1,0,0,0)
    def end():
        return datetime.datetime(2016,9,30,23,55,0)
    def cp():
        return ContactPerson.objects.first()

    JobPost.drop_collection()
    schedule1 = InternshipSchedule(start_at=start(), end_at=end())
    jobPost1 = JobPost(role='Software Engineer Intern',
                    why_us='We are the best of the best',
                    salary=Salary(fee=450000, currency="$", term="month"),
                    technical_requirements=['PHP', 'CSS', 'Python'],
                    internship_schedule= schedule1,
                    tasks=['Create back-end systems', 'Create front-end systems'],
                    skills_gained=['Leadership', 'Strong team-work'],
                    experiences_gained=['Get to know CEO of Quint', 'Meet investor'],
                    contact_person=cp())
    jobPost1.save()

def seedCompany():
    Company.drop_collection()
    def loc():
        return OfficeLocation.objects.all()
    def job():
        return JobPost.objects.all()
    def cp():
        return ContactPerson.objects.first()
    def photo():
        photo = CompanyPhoto()
        photo.img.put('tests/300.png')
        return [photo]

    company1 = Company(name='Quint',
                    office_locations=loc(),
                    job_posts=job(),
                    industry='Internship Third-Party',
                    website='http://quint.dev',
                    logo_url='http://quint.dev/logo.jpg',
                    photos=photo(),
                    contact_person=cp())
    company1.save()

def seedApplication():
    def job():
        return JobPost.objects.first()
    def student():
        return Student.objects.first()

    Application.drop_collection()
    application1 = Application(job_post=job(),
                            student=student(),
                            status='Accepted')
    application1.save()

class Seeder:
    def seed(self):
        seedStudent()
        seedOfficeLocation()
        seedContactPerson()
        seedJobPost()
        seedApplication()
        seedCompany()
        seedUserStudent()
        seedUserCompany()