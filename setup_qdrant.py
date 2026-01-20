from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import pandas as pd
import uuid
import os

def create_sample_data():
    """Create sample community resources dataset"""
    resources = [
        {
            "name": "City Community Health Clinic",
            "category": "Healthcare",
            "description": "Free health checkups, vaccinations, basic medical care for uninsured families. Mental health counseling and chronic disease management.",
            "location": "123 Main St, Downtown",
            "contact": "555-0100",
            "hours": "Mon-Fri 9AM-5PM",
            "services": "Primary Care, Vaccinations, Mental Health"
        },
        {
            "name": "Daily Bread Food Bank",
            "category": "Food Assistance",
            "description": "Emergency food supplies, weekly groceries for low-income households. Fresh produce, dairy, and non-perishables available.",
            "location": "456 Oak Ave, West Side",
            "contact": "555-0200",
            "hours": "Tue-Sat 8AM-4PM",
            "services": "Food Pantry, Emergency Meals"
        },
        {
            "name": "Legal Aid Society",
            "category": "Legal Services",
            "description": "Free legal consultation for housing disputes, family law, immigration issues. Available in English and Spanish.",
            "location": "789 Court St, City Center",
            "contact": "555-0300",
            "hours": "Mon-Thu 10AM-6PM",
            "services": "Housing Law, Family Law, Immigration"
        },
        {
            "name": "Adult Learning Center",
            "category": "Education",
            "description": "GED preparation, ESL classes, computer literacy, job training programs. All levels welcome, no cost.",
            "location": "321 School Rd, North District",
            "contact": "555-0400",
            "hours": "Mon-Fri 6PM-9PM, Sat 9AM-2PM",
            "services": "GED, ESL, Job Training"
        },
        {
            "name": "Mobile Medical Unit",
            "category": "Healthcare",
            "description": "Mobile clinic serving underserved neighborhoods. Basic health screenings, prescription assistance, dental checkups.",
            "location": "Various locations (call for schedule)",
            "contact": "555-0500",
            "hours": "Mon-Fri 10AM-3PM",
            "services": "Mobile Clinic, Dental, Prescriptions"
        },
        {
            "name": "Youth After-School Program",
            "category": "Education",
            "description": "Homework help, tutoring, sports activities for K-12 students. Nutritious snacks provided daily.",
            "location": "555 Park Ave, South Side",
            "contact": "555-0600",
            "hours": "Mon-Fri 3PM-6PM",
            "services": "Tutoring, Sports, Meals"
        },
        {
            "name": "Emergency Shelter Network",
            "category": "Housing",
            "description": "Temporary housing for homeless individuals and families. Case management, job placement assistance.",
            "location": "100 Shelter Ln, East Side",
            "contact": "555-0700",
            "hours": "24/7 Emergency Line",
            "services": "Emergency Shelter, Case Management"
        },
        {
            "name": "Community Meal Center",
            "category": "Food Assistance",
            "description": "Hot meals served daily, no questions asked. Weekend food packages for families in need.",
            "location": "200 Church St, Downtown",
            "contact": "555-0800",
            "hours": "Daily 11AM-1PM, 5PM-7PM",
            "services": "Hot Meals, Food Packages"
        },
        {
            "name": "Mental Health Crisis Line",
            "category": "Healthcare",
            "description": "24/7 crisis counseling, suicide prevention, referrals to mental health services. Multilingual support available.",
            "location": "Phone service (can arrange in-person)",
            "contact": "555-0900 or 1-800-CRISIS",
            "hours": "24/7",
            "services": "Crisis Counseling, Suicide Prevention"
        },
        {
            "name": "Job Readiness Center",
            "category": "Employment",
            "description": "Resume writing, interview preparation, job search assistance. Computer access and professional clothing closet.",
            "location": "400 Work St, Business District",
            "contact": "555-1000",
            "hours": "Mon-Fri 9AM-5PM",
            "services": "Job Training, Resume Help, Clothing"
        },
        {
            "name": "Prescription Assistance Program",
            "category": "Healthcare",
            "description": "Help obtaining low-cost medications, navigating insurance, connecting to pharmaceutical assistance programs.",
            "location": "123 Main St (inside Health Clinic)",
            "contact": "555-1100",
            "hours": "Mon-Wed-Fri 10AM-4PM",
            "services": "Medication Assistance, Insurance Help"
        },
        {
            "name": "Veterans Services Center",
            "category": "Support Services",
            "description": "Comprehensive support for veterans: housing assistance, PTSD counseling, benefits navigation, job placement.",
            "location": "600 Military Rd, Veterans Park",
            "contact": "555-1200",
            "hours": "Mon-Fri 8AM-6PM",
            "services": "Housing, PTSD Counseling, Benefits"
        },
        {
            "name": "Women and Children Shelter",
            "category": "Housing",
            "description": "Safe housing for women and children fleeing domestic violence. Counseling, legal advocacy, childcare available.",
            "location": "Confidential Location (call for access)",
            "contact": "555-1300 (24/7 hotline)",
            "hours": "24/7",
            "services": "Safe Housing, Counseling, Legal Aid"
        },
        {
            "name": "Transportation Assistance",
            "category": "Support Services",
            "description": "Free bus passes for medical appointments, job interviews, essential services. Volunteer driver network available.",
            "location": "Various pickup locations",
            "contact": "555-1400",
            "hours": "Mon-Fri 7AM-7PM",
            "services": "Bus Passes, Medical Transport"
        },
        {
            "name": "Senior Wellness Center",
            "category": "Healthcare",
            "description": "Health screenings, exercise classes, nutrition counseling for seniors 60+. Social activities and hot lunch daily.",
            "location": "700 Elder Ave, Retirement Community",
            "contact": "555-1500",
            "hours": "Mon-Fri 9AM-3PM",
            "services": "Health Screenings, Exercise, Meals"
        },
        {
            "name": "Immigrant Resource Center",
            "category": "Legal Services",
            "description": "Immigration legal services, citizenship classes, language assistance, cultural orientation programs.",
            "location": "800 Liberty St, Cultural District",
            "contact": "555-1600",
            "hours": "Tue-Sat 10AM-6PM",
            "services": "Immigration Law, Citizenship, ESL"
        },
        {
            "name": "Dental Care Clinic",
            "category": "Healthcare",
            "description": "Low-cost dental services: cleanings, fillings, extractions. Sliding scale fees based on income.",
            "location": "900 Tooth Ln, Medical Complex",
            "contact": "555-1700",
            "hours": "Mon-Thu 8AM-5PM",
            "services": "Dental Cleanings, Fillings, Extractions"
        },
        {
            "name": "Utility Assistance Program",
            "category": "Financial Aid",
            "description": "Help paying electricity, gas, water bills. Energy efficiency upgrades and budget counseling available.",
            "location": "1000 Power St, City Hall Annex",
            "contact": "555-1800",
            "hours": "Mon-Fri 9AM-4PM",
            "services": "Utility Bills, Energy Assistance"
        },
        {
            "name": "Addiction Recovery Center",
            "category": "Healthcare",
            "description": "Substance abuse counseling, recovery support groups, medication-assisted treatment. Family counseling available.",
            "location": "1100 Recovery Rd, Health Campus",
            "contact": "555-1900",
            "hours": "Mon-Sat 8AM-8PM",
            "services": "Addiction Counseling, MAT, Support Groups"
        },
        {
            "name": "Child Development Center",
            "category": "Education",
            "description": "Subsidized childcare for working families, early childhood education, developmental screenings.",
            "location": "1200 Kids Way, Family Services",
            "contact": "555-2000",
            "hours": "Mon-Fri 6AM-6PM",
            "services": "Childcare, Early Education, Screenings"
        },
        {
            "name": "Financial Literacy Workshop",
            "category": "Financial Aid",
            "description": "Free classes on budgeting, saving, credit repair, homeownership. One-on-one financial coaching available.",
            "location": "1300 Money St, Community Center",
            "contact": "555-2100",
            "hours": "Weekly Wed 6PM-8PM",
            "services": "Budgeting, Credit Repair, Coaching"
        },
        {
            "name": "Disability Services Office",
            "category": "Support Services",
            "description": "Assistance for people with disabilities: adaptive equipment, benefits navigation, accessibility advocacy.",
            "location": "1400 Access Blvd, Municipal Building",
            "contact": "555-2200",
            "hours": "Mon-Fri 9AM-5PM",
            "services": "Equipment, Benefits, Advocacy"
        },
        {
            "name": "Community Garden Program",
            "category": "Food Assistance",
            "description": "Free garden plots for families, gardening education, fresh produce distribution, cooking classes.",
            "location": "1500 Green St, Community Gardens",
            "contact": "555-2300",
            "hours": "Daily dawn to dusk",
            "services": "Garden Plots, Education, Fresh Produce"
        },
        {
            "name": "Tax Preparation Service",
            "category": "Financial Aid",
            "description": "Free tax filing assistance, help claiming EITC and child tax credits. IRS-certified volunteers.",
            "location": "1600 Tax Ave, Library",
            "contact": "555-2400",
            "hours": "Jan-Apr: Mon-Sat 10AM-6PM",
            "services": "Tax Filing, EITC, Credits"
        },
        {
            "name": "Youth Mentoring Program",
            "category": "Education",
            "description": "One-on-one mentoring for at-risk youth, college preparation, career exploration, life skills training.",
            "location": "1700 Future Rd, Youth Center",
            "contact": "555-2500",
            "hours": "Flexible scheduling",
            "services": "Mentoring, College Prep, Life Skills"
        }
    ]
    
    df = pd.DataFrame(resources)
    return df

