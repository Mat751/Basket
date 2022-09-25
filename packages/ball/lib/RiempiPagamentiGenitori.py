
import sys
from gnr.app.gnrapp import GnrApp


def pagamenti_genitori():
    db = GnrApp('mybasket').db
    iscritti= db.table('ball.iscritto')
    pagamenti_genitore= db.table('ball.genitore_pagamento')
    informazioni_pagamenti = iscritti.query(columns='$id,$nome,$cognome,$codice_fiscale,$nome_genitore,$cognome_genitore,$codice_fiscale_genitore,$pagamento,$pagamento2,$pagamento3,$pagamento1_22,$pagamento2_23,$pagamento3_23,$importo1_22,$data1_22,$importo2_23,$data2_23,$importo3_23,$data3_23,$pagamento_iscritto,$importo1,$data1,$importo2,$data2,$importo3,$data3').fetch()
    for r in informazioni_pagamenti:
        r = dict(r)
        pagamento, importo, data= controllo_importo_pagamento(r)
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
                            if check_if_exists(pagamenti_genitore, new_row):
                                pagamenti_genitore.insert(new_row)
    db.commit()

def controllo_importo_pagamento(row):
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
    print(f'pagamento: {pagamento} - importo: {importo} - data: {data_all}')
    return pagamento, importo, data_all

def check_if_exists(pagamenti_genitore,new_row):
    pagamenti = pagamenti_genitore.query(columns='$iscritto,$isc_cod_fisc,$data,$modalita,$importo').fetch()
    for i in pagamenti:
        i = dict(i)
        if new_row['isc_cod_fisc'] == i['isc_cod_fisc']:
            if new_row['data'] == i['data'] and new_row['modalita'] == i['modalita'] and new_row['importo'] == i['importo']:
                return None
    return 'non presente'

if __name__ == '__main__':
    pagamenti_genitori()
    