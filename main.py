#from compiler import to_program
#from reader import read, Literal, Expr
from rpython.config.translationoption import get_combined_translation_config
from util import STDIN, STDOUT, STDERR, read_file, write
import api
import base
import evaluator.loader
import space
import sys, os
config = get_combined_translation_config(translating=True)
if config.translation.continuation:
    import green

#def interactive():
#    module = space.Module(u'shell', {}, extends=base.module)
#    prompt = u"pyl> "
#    write(STDOUT, prompt)
#    source = os.read(0, 4096).decode('utf-8')
#    while source != u"":
#        try:
#            program = to_program(read(source))
#            write(STDOUT, program.call([module]).repr() + u"\n")
#        except space.Error as error:
#            print_traceback(error)
#        write(STDOUT, prompt)
#        source = os.read(0, 4096).decode('utf-8')
#    if source == u"":
#        write(STDOUT, u"\n")
#    return 0
#
#def batch(path):
#    module = space.Module(u'main', {}, extends=base.module)
#    try:
#        source = read_file(path)
#    except OSError, error:
#        os.write(2, "[Errno %d]: %s\n" % (error.errno, path) )
#        return 1
#    try:
#        program = to_program(read(source))
#        program.call([module])
#    except space.Error as error:
#        print_traceback(error)
#        return 1
#    return 0

#def entry_point(argv):
#    E = 10 # Debugging assist
#    green.process.init(config)
#    api.init(argv)
#    if len(argv) <= 1:
#        return interactive()
#    for arg in argv[1:]:
#        if arg == '-E0':
#            E = 0
#        elif arg == '-E1':
#            E = 1
#        elif arg == '-E2':
#            E = 2
#        elif E == 0:
#            # At this option, we're just parsing the input.
#            try:
#                source = read_file(arg)
#            except OSError, error:
#                os.write(2, "[Errno %d]: %s\n" % (error.errno, arg) )
#                return 1
#            for exp in read(source):
#                write(STDOUT, exp.repr() + u"\n")
#        else:
#            status = batch(arg)
#            if status != 0:
#                return status
#    return 0

def entry_point(argv):
    if config.translation.continuation:
        green.process.init(config)
    api.init(argv)
    try:
        for arg in argv[1:]:
            module = space.Module(u'main', {}, extends=base.module)
            program = evaluator.loader.from_file(arg)
            result = program.call([module])
            os.write(1, (result.repr() + u'\n').encode('utf-8'))
    except space.Error as error:
        print_traceback(error)
        return 1
    return 0

def print_traceback(error):
    out = u""
    if len(error.stacktrace) > 0:
        out = u"Traceback:\n"
    for frame, start, stop in reversed(error.stacktrace):
        out += u"    %s: %s %s\n" % (
            frame.module.name, start.repr(), stop.repr())
    out += error.__class__.__name__.decode('utf-8')
    write(STDERR, out + u": " + error.message + u"\n")

def target(*args):
    return entry_point, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()

if __name__=='__main__':
    sys.exit(entry_point(sys.argv))
