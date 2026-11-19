"""
TruthLens AI - Automated Test Suite
Verifies:
1. Valid news text -> Real or Fake + confidence
2. Empty input -> Validation / safe handling
3. Same input twice -> Consistent output
4. Long input -> Sub-second processing latency
"""

import time
from predictor import predictor_instance


def run_tests():
    print("=" * 65)
    print("TRUTHLENS AI - SYSTEM VALIDATION SUITE")
    print("=" * 65)

    passed_count = 0

    # Test Case 1: Valid news text
    print("\n[TEST 1] Valid News Text...")
    sample_text = "Reserve Bank of India announces new digital currency pilot program for commercial banks."
    res1 = predictor_instance.predict(sample_text)
    assert res1['success'] is True, "Test 1 failed: Expected success=True"
    assert res1['label'] in ["Real", "Fake"], "Test 1 failed: Expected valid label"
    assert 0.0 <= res1['confidence'] <= 100.0, "Test 1 failed: Expected valid confidence"
    print(f" -> PASS: Valid prediction obtained ({res1['label']}, Confidence: {res1['confidence']}%)")
    passed_count += 1

    # Test Case 2: Empty input
    print("\n[TEST 2] Empty Input Validation...")
    res2 = predictor_instance.predict("   \n\t  ")
    assert res2['success'] is False, "Test 2 failed: Expected success=False for blank input"
    print(f" -> PASS: Safe error handling on blank input: '{res2['error']}'")
    passed_count += 1

    # Test Case 3: Same input twice
    print("\n[TEST 3] Same Input Twice (Determinism & Consistency)...")
    identical_text = "NASA Mars rover discovers ancient sedimentary rocks indicating liquid water presence."
    run_a = predictor_instance.predict(identical_text, log_to_db=False)
    run_b = predictor_instance.predict(identical_text, log_to_db=False)
    assert run_a['label'] == run_b['label'], "Test 3 failed: Labels differed across runs"
    assert abs(run_a['confidence'] - run_b['confidence']) < 1e-4, "Test 3 failed: Confidence differed"
    print(f" -> PASS: Identical output produced: Label={run_a['label']}, Conf={run_a['confidence']}%")
    passed_count += 1

    # Test Case 4: Long input
    print("\n[TEST 4] Long Input (Large Article Processing)...")
    long_article = (
        "The World Meteorological Organization along with leading global environmental researchers "
        "have released a comprehensive multi-decade climate assessment documenting shifts in surface "
        "temperatures and polar ice cap extent. The technical monograph compiles satellite radar observations, "
        "oceanic buoy measurements, and atmospheric carbon sensors across ninety-five member nations. "
        "Scientists emphasized the necessity for unified national policies regarding decarbonization, "
        "investments in high-capacity electricity grids, and preservation of forested wetlands. "
    ) * 15
    start_time = time.time()
    res4 = predictor_instance.predict(long_article, log_to_db=False)
    duration = time.time() - start_time
    assert res4['success'] is True, "Test 4 failed: Long input processing failed"
    assert duration < 1.0, f"Test 4 failed: Inference took too long ({duration:.3f}s)"
    print(f" -> PASS: Long input ({len(long_article.split())} words) processed in {duration*1000:.1f}ms! (Label: {res4['label']})")
    passed_count += 1

    print("\n" + "=" * 65)
    print(f"ALL {passed_count}/4 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
