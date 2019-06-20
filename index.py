from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
   db_name = 'database.db'

   def __init__(self, window):
      self.wind = window
      self.wind.title('Products Application')

      ## Creating a Frame Container
      frame = LabelFrame(self.wind, text = 'Register a new product')
      frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

      ## Name input
      Label(frame, text = 'Name: ').grid(row = 1, column = 0)
      self.name = Entry(frame)
      self.name.focus()
      self.name.grid(row=1, column=1)

      ## Price input
      Label(frame, text='Price: ').grid(row=2, column=0)
      self.price = Entry(frame)
      self.price.grid(row=2, column=1)

      ## Button Add Product
      # sticky = De Oeste a Este (Todo el ancho disponible)
      ttk.Button(frame, text = 'Save', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

      # Output message
      self.message = Label(text = '', fg = 'red')
      self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

      ## Table
      self.tree = ttk.Treeview(height = 10, columns = 2)
      self.tree.grid(row = 4, column = 0, columnspan = 2)
      self.tree.heading('#0', text = 'Name', anchor = CENTER)
      self.tree.heading('#1', text = 'Price', anchor = CENTER)

      ## Buttons
      ttk.Button(text='Delete', command = self.delete_product).grid(row=5, column=0, sticky=W + E)
      ttk.Button(text='Edit', command = self.edit_product).grid(row=5, column=1, sticky=W + E)
      self.get_products()

   def run_query(self, query, parameters = ()):
      with sqlite3.connect(self.db_name) as conn:
         cursor = conn.cursor()
         result = cursor.execute(query, parameters)
         conn.commit()
      return result
   
   def get_products(self):
      # Obtener los datos de la tabla para limpiarla
      records = self.tree.get_children()      
      for element in records:
         self.tree.delete(element)

      # consultar los datos
      query = 'SELECT * FROM product ORDER BY name DESC'
      db_rows = self.run_query(query)
      for row in db_rows:
         self.tree.insert('', 0, text = row[1], values = row[2])

   def validation(self):
      return len(self.name.get()) != 0 and len(self.price.get()) != 0

   def add_product(self):
      self.message['text'] = ''
      if self.validation():
         # Insertar los datos
         query = 'INSERT INTO product VALUES(NULL, ?, ?)'
         parameters = (self.name.get(), self.price.get())
         self.run_query(query, parameters)
         self.message['text'] = 'Product {} added successfully'.format(self.name.get())
         self.get_products()
      else:
         self.message['text'] = 'Name and price are required'
      # limpiar los campos de texto
      self.name.delete(0, END)
      self.price.delete(0, END)
   
   def delete_product(self):
      self.message['text'] = ''
      try:
         self.tree.item(self.tree.selection())['text'][0]
      except IndexError:
         self.message['text'] = 'Please, select a record'
         return
      ##print(self.tree.item(self.tree.selection()))
      # Insertar los datos
      name = self.tree.item(self.tree.selection())['text']
      query = 'DELETE FROM product WHERE name = ?'
      self.run_query(query, (name, ))
      self.message['text'] = 'Record {} deleted successfully'.format(name)
      self.get_products()
   
   def edit_product(self):
      self.message['text'] = ''
      try:
         self.tree.item(self.tree.selection())['text'][0]
      except IndexError:
         self.message['text'] = 'Please, select a record'
         return
      # Actualizar los datos
      name = self.tree.item(self.tree.selection())['text']
      old_price = self.tree.item(self.tree.selection())['values'][0]
      # Crear una ventana encima
      self.edit_wind = Toplevel()
      self.edit_wind.title = 'Edit Product'

      #Old name
      Label(self.edit_wind, text = 'Old Name: ').grid(row = 0, column = 1)
      Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
      #New name
      Label(self.edit_wind, text = 'New Name: ').grid(row = 1, column = 1)
      new_name = Entry(self.edit_wind)
      new_name.grid(row = 1, column = 2)
      #Old price
      Label(self.edit_wind, text = 'Old Price: ').grid(row = 2, column = 1)
      Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
      #New price
      Label(self.edit_wind, text = 'New Price: ').grid(row = 3, column = 1)
      new_price = Entry(self.edit_wind)
      new_price.grid(row = 3, column = 2)

      Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
   
   def edit_records(self, new_name, name, new_price, old_price):
      query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
      parameters = (new_name, new_price, name, old_price)
      self.run_query(query, parameters)
      self.edit_wind.destroy()
      self.message['text'] = 'Record {} updated successfully'.format(name)
      self.get_products()

if __name__ == '__main__':
   window = Tk()
   application = Product(window)
   window.mainloop()
