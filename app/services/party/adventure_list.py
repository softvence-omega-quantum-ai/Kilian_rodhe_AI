from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "service_account.json"  # your JSON file path


SERVICE_ACCOUNT_INFO={
  "type": "service_account",
  "project_id": "secret-beacon-457506-v0",
  "private_key_id": "6fd95694ebb615b310865a32707fd16e68cac9fa",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxI+cor4Q65nJp\nZdamEmEKH4CbHuDgmCRwchSqiarYgkAwpDKVFl0ey73ZVnAfvt9YMmW9iMxbBCOc\nkOXdYLltnb6djJIt84/zRpzEMhUprYRY/pSOs0FZz8RDs3uu2WE0dmQBuG8QmotU\nNXxsNxmBJi8xkdwIaiqQfHwVATiza1loSe5JzKNLksG7chFgZlmtD8YXz6ZhlSPD\nJaE8M+T0Yz9a67tYFqmlLss4xEMm1pfOrFZ5VJDjsX6tbmtkp87f99V+6gV7k8IN\nlXD1NxH+mODlWJD0wGe1lzwq/bbJFOMA98A0si4mW6eSEvFsBll0o8Iy22RTX9dR\nqcAC11gpAgMBAAECggEAAbUipJACko3How/2AH5TXKVemEA1Mz0MNuBGpjkzAijJ\nRR7EFQ9U4PfeUeLFLG0q2n8L34aaz7LLxBXafWaSCwY3AO5Kt3IuXE49Mx/3d8Ii\nMThtBq4gLmU0E2H+ynnyd66/eovEWFDhEHP+ic2DK61KTaxGBne9hsyIZqxvFz2o\nyMl3S7GL1w049wWEXEIwFUe8DMHwKsWCzD2rbu3jAYogkOg8NUw3FdYD6O7H1Mwo\naVZKDuEotl6lIoQN0kMTnoTFvBglyVIgq9y2qUqPRw7ibiyPz2oMsE6Q/+WBIsn+\nb9c0S36pi6awFdS55izVFVE2qY+wSjY8yAdnbXiS3QKBgQDxp4gTJ5htEeiO7+eR\nBBCc/BT9NUd2qwFjpqRokNkn+E+dfAFFoXLMWOPEm06mJfObE27fo23WecwJgjNR\nZqPBK6q9SfE4kQI8LQcNirfpcRGZ3uPv9aOvz2dWDYlx8UbolhiVNBeM8wJMKzkc\n2cxLlZaIOBAmpd6dFq46NtgyDQKBgQC7p+/qq4mZXTKmlxJmhG649LnQsEoD3TQw\n3TOm2Z9zKZxATJwAlyo+VA2I6l/tnH83sYjg1ZxVGJr++yKmx9vIK3sWCD4Ka/iN\n4m0mh3th2CANJ+PEkIr/rpFu/o3i3NE60FKz/RNet90pWVoxaEsr5gXW5Hc3o8Sz\nLtob+5wjjQKBgA+BTVTVTI1rAb3yHKyMUziPYBVjDsPJcxxeu9vNt3E+GHWlWDuM\ngV4lMfASevhkJP5FP+7vgIOravENPpexez5Qu/LLRMP5YehUh0hSJzy+OX/i8kMa\nQrdsGlhGJBSAg6k2wDsKjZxIl1QlzdNREi+jWHZDCp5ANElmBCXOEQ8dAoGBALri\nwTjApUSrYGowQg7/DRX+A6AmMVAv2G5hnbMpQHb8lbQjl6mu4k84flJAuFB3busU\nT/E6S3skChiuGxBmMifjxa1ngAH5DYygV3vrqaEEEMeJVnjISuXgAM69jKjGqUkd\nd3/xJn1KN2OarQxPha2uY1pkJaav3pFks6rypclxAoGAF2+I1rKB1RrT3/qIzz19\naaijtoPkSRqUtdBipLUuSDdeUDKGnVXai9rPbL3+fzeOraSStuae5JK+axGpUUzK\nA6/OiXZcDSXV+G8FWPOBSeKRJcD2N17X17nTGc1aIP1tsu8KkA1i0C5g+XNCB9OT\nntVpTkr/jrfgIWy/McxV6uI=\n-----END PRIVATE KEY-----\n",
  "client_email": "youtubedataapi@secret-beacon-457506-v0.iam.gserviceaccount.com",
  "client_id": "105338036550821392143",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/youtubedataapi%40secret-beacon-457506-v0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Authenticate with the service account
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )
# Authenticate directly from the dict
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)
youtube = build("youtube", "v3", credentials=credentials)

def search_youtube_videos(query: str, max_results: int = 5):

    # Search videos
    search_request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    search_response = search_request.execute()

    # Get video IDs
    video_ids = [item['id']['videoId'] for item in search_response['items']]

    # Fetch video details
    video_request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    video_response = video_request.execute()

    # Format results
    videos = []
    for item in video_response['items']:
        videos.append({
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "channel": item['snippet']['channelTitle'],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "views": item['statistics'].get('viewCount', 0)
        })

    return videos

# Example usage
if __name__ == "__main__":
    query = "Party Music Superhero Adventure"
    top_videos = search_youtube_videos(query)
    for v in top_videos:
        print(v)
