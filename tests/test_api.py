def test_api(client):
    res = client.get('/')
    assert res.status_code == 200
    assert (res.get_data()).decode() == "Hello, World!"