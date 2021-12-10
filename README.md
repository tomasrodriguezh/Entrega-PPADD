# Entrega-PPRDD
Entrega del curso Python para Recogida de Datos

Mi Proyecto con Criptomonedas

Este proyecto tiene la finalidad de graficar todos los pares disponibles de criptomonedas de la API de Kraken. 
Los gráficos incluidos son el OHLC, el VWAP y los volúmenes de venta de la criptomoneda deseada por el usuario. 
El usuario tiene la capacidad de elegir tanto la cripto deseada, como el par sobre la cual quiere ver el precio y volumen de las transacciones realizadas. 
Además, puede elegir el intervalo de tiempo sobre los que se calculan los candlesticks, así como la cantidad de candlesticks por los cuales se realiza el VWAP. 
Finalmente, tiene la oportunidad de cambiar la fecha desde la que desea obtener los datos.

Las limitaciones más importantes son que la API obtiene como máximo las últimas 720 observaciones de la moneda solicitada, comenzando desde el presente. 
Lo que impide generar gráficos de cualquier periodo de tiempo o con más observaciones. 
Por otro lado, hay algunas monedas que no generan tantas transacciones (ya sea una cripto o una moneda de un país en específico como el dólar australiano) 
o que son más jóvenes, lo que hace que no todos los gráficos sirvan para aportar información. 
Este último punto es importante, pero también representa el gran potencial del programa ya que en este se pueden utilizar cada una de las monedas disponibles
en Kraken; desde la más importante como el Bitcoin como otras casi desconocidas como el 1INCH. 

El trabajo se realizó utilizando streamlit. 
El cual tiene una barra lateral que se puede esconder, diversas cajas de selección, un slider y una caja para seleccionar la fecha. 
Además, da a conocer información de los precios del par solicitado y en ocasiones da advertencias, recomendaciones o datos de lo que se solicita.

La versión web del proyecto está en el siguiente link: https://share.streamlit.io/tomasrodriguezh/entrega-pprdd/main/app.py 

Para poder utilizar el código hace falta tener descargado Pipenv. 
En PyCharm: Una vez abierto hay que escribir en la terminal $ pipenv install , 
lo que descargará todos los paquetes utilizados en el ambiente virtual. 
Ya descargados los paquetes, simplemente hay que escribir en la terminal $ streamlit run app.py , 
lo que correrá la aplicación y abrirá un local host en el navegador. 
Con eso el usuario será capaz de hacer lo descrito anteriormente en su computador, que es lo mismo que en la página web del link adjuntado. 
