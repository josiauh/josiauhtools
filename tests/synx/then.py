from josiauhtools_josiauh import synx

def foo():
    return 'bar'

def bar(p):
    print("i got " + p)

synx.then(foo, bar)