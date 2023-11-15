from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re
import requests

def scrap_moongyeong(url = 'https://council.gbmg.go.kr/kr/member/name.do') -> ScrapResult:
    '''문경시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all('div', class_="profile"):
        data_uid = profile.find("a", class_="btn_profile")["data-uid"]
        
        if data_uid:
            url = f"https://council.gbmg.go.kr/common/async/member/{data_uid}.do"
            result = requests.get(url).json()
            name = result['name'] if result['name'] else "이름 정보 없음"
            party = result['party_nm'] if result['party_nm'] else "정당 정보 없음"

            councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="moongyeong",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_moongyeong())