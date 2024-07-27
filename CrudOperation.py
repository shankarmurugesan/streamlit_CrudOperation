import streamlit as st
import mysql.connector

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 database="cruddb",
)
print(mydb)
mycursor = mydb.cursor(buffered=True)

def show():   
    display = '''
        SELECT * from aadhar
    '''
    mycursor.execute(display)
    save_display = mycursor.fetchall()
    for sd in save_display:
        adharid = st.write(f'adharid : {sd[0]}')
        name = st.write(f'name : {sd[1]}')
        sex = st.write(f'sex : {sd[2]}')
        age = st.write(f'age : {sd[3]}')
        dob = st.write(f'dob : {sd[4]}')
        address = st.write(f'address : {sd[5]}')
        st.write('-' * 50)

def select_show():

  #function to show the data
    adharid = st.text_input('Enter AdharID')

    #mysql command to select the data
    display = '''
        SELECT adharid,name,sex,age,dob,address from aadhar WHERE id = %s
    '''
  # we use %s to get the input outside from the command (it can be in the code or from user)
    value = adharid

  # cursor.execute is to execute the mysql command
    mycursor.execute(display,value)

  # we use fetchall / fetchone to save the data in a variable
    save_display = mycursor.fetchall()
    st.write(save_display)

def insert():
  #function to insert data
    adharid = st.text_input('Enter Adhar ID: ')
    name = st.text_input('Enter Name:')
    sex  = st.text_input('Enter Sex:')
    age= st.text_input('Enter Age:')
    dob= st.text_input('Enter DOB:')
    address= st.text_input('Enter Address:')

    data_in = '''
        INSERT INTO cruddb.aadhar(adharid,name,sex,age,dob,address) VALUES (%s, %s,%s,%s,%s,%s)
    '''
    value = (adharid,name,sex,age,dob,address)
    if st.button("Insert"):
      # cursor.execute is to execute the mysql command
        mycursor.execute(data_in,value)
      # connection.commit is to save the changes
        mydb.commit()
        st.success('Data Inserted')

def update():
  #function to update data
    command = '''SELECT adharid from aadhar'''
    mycursor.execute(command)
    id_data = mycursor.fetchall()
    select_id = st.selectbox('adharid: ', [adharid for adharid in id_data])

    if select_id : 
        update_name = st.text_input('Enter Name: ')
        # update_sex = st.text_input('Enter Sex: ')
        # update_age = st.text_input('Enter Age: ')
        # update_dob = st.text_input('Enter Dob: ')
        # update_address = st.text_input('Enter Address: ')

        if st.button('Update'):
            update_comd = '''
            UPDATE aadhar
            SET name = %s
            WHERE adharid = %s
            '''
            #val = (update_name, select_id[0], update_sex, select_id[1],update_age,select_id[2],update_dob,select_id[3],update_address ,select_id[4] )
            val = (update_name, select_id[0] )
            mycursor.execute(update_comd, val )
            mydb.commit()
            st.success('Data Updated')

def delete():
  #function for deleting data
    command = '''SELECT adharid from aadhar'''
    mycursor.execute(command)
    id_data = mycursor.fetchall()

    select_id = st.selectbox('adharid: ', [adharid for adharid in id_data]) 
    if select_id :
        display = '''
            SELECT adharid,name,sex,age,dob,address from aadhar where adharid = %s
        '''
        mycursor.execute(display,select_id)
        save_display = mycursor.fetchall()
        for sd in save_display : 
            st.write(f'id : {sd[0]}')
            st.write(f'name : {sd[1]}')
            st.write(f'sex : {sd[2]}')
            st.write(f'age : {sd[3]}')
            st.write(f'dob : {sd[4]}')
            st.write(f'address : {sd[5]}')
            st.write('-' * 50)

        if st.button('delete'):
            delete_comd = '''
                DELETE FROM aadhar
                WHERE adharid = %s
            '''
            value = select_id
            mycursor.execute(delete_comd,value)
            mydb.commit()
            st.success('data deleted')
def main():
    st.title('CRUD OPERATIONS')
    page = st.sidebar.selectbox('Select page', ['DISPLAY','INSERT','UPDATE','DELETE'])

    if page == 'DISPLAY':
        show()

    elif page == 'INSERT':
        insert()

    elif page == 'UPDATE':
        update()

    elif page == 'DELETE':
        delete()

if __name__ == "__main__":
    main()
