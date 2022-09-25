#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method


class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('genitore')
        r.fieldcell('gen_cod_fisc')
        r.fieldcell('codice_iscritto')
        r.fieldcell('isc_cod_fisc')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.fieldcell('importo')

    def th_order(self):
        return 'protocollo'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('protocollo')
        fb.field('genitore')
        fb.field('gen_cod_fisc')
        fb.field('codice_iscritto')
        fb.field('isc_cod_fisc')
        fb.field('data')
        fb.field('modalita')
        fb.field('importo')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class ViewFromIscrittoPagamenti2021(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('genitore')
        r.fieldcell('gen_cod_fisc')
        r.fieldcell('iscritto')
        r.fieldcell('isc_cod_fisc')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.fieldcell('importo',totalize=True)

    @public_method
    def th_applymethod(self,selection=None):
        def cb(row):
            if row['data'].year == 2021:
                return dict(importo=row['importo'])
        selection.apply(cb)


class ViewFromIscrittoPagamenti2022(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('genitore')
        r.fieldcell('gen_cod_fisc')
        r.fieldcell('iscritto')
        r.fieldcell('isc_cod_fisc')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.fieldcell('importo',totalize=True)

    @public_method
    def th_applymethod(self,selection=None):
        def cb(row):
            if row['data'].year == 2022:
                return dict(importo=row['importo'])
        selection.apply(cb)



class ViewFromIscrittoPagamenti2023(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('genitore')
        r.fieldcell('gen_cod_fisc')
        r.fieldcell('iscritto')
        r.fieldcell('isc_cod_fisc')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.fieldcell('importo',totalize=True)

    @public_method
    def th_applymethod(self,selection=None):
        def cb(row):
            if row['data'].year == 2023:
                return dict(importo=row['importo'])
        selection.apply(cb)
