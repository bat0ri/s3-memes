def test_get_meme_by_id(client):
    response = client.get("/memes/1")
    assert response.status_code == 200


def test_get_meme_by_id_not_found(client):
    response = client.get("/memes/2")
    assert response.json()['meme']['oid'] != 2


def test_get_all_memes(client):
    response = client.get("/memes", params={"page": 1, "paginator": 10})
    assert response.status_code == 200


def test_get_all_memes_not_found(client):
    response = client.get("/memes", params={"page": 2, "paginator": 10})
    assert response.status_code == 200
    assert response.json() == {"memes": []}


def test_post_meme(client):
    with open("tests/app/image.png", "rb") as img:
        response = client.post(
            "/memes",
            files={"file": img},
            params={"title": "MockData"},
        )
        assert response.status_code == 201
        assert response.json()["meme"]["title"] == "MockData"

        assert response.json()["meme"]["content_size"] == 100

        assert response.json()["meme"]["content_type"] == "png"


def test_put_meme(client):
    with open("tests/app/image.png", "rb") as img:
        response = client.put(
            '/memes/1',
            params={"title": "MockDataUpdate"},
            files={"file": img}
        )
        assert response.status_code == 200
        assert response.json()["Файл загружен как"] == '1.png'
        assert response.json()['Исходник'] == 'image.png'