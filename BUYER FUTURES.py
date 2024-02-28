#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter
import time
from tkinter import ttk
from tkinter import *

from binance.client import Client
from datetime import datetime

variable = {}
with open('keys.txt', 'r') as file:
    for line in file:
        name, _, value = line.partition('=')
        variable[name.strip()] = value.strip()

BINANCE_API_KEY=(variable['BINANCE_API_KEY'])
BINANCE_API_SECRET_KEY=(variable['BINANCE_API_SECRET_KEY'])
MAX_AMOUNT=int((variable['MAX_AMOUNT']))
MIN_AMOUNT=int((variable['MIN_AMOUNT']))
APUESTA=int((variable['APUESTA'])) #cantidad de dinero que estas dispuesto a perder en la operacion

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET_KEY, testnet=False)

ventana=tkinter.Tk()
ventana.geometry("410x600")

#limit irders
price_coin=DoubleVar()
monto_coin=DoubleVar()
coin_tiket=StringVar()
stop_losses=DoubleVar()

#market orders
monto_coin_market=DoubleVar()
coin_tiket_market=StringVar()
stop_losses_market=DoubleVar()

    
def truncate(number,digits)-> float:
    startCounting=False
    if number<1:
        number_str=str('{:.20f}'.format(number))
        resp=''
        count_digits=0
        for i in range(0,len(number_str)):
            if number_str[i] !='0' and number_str[i] !='.' and number_str[i] !=',':
                startCounting=True
            if startCounting:
                count_digits=count_digits+1
            resp=resp+number_str[i]
            if count_digits==digits:
                break
        return float(resp)
    else:
        return round(number)

#caculate risk

def calculate_risk():
    if price_coin.get()>0:
        ticket_coin=coin_futures.get().upper()+"USDT"
        quantity_coins=truncate((float(monto_coin.get())/float(price_coin.get())),1)
        total2=quantity_coins*price_coin.get()
        total_loss=quantity_coins*stop_losses.get()
        riesgo=round(abs(total2-total_loss),2)
        label_box.config(text=" ")
        label_box1.config(text="Pair: "+ ticket_coin)
        label_box2.config(text=" ")
        label_box3.config(text=" ")
        label_box4.config(text=" ")
        label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures.get().upper())
        label_box6.config(text="APUESTA: "+str(riesgo)+" USDT")
        label_box7.config(text="")
    else:
        label_box.config(text="")
        label_box1.config(text="")
        label_box2.config(text="")
        label_box3.config(text="")
        label_box4.config(text="")
        label_box5.config(text="")
        label_box6.config(text="!!ERROR!! Check values")
        label_box7.config(text="")
        
def calculate_risk_market():
    ticket_coin_market=coin_futures_market.get().upper()+"USDT"
    if get_price_coin(ticket_coin_market)>0:
        price_coin_now=get_price_coin(ticket_coin_market)
        quantity_coins=truncate((float(monto_coin_market.get())/float(price_coin_now)),1)
        total2=quantity_coins*price_coin_now
        total_loss=quantity_coins*stop_losses_market.get()
        riesgo=round(abs(total2-total_loss),2)
        price_coin=get_price_coin(ticket_coin_market)
        label_box.config(text=" ")
        label_box1.config(text="Pair: "+ ticket_coin_market)
        label_box2.config(text=" ")
        label_box3.config(text=" ")
        label_box4.config(text=" ")
        label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures.get().upper())
        label_box6.config(text="APUESTA: "+str(riesgo)+" USDT")
        label_box7.config(text="")
        
    else:
        label_box.config(text="")
        label_box1.config(text="")
        label_box2.config(text="")
        label_box3.config(text="")
        label_box4.config(text="")
        label_box5.config(text="")
        label_box6.config(text="!!ERROR!! Check values")
        label_box7.config(text="")
    
#get price market coin

