def file_operate(info1,info2,info3,info4):
    septal_line = '--------------------------\n'
    with open('info.log', 'a') as f:
        f.write(septal_line)
        f.write(info1)
        f.write(info2)
        f.write(info3)
        f.write(info4)
        f.write(septal_line)

a='aaaa\n'
b='bbbb\n'
c='cccc\n'
d='dddd\n'

file_operate(a,b,c,d)