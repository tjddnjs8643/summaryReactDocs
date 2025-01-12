import requests
from bs4 import BeautifulSoup
import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize

# NLTK 리소스를 다운로드
nltk.download('punkt')
nltk.download('punkt_tab')

# 리액트 공식 문서에서 검색어에 맞는 내용을 가져오는 함수
def search_react_docs(query):
    base_url = "https://ko.legacy.reactjs.org/docs/getting-started.html"
    edit_url = "https://ko.legacy.reactjs.org/"
    
    response = requests.get(base_url)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", href=True)
    matching_urls = []

    for link in links:
        relative_url = link['href']
        if relative_url.startswith("/docs/"):
            full_url = edit_url + relative_url[1:]

            page_response = requests.get(full_url)
            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                page_content = page_soup.get_text().lower()

                if query.lower() in page_content:
                    h1_tag = page_soup.find('h1')
                    title = h1_tag.get_text() if h1_tag else 'No Title'
                    matching_urls.append((full_url, title))

    return matching_urls

# NLTK 기반 요약 함수
def summarize_text_with_nltk(text):
    sentences = sent_tokenize(text)
    # 상위 3개의 문장만을 요약으로 선택
    return ' '.join(sentences[:10])

# 페이지에서 검색어가 포함된 내용을 가져오는 함수
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()
        return content
    else:
        return "검색어가 포함된 내용이 없습니다."

# Streamlit UI 및 애플리케이션 실행 함수
def main():
    st.title("React Docs Summarizer")

    query = st.text_input("검색어를 입력하세요:")

    if query:
        matching_urls = search_react_docs(query)
        if matching_urls:
            st.write("요약을 원하는 항목을 선택하세요.")
            for i, (url, title) in enumerate(matching_urls):
                if st.button(f"{title}", key=f"button_{i}"):
                    content = get_page_content(url)
                    if content:
                        summary = summarize_text_with_nltk(content)
                        st.write(summary)
                    else:
                        st.write("일치하는 내용이 없습니다.")
        else:
            st.write("검색어와 일치하는 내용이 없습니다.")

if __name__ == "__main__":
    main()
