import mysql.connector
from faker import Faker
import random
from dotenv import load_dotenv
import os

load_dotenv()
# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user=os.getenv('mysql_user'),
    password=os.getenv('mysql_password'),
    database="skillsights"
)
cursor = conn.cursor()
fake = Faker()

# Config
num_addresses = 100
num_students = 50
num_tutors = 50
num_organizations = 20
num_courses = 20

# Reference data
enrollment_modes = ['Online', 'Offline', 'Hybrid']
payment_modes = ['Credit Card', 'Bank Transfer']
courses = ["Mathematics", "Physics", "Chemistry", "Biology", "History",
           "Geography", "English", "Computer Science", "Art", "Music",
           "Physical Education", "Economics", "Business Studies", "Psychology",]

# ID storage
address_ids = []
student_ids = []
tutor_ids = []
organization_ids = []
course_ids = []
enrollment_ids = []

# 1. Address
for _ in range(num_addresses):
    cursor.execute("""
        INSERT INTO address (street1, street2, city, state, zipcode, country)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (fake.street_address(), fake.secondary_address() if random.random() > 0.5 else None,
          fake.city(), fake.state(), fake.postcode(), fake.country()))
    address_ids.append(cursor.lastrowid)

conn.commit()

# 2. Enrollmentmode
for mode in enrollment_modes:
    cursor.execute("INSERT INTO Enrollmentmode (mode) VALUES (%s)", (mode,))
    enrollment_ids.append(cursor.lastrowid)

conn.commit()

# 3. Paymentmode
for mode in payment_modes:
    cursor.execute("INSERT INTO Paymentmode (payment_mode) VALUES (%s)", (mode,))

conn.commit()
# 4. Students
for _ in range(num_students):
    cursor.execute("""
        INSERT INTO Student (fname, lname, Email, Phone, address_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(),
          random.choice(address_ids)))
    student_ids.append(cursor.lastrowid)

conn.commit()

# 5. Tutors
for _ in range(num_tutors):
    cursor.execute("""
        INSERT INTO Tutor (fname, lname, Email, Phone, address_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(),
          random.choice(address_ids)))
    tutor_ids.append(cursor.lastrowid)

conn.commit()

# 6. Organizations
for _ in range(num_organizations):
    cursor.execute("""
        INSERT INTO Organization (sector, no_of_employees, name, address_id)
        VALUES (%s, %s, %s, %s)
    """, (random.choice(['Education', 'Technology', 'Finance', 'Healthcare']),
          random.randint(10, 500), fake.company(), random.choice(address_ids)))
    organization_ids.append(cursor.lastrowid)

conn.commit()

# 7. Courses
for _ in range(num_courses):
    course_name = courses[random.randint(0, len(courses)-1)]
    cursor.execute("""
        INSERT INTO Course (course_name, enrollment_id)
        VALUES (%s, %s)
    """, (course_name, random.choice(enrollment_ids)))
    course_ids.append(cursor.lastrowid)

conn.commit()
# 8. StudentCourse
for _ in range(num_students):
    cursor.execute("""
        INSERT INTO StudentCourse (course_id, student_id, enrollment_id)
        VALUES (%s, %s, %s)
    """, (random.choice(course_ids), random.choice(student_ids), random.choice(enrollment_ids)))
conn.commit()

# 9. TutorCourse
for _ in range(num_tutors):
    cursor.execute("""
        INSERT INTO TutorCourse (course_id, tutor_id)
        VALUES (%s, %s)
    """, (random.choice(course_ids), random.choice(tutor_ids)))
conn.commit()

# 10. OrganizationCourse
for _ in range(num_organizations):
    cursor.execute("""
        INSERT INTO OrganizationCourse (course_id, organization_id, enrollment_id)
        VALUES (%s, %s, %s)
    """, (random.choice(course_ids), random.choice(organization_ids), random.choice(enrollment_ids)))
conn.commit()

# 11. OrgContract
for _ in range(num_organizations):
    cursor.execute("""
        INSERT INTO OrgContract (organization_id, contract_term, contract_status, contract_price)
        VALUES (%s, %s, %s, %s)
    """, (random.choice(organization_ids), random.choice(['6M', '12M', '24M']),
          random.choice(['Active', 'Pending', 'Expired']), round(random.uniform(1000, 10000), 2)))
conn.commit()

# 12. OrgPayment
org_payment_ids = []
for _ in range(num_organizations):
    cursor.execute("""
        INSERT INTO OrgPayment (organization_id, Amount, payment_mode)
        VALUES (%s, %s, %s)
    """, (random.choice(organization_ids), round(random.uniform(500, 5000), 2), random.choice(payment_modes)))
    org_payment_ids.append(cursor.lastrowid)
conn.commit()

# 13. StudentPayment
for _ in range(num_students):
    cursor.execute("""
        INSERT INTO StudentPayment (student_id, Amount, payment_mode)
        VALUES (%s, %s, %s)
    """, (random.choice(student_ids), round(random.uniform(50, 500), 2), random.choice(payment_modes)))
conn.commit()

# 14. CreditCardPayment / BankPayment
for payment_id in org_payment_ids:
    if random.random() > 0.5:
        cursor.execute("""
            INSERT INTO CreditCardPayment (payment_id, creditcard_no, card_type)
            VALUES (%s, %s, %s)
        """, (payment_id, random.randint(4000000000000000, 4999999999999999), random.choice(['Visa', 'MasterCard'])))
    else:
        cursor.execute("""
            INSERT INTO BankPayment (payment_id, account_no, routing_no)
            VALUES (%s, %s, %s)
        """, (payment_id, random.randint(10000000, 99999999), random.randint(100000000, 999999999)))

# Commit and close
conn.commit()
cursor.close()
conn.close()
print("Data inserted successfully with FK integrity!")
