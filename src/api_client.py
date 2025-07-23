import requests

def fetch_bulk_postcodes(batch):
    url = "https://api.postcodes.io/postcodes"
    headers = {"Content-Type": "application/json"}

    payload = {
        "geolocations": [{"longitude": row["lon"], "latitude": row["lat"]} for row in batch]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"⚠️ Error en respuesta: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error al llamar API: {e}")
        return []