def get_price_coin(token_future):
    try:
        price_now = client.futures_mark_price(symbol = token_future)
        market_price=float(price_now.get('markPrice'))
        return (market_price)
    except:
        market_price=0
        return(market_price)

def buy_coin():

    if MAX_AMOUNT>monto_coin.get()>MIN_AMOUNT:
        label_box.config(text="!!!LONG!!!!")
        ticket_coin=coin_futures.get().upper()+"USDT"
        label_box1.config(text="Pair: "+ ticket_coin)
        label_box2.config(text="Limit order: "+price_futures.get())
        label_box3.config(text="Tamaño: "+monto_futures.get()+' USDT')
        label_box4.config(text="Stop loss: "+stop_futures.get())
        quantity_coins=truncate((float(monto_coin.get())/float(price_coin.get())),1)
        label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures.get().upper())
        total2=quantity_coins*price_coin.get()
        total_loss=quantity_coins*stop_losses.get()
        riesgo=round(abs(total2-total_loss),2)

        if riesgo>APUESTA:
            label_box2.config(text="")
            label_box3.config(text="")
            label_box4.config(text="")
            label_box5.config(text="")
            label_box6.config(text="!!!MUCHO RIESGO!!!")
            label_box7.config(text="REVISA EL SL")
        else:
            if price_coin.get()<stop_losses.get():
                label_box2.config(text="")
                label_box3.config(text="")
                label_box4.config(text="")
                label_box5.config(text="")
                label_box6.config(text="!!!ERROR!!!")
                label_box7.config(text="VERIFY PRICE & SL")
            else:
                try:
                    buyorder=client.futures_create_order(symbol=ticket_coin,side='BUY',type='LIMIT',quantity=quantity_coins,price=price_coin.get(),timeInForce='GTC')
                    time.sleep(3)
                    stop_loss_order=client.futures_create_order(symbol=ticket_coin,side='SELL',type='STOP_MARKET',stopPrice=stop_losses.get(),closePosition='true')
                    
                    label_box6.config(text="APUESTA: "+str(riesgo)+" USDT")
                    label_box7.config(text="")
                    
                    coin_futures.delete(0, END)
                    price_futures.delete(0, END)
                    monto_futures.delete(0, END)
                    stop_futures.delete(0, END)
            
                except:
                    label_box2.config(text="")
                    label_box3.config(text="")
                    label_box4.config(text="")
                    label_box5.config(text="")
                    label_box6.config(text="!!!ERROR!!!")
                    label_box7.config(text="CHECK SL & PRICE")



    else:
        label_box2.config(text="")
        label_box3.config(text="")
        label_box4.config(text="")
        label_box5.config(text="")
        label_box6.config(text="!!!ERROR!!!")
        label_box7.config(text="error de monto")


