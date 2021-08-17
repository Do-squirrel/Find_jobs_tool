import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/취업?q=python&limit={LIMIT}"

def get_last_page () : 
    result = requests.get(URL)
    # indeed_result를 print시 <Response [200]> 작동된다는 뜻.
    # indeed_result.text print시 모든 html을 프린트한다.

    soup = BeautifulSoup(result.text, 'html.parser')
    # soup = BeautifulSoup(html_doc, 'html.parser')
    # 위에 쓰여진게 soup 공식인데, soup는 쉽게 말해 데이터를 분류해주는 역할을 한다.
    # 여기서 html_doc을 indeed_result.text 로 html document 를 가져와서 적어준것.

    pagination = soup.find("div", {"class" : "pagination"})
    # 페이지 관련 검사를 보면, div class="pagination"이 페이지를 나타낸다
    # 따라서 indeed_soup는 html을 가져왔으니까 여기서 find해라 어떤걸? div class pagination을 가진 정보들을 가져온다.

    links = pagination.find_all('a')
    # links는 pagination 변수 에서 find all 'a'를 찾아서 리스트를 만들어준것
    # 'a'는 페이지를 가르키는 html에서 2,3,4,5 페이지를 찾는것

    pages = []
    for link in links[:-1] :
        pages.append(int(link.string))
    # pages를 빈 리스트로 만들어주고 for문을 활용한다.
    # for문은 links 안에서 link라고하고 span을 찾아서 pages에 추가해라 

    max_page = pages[-1] +1
    #max_page를 [-1]로 마지막 값만 나오게 지정
    return max_page

def extract_job(html) : 
    jobTitle = html.find("h2", {"class": "jobTitle"})
    title = jobTitle.find("span").string
    company = html.find("span", {"class" : "companyName"})
    if title == "new":
      title = jobTitle.find_all("span")[1].string
    if company is not None :
      company = str(company.string)
    else : 
      company = jobTitle
    location = html.find("div", {"class" : "companyLocation"}).string
    job_id = html["data-jk"]
    return {'title' : title,  
    'company' : company, 
    'location' : location, 
    "link": f"https://kr.indeed.com/jobs?q=python&vjk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
       print(f"Scrapping page: {page}")
       result = requests.get(f"{URL}&start={page*LIMIT}")
       soup = BeautifulSoup(result.text, "html.parser")
       results = soup.find_all("a", {"class": "fs-unmask"})
       print("")
       for result in results:
          job = extract_job(result)
          jobs.append(job) 
    return jobs

def get_jobs() : 
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs