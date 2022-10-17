<h1>1. Instalação </h1>
<h4>Crie um ambiente virtual em Python </h4>
$ python -m venv venv <br />
$ source venv/bin/activate <br />

<h4>Instalando o airflow.</h4>
$ bash install.sh<br /><br />
$ touch .env<br />
export AIRFLOW_HOME = (caminho desejado para a HOME do airflow)

<h1>2. Executando o projeto</h1> 
$ source .env<br />
$ airflow standalone<br />
Login e senha aparecerão no console.<br />
Acesso pelo navegador: http://0.0.0.0:8080/

<h1>3. Features</h1> 
<h4>Conecta com um banco de dados sqlite e exporta uma tabela order em csv</h4>

    def order_to_csv():
    
      # Read sqlite query results into a pandas DataFrame.
      con = sqlite3.connect("Northwind_small.sqlite")
      df = pd.read_sql_query("SELECT * FROM 'Order'", con)

      # Verify that result of SQL query is stored in the dataframe
      print(df.head())

      # Converting to CSV file
      df.to_csv("output_orders.csv")

      # Close Connection
      con.close()
<h4>Do mesmo banco de dados, exporta uma tabela order details em csv.</h4>

    def order_details_to_csv():
    
      # Read sqlite query results into a pandas DataFrame.
      con = sqlite3.connect("Northwind_small.sqlite")
      df = pd.read_sql_query("SELECT * FROM 'OrderDetail'", con)

      # Verify that result of SQL query is stored in the dataframe
      print(df.head())

      # Converting to CSV file
      df.to_csv("output_order_details.csv")

      # Close Connection
      con.close()
      
<h4>Mescla as duas tabelas, faz uma soma condicional das quantidades onde 'ShipCity' == 'Rio de Janeiro', e exporta um txt com o resultado</h4>

    def merge_sum_export():

      #Save the tables
      orders_table = pd.read_csv("output_orders.csv")
      order_details_table = pd.read_csv("output_order_details.csv")

      #Join tables
      left_merged = pd.merge(orders_table, order_details_table, how="left", left_on='Id', right_on='OrderId')
     
      #Conditional sum of quantities
      quantity = left_merged.loc[left_merged['ShipCity']=='Rio de Janeiro']['Quantity'].sum()

      #Write the answer
      with open('count.txt', 'w') as arquivo:
          arquivo.write(str(quantity))
          
<h4>Codifica a mensagem e gera um 'final_output.txt'</h4>

    def export_final_answer():
      
      import base64

      # Import count
      with open('count.txt') as f:
        count = f.readlines()[0]

      my_email = Variable.get("my_email")
      message = my_email+count
      message_bytes = message.encode('ascii')
      base64_bytes = base64.b64encode(message_bytes)
      base64_message = base64_bytes.decode('ascii')

      with open("final_output.txt","w") as f:
          f.write(base64_message)
      return None

<h1>4. Sobre o autor</h1> 
Róbson Samuel Hoffmann: https://www.linkedin.com/in/robson-samuel-hoffmann-225328191/

<h1>5. Licença</h1>
Apache License<br />
Version 2.0, January 2004<br />
http://www.apache.org/licenses/
