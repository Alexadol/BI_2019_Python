a=int(input())
c=str(input())
b=int(input())
if c in ['%','/','//'] and b==0:
    print('Деление на 0!')
elif c=='+':
    print(a+b)
elif c=='-':
    print(a-b)
elif c=='/':
    print(a/b)
elif c=='*':
    print(a*b)
elif c=='%':
    print(a%b)
elif c=='**':
    print(a**b)
elif c=='//':
    print(a//b)

