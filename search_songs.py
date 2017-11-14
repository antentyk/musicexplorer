from auth import sp as client


def search(request, limit=5):
    try:
        response = client.search(q=request, limit=limit, offset=0, type='track')
        return [(item['id'],
                 item['uri'],
                 item['name'],
                 item['artists'][0]['name'],
                 item['popularity'])
                for item in response['tracks']['items']]
    except:
        return []