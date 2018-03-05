TARGET_INFO='''
~/Documents/dev/sreplacer/replace.py
https://github.com/Donaim/sreplacer.git
https://raw.githubusercontent.com/Donaim/sreplacer/master/replace.py
'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string

import urllib.request
import os
import subprocess
import re
import sys



        #########
       ## MODES ##
        #########

DEFAULT_MODE = 'auto'

class mode_funcs(object):
    
    
    def auto(at): raise Exception("Not supposed to be here")
    def _format_path(path):
        path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
        if (path[0] == '~'): return os.path.expanduser('~') + path[1:]
        else: return path
    
    def local(at):
        path = at.command
        path = mode_funcs._format_path(path)
        
        isdir = False
        if path[-1] == os.path.sep: isdir = True
        
        if isdir: path += 'lnkpy-run.py'
        
        try:
            subprocess.check_call([path] + sys.argv[1:], shell=True)
            # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
        except Exception as ex:
            print("Couldn't open file {}".format(path), file=sys.stderr)
            raise ex
    
    def _get_first_local(args_t):
        for a in args_t:
            if a.mode.name == 'local': return a 
    def web(at):
        def try_get_file_size(meta):
            re = 0.0
            try:
                re = int(meta.get("Content-Length"))
            except: pass
            return re
    
        target_at = mode_funcs._get_first_local(at.args_t)
        file_name = target_at.command
        file_name = mode_funcs._format_path(file_name)
        di = os.path.dirname(file_name)
        if not os.path.isdir(di): os.mkdir(di)
    
        url = at.command
        u = urllib.request.urlopen(url)
    
        meta = u.info()
        file_size = try_get_file_size(meta)
    
        f = open(file_name, 'wb')
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer: break
    
            file_size_dl += len(buffer)
            f.write(buffer)
       
            status = "downloading.. {:10d}b".format(file_size_dl)
            if file_size > 0: status += " ({:3.2f} %)".format(file_size_dl * 100. / file_size)
            print(status)
    
        f.close()
    
        mode_funcs.local(target_at)
    
    
    def git(at):
        repository = at.command
        first_local_at = mode_funcs._get_first_local(at.args_t)
        file = mode_funcs._format_path(first_local_at.command)
    
        try:
            subprocess.call(["git", "clone"] + [repository] + [os.path.dirname(file)])
            # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
        except Exception as ex:
            print("Couldn't download git repository {}".format(repository), file=sys.stderr)
            raise ex
    
        # after clonning - run
        first_local_at.invoke()
        


class mode_initializators(object):
    
        # The MIT License (MIT)
    
        # Copyright (c) 2013-2014 Konsta Vesterinen
    
        # Permission is hereby granted, free of charge, to any person obtaining a copy of
        # this software and associated documentation files (the "Software"), to deal in
        # the Software without restriction, including without limitation the rights to
        # use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
        # the Software, and to permit persons to whom the Software is furnished to do so,
        # subject to the following conditions:
    
        # The above copyright notice and this permission notice shall be included in all
        # copies or substantial portions of the Software.
    
        # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
        # FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
        # COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
        # IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
        # CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
        # SOURCE REPOSITORY: https://github.com/kvesteri/validators
    
    
    ip_middle_octet = u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
    ip_last_octet = u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    
    url_regex = re.compile(
        u"^"
        # protocol identifier
        u"(?:(?:https?|ftp)://)"
        # user:pass authentication
        u"(?:[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:]+"
        u"(?::[-a-z0-9._~%!$&'()*+,;=:]*)?@)?"
        u"(?:"
        u"(?P<private_ip>"
        # IP address exclusion
        # private & local networks
        u"(?:(?:10|127)" + ip_middle_octet + u"{2}" + ip_last_octet + u")|"
        u"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + u")|"
        u"(?:172\.(?:1[6-9]|2\d|3[0-1])" + ip_middle_octet + ip_last_octet + u"))"
        u"|"
        # private & local hosts
        u"(?P<private_host>"
        u"(?:localhost))"
        u"|"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?P<public_ip>"
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"" + ip_middle_octet + u"{2}"
        u"" + ip_last_octet + u")"
        u"|"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # resource path
        u"(?:/[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:@/]*)?"
        # query string
        u"(?:\?\S*)?"
        # fragment
        u"(?:#\S*)?"
        u"$",
        re.UNICODE | re.IGNORECASE
    )
    
    url_pattern = re.compile(url_regex)
    
    def _is_valid_url(value, public = False):
        result = mode_initializators.url_pattern.match(value)
        if not public:
            return result
    
        return result and not any((result.groupdict().get(key) for key in ('private_ip', 'private_host')))
    

    
    def _is_pathname_valid(pathname: str) -> bool: # https://stackoverflow.com/a/34102855/7038168
        try:
            
            if len(pathname) < 1: return False
            _, pathname = os.path.splitdrive(pathname)
            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law
            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
            for pathname_part in pathname.split(os.path.sep):
                try: os.lstat(root_dirname + pathname_part)
                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == 123: # ERROR_INVALID_NAME = 123
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        except TypeError as exc: return False
        else: return True
    
    def auto(at):
        def is_valid_git(string):
            return (string.startswith("https://") or string.startswith("http://")) and string.endswith(".git")
        if (mode_initializators._is_pathname_valid(at.command)):
            if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
            at.mode = at.mode_lookup['local']
        elif(mode_initializators._is_valid_url(at.command)):
            if(is_valid_git(at.command)):
                if not 'git' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
                at.mode = at.mode_lookup['git']
            else:
                if not 'web' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
                at.mode = at.mode_lookup['web']
        else: raise Exception("Path \"{}\" is neither local nor git".format(at.command))


########## parsing classes
mode_funcs_static = filter(lambda name: name[0] != '_', dir(mode_funcs))
mode_funcs_di = dict(map(lambda name: (name, getattr(mode_funcs, name)), mode_funcs_static))

mode_inits_static = filter(lambda name: name[0] != '_', dir(mode_initializators))
mode_inits_di = dict(map(lambda name: (name, getattr(mode_initializators, name)), mode_inits_static))

        ###########
       ## PARSING ##
        ###########

split = TARGET_INFO.split('\n')
filtered  = filter(lambda line: len(line) > 0 and not line.isspace() and line[0] != '#', split)

# filtered contains non-empty non-comment lines from TARGET_INFO

# for stderr

class arg_tuple(object):
    def __init__(self, command, mode):
        self.command = command
        self.mode = mode
        self.mode_lookup = mode_lookup
        self.args_t = args_t
    def invoke(self):
        try:
            self.mode.func(self)
            return True
        except Exception as ex:
            print(ex, file=sys.stderr)
            return False
class mode(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def invoke_all(self):
        for a_tuple in args_t:
            if a_tuple.mode == self: 
                if a_tuple.invoke(): return True
        return False
    def init(self, args):
        if self.name in mode_inits_di:
            init_func = mode_inits_di[self.name]
            for a_tuple in args:
                if a_tuple.mode == self:
                    init_func(a_tuple)

mode_lookup = dict(map(lambda p: (p[0], mode(p[0], p[1])), mode_funcs_di.items()))
args_t = []

def parse_args(lines):
    curr = mode_lookup[DEFAULT_MODE]
    for line in lines:
        if line[0] == '$':
            mname = line[1:].strip()
            if mname in mode_lookup:
                curr = mode_lookup[mname]
                continue
            # else: raise Exception("unknown mode name: {}".format(mname))
        args_t.append( arg_tuple(line, curr) )
parse_args(filtered)

for (name, m) in mode_lookup.items():
    m.init(args_t)
for t in args_t:
    if t.invoke(): break
