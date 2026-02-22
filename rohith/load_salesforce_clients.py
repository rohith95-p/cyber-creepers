# Salesforce Client Loader
from simple_salesforce import Salesforce
import random
import string

USERNAME = 'v1817517.df4e91c9398b@agentforce.com'
PASSWORD = 'puneeth123@'
SECURITY_TOKEN = 'nQFLGXz8FkIcRqrxVDifTbafU'

sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)

# Create custom object if not exists (Wealth_Client__c)
# This step is skipped for demo, as custom object creation requires metadata API
# We'll use Contact for demo purposes

def random_name():
    first = random.choice(['John', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'James', 'Anna', 'Robert', 'Maria'])
    last = random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'])
    return f"{first} {last}"

def random_email():
    return f"client{random.randint(1000,9999)}@wealth.ai"

for i in range(50):
    name = random_name()
    email = random_email()
    portfolio_value = random.randint(100000, 1000000)
    risk_tolerance = random.choice(['Conservative', 'Moderate', 'Aggressive'])
    status = random.choice(['On Track', 'At Risk', 'Needs Review'])
    goal_amount = random.randint(500000, 2000000)
    last_report = '2026-02-21'

    sf.Contact.create({
        'LastName': name,
        'Email': email,
        'Description': f"Portfolio: ${portfolio_value}, Risk: {risk_tolerance}, Status: {status}, Goal: ${goal_amount}, Last Report: {last_report}"
    })

print("✓ 50 sample clients created in Salesforce Contacts!")
