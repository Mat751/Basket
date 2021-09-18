
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('genitore_pagamento', pkey='id', name_long='Pagamento genitore', name_plural='Pagamento genitori',caption_field='protocollo')
        self.sysFields(tbl)
        
        tbl.column('protocollo', name_long='Protocollo')
        tbl.column('codice_genitore',size='22', group='_', name_long='Genitore'
                    ).relation('genitore.id', relation_name='pagamenti_genitori', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_long='Data Pagamento')
        tbl.column('modalita', name_long='Tipo pagamento')
        tbl.column('importo', dtype='N', name_long='Importo')
        tbl.column('note', name_long='Note')
        tbl.column('entrate_uscite', name_long='Entrate o Uscite')

    def defaultValues(self):
        return dict(data=self.db.workdate,entrate_uscite="Uscite")

    def counter_protocollo(self, record=None):
      pars = dict(format='$K$YY.$NNNNN', period='YY', code='M',
                  date_field='data', showOnLoad=True, recycle=False, date_tolerant=True,
                  message_dateError="Impossibile creare riga in data corrente. Ultima riga in data %(last_used)s",
                  message_failed='La riga ha ricevuto un protocollo differente da quello in precedenza allocato: %(sequence)s')
      return pars