import tkinter as tk
from tkinter.ttk import Treeview
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from PIL import ImageTk, Image
import os
import sqlite3
 
root = tk.Tk()
root.geometry('600x620')
root.title('ESTOQUE INTELIGENTE')
 
 
def init_database():
    if os.path.exists('Registration_Data.db'):
        load_data()
 
    else:
        connection = sqlite3.connect('Registration_Data.db')
 
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE data (
        id_number int,
        name text,
        age text,
        gender text,
        phone_number text,
        email text,
        image blob
        )
        """)
 
        connection.commit()
        connection.close()
 
 
def load_data():
    connection = sqlite3.connect('Registration_Data.db')
 
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM data
    """)
 
    connection.commit()
    data = cursor.fetchall()
    connection.close()
 
    if data:
        for item in record_table.get_children():
            record_table.delete(item)
 
        for r in range(len(data)):
            record_table.insert(parent='', iid=r, index='end', values=data[r][0:6])
 
    else:
        for item in record_table.get_children():
            record_table.delete(item)
 
 
image_data = b''
 
 
def read_open_image():
    global image_data, img
 
    path = askopenfilename()
    if path:
        read_image = open(path, 'rb')
        image_data = read_image.read()
        read_image.close()
 
        img = ImageTk.PhotoImage(Image.open(path))
        image_lb.config(image=img)
 
 
def delete_image():
    global image_data
 
    image_data = b''
    image_lb.config(image=default_image)
 
 
def check_id_already_exists(_id, update):
    connection = sqlite3.connect('Registration_Data.db')
 
    cursor = connection.cursor()
 
    cursor.execute(f"""
    SELECT id_number FROM data
    WHERE id_number == {_id}
    """)
 
    connection.commit()
    response = cursor.fetchall()
    connection.close()
 
    if update == 'update':
        index = int(record_table.selection()[0])
        selected_id = record_table.item(index, 'values')[0]
 
        if _id == selected_id:
            return False
 
        elif response:
            return True
 
        else:
            return False
 
    elif response:
        return True
 
    else:
        return False
 
 
def check_collect_data(order):
    if id_number.get() != '':
        if not check_id_already_exists(id_number.get(), update=order):
 
            if order == 'add':
                add_data(_id=id_number.get(),
                         _name=full_name.get(),
                         _age=age.get(),
                         _gender=gender.get(),
                         _phone_number=phone_number.get(),
                         _email=email_address.get())
 
            elif order == 'update':
                update_data(_id=id_number.get(),
                            _name=full_name.get(),
                            _age=age.get(),
                            _gender=gender.get(),
                            _phone_number=phone_number.get(),
                            _email=email_address.get())
        else:
            showerror('ESTOQUE INTELIGENTE', 'ID já existente')
            id_number.focus()
 
    else:
        showerror('ESTOQUE INTELIGENTE', 'Informe um ID')
 
 
def clear_data():
    global image_data
 
    id_number.delete(0, tk.END)
    full_name.delete(0, tk.END)
    age.delete(0, tk.END)
    gender.set('Retirada')
    phone_number.delete(0, tk.END)
    email_address.delete(0, tk.END)
 
    image_lb.config(image=default_image)
    image_data = b''
 
 
def clean_data():
    clear_data()
    load_data()
 
 
def add_data(_id, _name, _age, _gender, _phone_number,
             _email):
    connection = sqlite3.connect('Registration_Data.db')
 
    cursor = connection.cursor()
 
    cursor.execute(f"""
    INSERT INTO data VALUES({_id}, '{_name}', '{_age}', '{_gender}',
    '{_phone_number}', '{_email}', ?) 
    """, [image_data])
 
    connection.commit()
    connection.close()
 
    clear_data()
    load_data()
 
    showinfo('ESTOQUE INTELIGENTE', 'Adicionado com sucesso')
 
 
 
def update_data(_id, _name, _age, _gender, _phone_number,
                _email):
    if record_table.selection():
        index = int(record_table.selection()[0])
        selected_id = record_table.item(index, 'values')[0]
 
        connection = sqlite3.connect('Registration_Data.db')
 
        cursor = connection.cursor()
 
        cursor.execute(f"""
        UPDATE data SET name = '{_name}', age = '{_age}', gender = '{_gender}',
        phone_number = '{_phone_number}', email = '{_email}', image = ?
        WHERE id_number = {selected_id}
        """, [image_data])
 
        connection.commit()
 
        if _id != selected_id:
            cursor.execute(f"""UPDATE data SET id_number = {_id} WHERE id_number = {selected_id}""")
            connection.commit()
 
        connection.close()
 
        clear_data()
        load_data()
 
        showinfo('ESTOQUE INTELIGENTE', 'Atualizado com sucesso')
 
 
