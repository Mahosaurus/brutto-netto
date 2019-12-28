from request_page import request_form
from parse_res import parse_res

respons = request_form.request_website().decode("ISO-8859-1")
parsed_respons = parse_res.parse_res(respons)
