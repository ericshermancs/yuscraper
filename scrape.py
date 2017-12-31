import requests, os, re, time
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import TimeoutError
import traceback

import argparse
completedlist = []


def getjson(key):
	r = requests.get('http://www.yutorah.org/sidebar/getLectureDataJSON.cfm?shiurID={}'.format(key))
	j = r.json()
	
	if j == {}:
		print(key,'is empty. End of list?')
		with open('completedlist.txt','a+') as f:
			f.write(key+'\n')
			completedlist.append(key)
		return
	if j['mediaTypeCategory'] != 'audio':
		print(key,'is not audio')
		with open('completedlist.txt','a+') as f:
			f.write(key+'\n')
			completedlist.append(key)
		return
	if j['shiurIsFileMissingOnServer'] != 0:
		print(key,'is missing on server')
		with open('completedlist.txt','a+') as f:
			f.write(key+'\n')
			completedlist.append(key)
		return

	dlurl = dlurl = j['downloadURL']
	name = j['shiurTitle']
	name = re.sub('\s','_',name)
	author = j['shiurTeacherFullName']
	author = re.sub('\s','_',author)
	#category_json = j['postedInCategories']
	date = j['shiurDateFormatted']
	print(key,'\n',name , author , date,'\n', \
			dlurl, '\n', \
	'=========================================')
	r = requests.get(dlurl)
	try:
		os.makedirs('output/{}'.format(author))
	except:
		pass
	with open('output/{}/{}-{}-{}.mp3'.format(author,name,author,date),'wb') as f:
		f.write(r.content)
	with open('completedlist.txt','a+') as f:
		f.write(key+'\n')
		completedlist.append(key)
def main():
	if not os.path.isfile('completedlist.txt'):
		with open('completedlist.txt','w+') as f:
			pass
	with open('completedlist.txt','r+') as f:
		for line in f:
			completedlist.append(line.strip())

	print('YU Torah Web Scraper Built By Akiva Eric Sherman (@ericshermancs)\n')
	parser = argparse.ArgumentParser(description='YU Torah Web Scraper')
	parser.add_argument('-s','--start',help='Specify the lower bound of the range of numbers', default='709393',required=False)
	parser.add_argument('-e','--end',help='specify the upper bound of the range of numbers',default='900000', required = False)
	parser.add_argument('-t','--threads',help='Specify the number of threads',default='1',required=False)
	args = parser.parse_args()

	thread_count = int(args.threads)
	start = int(args.start)
	end = int(args.end)
	if thread_count == 1:
		print('########### WARNING ###########')
		print('USING ONLY 1 THREAD')
		print('IF THIS IS A MISTAKE, USE --thread TO SET THREAD COUNT')
		time.sleep(2)
	print('Threads:',thread_count)
	print('Lower bound:',start)
	print('Upper bound:',end)
	print('\n')

	executor = ThreadPoolExecutor(max_workers=thread_count)
	
	for i in range(start,end):
		key = str(i).zfill(6)
		if not key in completedlist:	
			executor.submit(getjson,key)
	

	executor.shutdown(wait=True)

	print('End of list. Goodbye!')


	


def test():
	r = r = requests.get('http://www.yutorah.org/sidebar/getLectureDataJSON.cfm?shiurID=888888')
	j = r.json()
	#pprint(j)
	#dlurl = j['downloadURL']
	#print(dlurl)
	pprint(j)

if __name__ == '__main__':
	#test()
	#exit(0)
	main()


