def create_logs_table(self):
    self.cursor.execute('''DROP TABLE IF EXISTS logs''')
    self.cursor.execute('''CREATE TABLE logs(
      time text,
      type text,
      location text,
      url text,
      description text
    )''')


def create_products_table(self):
    self.cursor.execute('''DROP TABLE IF EXISTS products''')
    self.cursor.execute('''CREATE TABLE products(
      url text,
      available boolean,
      category text,
      name text,
      new_price float,
      old_price float,
      images text,
      description text,
      sizes text,
      colors text
    )''')


def create_errors_table(self):
    self.cursor.execute('''DROP TABLE IF EXISTS errors0''')
    self.cursor.execute('''CREATE TABLE errors0(
      depth int,
      url text,
      meta text
    )''')


def create_tables(self):
    if (self.name == 'firstRun'):
        # ? scraper:
        create_logs_table(self)
        create_errors_table(self)
        # ? website:
        create_products_table(self)