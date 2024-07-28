def test_InternalServerError(client):
    response = client.get('/throw_error/single')
    assert response.status_code == 500
    assert len(response.json) == 1
    assert response.json['description'] == 'Single arg'

    response = client.get('/throw_error/multi')
    assert response.status_code == 500
    assert len(response.json) == 1
    assert response.json['description'] == 'Multi arg'.split()

    description = (
    "The server encountered an internal error and was unable to"
    " complete your request. Either the server is overloaded or"
    " there is an error in the application."
    )

    response = client.get('/throw_error/none')
    assert response.status_code == 500
    assert len(response.json) == 1
    assert response.json['description'] == ''.join(description)

def test_NotFound(client):
    response = client.get('/unknownroute')
    assert response.status_code == 302
    response = client.get('/unknownroute', follow_redirects=True)
    assert len(response.history) == 1
    assert response.status_code == 200
    assert response.request.path == "/"

def test_BadRequest(client):
    res = client.get('/badrequest')
    assert res.status_code == 400
    assert res.json['description'] == "Testing BadRequest"