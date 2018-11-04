'''Natch Sirisumpun 5930156421'''

Rules =  { 1  : ["line", "pgm"],
           2  : ["EOF"],
           3  : ["line_num", "stmt"],
           4  : ["asgmnt"],
           5  : ["if"],
           6  : ["print"],
           7  : ["goto"],
           8  : ["stop"],
           9  : ["id", "=", "exp"],
           10 : ["term", "exp'"],
           11 : ["+", "term"],
           12 : ["-", "term"],
           13 : [],
           14 : ["id"],
           15 : ["const"],
           16 : ["IF", "cond", "line_num"],
           17 : ["term", "cond'"],
           18 : ["<", "term"],
           19 : ["=", "term"],
           20 : ["PRINT", "id"],
           21 : ["GOTO", "line_num"],
           22 : ["STOP"]                      }

Parser = { "pgm to line_num"  : 1,
           "pgm to EOF"       : 2,
           "line to line_num" : 3,
           "stmt to id"       : 4,
           "stmt to IF"       : 5,
           "stmt to PRINT"    : 6,
           "stmt to GOTO"     : 7,
           "stmt to STOP"     : 8,
           "asgmnt to id"     : 9,
           "exp to id"        : 10,
           "exp to const"     : 10,
           "exp' to +"        : 11,
           "exp' to -"        : 12,
           "exp' to EOF"      : 13,
           "exp' to line_num" : 13,
           "term to id"       : 14,
           "term to const"    : 15,
           "if to IF"         : 16,
           "cond to id"       : 17,
           "cond to const"    : 17,
           "cond' to <"       : 18,
           "cond' to ="       : 19,
           "print to PRINT"   : 20,
           "goto to GOTO"     : 21,
           "stop to STOP"     : 22  }

Values = { "line_num" : [str(e) for e in range(0, 1001)],
           "id"       : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
           "const"    : [str(e) for e in range(0, 101)]     }

ReservedWord = {"IF", "PRINT", "GOTO", "STOP", "EOF", "+", "-", "<", "="}

def update(stack, parse) :
    stack = stack[:len(stack)-1]
    x = Rules[Parser[parse]]
    for e in x[::-1] :
        stack.append(e)
    return stack

'''input from keyboard'''
'''1.scanner'''
l = list()
while (True) :
    x = input().strip()
    l.append(x)
    if (x == "EOF") :
        break
print(l, '\n')

'''2.Parser to Bcode'''
stack = list()
ALL_Bcode = list()
stack.append("pgm")
i = 0
while (len(stack) != 0) :
    x = l[i].split()
    t = "check"
    Bcode = list()
    if (x[0] == "EOF") :
        while (stack[len(stack)-1] != "EOF") :
            parse = stack[len(stack)-1] + " to EOF"
            stack = update(stack, parse)
        stack = stack[:len(stack)-1]
    else :
        while (stack[len(stack)-1] != "line_num") :
            parse = stack[len(stack)-1] + " to line_num"
            stack = update(stack, parse)
        if (x[0] in Values["line_num"]) :
            Bcode.append(("#line", x[0]))
            stack = stack[:len(stack)-1]
    for e in x[1:] :
        if (t == "GOTO") :
            if (e in Values["line_num"]) :
                Bcode.append(("#goto", e))
                stack = stack[:len(stack)-1]
                t = "check"
        elif (t == "IF" and e == x[len(x)-1]) :
            if (e in Values["line_num"]) :
                Bcode.append(("#goto", e))
                stack = stack[:len(stack)-1]
                t = "check"
        elif (e in Values["id"]) :
            while (stack[len(stack)-1] != "id") :
                parse = stack[len(stack)-1] + " to id"
                stack = update(stack, parse)
            Bcode.append(("#id", e))
            stack = stack[:len(stack)-1]
        elif (e in Values["const"]) :
            while (stack[len(stack)-1] != "const") :
                parse = stack[len(stack)-1] + " to const"
                stack = update(stack, parse)
            Bcode.append(("#const", e))
            stack = stack[:len(stack)-1]
        elif (e in ReservedWord) :
            if (e == "STOP") :
                while (stack[len(stack)-1] != e) :
                    parse = stack[len(stack)-1] + " to " + e
                    stack = update(stack, parse)
                Bcode.append(("#stop", '0'))
                stack = stack[:len(stack)-1]
            elif (e == "PRINT") :
                while (stack[len(stack)-1] != e) :
                    parse = stack[len(stack)-1] + " to " + e
                    stack = update(stack, parse)
                Bcode.append(("#print", '0'))
                stack = stack[:len(stack)-1]
            elif (e == "GOTO") :
                while (stack[len(stack)-1] != e) :
                    parse = stack[len(stack)-1] + " to " + e
                    stack = update(stack, parse)
                t = "GOTO"
                stack = stack[:len(stack)-1]
            elif (e in ["+", "-", "<", "="]) :
                while (stack[len(stack)-1] != e) :
                    parse = stack[len(stack)-1] + " to " + e
                    stack = update(stack, parse)
                Bcode.append(("#op", e))
                stack = stack[:len(stack)-1]
            elif (e == "IF") :
                while (stack[len(stack)-1] != e) :
                    parse = stack[len(stack)-1] + " to " + e
                    stack = update(stack, parse)
                Bcode.append(("#if", '0'))
                t = "IF"
                stack = stack[:len(stack)-1]
    if len(Bcode) != 0 :
        ALL_Bcode.append(Bcode)
    i += 1
    
for e in ALL_Bcode :
    print(e)
print()

'''3.change to real B-code'''
d = dict()
x = 10
for e in ["#line", "#id", "#const", "#if", "#goto", "#print", "#stop", "#op"] :
    d[e] = str(x)
    x += 1
x = 1
for e in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" :
    d[e] = str(x)
    x += 1
x = 1
for e in "+-<=" :
    d[e] = str(x)
    x += 1

for e in ALL_Bcode :
    ans = list()
    for f in e :
        for k in f :
            if k in d:
                ans.append(d[k])
            else :
                ans.append(k)
    print(' '.join(ans))
print(0)   
    