def sell_coin():
    if MAX_AMOUNT>monto_coin.get()>MIN_AMOUNT:
        label_box.config(text="!!!SHORT!!!!")
        ticket_coin=coin_futures.get().upper()+"USDT"
        label_box1.config(text="Pair: "+ ticket_coin)
        label_box2.config(text="Limit order: "+price_futures.get())
        label_box3.config(text="Tamaño: "+monto_futures.get()+' USDT')
        label_box4.config(text="Stop loss: "+stop_futures.get())
        quantity_coins=truncate((float(monto_coin.get())/float(price_coin.get())),1)
        label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures.get().upper())
        total2=quantity_coins*price_coin.get()
        total_loss=quantity_coins*stop_losses.get()
        riesgo=round(abs(total2-total_loss),2)
        
        if riesgo>APUESTA:
            label_box2.config(text="")
            label_box3.config(text="")
            label_box4.config(text="")
            label_box5.config(text="")
            label_box6.config(text="!!!MUCHO RIESGO!!!")
            label_box7.config(text="REVISA EL SL")
            
        else:
            if price_coin.get()>stop_losses.get():
                label_box2.config(text="")
                label_box3.config(text="")
                label_box4.config(text="")
                label_box5.config(text="")
                label_box6.config(text="!!!ERROR!!!")
                label_box7.config(text="VERIFY PRICE & SL")

            else:
                try:
                    sellorder=client.futures_create_order(symbol=ticket_coin,side='SELL',type='LIMIT',quantity=quantity_coins,price=price_coin.get(),timeInForce='GTC')
                    time.sleep(3)
                    stop_loss_order=client.futures_create_order(symbol=ticket_coin,side='BUY',type='STOP_MARKET',stopPrice=stop_losses.get(),closePosition='true')
                    
                    label_box6.config(text="APUESTA: "+str(riesgo)+" USDT")
                    label_box7.config(text="")
                    
                    coin_futures.delete(0, END)
                    price_futures.delete(0, END)
                    monto_futures.delete(0, END)
                    stop_futures.delete(0, END)
                    
                except:
                    label_box2.config(text="")
                    label_box3.config(text="")
                    label_box4.config(text="")
                    label_box5.config(text="")
                    label_box6.config(text="!!!ERROR!!!")
                    label_box7.config(text="CHECK SL & PRICE")
        #print(price_coin.get())
        #print(monto_coin.get())
        #print(stop_losses.get())

    else:
        label_box2.config(text="")
        label_box3.config(text="")
        label_box4.config(text="")
        label_box5.config(text="")
        label_box6.config(text="!!!ERROR!!!")
        label_box7.config(text="error de monto")
        
def buy_coin_market():

    if MAX_AMOUNT>monto_coin_market.get()>MIN_AMOUNT:
        label_box.config(text="!!!LONG!!!!")
        ticket_coin_market=coin_futures_market.get().upper()+"USDT"
        label_box1.config(text="Pair: "+ ticket_coin_market)
        
        if get_price_coin(ticket_coin_market)!=0:
            label_box2.config(text="Market Price: "+str(get_price_coin(ticket_coin_market)))
            price_coin_now=get_price_coin(ticket_coin_market)
            quantity_coins=truncate((float(monto_coin_market.get())/float(price_coin_now)),1)
            label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures_market.get().upper())
            total2=quantity_coins*price_coin_now
            total_loss=quantity_coins*stop_losses_market.get()
            riesgo=round(abs(total2-total_loss),2)
            price_coin=get_price_coin(ticket_coin_market)
        else:
            label_box2.config(text="Market Price: !!!ERROR!!! ")
            quantity_coins=0
            label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures_market.get().upper())
            riesgo=999999
            price_coin=99999999999999999
            
        label_box3.config(text="Tamaño: "+monto_futures_market.get()+' USDT')
        label_box4.config(text="Stop loss: "+stop_futures_market.get())
            
        if riesgo>APUESTA:
            label_box6.config(text="!!!MUCHO RIESGO!!!")
            label_box7.config(text="REVISA EL SL")
        else:
            if price_coin<stop_losses_market.get():
                label_box6.config(text="!!!ERROR!!!")
                label_box7.config(text="VERIFY PRICE & SL")
            else:
                try:
                    buyorder=client.futures_create_order(symbol=ticket_coin_market,side='BUY',type='MARKET',quantity=quantity_coins)
                    time.sleep(3)
                    stop_loss_order=client.futures_create_order(symbol=ticket_coin_market,side='SELL',type='STOP_MARKET',stopPrice=stop_losses_market.get(),closePosition='true')
                    label_box6.config(text="APUESTA: "+str(riesgo)+" USDT")
                    label_box7.config(text="")
                    coin_futures_market.delete(0, END)
                    monto_futures_market.delete(0, END)
                    stop_futures_market.delete(0, END)
            
                except:
                    label_box2.config(text="")
                    label_box3.config(text="")
                    label_box4.config(text="")
                    label_box5.config(text="")
                    label_box6.config(text="!!!ERROR!!!")
                    label_box7.config(text="CHECK SL & PRICE")



    else:
        label_box2.config(text="")
        label_box3.config(text="")
        label_box4.config(text="")
        label_box5.config(text="")
        label_box6.config(text="!!!ERROR!!!")
        label_box7.config(text="error de monto")


