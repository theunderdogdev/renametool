import os
import re
files = os.listdir("E:/Songs/")
reg_mtch = re.compile("^[aA]la")
print(list(filter(lambda x: 'Alan' in x or 'alan' == 'x', files)))