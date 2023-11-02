import re

# str = 'Filesystem      Size  Used Avail Use% Mounted on \n /dev/nvme0n1p3   18G  4.9G   13G  28% /'
# test = re.search(r'.*', str).string
# print(test)


str = '3.20%'
a = str.replace('\n', '').replace('%', ' ').strip(' ')
my_list = [x for x in a.split()]
print(my_list)




# line = "some cats are smarter than dogs are true"
# mat1 = re.match(r".* are", line)
# mat2 = re.match(r".*? are", line)
#
# print(mat1)
# print(mat2)
# print(mat1.group(0))