def delete_data():
    if record_table.selection():
        index = int(record_table.selection()[0])
        id_data = record_table.item(index, 'values')[0]
 
        connection = sqlite3.connect('Registration_Data.db')
 
        cursor = connection.cursor()
 
        cursor.execute(f"""
        DELETE FROM data WHERE id_number = {id_data}
            """)
 
        connection.commit()
        connection.close()
 
        load_data()
        clear_data()
 
        showinfo('ESTOQUE INTELIGENTE', 'Deletado com sucesso')
 
 
def put_data():
    global image_data, img
 
    if record_table.selection():
        index = int(record_table.selection()[0])
 
        data = record_table.item(index, 'values')
        clear_data()
 
        id_number.insert(tk.END, data[0])
        full_name.insert(tk.END, data[1])
        age.insert(tk.END, data[2])
        gender.set(data[3])
        phone_number.insert(tk.END, data[4])
        email_address.insert(tk.END, data[5])
 
        connection = sqlite3.connect('Registration_Data.db')
 
        cursor = connection.cursor()
 
        cursor.execute(f"""
 
        SELECT image FROM data
        WHERE id_number == {data[0]}
           """)
 
        connection.commit()
        response = cursor.fetchall()
        connection.close()
 
        if response[0] != (b'',):
            image_data = response[0][0]
            img_data = response[0][0]
 
            with open('.temp_pic', 'wb') as write_img:
                write_img.write(img_data)
                write_img.close()
 
            img = ImageTk.PhotoImage(Image.open('.temp_pic'))
            image_lb.config(image=img)
 
 
def search_record(_id):
    if _id != '':
 
        connection = sqlite3.connect('Registration_Data.db')
 
        cursor = connection.cursor()
 
        search_by_id_query = f""" SELECT id_number, name, age, gender, phone_number,
         email FROM data WHERE id_number == {_id}"""
 
        search_by_name_query = f""" SELECT id_number, name, age, gender, phone_number,
         email FROM data WHERE name LIKE '%{_id}%' """
 
        cursor.execute(search_by_name_query)
 
        connection.commit()
        response = cursor.fetchall()
        connection.close()
 
        if response:
            for item in record_table.get_children():
                record_table.delete(item)
 
            for r in range(len(response)):
                record_table.insert(parent='', iid=r, index='end', values=response[r])
 
        else:
            for item in record_table.get_children():
                record_table.delete(item)
 
 
 
    else:
        load_data()
 
 
main_frame = tk.Frame(root)
 
heading = tk.Label(main_frame, text='Sistema de Registro', bg='#008', fg= '#999',
                   font=('Bold', 18))
heading.pack(fill=tk.X)
 
image_frame = tk.Frame(main_frame)
 
default_image = tk.PhotoImage(file='1.png')
 
image_lb = tk.Label(image_frame, image=None,text="Sem imagem",
                    bd=2, relief=tk.SOLID)
image_lb.pack(side=tk.LEFT)
 
open_image_btn = tk.Button(image_frame, text='Abrir', font=('Bold', 12),
                           bg='#29cb4e', width=6,
                           command=read_open_image)
open_image_btn.pack(side=tk.LEFT, anchor=tk.S, padx=5)
 
delete_image_btn = tk.Button(image_frame, text='Deletar', font=('Bold', 12),
                             bg='red', width=6,
                             command=delete_image)
delete_image_btn.pack(side=tk.LEFT, anchor=tk.S, padx=5)
 
image_frame.pack(anchor=tk.W, pady=5)
 
form_frame = tk.Frame(main_frame)
 
id_lb = tk.Label(form_frame, text='ID do Lote', font=('Bold', 12))
id_lb.grid(row=0, column=0, sticky=tk.W, pady=2)
 
id_number = tk.Entry(form_frame, font=('Bold', 12))
id_number.grid(row=0, column=1)
 
full_name_lb = tk.Label(form_frame, text='Nome do Produto', font=('Bold', 12))
full_name_lb.grid(row=1, column=0, sticky=tk.W, pady=2)
 
full_name = tk.Entry(form_frame, font=('Bold', 12))
full_name.grid(row=1, column=1)
 
