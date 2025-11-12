#!/usr/bin/env python3
"""
Target Assignment Workflow Test - Flourish Skills Tracker

Tests the complete target assignment workflow:
1. Assign a target to a student
2. Verify target saved in database
3. Retrieve target via API
4. Mark target as complete
5. Verify completion

Usage:
    python scripts/test_target_workflow.py
"""

import sys
import os
import requests
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://flourish_admin:secure_password_123@localhost:5433/skills_tracker_db")
TEST_STUDENT_ID = "S001"  # Eva
TEST_TEACHER_ID = "T001"
TEST_SKILL = "Communication"


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def test_target_workflow():
    """
    Test the complete target assignment workflow

    Returns:
        bool: True if all tests pass, False otherwise
    """
    logger.info("=" * 60)
    logger.info("TARGET ASSIGNMENT WORKFLOW TEST")
    logger.info("=" * 60)

    test_results = []
    target_id = None

    # Step 1: Clear any existing active targets for this skill
    logger.info("\n[SETUP] Checking for existing active targets...")
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/students/{TEST_STUDENT_ID}/targets?completed=false",
            timeout=10
        )
        response.raise_for_status()
        active_targets = response.json()

        # Complete any existing active targets for our test skill
        for target in active_targets:
            if target['skill_name'] == TEST_SKILL:
                logger.info(f"   Completing existing target: {target['id']}")
                complete_response = requests.put(
                    f"{BACKEND_URL}/api/students/targets/{target['id']}/complete",
                    timeout=10
                )
                complete_response.raise_for_status()

        logger.info(f"✅ Setup complete")

    except Exception as e:
        logger.warning(f"⚠️  Warning during setup: {e}")

    # Step 1: Assign a target
    logger.info(f"\n[STEP 1] Assigning target to student {TEST_STUDENT_ID}...")

    target_data = {
        "student_id": TEST_STUDENT_ID,
        "skill_name": TEST_SKILL,
        "starting_level": "Developing",
        "target_level": "Proficient",
        "assigned_by": TEST_TEACHER_ID
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/students/{TEST_STUDENT_ID}/target-skill",
            json=target_data,
            timeout=10
        )
        response.raise_for_status()
        target_response = response.json()

        if 'id' in target_response:
            target_id = target_response['id']
            logger.info(f"✅ PASS: Target assigned (ID: {target_id})")
            logger.info(f"   Skill: {TEST_SKILL}")
            logger.info(f"   Progression: Developing → Proficient")
            test_results.append(("Assign target", True))
        else:
            logger.error(f"❌ FAIL: Target assignment response invalid: {target_response}")
            test_results.append(("Assign target", False))
            return False

    except Exception as e:
        logger.error(f"❌ FAIL: Error assigning target: {e}")
        test_results.append(("Assign target", False))
        return False

    # Step 2: Verify target saved in database
    logger.info("\n[STEP 2] Verifying target saved in database...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, student_id, skill_name, starting_level, target_level, assigned_by, completed
            FROM skill_targets
            WHERE id = %s
        """, (target_id,))

        target_record = cur.fetchone()

        if target_record:
            logger.info(f"✅ PASS: Target found in database")
            logger.info(f"   Student: {target_record['student_id']}")
            logger.info(f"   Skill: {target_record['skill_name']}")
            logger.info(f"   Levels: {target_record['starting_level']} → {target_record['target_level']}")
            logger.info(f"   Completed: {target_record['completed']}")

            # Verify data matches what we sent
            if (target_record['student_id'] == TEST_STUDENT_ID and
                target_record['skill_name'] == TEST_SKILL and
                target_record['starting_level'] == 'Developing' and
                target_record['target_level'] == 'Proficient' and
                not target_record['completed']):
                test_results.append(("Target in database", True))
            else:
                logger.error(f"❌ FAIL: Target data doesn't match")
                test_results.append(("Target in database", False))
                cur.close()
                conn.close()
                return False
        else:
            logger.error(f"❌ FAIL: Target not found in database")
            test_results.append(("Target in database", False))
            cur.close()
            conn.close()
            return False

        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"❌ FAIL: Error verifying target in database: {e}")
        test_results.append(("Target in database", False))
        return False

    # Step 3: Retrieve target via API
    logger.info("\n[STEP 3] Retrieving active targets via API...")
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/students/{TEST_STUDENT_ID}/targets?completed=false",
            timeout=10
        )
        response.raise_for_status()
        active_targets = response.json()

        found_target = None
        for target in active_targets:
            if target['id'] == target_id:
                found_target = target
                break

        if found_target:
            logger.info(f"✅ PASS: Target retrieved via API")
            logger.info(f"   Found target in active targets list")
            test_results.append(("Retrieve target via API", True))
        else:
            logger.error(f"❌ FAIL: Target not found in API response")
            test_results.append(("Retrieve target via API", False))
            return False

    except Exception as e:
        logger.error(f"❌ FAIL: Error retrieving target via API: {e}")
        test_results.append(("Retrieve target via API", False))
        return False

    # Step 4: Mark target as complete
    logger.info("\n[STEP 4] Marking target as complete...")
    try:
        response = requests.put(
            f"{BACKEND_URL}/api/students/targets/{target_id}/complete",
            timeout=10
        )
        response.raise_for_status()
        completion_response = response.json()

        if completion_response.get('success'):
            logger.info(f"✅ PASS: Target marked as complete")
            test_results.append(("Mark target complete", True))
        else:
            logger.error(f"❌ FAIL: Target completion failed: {completion_response}")
            test_results.append(("Mark target complete", False))
            return False

    except Exception as e:
        logger.error(f"❌ FAIL: Error marking target complete: {e}")
        test_results.append(("Mark target complete", False))
        return False

    # Step 5: Verify completion in database
    logger.info("\n[STEP 5] Verifying target completion in database...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, completed, completed_at
            FROM skill_targets
            WHERE id = %s
        """, (target_id,))

        target_record = cur.fetchone()

        if target_record and target_record['completed'] and target_record['completed_at']:
            logger.info(f"✅ PASS: Target completion verified")
            logger.info(f"   Completed: {target_record['completed']}")
            logger.info(f"   Completed at: {target_record['completed_at']}")
            test_results.append(("Verify completion", True))
        else:
            logger.error(f"❌ FAIL: Target not properly completed")
            test_results.append(("Verify completion", False))
            cur.close()
            conn.close()
            return False

        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"❌ FAIL: Error verifying completion: {e}")
        test_results.append(("Verify completion", False))
        return False

    # Step 6: Verify target appears in completed targets
    logger.info("\n[STEP 6] Retrieving completed targets via API...")
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/students/{TEST_STUDENT_ID}/targets?completed=true",
            timeout=10
        )
        response.raise_for_status()
        completed_targets = response.json()

        found_completed = None
        for target in completed_targets:
            if target['id'] == target_id:
                found_completed = target
                break

        if found_completed:
            logger.info(f"✅ PASS: Completed target found in completed targets list")
            test_results.append(("Target in completed list", True))
        else:
            logger.error(f"❌ FAIL: Completed target not found in completed list")
            test_results.append(("Target in completed list", False))
            return False

    except Exception as e:
        logger.error(f"❌ FAIL: Error retrieving completed targets: {e}")
        test_results.append(("Target in completed list", False))
        return False

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    total_tests = len(test_results)
    passed_tests = sum(1 for _, passed in test_results if passed)

    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\nTotal: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        logger.info("\n🎉 TARGET ASSIGNMENT WORKFLOW TEST PASSED!")
        logger.info("=" * 60)
        return True
    else:
        logger.error(f"\n❌ TARGET ASSIGNMENT WORKFLOW TEST FAILED ({total_tests - passed_tests} failures)")
        logger.error("=" * 60)
        return False


def main():
    """Main entry point"""
    try:
        # Test backend connectivity
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code != 200:
            logger.error(f"❌ Backend not healthy: {response.status_code}")
            sys.exit(1)

        logger.info(f"✅ Backend connected: {BACKEND_URL}\n")

        # Run workflow test
        success = test_target_workflow()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
