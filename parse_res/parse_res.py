from bs4 import BeautifulSoup

def parse_res(respons):
    parsed_html = BeautifulSoup(respons, features="html.parser")
    text = parsed_html.body.find('div', attrs={'class':'calculator_area'}).text
    for 

if __name__ == "__main__":
    print(parse_res("abc"))
