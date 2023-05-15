from bs4 import BeautifulSoup
import requests

class AspFlow:
    def __init__(self, url, default_headers, default_filename) -> None:
        self.session = requests.Session()
        response = self.session.get(url, headers=default_headers)
        self.page = BeautifulSoup(response.text, 'html.parser')
        self.url = url
        self.default_headers = default_headers
        self.default_filename = default_filename

    def click(self, target_id, event_argument=None, download_result=False, **kwargs):
        print(f"Clicking {target_id}")
        viewstate = self.page.find('input', {'name': '__VIEWSTATE'})['value']
        eventvalidation = self.page.find('input', {'name': '__EVENTVALIDATION'})['value']
        viewstategenerator = self.page.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

        data = {
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTARGUMENT': event_argument,
            '__LASTFOCUS': '',
            '__EVENTTARGET': target_id,
            **kwargs
        }
        response = self.session.post(self.url, data=data, headers=self.default_headers)

        if download_result:
            with open(self.default_filename, 'wb') as f:
                f.write(response.content)
        else:
            self.page = BeautifulSoup(response.text, 'html.parser')

        return self