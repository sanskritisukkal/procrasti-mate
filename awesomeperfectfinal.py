#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 22:50:09 2021

@author: sanskritisukkal
"""

from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import datetime
import os, subprocess
from tkcalendar import DateEntry
import mysql.connector

def main():
    #connecting mysql database to python
    while True:
        global mydb, mycursor
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='sanchu14',database='reminder')
        mycursor=mydb.cursor()
        #if mydb.is_connected():
            #print('database successfully connected')    #confirming the connection
        break
    
    #the following function gets executed when clicked on the 'today's reminder menu option    
    def today_rem():
        t_sql=tk.Toplevel(master)
        t_sql.geometry('400x400')
        t_sql.configure(background='yellow')
        t_output=mycursor.execute('select * from today')
        Label(t_sql, text="Today's reminders").pack()
        t_msg=Message(t_sql, text=t_output).pack()
    
    #the following function gets executed when clicked on the scheduled reminders menu option
    def sch_rem():
        sc_sql=tk.Toplevel(master)
        sc_sql.geometry('400x400')
        sc_sql.configure(background='green')
        sc_output=mycursor.execute('select * from scheduled')
        Label(sc_sql, text='Scheduled reminders')
        sc_msg=Message(sc_sql, text=sc_output).pack()
    
    #the following function gets executed when clicked on the 'all reminders' menu option
    def all_rem():
        all_sql=tk.Toplevel(master)
        all_sql.geometry('400x400')
        all_sql.configure(background='yellow')
        all_output=mycursor.execute('select * from allreminders')
        Label(all_sql, text='all reminders')
        all_msg=Message(all_sql, text=all_output)
        
        
    #creation of the menu driven tkinter window 
    global master, path, img, panel
    master = tk.Tk()        #the text box title
    master.title(string='Procrasti-mate')
    path=Image.open("/Users/sanskritisukkal/Desktop/cs proj/Procrasti-mate.jpg")
    img = ImageTk.PhotoImage(path)
    panel = tk.Label(image = img)
    
    panel.image=img         #image attached to the tkinter box
    frame1=Frame(master)
    frame1.pack(side=TOP,fill=X)
    frame2=Frame(master)
    frame2.pack(side=TOP,fill=X)
    panel.pack(side = "right", fill = "both", expand = "yes")
  
    #the following functions gets executed when clicked on 'create a new reminder' menu option
    def new():

        #displays the user inputed values when pressed on show
        def display():
            print("Reminder: %s\nDate: %s\nHours: %s\nMinutes: %s\nDescription: %s" % (e1.get(),e2,e3.get(),e4.get(),e5.get()))
        
        final=tk.Toplevel(master)
        final.geometry("700x280")
        final.configure(background='pink')
        
        #labelling the rows
        tk.Label(final,text='Reminder').grid(row=4,column=0,sticky=E)
        tk.Label(final,text='Date (DD-MM-YYYY)').grid(row=5,column=0,sticky=E)
        tk.Label(final,text='Hours').grid(row=6,column=0,sticky=E)
        tk.Label(final,text='Minutes').grid(row=6,column=2,sticky=E)
        tk.Label(final,text='Description').grid(row=7,column=0,sticky=E)
        #tk.label(frame2,text='location').grid(row=8,column=0,sticky=E)
        
        #to create a calendar derived date effect
        def date_entry():
            top = tk.Toplevel(master)
            tk.Label(top, text='Choose date').pack(padx=10, pady=10)
            cal = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2)
            cal.pack(padx=10, pady=10)
            def storedate():
                global e2
                e2=cal.get_date()
                date.config(text = "Selected Date is: " + str(e2))
            date = Label(top, text="") 
            date.pack(pady = 20) 
            tk.Button(top, text="ok", command=storedate).pack()
        
        #the creation widgets in the new reminder option
        global e1, e2, e3, e4, e5
        e1=tk.Entry(final)         #to enter values
        #e2=tk.Entry(frame2)
        e3=tk.Spinbox(final, from_=0, to=23)
        e4=tk.Spinbox(final, from_=0, to=59)
        e5=tk.Entry(final)
        #e6=tk.Entry(frame2) #-> if we need location
        e1.grid(row=4,column=1)       #to display a seperate textbox and grid
        #e2.grid(row=5,column=1)
        e3.grid(row=6,column=1)
        e4.grid(row=6,column=3)
        e5.grid(row=7,column=1)
        #e6.grid(row=8,column=1) #-> if we need location
        
        #variable validation
        def validation():
            if e1=='' and e2=='' and e3=='' and e4=='' and type(e3)!=int and type(e4)!=int:
                empty=tk.Toplevel(master)
                empty.geometry("250x200")
                w = Label(empty, text ='ALERT!!!', font = "80")  
                w.pack()
                msg = Message(empty, text = "All entries except description are required and the hour and mins value should be integrers only, to proceed further")   
                msg.pack() 
            
            else:
                success=tk.Toplevel(master)
                success.geometry("250x200")
                t=Label(success, text='SUCCESS', font='80')
                t.pack()
                msg=Message(success, text='You reminder has been set. You can now close this window')
                msg.pack()
        
        #desktop voiceover (text to speech) - voices the reminder out loud
        #also notifies the user with a notification
        #for macOS operating system
        def os_notifier():
            os.system('say "your reminder"')
            def say(rem):
                subprocess.call(['say', rem])
            say(rem)
            os.system('say "is due now"')
            title = "Reminder"
            message = "is due now!"
            command = f''' osascript -e 'display notification "{rem} {message}" with title "{title}"' '''
            os.system(command)
        
        #the following is the backend of the whole program
        #only applicable for new reminders
        def backend():
            #backend storing
            validation()
            global rem, x, hours, mins, date, desc
            rem=e1.get()
            s_e2=str(e2)
            x=s_e2.split('-')
            hours=int(e3.get())
            mins=int(e4.get())
            date=datetime.datetime(int(x[0]),int(x[1]),int(x[2]),hours,mins)
            desc=e5.get()
            global currenttime
            currenttime=datetime.datetime.now()
            
            master.destroy()
        
            #backend processing
            while True:
                if currenttime>date:
                    os_notifier()
                    break
                else:
                    continue
            
            #storing of reminders accordingly to the tables - all, today and scheduled
            mycursor.execute('insert into allreminders values(rem,e2,hours,mins')
            mycursor.execute('insert into scheduled values(rem,desc,e2,hours,mins')
            if currenttime.strftime('%m')==date.strftime('%m') and currenttime.strftime('%d')==date.strftime('%d'):
                mycursor.execute('insert into today values(rem,desc,e2,hours,mins')
            
        #buttons for new reminder fn      #check if sticky,pady is needed
        tk.Button(final,text='choose date',command=date_entry).grid(row=5,column=1,sticky=tk.W,pady=9)
        tk.Button(final,text='Save',command=backend).grid(row=8,column=0,sticky=tk.W,pady=9)
        tk.Button(final,text='Show',command=display).grid(row=8,column=1,sticky=tk.W,pady=9)
        tk.Button(final,text='Go back to menu',command=main).grid(row=8,column=2,sticky=tk.W,pady=9)
        
    #heading for the master window    
    label = Label(master, text ="**Choose your desired action to be performed from the options given below**")
    master.configure(background='orange')
    label.pack(pady = 10)
    
    # new window on button click
    btn = Button(master, text ="Create a new reminder",command = new)
    btn.pack(pady = 10)
    btn = Button(master, text ="Scheduled Reminders", command = sch_rem)
    btn.pack(pady = 11)
    btn = Button(master, text ="Reminders for Today", command = today_rem)
    btn.pack(pady = 12)
    btn = Button(master, text ="All Reminders", command = all_rem)
    btn.pack(pady = 13)
    btn = Button(master, text ="exit", command = master.destroy)
    btn.pack(pady = 14)
        
    master.mainloop()       #looping the above process 
    
    master.quit()       #once the process is done, it quits

main()
            

        
        
        
        
        
        
        
        
        
        
        