def setup_qdrant():
    """Initialize Qdrant and load data"""
    print("🚀 Setting up Qdrant Vector Database...")
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate sample data
    print("📊 Creating sample community resources data...")
    df = create_sample_data()
    df.to_csv('data/community_resources.csv', index=False)
    print(f"✅ Created {len(df)} community resources")
    
    # Initialize Qdrant client (in-memory for demo)
    print("\n🔧 Initializing Qdrant client...")
    client = QdrantClient(":memory:")
    
    # Initialize embedding model
    print("🧠 Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create collection
    print("📦 Creating Qdrant collection...")
    client.create_collection(
        collection_name="community_resources",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    
    # Prepare points for upload
    print("⚡ Generating embeddings and uploading to Qdrant...")
    points = []
    
    for idx, row in df.iterrows():
        # Combine text fields for rich embedding
        text = f"{row['name']} {row['category']} {row['description']} {row['services']}"
        vector = model.encode(text).tolist()
        
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "name": row['name'],
                "category": row['category'],
                "description": row['description'],
                "location": row['location'],
                "contact": row['contact'],
                "hours": row['hours'],
                "services": row['services']
            }
        ))
    
    # Upload to Qdrant
    client.upsert(collection_name="community_resources", points=points)
    
    print(f"✅ Successfully uploaded {len(points)} resources to Qdrant!")
    print("\n" + "="*60)
    print("Setup complete! Qdrant is ready to use.")
    print("="*60)
    
    return client, model

if __name__ == "__main__":
    setup_qdrant()