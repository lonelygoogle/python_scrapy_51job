import requests
from multiprocessing import Queue
from lxml import etree
import threading
from study_mongo.handle_mongo import insert_data

# 处理页码类
class Crawl_page(threading.Thread):
	# 重写父类
	def __init__(self, thread_name, page_queue, data_queue):
		super(Crawl_page, self).__init__()
		self.thread_name = thread_name
		self.page_queue = page_queue
		self.data_queue = data_queue
		self.header = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
			"Connection": "keep-alive",
			"Cookie": "guid=83ccf6fda9111071eb858c0563c23189; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60010000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60110300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; adv=adsnew%3D0%26%7C%26adsnum%3D2004282%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.0s0000aEzMPC0P5XBxctrtY91NkaLf5h11dRMy4d3Bk0sny_lRBOS72ArHigHoOOG_vAMUBfHJZgx59Tm9qGWVUwT5P4mtDu5iHSyb4R7tgv2dz3ORIRmHKyoQ7aLg0XOQFG9wpQkLW7kjhveYXjmtU3HnJ1XGQ0jZMHeM6aISmnKH_J7Y-rSgPNSbZsl4S1KnuPhc00QFw8pgOy3RsGbeQme0NW.7b_NR2Ar5Od66CHnsGtVdXNdlc2D1n2xx81IZ76Y_uQQr1F_zIyT8P9MqOOgujSOODlxdlPqKMWSxKSgqjlSzOFqtZOmzUlZlS5S8QqxZtVAOtIO0hWEzxkZeMgxJNkOhzxzP7Si1xOvP5dkOz5LOSQ6HJmmlqoZHYqrVMuIo9oEvpSMG34QQQYLgFLIW2IlXk2-muCyr1FkzTf.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqPH7JUvc0IgP-T-qYXgK-5H00mywxIZ-suHY10ZIEThfqPH7JUvc0ThPv5HmdPHnL0ZNzU7qGujYkPHD3PjD1PWDY0Addgv-b5HDznWRzrjT40AdxpyfqnH0vPjfvrHD0UgwsU7qGujYknHR1P0KsI-qGujYs0APzm1Y1rjms%2526ck%253D3087.3.98.378.169.370.172.142%2526dt%253D1593674413%2526wd%253D51job%2526tpl%253Dtpl_11534_22672_18815%2526l%253D1518413614%2526us%253DlinkName%25253D%252525E6%252525A0%25252587%252525E5%25252587%25252586%252525E5%252525A4%252525B4%252525E9%25252583%252525A8-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E3%25252580%25252590%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A751Job%252525E3%25252580%25252591-%25252520%252525E5%252525A5%252525BD%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%2521%252526linkType%25253D%26%7C%26",
			"DNT": "1",
			"Host": "search.51job.com",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "none",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
		}

	def run(self):
		print('当前处理页码的任务是%s' % self.thread_name)
		while not page_flag:
			try:
				page = self.page_queue.get(block = False)
				print(page)
				page_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,'+str(page)+'.html'
				# print('当前构造的url为%s' % page_url)
				response = requests.get(url=page_url, headers=self.header)
				response.encoding = 'gbk'
				self.data_queue.put(response.text)
			except:
				pass


# 处理文本类
class Crawl_html(threading.Thread):
	def __init__(self, thread_name, data_queue, lock):
		super(Crawl_html, self).__init__()
		self.thread_name = thread_name
		self.data_queue = data_queue
		self.lock = lock

	def run(self):
		print('启动处理文本任务的线程为%s' % self.thread_name)
		while not data_flag:
			try:
				text = self.data_queue.get(block= False)
				result = self.parse(text)
				with self.lock:
					insert_data.insert_db(result)
			except:
				pass

	def parse(self, text):
		html_51jobs = etree.HTML(text)
		all_div = html_51jobs.xpath('//div[@id="resultList"]//div[@class="el"]')
		info_list = []
		for item in all_div:
			info = {}
			info['job_name'] = item.xpath('./p/span/a/@title')[0]
			info['company_name'] = item.xpath('.//span[@class="t2"]/a/@title')[0]
			info['company_address'] = item.xpath('.//span[@class="t3"]/text()')[0]
			try:
				info['salary'] = item.xpath('.//span[@class="t4"]/text()')[0]
			except IndexError:
				info['salary'] = '无数据'
			info['publish_time'] = item.xpath('.//span[@class="t5"]/text()')[0]
			info_list.append(info)
		return info_list


page_flag = False
data_flag = False

def main():
	# 定义2个队列
	page_queue = Queue()
	data_queue = Queue()

	lock = threading.Lock
	for page in range(0,680):
		page_queue.put(page)
		# print()

	print('当前页码队列的总量为%s' % page_queue.qsize())
	crawl_page_list = ['页码线程处理1号', '页码线程处理2号', '页码线程处理3号']
	page_thread_list = []
	for thread_name_page in crawl_page_list:
		thread_page = Crawl_page(thread_name_page, page_queue, data_queue)
		# 启动线程
		thread_page.start()
		page_thread_list.append(thread_page)

	# 设置3个线程，用于处理文本数据
	parseList = ['文本线程处理1号', '文本线程处理2号', '文本线程处理3号']
	parse_thread_list = []
	for thread_name_parse in parseList:
		thread_parse = Crawl_page(thread_name_parse, data_queue, lock)
		# 启动线程
		thread_parse.start()
		parse_thread_list.append(thread_parse)

	# 设置线程的退出机制
	global page_flag
	while not page_queue.empty():
		pass
	page_flag = True

	# 结束页面处理线程
	for thread_page_join in page_thread_list:
		thread_page_join.join()
		print(thread_page_join.thread_name, '处理结束')

	# 设置文本线程的退出机制
	global data_flag
	while not data_queue.empty():
		pass
	data_flag = True
	for thread_parse_join in parse_thread_list:
		thread_parse_join.join()
		print(thread_parse_join.thread_name, '处理结束')


if __name__ == '__main__':
	main()

