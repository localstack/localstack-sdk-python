def test_reset_state(pytester):
    """Smoke test for the reset_state fixture"""
    pytester.makeconftest("")
    pytester.makepyfile(
        """
        def test_hello_default(reset_state):
            pass
    """
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
