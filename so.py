import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page() :
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div", {"class" : "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True) # strip이란 빈칸 다 제거
    return int (last_page) # int이유는 페이지를 정수로 반환하기 위함
   
def extract_job(html) :
    title = html.find("h2" , {"class" : "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class" : "mb4"}).find_all("span", recursive=False)
    # recursive는 span이 겹겹이 있을때 첫번째 span만 가져오는 결과를 보여준다.
    # 또한 겹겹히 쌓여있을때 하나씩 변수를 저장해주면서 unpacing이 가능하다 ]
    # 첫번재 리스트를 company 두번재 리스트를 location 으로 자동으로 해준다. 
    company = company.get_text(strip=True).strip("\n")
    location = location.get_text(strip=True).strip("-").strip("\n")
    job_id = html['data-jobid']

    return {'title' : title, 'company' : company, 'location' : location, 'apply_link' : f"https://stackoverflow.com/jobs/{job_id}"}



# def안에서만 함수가 정의되고 벗어나서는 똑같은 함수를 정의해도된다.
def extract_jobs(last_page) :
    jobs = []
    for page in range(last_page) :
        print(f"Scrapping SO : Page : {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div" , {"class" : "-job"})
        for result in results : 
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs() :
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs