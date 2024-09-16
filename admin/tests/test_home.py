from src.web import create_app 

app = create_app()
app.testing = True

client = app.test_client()


def test_home():
    response = client.get("/")

    assert 200 == response.status_code
    assert b"<h1>Inicio</h1>" in response.data