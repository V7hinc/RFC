#! /usr/bin/python
'''
  File      : getRFC.py
'''
import urllib, os, shutil, time
import hashlib


def downloadHtmlPage(url, tmpf=''):
    i = url.rfind('/')
    fileName = url[i + 1:]
    if tmpf: fileName = tmpf
    print url, "->", fileName
    urllib.urlretrieve(url, fileName)
    print 'Downloaded ', fileName
    time.sleep(0.2)
    return fileName

def get_status(url):
    res = urllib.urlopen(url)
    page_status = res.getcode()
    return page_status

def get_md5(file_path):
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5

def del_specify_md5(md5,file_path):
    md5_demo="1197f290bae092c70a6cf07a223ed8bc"
    if md5 == md5_demo:
        os.remove(file_path)

# http://www.networksorcery.com/enp/rfc/rfc1000.txt
# http://www.networksorcery.com/enp/rfc/rfc6409.txt
if __name__ == '__main__':
    addr = 'http://www.networksorcery.com/enp/rfc'
    dirPath = "RFC"
    startIndex = 1
    #startIndex = int(raw_input('start : '))
    #endIndex = 6786
    endIndex = 8000
    #endIndex = int(raw_input('end : '))
    if startIndex > endIndex:
        print 'Input error!'
    if False == os.path.exists(dirPath):
        os.makedirs(dirPath)
    fileDownloadList = []
    logFile = open("log.txt", "w")
    for i in range(startIndex, endIndex + 1):
        try:
            t_url = '%s/rfc%d.txt' % (addr, i)
            status = get_status(t_url)
            if not status == 200:
                print t_url,"is not exists"
                continue
            print t_url
            fileName = downloadHtmlPage(t_url)
            oldName = './' + fileName
            newName = './' + dirPath + '/' + fileName
            if True == os.path.exists(oldName):
                shutil.move(oldName, newName)
                print 'Moved ', oldName, ' to ', newName
            '''
            file_path = newName
            md5 = get_md5(file_path)
            del_specify_md5(md5, file_path)
            '''
        except:
            msgLog = 'get %s failed!' % (i)
            print msgLog
            logFile.write(msgLog + '\n')
            continue
    logFile.close()
