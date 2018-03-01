import sys

def getOpts():
    opts={}
    args=sys.argv
    lastKey='nokey'
    opts[lastKey]=[]

    while(args):
        if args[0][0]=='-':
            lastKey=args[0]
            opts[lastKey]=[]
        else:
            try:
                opts[lastKey].append(args[0])
            except:
                break
        args=args[1:]

    return opts