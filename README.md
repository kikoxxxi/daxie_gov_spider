# DaXieGovSpider
---
This is a Scrapy project to scrape bidding information from http://www.daxie.gov.cn/col/col85336/index.html.
---
## Extracted data
This project extracts project name, combined with the respective date, bidder's name and detail url. 
The crawler use MySQL for storing data.
The extracted data in MySQL looks like this:
```
{
    'project_id': '1',
    'pro_name': '宁波大榭开发区管委会南广场音乐喷泉修缮工程',
    'pro_date': '2017-12-28',
    'com_name': '杭州金蓝喷泉有限公司',
    'original_url': 'http://www.daxie.gov.cn/art/2017/12/28/art_85336_5787265.html'
}
```
## Running the spiders
`scrapy crawl daxie_spider`
