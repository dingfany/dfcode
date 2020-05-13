# encoding:utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter

def filebasicinfo(file):
    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(file)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 获取 PDF 文件的文档信息
    documentInfo = pdfFileReader.getDocumentInfo()
    print('documentInfo = %s' % documentInfo)
    # 获取页面布局
    pageLayout = pdfFileReader.getPageLayout()
    print('pageLayout = %s ' % pageLayout)

    # 获取页模式
    pageMode = pdfFileReader.getPageMode()
    print('pageMode = %s' % pageMode)

    xmpMetadata = pdfFileReader.getXmpMetadata()
    print('xmpMetadata  = %s ' % xmpMetadata)

    # 获取 pdf 文件页数
    pageCount = pdfFileReader.getNumPages()

    print('pageCount = %s' % pageCount)
    for index in range(0, pageCount):
        # 返回指定页编号的 pageObject
        pageObj = pdfFileReader.getPage(index)
        print('index = %d , pageObj = %s' % (index, type(pageObj)))  # <class 'PyPDF2.pdf.PageObject'>
        # 获取 pageObject 在 PDF 文档中处于的页码
        pageNumber = pdfFileReader.getPageNumber(pageObj)
        print('pageNumber = %s ' % pageNumber)

def splitPdf(inFile,outFile,pagestart, pageend):
    '''
    切分文档
    :param ipagestart: 要切分的文档的起始页，按照普通习惯，不是从0开始
    :param outFile:    合并后的输出文件
    :return:
    '''
    if pagestart < 1:
        print('wrong start page pageNumber')
        return
    if pageend < pagestart:
        print('end should bigger than start pageNumber')
        return    
 
    #since page index is from 0 to Numpages-1
    begin=pagestart-1 
    end=pageend

    pdfFileWriter = PdfFileWriter()

    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(inFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()
    if pageend > numPages:
        print('page end exceed totalpage, will split to end')
        end = numPages
    
    if numPages > pagestart:
        #range function not include 'end'
        for index in range(begin, end):
            pageObj = pdfFileReader.getPage(index)
            pdfFileWriter.addPage(pageObj)
    
        # 添加完每页，再一起保存至文件中
        pdfFileWriter.write(open(outFile, 'wb'))

def mergePdf(inFileList, outFile):
    '''
    合并文档
    :param inFileList: 要合并的文档的 list
    :param outFile:    合并后的输出文件
    :return:
    '''
    pdfFileWriter = PdfFileWriter()
    for inFile in inFileList:
        # 依次循环打开要合并文件
        pdfReader = PdfFileReader(open(inFile, 'rb'))
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)

        # 最后,统一写入到输出文件中
        pdfFileWriter.write(open(outFile, 'wb'))

myreport = 'data/MyFeeReport.pdf'
splited='data/aftersplit.pdf'
merged='data/aftermerge.pdf'


filebasicinfo(myreport)
splitPdf(myreport, splited,5,10)

mergelist = ['data/hetong1.pdf','data/hetong2.pdf',splited]
mergePdf(mergelist,merged)