import pandas as pd
from scipy.stats import iqr
from pykafka import KafkaClient
import datetime
import numpy as np

client = KafkaClient(hosts="127.0.0.1:9092")
#Selezione topic
topic = client.topics['test']
#Creazione di un simple consumer
consumer = topic.get_simple_consumer()
#!kafka-topics --zookeeper localhost:2181 --alter --topic test --config retention.ms=5


def out_uni(distr,y):
    Q1, Q3 = np.quantile(distr,[0.25, 0.75])
    IQR = iqr(distr)
    if (y < Q1 - 1.5 * IQR):
        return "OUTLIER [<Q1]"
    elif (y > Q3 + 1.5 * IQR):
        return "OUTLIER [>Q3]"
    else:
        return " "

db = pd.read_csv("/Users/riccardocervero/Desktop/Progetto Industry Lab/DbRidotto.csv")
values=[k for k in db.Coefficiente_140]    

i=0    
for message in consumer:
    if message is not None:
        file = open("/Users/riccardocervero/Desktop/Coefficiente.csv","a")
        file.write(str(datetime.datetime.now().time()))
        file.write(",")
        file.write(message.value.decode("utf-8"))
        file.write(",")
        file.write(out_uni(values,float(message.value.decode("utf-8"))))
        file.write("\n")
        values.append(float(message.value.decode("utf-8")))
        file.close()
        i=i+1
        print('Received',i,"\r",end="")

#consumer.stop()
