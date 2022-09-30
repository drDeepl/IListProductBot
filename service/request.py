import requests
from io import BytesIO
from pdf2image import convert_from_bytes


def get_schedule():
    url = r"https://schedule-api.nbikemsu.ru/schedule/?groups=3426"
    response = requests.get(url)
    response_JSON = response.json()
    response.close()
    return response_JSON.get("results")

def download_schedule(url):
    response = requests.get(url)
    response_pdf_schedule= response.content
    pdf_bytes = BytesIO(response_pdf_schedule)
    with open("./images/schedule.pdf", "wb") as file:
        for byte in pdf_bytes:
            file.write(byte)
    response.close()
    return
