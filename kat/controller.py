from kat.lib.tag import Tag
from kat.lib.file import File
from kat.lib.scope import Scope
from kat.tracer import ccscanner as ccs
from kat.tracer import ccparser as ccp
from kat.tracer import ppscanner as pps
from kat.tracer import ppparser as ppp
from kat.ui.tabpage import *
import kat.ui.filetree as ft
import kat.ui.taglist as tl
import kat.ui.explorer as ep
from kat.katconfig import Katconfig

import vim

import codecs

def initializeKAT(configPath):
    config = Katconfig(configPath)
    kernel_root_dir = vim.vars['KATRootDir'].decode()

    katconfig = {}

    global_tags = {}
    global_tags['preprocess'] = {}
    global_tags['curconfig'] = {}
    cc_tags = []
    pp_tags = []

    files = []
    for it in config.files:
        files.append(File(it, kernel_root_dir + '/'))
    files = sorted(files, key=lambda x: x.path)
    katconfig['files'] = files
    
    i = 0
    files_nr = len(katconfig['files'])
    for it in katconfig['files']:
        i += 1
        print(str(i) + "/" + str(files_nr) + " - " + it.path)
        filename = kernel_root_dir + '/' + it.path
        #  with open(filename, "r", encoding="utf-8") as f:
        with open(filename, "r", encoding="utf-8") as f:
            try:
                raw_data = f.read()
            except UnicodeDecodeError:
                with open(filename, "r", encoding="iso-8859-1") as f2:
                    raw_data = f2.read()
        tokens = pps.scan(raw_data)
        it.scope = Scope(it.path, None, 0, 0)
        tags, _, _ = ppp.parse(tokens, it)
        pp_tags += tags

    #  pp_tags = sorted(pp_tags, key=lambda x: x.path.path)
    for it in pp_tags:
        if it.name in global_tags['preprocess']:
            global_tags['preprocess'][it.name].append(it)
        else:
            global_tags['preprocess'][it.name] = [it]
    
    #  print("files load success")

    kconfigs = []
    for it in config.kconfigs:
        kconfigs.append(File(it, vim.vars['KATRootDir'].decode() + '/'))
    kconfigs = sorted(kconfigs, key=lambda x: x.path)
    katconfig['kconfigs'] = kconfigs

    #  print("kconfigs load success")

    TabPage(katconfig, global_tags)
    #  print(type(tabpages[currentTabpageNumber()].global_tags))
    #  print(type(global_tags))

    ft.preInitialize()
    tl.preInitialize()
    ep.preInitialize()


