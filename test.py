import re

str = 'Filesystem      Size  Used Avail Use% Mounted on \n /dev/nvme0n1p3   18G  4.9G   13G  28% /'
test = re.search(r'.*', str).string
print(test)


# line = "some cats are smarter than dogs are true"
# mat1 = re.match(r".* are", line)
# mat2 = re.match(r".*? are", line)
#
# print(mat1)
# print(mat2)
# print(mat1.group(0))