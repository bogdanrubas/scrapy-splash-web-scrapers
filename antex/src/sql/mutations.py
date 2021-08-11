def add_log_to_db(spider, item):
  spider.cursor.execute('''INSERT INTO logs VALUES (%s, %s, %s, %s, %s)''', (
      item['time'],
      item['type'],
      item['location'],
      item['url'],
      item['description']
  ))
  spider.connection.commit()

def add_error_to_db(spider, item):
  if spider.name == 'firstRun':
    spider.cursor.execute('''INSERT INTO errors0 VALUES (%s, %s, %s)''', (
        item['depth'],
        item['url'],
        item['meta']
    ))
    spider.connection.commit()
  elif spider.name == 'debugRun':
    spider.cursor.execute(f'''INSERT INTO {spider.runCount} VALUES (%s, %s, %s)''', (
          item['depth'],
          item['url'],
          item['meta']
      ))
    spider.connection.commit()

def add_product_to_db(spider, item):
  spider.cursor.execute('''INSERT INTO products VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
      item['url'],
      item['category'],
      item['sub_category'],
      item['name'],
      item['price_brutto'],
      item['in_stock'],
      item['sklad'],
      item['gramatura'],
      item['szerokosc'],
      item['belka'],
      item['icons'],
      item['description']
  ))
  spider.connection.commit()