
from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["skillsights"]

students_collection = db["students"]
courses_collection = db["courses"]
orgs_collection = db["organizations"]
orgcourses_collection = db["orgcourses"]
orgemployees_collection = db["orgemployees"]
offered_courses = ["Mathematics", "Physics", "Chemistry", "Biology", "History",
           "Geography", "English", "Computer Science", "Art", "Music",
           "Physical Education", "Economics", "Business Studies", "Psychology",]

# Generate Courses
courses = []
for i in range(len(offered_courses)):
    course = {
        "course_id": f"CRS{i+1:03}",
        "title":random.choice(offered_courses),
        "description": fake.text(max_nb_chars=200),
        "duration_weeks": random.randint(4, 12),
        "price": round(random.uniform(100, 1000), 2),
        "delivery_mode": random.choice(["online", "inclass"]),
        "created_at": datetime.utcnow()
    }
    courses.append(course)
courses_collection.insert_many(courses)

# Generate Students
students = []
for i in range(50):
    enrolled = random.sample([c["course_id"] for c in courses], random.randint(1, 3))
    course = courses[(random.randint(0, len(courses)-1))]
    student = {
        "student_id": f"STD{i+1:03}",
        "name": fake.name(),
        "email": fake.email(),
        "mode": random.choice(["online", "inclass"]),
        "course":{
           "course_id": course["course_id"],
            "title": course["title"],
            "price": course["price"]                     
        },
        "payment": {
            "amount": course["price"],
            "payment_mode": random.choice(["credit_card", "bank_transfer"]),
            "payment_date": datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            "credit_card":{
                "card_number": fake.credit_card_number(),
                "expiry_date": fake.credit_card_expire(),
                "cvv": fake.credit_card_security_code()
            },
            "bank_transfer":{
                "account_number": fake.bban(), 
                "transfer_date": datetime.utcnow() - timedelta(days=random.randint(1, 30))
            }               
        },
        "status": random.choice(["active", "completed", "dropped"]),
        "created_at": datetime.utcnow()
    }
    students.append(student)
students_collection.insert_many(students)

# Generate Organizations
organizations = []
for i in range(10):
    org = {
        "org_id": f"ORG{i+1:03}",
        "name": fake.company(),
        "contact_email": fake.company_email(),
        "sector": random.choice(["Education", "Technology", "Finance", "Healthcare"]),
        "no_of_employees": random.randint(100, 5000),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country()
        },
        "contract":{
            "contract_id": f"CTR{i+1:03}",
            "contract_price": round(random.uniform(5000, 50000), 2),
            "start_date": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
            "end_date": datetime.utcnow() + timedelta(days=random.randint(30, 365))
        }
    }
    organizations.append(org)
orgs_collection.insert_many(organizations)

orgcourses = []
# Generate OrgCourses , courses skillsights offers for an oraganization
for i in range(len(courses)):
    orgcourse = {
        "orgcourse_id": f"ORGC{i+1:03}",
        "organization": random.choice(organizations)["name"],
        "course": {
            "course_id": courses[i]["course_id"],
            "title": courses[i]["title"],
            "price": courses[i]["price"]
        },
    }
    orgcourses.append(orgcourse)
orgcourses_collection.insert_many(orgcourses)

orgemployees = []
# Generate OrgEmployees , employees of an organization enrolled in courses
for i in range(30):
    orgemployee = {
        "orgemployee_id": f"ORGE{i+1:03}",
        "employee_name": fake.name(),
        "employee_email": fake.email(),
        "organization":{
            "org_id": random.choice(organizations)["org_id"],
            "name": random.choice(organizations)["name"]
        },
        "course": {
            "course_id": random.choice(courses)["course_id"],
            "title": random.choice(courses)["title"],
            "status": random.choice(["inprogress", "completed", "dropped"])
        },
        "enrollment_date": datetime.utcnow() - timedelta(days=random.randint(1, 60)),
        "completion_status": random.choice(["inprogress", "completed", "dropped"])
    }
    orgemployees.append(orgemployee)

orgemployees_collection.insert_many(orgemployees)
print("Synthetic LMS data inserted successfully!")
