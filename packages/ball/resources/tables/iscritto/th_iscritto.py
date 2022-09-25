#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.app.gnrapp import GnrApp
from gnr.core.gnrdecorator import public_method,customizable
from datetime import date as dat


class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        
        anag = r.columnset('anag', name='ANAGRAFICA', color='white', font_weight='bold', background='darkblue')
        anag.fieldcell('nome_completo')
        anag.fieldcell('data_nascita')
        anag.fieldcell('anni')
        anag.fieldcell('sex')
        anag.fieldcell('stato_estero')
        anag.fieldcell('provincia')
        anag.fieldcell('comune_id')
        anag.fieldcell('codice_fiscale')
        anag.fieldcell('indirizzo')
        anag.fieldcell('comune')
        anag.fieldcell('cap')

        paf = r.columnset('pag', name='PAGAMENTI', color='white', font_weight='bold', background='darkred')
        paf.fieldcell('pag_completo',semaphore=True)

        isc= r.columnset('isc', name='ISCRIZIONE', color='white', font_weight='bold', background='orange')

        isc.fieldcell('data_iscrizione')
        isc.fieldcell('categoria')
        isc.fieldcell('email')

        carac= r.columnset('carac', name='CARATTERISTICHE', color='white', font_weight='bold', background='darkgreen')

        carac.fieldcell('telefono')
        carac.fieldcell('altezza')
        carac.fieldcell('ruolo')
        carac.fieldcell('voto')
        #r.fieldcell('terra')

        importo = r.columnset('importo', name='IMPORTI', color='white', font_weight='bold', background='green')
        importo.fieldcell('pagamento1_22')
        importo.fieldcell('importo1_22')
        importo.fieldcell('data1_22')
        importo.fieldcell('pagamento2_23')
        importo.fieldcell('importo2_23')
        importo.fieldcell('data2_23')
        importo.fieldcell('pagamento3_23')
        importo.fieldcell('importo3_23')
        importo.fieldcell('data3_23')

        #r.fieldcell('modulo_iscrizione', format_trueclass='greenLight', format_nullclass='yellowLight', format_falseclass='redLight')

        
        
    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')

    
   
    #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):

            
        def calculate_age(born):
            today = dat.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

            # se il mese è inferiore a settembre allora siamo già
            # nell'anno successivo

            if today.month < 9:
                anno = anno -1
            return anno 

        #calcola gli elementi ricorsivamente per riga
        def cb(row):
            
            data = self.db.table('ball.iscritto').query(
                    columns='$voto,$codice_fiscale,$provincia,$data_nascita,$nome_completo,$categoria,$nome,$cognome,$comune_id,$sex'
                ).fetchAsDict(key='nome_completo')  
 
            dato = data[row['nome_completo']]
            if dato['data_nascita']:
                row['anni'] = calculate_age(dato['data_nascita'])
            else:
                row['anni'] = 0
            return dict(anni=row['anni'])
            
        selection.apply(cb)    


    

