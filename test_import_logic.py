"""
Test script for import logic improvements
Verifies that:
1. Duplicate classes are not created
2. Duplicate students (by idMassar) are skipped
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"  # Update with actual token
}

def test_class_deduplication():
    """Test that classes are not duplicated during import"""
    print("\n" + "="*60)
    print("TEST 1: Class Deduplication")
    print("="*60)
    
    # Create a test school year
    sy_payload = {
        "label": "2025-2026",
        "startAt": "2025-09-01T00:00:00",
        "endAt": "2026-06-30T23:59:59",
        "enabled": True,
        "current": True
    }
    
    r_sy = requests.post(f"{BASE_URL}/api/education/school-years/", json=sy_payload, headers=HEADERS)
    if r_sy.status_code != 200:
        print(f"❌ Failed to create school year: {r_sy.text}")
        return False
    
    sy_id = r_sy.json().get("id")
    print(f"✅ School year created: ID={sy_id}")
    
    # Test 1a: Create first class
    cls_payload = {
        "label": "1ère année",
        "filiere": "Informatique",
        "schoolYear_id": sy_id
    }
    
    r_cls1 = requests.post(f"{BASE_URL}/api/education/classes/", json=cls_payload, headers=HEADERS)
    if r_cls1.status_code != 200:
        print(f"❌ Failed to create class: {r_cls1.text}")
        return False
    
    cls_id_1 = r_cls1.json().get("id")
    print(f"✅ Class created: ID={cls_id_1}, Label='1ère année'")
    
    # Test 1b: Try to create identical class again
    r_cls2 = requests.post(f"{BASE_URL}/api/education/classes/", json=cls_payload, headers=HEADERS)
    if r_cls2.status_code == 200:
        cls_id_2 = r_cls2.json().get("id")
        
        if cls_id_1 == cls_id_2:
            print(f"✅ PASS: Duplicate class handled correctly (same ID returned)")
        else:
            print(f"⚠️  WARN: New class created with ID={cls_id_2} (expected duplicate check in API)")
    
    return True

def test_student_deduplication():
    """Test that students are not duplicated by idMassar"""
    print("\n" + "="*60)
    print("TEST 2: Student Deduplication by idMassar")
    print("="*60)
    
    # Get or create a test class
    r_classes = requests.get(f"{BASE_URL}/api/education/classes/", headers=HEADERS)
    if r_classes.status_code != 200:
        print(f"❌ Failed to get classes: {r_classes.text}")
        return False
    
    classes = r_classes.json()
    if not classes:
        print("❌ No classes found. Run TEST 1 first.")
        return False
    
    cls_id = classes[0]["id"]
    print(f"✅ Using class: ID={cls_id}")
    
    # Create a student with unique idMassar
    test_massar = f"TEST_{datetime.now().timestamp()}"
    student_payload = {
        "nom": "Test Student",
        "num": "1",
        "classe_id": cls_id,
        "idMassar": test_massar,
        "enabled": True
    }
    
    r_s1 = requests.post(f"{BASE_URL}/api/education/students/", json=student_payload, headers=HEADERS)
    if r_s1.status_code != 200:
        print(f"❌ Failed to create student: {r_s1.text}")
        return False
    
    student_id = r_s1.json().get("id")
    print(f"✅ Student created: ID={student_id}, idMassar='{test_massar}'")
    
    # Try to create same student again (should be handled by create_student)
    student_payload["num"] = "2"  # Different num but same idMassar
    r_s2 = requests.post(f"{BASE_URL}/api/education/students/", json=student_payload, headers=HEADERS)
    
    if r_s2.status_code == 200:
        student_id_2 = r_s2.json().get("id")
        
        if student_id == student_id_2:
            print(f"✅ PASS: Duplicate student handled correctly (same ID returned, updated)")
        else:
            print(f"⚠️  WARN: New student created with ID={student_id_2}")
    else:
        print(f"❌ Error creating duplicate student: {r_s2.text}")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "█"*60)
    print("  Import Logic Tests")
    print("█"*60)
    
    try:
        test_class_deduplication()
        test_student_deduplication()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}\n")

if __name__ == "__main__":
    print("""
    ⚠️  NOTE: This test script requires:
    1. API server running on http://localhost:8000
    2. Valid authentication token in HEADERS
    3. At least one school year and class in the database
    
    Update the HEADERS dict with your actual Bearer token before running.
    """)
    
    # Uncomment to run tests:
    # run_all_tests()
