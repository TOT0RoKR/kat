import vim
import kat.ui.render
from kat.katconfig import Katconfig

nameFileTree = vim.eval("g:KATBufNameFileTree")
nameTagList = vim.eval("g:KATBufNameTagList")
nameExplorer = vim.eval("g:KATBufNameExplorer")

def currentTabpageNumber():
    return vim.eval('tabpagenr()')

tabpages = {}       # global tabpages. 
class TabPage:
    def __init__(self, katconfig, global_tags):
        self.tabpageNumber = currentTabpageNumber()
        self.tabpage = vim.current.tabpage
        self.katconfig = katconfig
        self.buf_filetree = []      # buf contents
        self.buf_taglist = []       # buf contents
        self.buf_explorer = []      # buf contents
        self.global_tags = global_tags
        self.matched_filetree = {}  # what is matched between files and filetree
        self.matched_explorer = {}  # if multiple tags are matched this is made.
                                    # otherwise, this is empty.
        self.helplen = 0
        tabpages[self.tabpageNumber] = self


def window_number(kind):
    tmp = None
    if kind == 'filetree':
        tmp = int(vim.eval("bufwinnr(\"" + nameFileTree + "\")"))
    elif kind == 'taglist':
        tmp = int(vim.eval("bufwinnr(\"" + nameTagList + "\")"))
    elif kind == 'explorer':
        tmp = int(vim.eval("bufwinnr(\"" + nameExplorer + "\")"))
    return tmp


def findSuitableWindowOfNewFile(tab):
    backupWindow = vim.current.window
    window = None
    for w in tab.tabpage.windows:
        filename = w.buffer.name.split("/")[-1]
        if filename != nameFileTree \
                and filename != nameTagList \
                and filename != nameExplorer:
            bufinfo = vim.eval("getbufinfo(winbufnr(" + str(w.number) \
                        + "))[0]")
            if bool(int(bufinfo['hidden'])) is True:
                continue
            if bool(int(bufinfo['listed'])) is False:
                continue
            if bool(int(bufinfo['loaded'])) is False:
                continue
            if window is None:
                window = w
            if bool(int(bufinfo['changed'])) is False:
                window = w
                return window
    if window is not None:
        vim.current.window = window
    vim.command("silent bo vert new")
    window = vim.current.window
    vim.current.window = backupWindow
    return window
