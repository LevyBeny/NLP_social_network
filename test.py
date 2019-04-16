import re
r = re.compile(r"< a href=.*(instagram|pinterest).*>")
test_str = "< a href=instagramblaa>"
test_res = r.search(test_str)
print(test_res)