age_lb = tk.Label(form_frame, text='Custo', font=('Bold', 12))
age_lb.grid(row=2, column=0, sticky=tk.W, pady=2)
 
age = tk.Entry(form_frame, font=('Bold', 12))
age.grid(row=2, column=1)
 
gender_lb = tk.Label(form_frame, text='Forma de envio', font=('Bold', 12))
gender_lb.grid(row=3, column=0, sticky=tk.W, pady=2)
 
gender_btn_frame = tk.Frame(form_frame)
 
gender = tk.StringVar()
gender.set('Retirada')
 
male_btn = tk.Radiobutton(gender_btn_frame, text='Retirada', font=('Bold', 12),
                          variable=gender, value='Retirada')
male_btn.pack(side=tk.LEFT)
 
female_btn = tk.Radiobutton(gender_btn_frame, text='Entrega', font=('Bold', 12),
                            variable=gender, value='Entrega')
female_btn.pack(side=tk.LEFT)
 
gender_btn_frame.grid(row=3, column=1)
 
phone_number_lb = tk.Label(form_frame, text='Fornecedor', font=('Bold', 12))
phone_number_lb.grid(row=4, column=0, sticky=tk.W, pady=2)
 
phone_number = tk.Entry(form_frame, font=('Bold', 12))
phone_number.grid(row=4, column=1)
 
email_address_lb = tk.Label(form_frame, text='E-mail de contato', font=('Bold', 12))
email_address_lb.grid(row=5, column=0, sticky=tk.W, pady=2)
 
email_address = tk.Entry(form_frame, font=('Bold', 12))
email_address.grid(row=5, column=1)
 
form_frame.pack(anchor=tk.W, pady=5)
 
buttons_frame = tk.Frame(main_frame)
 
add_btn = tk.Button(buttons_frame, text='Adicionar', bg='#29cb4e', width=8,
                    font=('Bold', 12),
                    command=lambda: check_collect_data('add'))
add_btn.pack(side=tk.LEFT, padx=10)
 
update_btn = tk.Button(buttons_frame, text='Atualizar', bg='yellow', width=8,
                       font=('Bold', 12),
                       command=lambda: check_collect_data('update'))
update_btn.pack(side=tk.LEFT, padx=10)
 
delete_btn = tk.Button(buttons_frame, text='Deletar', bg='red', width=8,
                       font=('Bold', 12),
                       command=delete_data)
delete_btn.pack(side=tk.LEFT, padx=10)
 
clear_btn = tk.Button(buttons_frame, text='Limpar', bg='#ff7f27', width=8,
                      font=('Bold', 12),
                      command=clean_data)
clear_btn.pack(side=tk.LEFT, padx=10)
 
buttons_frame.pack(anchor=tk.W, pady=20)
 
main_frame.pack(anchor=tk.W, pady=5, padx=5)
 
main_frame.pack_propagate(False)
main_frame.configure(width=500, height=400)
 
record_frame = tk.Frame(root)
 
search_lb = tk.Label(record_frame, text='Procure pelo nome do produto',
                     font=('Bold', 12))
search_lb.pack(anchor=tk.W, padx=5)
 
search = tk.Entry(record_frame,
                  font=('Bold', 12))
search.pack(anchor=tk.W, padx=5, pady=10)
 
search.bind('<KeyRelease>', lambda e: search_record(search.get()))
 
record_table = Treeview(record_frame)
record_table.pack(fill=tk.X)
record_table.bind('<<TreeviewSelect>>', lambda e: put_data())
 
record_table['column'] = ['id', 'name', 'age', 'gender', 'phone number',
                          'email']
 
record_table.column('#0', stretch=tk.NO, width=0)
 
record_table.heading('id', text='ID do Lote', anchor=tk.W)
record_table.column('id', width=80, anchor=tk.W)
 
record_table.heading('name', text='Nome do Produto', anchor=tk.W)
record_table.column('name', width=100, anchor=tk.W)
 
record_table.heading('age', text='Custo', anchor=tk.W)
record_table.column('age', width=80, anchor=tk.W)
 
record_table.heading('gender', text='Forma de Envio', anchor=tk.W)
record_table.column('gender', width=80, anchor=tk.W)
 
record_table.heading('phone number', text='Fornecedor', anchor=tk.W)
record_table.column('phone number', width=120, anchor=tk.W)
 
record_table.heading('email', text='E-mail de contato', anchor=tk.W)
record_table.column('email', width=120, anchor=tk.W)
 
record_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
init_database()
root.mainloop()