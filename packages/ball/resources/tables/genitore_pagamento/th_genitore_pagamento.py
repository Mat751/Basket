#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('codice_genitore')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.fieldcell('importo')
        #r.fieldcell('note')
        r.fieldcell('entrate_uscite')

    def th_order(self):
        return 'protocollo'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('protocollo')
        fb.field('codice_genitore')
        fb.field('data')
        mod = 'Paypal:Paypal,Bonifico:Bonifico,Contanti:Contanti'   
        fb.filteringSelect('^.modalita',lbl='Tipo pagamento: ', 
                       tooltip="""Seleziona ruolo""",
                       values=mod)
        fb.field('importo')
        #fb.field('note')
        fb.field('entrate_uscite')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class ViewFromGenitore2021(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('codice_genitore')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.cell('figli')
        r.fieldcell('importo',totalize=True)
        #r.fieldcell('entrate_uscite')    

     #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):
        
        
        #calcola gli elementi ricorsivamente per riga
        def cb(row):

            data = self.db.table('ball.genitore_pagamento').query(
                    columns='$entrate_uscite,$importo,$protocollo,$data',
                ).fetchAsDict(key='protocollo')  
 
            chiavi = data.keys()
            
            for i in chiavi:
                if data[i]['protocollo'] == row['protocollo'] and data[i]['data'].year == 2021:
                    dato = data[i]
                    
                    if dato['entrate_uscite'].lower() == 'entrate':
                        row['importo'] = row['importo'] * (-1)
            
            data = self.db.table('ball.genitore').query(
                    columns='$pkey,$figli,$nome_completo',
                ).fetchAsDict(key='pkey')  

            dato = data[row['codice_genitore']]

            if row['data'].year == 2021:
                return dict(importo=row['importo'],
                figli=dato['figli'])

        selection.apply(cb)

class ViewFromGenitore2022(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.cell('figli')
        r.fieldcell('importo',totalize=True)
        #r.fieldcell('entrate_uscite')    

     #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):
        
        
        #calcola gli elementi ricorsivamente per riga
        def cb(row):

            data = self.db.table('ball.genitore_pagamento').query(
                    columns='$entrate_uscite,$importo,$protocollo,$data',
                ).fetchAsDict(key='protocollo')  
 
            chiavi = data.keys()
            
            for i in chiavi:
                if data[i]['protocollo'] == row['protocollo'] and data[i]['data'].year == 2022:
                    dato = data[i]
                    
                    if dato['entrate_uscite'].lower() == 'entrate':
                        row['importo'] = row['importo'] * (-1)

            data = self.db.table('ball.genitore').query(
                    columns='$pkey,$figli,$nome_completo',
                ).fetchAsDict(key='pkey')  

            dato = data[row['codice_genitore']]

            if row['data'].year == 2021:
                return dict(importo=row['importo'],
                figli=dato['figli'])
            
            if row['data'].year == 2022:
                return dict(importo=row['importo'],
                figli=dato['figli'])

        selection.apply(cb)