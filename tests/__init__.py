def assert_response_eq(response, comparison):
    assert sorted(response.items()) == sorted(comparison.items())
