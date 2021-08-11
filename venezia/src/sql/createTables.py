def create_products_table(self):
    self.cursor.execute('''DROP TABLE IF EXISTS products''')
    self.cursor.execute('''CREATE TABLE products(
          url text,
          category text,
          sub_category text,
          sub_sub_category text,
          artykul text,
          name text,
          color text,
          old_price float,
          new_price float,
          description text,
          description_table text
        )''')


def create_logs_table(self):
    self.cursor.execute('''DROP TABLE IF EXISTS logs''')
    self.cursor.execute('''CREATE TABLE logs(
      time text,
      type text,
      location text,
      url text,
      description text
    )''')


def create_errors_table(self):
    self.cursor.execute('''DROP TABLE IF EXISTS errors0''')
    self.cursor.execute('''CREATE TABLE errors0(
      depth int,
      url text,
      meta text
    )''')


def create_debug_errors_table(self, runCount):
    self.cursor.execute(f'''DROP TABLE IF EXISTS errors{runCount}''')
    self.cursor.execute(f'''CREATE TABLE errors{runCount}(
      depth int,
      url text,
      meta text
    )''')


def create_tables(self, runCount):
    if (self.name == 'firstRun'):
        # ? scraper:
        create_logs_table(self)
        create_errors_table(self)
        # ? website:
        create_products_table(self)
    elif (self.name == 'debugRun'):
        # ? scraper:
        create_logs_table(self)
        create_debug_errors_table(self, runCount)
        # ? website:
        create_products_table(self)
