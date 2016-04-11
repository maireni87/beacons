# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BeaconscrapePipeline(object):
    def process_item(self, item, spider):
        return item

def process_item(self, item, spider):
        if spider.conf['DO_ACTION']:
            try:
                item['news_website'] = spider.ref_object
                
                checker_rt = SchedulerRuntime(runtime_type='C')
                checker_rt.save()
                item['checker_runtime'] = checker_rt
                
                item.save()
                spider.action_successful = True
                spider.log("Item saved to Django DB.", logging.INFO)
                    
            except IntegrityError, e:
                spider.log(str(e), logging.ERROR)
                raise DropItem("Missing attribute.")
                
        return item