from dmoj import judgeenv
from dmoj.citest import ci_test

EXECUTORS = ['AWK', 'BF', 'C', 'CPP03', 'CPP11', 'CLANG', 'CLANGX',
             'JAVA8', 'PERL', 'PY2', 'PY3', 'RUBY2', 'SED', 'TEXT']
OVERRIDES = {}


def main():
    judgeenv.env['runtime'] = {}
    judgeenv.env['extra_fs'] = {}

    print 'Using extra allowed filesystems:'
    for lang, fs in judgeenv.env['extra_fs'].iteritems():
        print '%-6s: %s' % (lang, '|'.join(fs))
    print

    print 'Testing executors...'

    ci_test(EXECUTORS, OVERRIDES)


if __name__ == '__main__':
    main()