def sell_coin_market():
    if MAX_AMOUNT>monto_coin_market.get()>MIN_AMOUNT:
        label_box.config(text="!!!SHORT!!!!")
        ticket_coin_market=coin_futures_market.get().upper()+"USDT"
        label_box1.config(text="Pair: "+ ticket_coin_market)
        
        if get_price_coin(ticket_coin_market)!=0:
            label_box2.config(text="Market Price: "+str(get_price_coin(ticket_coin_market)))
            price_coin_now=get_price_coin(ticket_coin_market)
            quantity_coins=truncate((float(monto_coin_market.get())/float(price_coin_now)),1)
            label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures_market.get().upper())
            total2=quantity_coins*price_coin_now
            total_loss=quantity_coins*stop_losses_market.get()
            riesgo=round(abs(total2-total_loss),2)
            price_coin=get_price_coin(ticket_coin_market)
        else:
            label_box2.config(text="Market Price: !!!ERROR!!! ")
            quantity_coins=0
            label_box5.config(text="cantidad: " + str(quantity_coins)+" "+coin_futures_market.get().upper())
            riesgo=999999
            price_coin=0
            
        label_box3.config(text="Tamaño: "+monto_futures_market.get()+' USDT')
        label_box4.config(text="Stop loss: "+stop_futures_market.get())


        if riesgo>APUESTA:
            label_box2.config(text="")
            label_box3.config(text="")
            label_box4.config(text="")
            label_box5.config(text="")
            label_box6.config(text="!!!MUCHO RIESGO!!!")
            label_box7.config(text="REVISA EL SL")
        else:
            if price_coin>stop_losses_market.get():
                label_box2.config(text="")
                label_box3.config(text="")
                label_box4.config(text="")
                label_box5.config(text="")
                label_box6.config(text="!!!ERROR!!!")
                label_box7.config(text="VERIFY PRICE & SL")
            else:
                try:
                    buyorder=client.futures_create_order(symbol=ticket_coin_market,side='SELL',type='MARKET',quantity=quantity_coins)
                    time.sleep(3)
                    stop_loss_order=client.futures_create_order(symbol=ticket_coin_market,side='BUY',type='STOP_MARKET',stopPrice=stop_losses_market.get(),closePosition='true')
                    
                    label_box6.config(text="APUESTA: "+str(riesgo)+" USDT")
                    label_box7.config(text="")
                    
                    coin_futures_market.delete(0, END)
                    monto_futures_market.delete(0, END)
                    stop_futures_market.delete(0, END)
            
                except:
                    label_box2.config(text="")
                    label_box3.config(text="")
                    label_box4.config(text="")
                    label_box5.config(text="")
                    label_box6.config(text="!!!ERROR!!!")
                    label_box7.config(text="CHECK SL & PRICE")

    else:
        label_box2.config(text="")
        label_box3.config(text="")
        label_box4.config(text="")
        label_box5.config(text="")
        label_box6.config(text="!!!ERROR!!!")
        label_box7.config(text="error de monto")

#limit orders
#coin
coin_futures=tkinter.Entry(ventana, textvariable=coin_tiket,font= "Helvetica 15")
coin_futures.grid(row=1, column=1)

#price
price_futures=tkinter.Entry(ventana, textvariable=price_coin,font= "Helvetica 15")
price_futures.grid(row=2, column=1)

#monto
monto_futures=tkinter.Entry(ventana, textvariable=monto_coin,font= "Helvetica 15")
monto_futures.grid(row=3, column=1)

#stop loss
stop_futures=tkinter.Entry(ventana, textvariable=stop_losses,font= "Helvetica 15")
stop_futures.grid(row=4, column=1)

#Market Orders
#coin
coin_futures_market=tkinter.Entry(ventana, textvariable=coin_tiket_market,font= "Helvetica 15")
coin_futures_market.grid(row=15, column=1)

