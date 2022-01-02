import requests
from bs4 import BeautifulSoup
from flask import flash

class PracujScrap:
    """ Skrypt pobierający url i wyciągający potrzebne informacje"""
    def __init__(self, url: str):
        self.job_url = url
        self.bad_url = False
        self.result_soup = self.main()
            
    def main(self):
        """Głowne działanie scrapera"""
        if self.check_pracuj_url():
            self.raw_html = self.check_response()
            if self.raw_html:
                self.ready_data = self.parser_html()
                return self.ready_data
            else:
                flash("Nieprawidłowy adres.", category="error")
                self.bad_url = True
                return self.bad_url
        else:
            flash("Nieprawidłowy adres.", category="error")
            self.bad_url = True
            return self.bad_url
        
    def check_pracuj_url(self):
        if "www.pracuj.pl/praca" in str(self.job_url):
            return True
        else:
            return False
        
        
    def check_response(self):
        """Sprawdzanie poprawności linku"""
        try:
            self.res = requests.get(self.job_url)
            self.res.raise_for_status()
        except Exception:
            flash("Nie znaleziono strony.", category="error")
            print(f"Bład, nie znaleziono strony.")
        else:
            self.res.encoding = self.res.apparent_encoding
            return self.res.text
        
    def parser_html(self):
        """Wyciąganie interesujących nas elementów"""
        self.doc = BeautifulSoup(self.raw_html, 'html.parser')
        try:
            self.job_name = self.doc.find('h1').string
            self.company_name = self.doc.select('h2[data-test="text-employerName"]')[0].getText().replace("O firmie", "")
            self.job_level = self.doc.select('div[data-test="sections-benefit-employment-type-name-text"]')[0].getText()
            self.offer_expire_date = self.doc.select('div.OfferView1YEokC')[0].getText().replace("do: ", "")
            self.work_place = self.doc.select('div[data-test="text-benefit"]')[0].getText().split(", ")[0]
            try:
                self.salary_from = self.doc.select('span.OfferView37GVCA')[0].getText().replace(u"\xa0", u" ")[:-1]
                self.salary_to = self.doc.select('span.OfferView2aAlUX')[0].getText().replace(u"\xa0", u" ")
            except IndexError:
                self.job_informations = {
                "job_name": self.job_name,
                "company_name": self.company_name,
                "job_level": self.job_level,
                "offer_expire_date": self.offer_expire_date,
                "work_place": self.work_place,
            }
            else:
                self.job_informations = {
                    "job_name": f"{self.job_name}",
                    "company_name": self.company_name,
                    "job_level": self.job_level,
                    "offer_expire_date": self.offer_expire_date,
                    "work_place": self.work_place,
                    "salary_from" : self.salary_from,
                    "salary_to": self.salary_to      
                }
        except IndexError:
            flash("Nieprawidłowy adres.", category="error")
            self.bad_url = True
            return self.bad_url
        else:
            return self.job_informations
    
class IndeedScraper:
    
    def __init__(self, url: str) -> None:
        self.job_url = url  
        self.bad_url = False
        self.result_soup = self.main()  
        
    def main(self):
        """Głowne działanie scrapera"""
        if self.check_indeed_url():
            self.raw_html = self.check_response()
            if self.raw_html:
                self.ready_data = self.parser_html()
                return self.ready_data
            else:
                flash("Nieprawidłowy adres.", category="error")
                self.bad_url = True
                return self.bad_url
        else:
            flash("Nieprawidłowy adres.", category="error")
            self.bad_url = True
            return self.bad_url
        
    def check_indeed_url(self):
        if "www.indeed.com/praca" in str(self.job_url):
            return True
        else:
            return False
        
        
    def check_response(self):
        """Sprawdzanie poprawności linku"""
        try:
            self.res = requests.get(self.job_url)
            self.res.raise_for_status()
        except Exception:
            flash("Nie znaleziono strony.", category="error")
            print(f"Bład, nie znaleziono strony.")
        else:
            self.res.encoding = self.res.apparent_encoding
            return self.res.text
        
    def parser_html(self):
        """Wyciąganie interesujących nas elementów"""
        self.doc = BeautifulSoup(self.raw_html, 'html.parser')
        try:
            self.job_name = self.doc.find('h1').string
            self.company_name = self.doc.select('h2[data-test="text-employerName"]')[0].getText().replace("O firmie", "")
            self.job_level = self.doc.select('div[data-test="sections-benefit-employment-type-name-text"]')[0].getText()
            self.offer_expire_date = self.doc.select('div.OfferView1YEokC')[0].getText().replace("do: ", "")
            self.work_place = self.doc.select('div[data-test="text-benefit"]')[0].getText().split(", ")[0]
            try:
                self.salary_from = self.doc.select('span.OfferView37GVCA')[0].getText().replace(u"\xa0", u" ")[:-1]
                self.salary_to = self.doc.select('span.OfferView2aAlUX')[0].getText().replace(u"\xa0", u" ")
            except IndexError:
                self.job_informations = {
                "job_name": self.job_name,
                "company_name": self.company_name,
                "job_level": self.job_level,
                "offer_expire_date": self.offer_expire_date,
                "work_place": self.work_place,
            }
            else:
                self.job_informations = {
                    "job_name": f"{self.job_name}",
                    "company_name": self.company_name,
                    "job_level": self.job_level,
                    "offer_expire_date": self.offer_expire_date,
                    "work_place": self.work_place,
                    "salary_from" : self.salary_from,
                    "salary_to": self.salary_to      
                }
        except IndexError:
            flash("Nieprawidłowy adres.", category="error")
            self.bad_url = True
            return self.bad_url
        else:
            return self.job_informations
        