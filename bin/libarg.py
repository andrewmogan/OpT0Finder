import sys,os

if sys.version_info.major == 3:
    import subprocess
    dirs=[]
    for d in os.listdir(os.environ['FMATCH_BUILDDIR']):
        if not len([x for x in os.listdir('%s/%s' % (os.environ['FMATCH_BUILDDIR'],d)) if x.endswith('.o')]): continue
        dirs.append(d)
    libs=[x for x in subprocess.getoutput('flashmatch-config --libs').split() if not x.startswith('-lflashmatch')]
    libs+= ['-L%s' % subprocess.getoutput('root-config --libdir').rstrip('\n'), '-lMinuit']
    libs+= subprocess.getoutput('root-config --libs').split()
else:
    import commands
    dirs=[]
    for d in os.listdir(os.environ['FMATCH_BUILDDIR']):
        if not len([x for x in os.listdir('%s/%s' % (os.environ['FMATCH_BUILDDIR'],d)) if x.endswith('.o')]): continue
        dirs.append(d)
    libs=[x for x in commands.getoutput('flashmatch-config --libs').split() if not x.startswith('-lflashmatch')]
    libs+= ['-L%s' % commands.getoutput('root-config --libdir').rstrip('\n'), '-lMinuit']
    libs+= commands.getoutput('root-config --libs').split()
if 'PYTHON_LIB' in os.environ:
    libs+= [" -L{} -lpython{}.{}".format(os.environ["PYTHON_LIB"].strip(), 
        sys.version_info.major, 
        sys.version_info.minor)]

objs_list=[]
dict_list=[]
for l in dirs:
    d='%s/%s' % (os.environ['FMATCH_BUILDDIR'],l)
    #print d, os.path.isdir(d)
    #print os.listdir(d)
    src_obj = ['%s/%s' % (d,x) for x in os.listdir(d) if x.endswith('.o') and not x.endswith('Dict.o')]
    dic_obj = ['%s/%s' % (d,x) for x in os.listdir(d) if x.endswith('Dict.o')]

    if len(src_obj) == 0 and len(dic_obj) == 0: continue
    
    objs_list.append(src_obj)
    dict_list.append(dic_obj)
    #print objs_list[-1]
    #print dict_list[-1]

if not dict_list and not objs_list: sys.exit(0)

libname = '%s/libflashmatch.so' % os.environ['FMATCH_LIBDIR']
    
cmd='-o %s ' % libname
base_ts = None
if os.path.isfile(libname):
    base_ts=os.path.getmtime(libname)

skip_build = base_ts is not None
for objs in objs_list:
    for obj in objs:
        cmd += '%s ' % obj
        ts = os.path.getmtime(obj)
        if skip_build and ts > base_ts:
            skip_build = False

if skip_build: sys.exit(0)

for d in dict_list:
    if d: cmd += '%s ' % d[0]

for l in libs:
    cmd += '%s ' % l

if 'build' in sys.argv: print(1)
else: print(cmd)
sys.exit(1)