#monto
monto_futures_market=tkinter.Entry(ventana, textvariable=monto_coin_market,font= "Helvetica 15")
monto_futures_market.grid(row=16, column=1)

#stop loss
stop_futures_market=tkinter.Entry(ventana, textvariable=stop_losses_market,font= "Helvetica 15")
stop_futures_market.grid(row=17, column=1)

etiqueta=tkinter.Label(ventana, text="LIMIT", fg='black', bg="light pink", font= "Helvetica 15")
etiqueta.grid(row=0, column=1)
etiqueta=tkinter.Label(ventana, text="COIN", bg="white")
etiqueta.grid(row=1, column=0)
etiqueta=tkinter.Label(ventana, text="PRICE", bg="white")
etiqueta.grid(row=2, column=0)
etiqueta2=tkinter.Label(ventana, text="MONTO (USDT)", bg="white")
etiqueta2.grid(row=3, column=0)
etiqueta3=tkinter.Label(ventana, text="STOP LOSS", bg="white")
etiqueta3.grid(row=4, column=0)

#market
etiqueta=tkinter.Label(ventana, text="MARKET", fg='black', bg="light cyan", font= "Helvetica 15")
etiqueta.grid(row=14, column=1)
etiqueta=tkinter.Label(ventana, text="COIN", bg="white")
etiqueta.grid(row=15, column=0)
#etiqueta=tkinter.Label(ventana, text="PRICE", bg="white")
#etiqueta.grid(row=16, column=0)
etiqueta2=tkinter.Label(ventana, text="MONTO (USDT)", bg="white")
etiqueta2.grid(row=16, column=0)
etiqueta3=tkinter.Label(ventana, text="STOP LOSS", bg="white")
etiqueta3.grid(row=17, column=0)

#limit

boton1=tkinter.Button(ventana, text="LONG", width = 10, height = 2, command=buy_coin, fg='white', bg='green' )
boton1.grid(row=5, column=0)
boton2=tkinter.Button(ventana, text="SHORT", width = 10, height = 2, command=sell_coin, fg='white', bg='red' )
boton2.grid(row=5, column=3)

#market

boton3=tkinter.Button(ventana, text="LONG MKT", width = 10, height = 2, command=buy_coin_market, fg='white', bg='green' )
boton3.grid(row=20, column=0)
boton4=tkinter.Button(ventana, text="SHORT MKT", width = 10, height = 2, command=sell_coin_market, fg='white', bg='red' )
boton4.grid(row=20, column=3)

#calculate risk limit
boton5=tkinter.Button(ventana, text="CAL RISK", width = 10, height = 2, command=calculate_risk, fg='black', bg='white' )
boton5.grid(row=5, column=1)

#calculate risk limit
boton5=tkinter.Button(ventana, text="CAL RISK", width = 10, height = 2, command=calculate_risk_market, fg='black', bg='white' )
boton5.grid(row=20, column=1)


# Create a Label widget
label_box=Label(ventana, text="", font=('Calibri 15'))
label_box.grid(row=6, column=1)
label_box1=Label(ventana, text="", font=('Calibri 15'))
label_box1.grid(row=7, column=1)
label_box2=Label(ventana, text="", font=('Calibri 15'))
label_box2.grid(row=8, column=1)
label_box3=Label(ventana, text="", font=('Calibri 15'))
label_box3.grid(row=9, column=1)
label_box4=Label(ventana, text="", font=('Calibri 15'))
label_box4.grid(row=10, column=1)
label_box5=Label(ventana, text="", font=('Calibri 15'))
label_box5.grid(row=11, column=1)
label_box6=Label(ventana, text="", font=('Calibri 15'))
label_box6.grid(row=12, column=1)
label_box7=Label(ventana, text="", font=('Calibri 15'))
label_box7.grid(row=13, column=1)

ventana.attributes('-topmost',True)
ventana.geometry("-2560+340")
ventana.mainloop()

