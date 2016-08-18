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

def seedUser():
    User.drop_collection()
    user1 = User(email='genturwt@gmail.com',
                password=generate_password_hash('quint-dev'))
    user1.save()

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
                    salary='18000000',
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
        seedUser()
        seedStudent()
        seedOfficeLocation()
        seedContactPerson()
        seedJobPost()
        seedCompany()
        seedApplication()

