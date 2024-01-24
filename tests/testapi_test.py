def test_app(client):
    response=client.get(
        '/'
    )
    value=response.json
    assert value['status']=='ready'
    assert response.status_code==200