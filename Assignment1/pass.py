s1 = "wlA"
s2 = "31P"
s3= "g"
left = ['j', 'k', 'x', 'z']

for i in left:
    for j in left:
        if i==j:
            continue
        for k in left:
            if k==i or k==j:
                continue;
            print(s1+i+s2+j+s3+k)
            input()
