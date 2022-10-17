from airflow.utils.edgemodifier import Label
from datetime import datetime, timedelta
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import Variable
from tasks import *

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


## Do not change the code below this line ---------------------!!#
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
## Do not change the code above this line-----------------------##

with DAG(
    'DesafioAirflow',
    default_args=default_args,
    description='Desafio de Airflow da Indicium',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = """
        Esse é o desafio de Airflow da Indicium.
    """
   
    #Task to get order table in csv
    export_order_to_csv = PythonOperator(
        task_id='order_to_csv',
        python_callable=order_to_csv,
        provide_context=True
   )

    #Task to get order details table in csv
    export_order_details_to_csv = PythonOperator(
        task_id='order_details_to_csv',
        python_callable=order_details_to_csv,
        provide_context=True
   )

    #Task to join the tables and get the sums of the quantities
    merge_and_export = PythonOperator(
        task_id='export_output',
        python_callable=merge_sum_export,
        provide_context=True
    )

    #Task to export final answer
    export_final_output = PythonOperator(
        task_id='export_final_output',
        python_callable=export_final_answer,
        provide_context=True
    )
    
    #Ordering of tasks
    export_order_to_csv >> export_order_details_to_csv >> merge_and_export >> export_final_output