class Form(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        tc = form.center.tabContainer(margin='2px')
        self.dati_iscritto(tc.borderContainer(title='Dati iscritto'))
        self.allegati(tc.contentPane(title='Allegati iscritto'))
        self.pagamenti2021(tc.contentPane(title='Pagamenti 2021'))
        self.pagamenti2022(tc.contentPane(title='Pagamenti 2022'))
        self.pagamenti2023(tc.contentPane(title='Pagamenti 2023'))


    @customizable    
    def dati_iscritto(self,bc):
        top = bc.contentPane(region='top',datapath='.record')
        fb = top.formbuilder(cols=3, border_spacing='4px')

        sesso = 'F:Femmina,M:Maschio'
        fb.field('nome')
        fb.field('cognome')
        fb.field('data_nascita')
        fb.filteringSelect('^.sex',lbl='Sesso', 
                       tooltip="""FilteringSelect: you can select only an existing value.<br/>
                                  You see the description but in the store we will have the value.""",
                       values=sesso)
        fb.field('stato_estero')
        fb.field('provincia')
        fb.field('comune_id')
        fb.field('codice_fiscale')

        fb.field('indirizzo')
        fb.field('comune')
        fb.field('cap')
        
        # condition='$sigla_provincia=:provincia',
        #        condition_provincia='^.provincia')
        #fb.field('codice_fiscale')
        #fb.field('anni',edit=False)
        
        fb.field('telefono',lbl='Cell.')
        fb.field('altezza',lbl='Altezza (cm)')
        
        ruolo = 'Playmaker:Playmaker,Ala:Ala,Guardia:Guardia,Pivot:Pivot'

        #fb.field('categoria',edit=True,colspan=2)
        
        
        fb.field('data_iscrizione')
        fb.field('email')

        valori = 'Scarso:1,Sufficiente:2,Buono:3,Discreto:4,Ottimo:5'
        center = bc.tabContainer(region='left', title='Valutazioni',width='60%',margin='4px',datapath=".record")
        #center = bc.contentPane(region='center',)
        center = center.tabContainer(title='Valutazioni',region='center')
        fb = center.formbuilder(cols=2, border_spacing='4px',width='auto')

        #categorie='MCB:Micro Basket,MBA:Mini Basket A,MBB:Mini Basket B,U13:Under 13,U14:Under 14,U15:Under 15,U16:Under 16,U17:Under 17,U19:Under 19'
        categorie='2016:2016,2015:2015,2014:2014,2013:2013,2012:2012,2011:2011,U13:Under 13,U14:Under 14,U15:Under 15,U17:Under 17,U18:Under 18,U19:Under 19'
        fb.filteringSelect('^.ruolo',lbl='Ruolo: ', 
                       tooltip="""Seleziona ruolo""",
                       values=ruolo)

        fb.filteringSelect('^.categoria',values=categorie,
                            lbl='Categoria: ',
                            tooltip="""Seleziona categorie""")
        
        fb.radioButtonText(value='^.voto', values=valori,colspan=2,
                           lbl='Voto: ',
                           tooltip="""Seleziona voto ma sii magnanimo<br>
                           non si sa mai chi potresti trovarti davanti!""")
        fb.simpleTextArea(value='^.note',
        lbl='Commenti: ',width='400px',height='200px',colspan=2)

        #fb = top.borderContainer(cols=3, border_spacing='4px',title='Genitore')
        
        center = bc.tabContainer(region='right', title='Valutazioni',width='35%',
                                 height='50%',margin='4px',datapath=".record")
        
        self.anagrafica(center)    
        #self.pagamenti(center,anno="21/22")
        self.pagamenti(center,anno="22/23")
    

        # bottom = bc.contentPane(region='bottom',datapath='.record')
        # fb = bottom.formbuilder(cols=3,border_spacing='10px')
        # btn = fb.button('SALVA PAGAMENTI',color='red')
        # btn.dataRpc('.risposta',self.getTime)
        # fb.div('^.risposta')

    def anagrafica(self,center):
        center = center.tabContainer(title=f'Angrafica genitori',region='center')
        fb = center.formbuilder(cols=1, border_spacing='4px',width='auto')
        fb.radiobuttontext('^.pagamento_iscritto',lbl='Pagamento: ',
                        values='Ragazzo:Ragazzo,Genitore:Genitore')   
        fb.field('nome_genitore')
        fb.field('cognome_genitore')
        fb.field('codice_fiscale_genitore')
        fb.div('^.pag_completo',lbl='Stato pagamenti: ',
                _virtual_column='$pag_completo',format='semaphore',dtype='B')
        fb.div('^.num_figli',lbl='Figli a carico del genitore: ',_virtual_column='$num_figli',
                 dtype='L')

    def pagamenti(self,center,anno=None):
        center = center.tabContainer(title=f'Pagamenti {anno}',region='center')
        fb = center.formbuilder(cols=1, border_spacing='4px',width='auto')

        mod = 'Paypal:Paypal,Bonifico:Bonifico,Assegno:Assegno,Altro:Altro'
        fb.filteringSelect('^.pagamento1_22',lbl='Tipo pagamento 1: ', 
                       tooltip="""Seleziona ruolo""",
                       values=mod)
        
        fb.field('importo1_22')
        fb.field('data1_22')

        fb.filteringSelect('^.pagamento2_23',lbl='Tipo pagamento 2: ', 
                       tooltip="""Seleziona ruolo""",
                       values=mod)
        fb.field('importo2_23')
        fb.field('data2_23')

        fb.filteringSelect('^.pagamento3_23',lbl='Tipo pagamento 3: ', 
                       tooltip="""Seleziona ruolo""",
                       values=mod)
        fb.field('importo3_23')
        fb.field('data3_23')

        fb = center.formbuilder(cols=3, border_spacing='10px',width='auto')
        btn = fb.button('OTTIENI PAGAMENTI ANNO SOLARE',color='red')
        btn.dataRpc('.risposta',self.getTime)
        fb.div('^.risposta')


    def allegati(self,pane):
        pane.attachmentGrid()
        


    @public_method
    def getTime(self):
        message = self.pagamenti_genitori()
        return message


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


    def pagamenti2021(self,pane):
        pane.plainTableHandler(relation='@iscrittipagamenti',viewResource='ViewFromIscrittoPagamenti2021')

    def pagamenti2022(self,pane):
        pane.plainTableHandler(relation='@iscrittipagamenti',viewResource='ViewFromIscrittoPagamenti2022')

    def pagamenti2023(self,pane):
        pane.plainTableHandler(relation='@iscrittipagamenti',viewResource='ViewFromIscrittoPagamenti2023')


    def pagamenti_genitori(self):
        conta = 0
        db = GnrApp('mybasket').db
        iscritti= db.table('ball.iscritto')
        pagamenti_genitore= db.table('ball.genitore_pagamento')
        informazioni_pagamenti = iscritti.query(columns='$id,$nome,$cognome,$codice_fiscale,$nome_genitore,$cognome_genitore,$codice_fiscale_genitore,$pagamento,$pagamento2,$pagamento3,$pagamento1_22,$pagamento2_23,$pagamento3_23,$importo1_22,$data1_22,$importo2_23,$data2_23,$importo3_23,$data3_23,$pagamento_iscritto,$importo1,$data1,$importo2,$data2,$importo3,$data3').fetch()
        for r in informazioni_pagamenti:
            r = dict(r)
            pagamento, importo, data= self.controllo_importo_pagamento(r)
            if pagamento != [] and importo != [] and data != []:
                for number_of_payment in range(len(pagamento)):
                    if r['codice_fiscale_genitore']:
                                new_row= { 'genitore':r['cognome_genitore'] + ' ' + r['nome_genitore'],
                                           'gen_cod_fisc':r['codice_fiscale_genitore'],
                                           'codice_iscritto': r['id'],
                                           'iscritto': r['cognome'] + ' ' + r['nome'],
                                           'isc_cod_fisc': r['codice_fiscale'],
                                           'data': r[data[number_of_payment]],
                                           'modalita': r[pagamento[number_of_payment]],
                                           'importo': r[importo[number_of_payment]]}
                                if self.check_if_exists(pagamenti_genitore, new_row):
                                    conta += 1
                                    pagamenti_genitore.insert(new_row)
        db.commit()
        if conta > 0:
            return 'PAGAMENTI TRASFERITI NELLA TABELLA PAGAMENTI GENITORI.\nTROVERAI CARICATI I PAGAMENTI ANCHE IN SEZIONE PAGAMENTI IN ALTO.'
        return '\nNON CI SONO AGGIORNAMENTI:\n\t-INSERISCI GENITORE E CODICE FISCALE\n\t-INSERISCI PAGAMENTI\n\t-SALVA PAGAMENTI (IN ALTO A DESTRA)'


    def controllo_importo_pagamento(self,row):
        pagamento = []
        importo = []
        data_all = []
        for data in ['data1','data2','data3','data1_22','data2_23','data3_23']:
                    if row[data]:
                        data_all.append(data)
        for p in ['pagamento','pagamento2', 'pagamento3', 'pagamento1_22', 'pagamento2_23', 'pagamento3_23']:
            if row[p]:
                pagamento.append(p)
        for imp in ['importo1','importo2','importo3','importo1_22','importo2_23','importo3_23']:
            if row[imp]:
                importo.append(imp)
        return pagamento, importo, data_all


    def check_len(self,pagamenti_genitore):
        tot = 0
        pagamenti = pagamenti_genitore.query(columns='$iscritto,$isc_cod_fisc,$data,$modalita,$importo').fetch()
        for i in pagamenti:
            tot += 1
        return tot

    def check_if_exists(self,pagamenti_genitore,new_row):
        pagamenti = pagamenti_genitore.query(columns='$iscritto,$isc_cod_fisc,$data,$modalita,$importo').fetch()
        for i in pagamenti:
            i = dict(i)
            if new_row['isc_cod_fisc'] == i['isc_cod_fisc']:
                if new_row['data'] == i['data'] and new_row['modalita'] == i['modalita'] and new_row['importo'] == i['importo']:
                    return None
        return 'non presente'
