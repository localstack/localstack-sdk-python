from pytest import cloudpods


@cloudpods(pod_name="cloudpod!!!!")
def test_something():
    print("Running the test!")
    assert 1 == 1