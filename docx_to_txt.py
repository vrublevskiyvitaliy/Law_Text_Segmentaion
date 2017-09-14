import docx2txt

a = docx2txt.process('documents/file0.docx').encode('utf-8')
f = open('file0.txt', 'w')
f.write(a)