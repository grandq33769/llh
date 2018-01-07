import sys
import re
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from db import Db
Builder.load_file('app.kv')

class Table(BoxLayout):
    
    def __init__(self, db, **kwargs):
        self.db = db
        super(Table, self).__init__(**kwargs)

    def execute(self, comm='', *args):
        try:
            if comm != '':
               a,r = self.db.query(comm)
            else:
               a,r = self.db.query(self.sqlinput.text)
            self.lc = len(a)
            self.rgl.cols = self.lc
            self.rv.refresh_from_layout()
            results = [{'value':v} for v in a]
            for t in r:
                str_t = [{'value':str(v)} for v in t]
                results.extend(str_t)

            self.rv.data = results

        except:
            self.rv.data = [{'value':'Error in SQL query'},
                            {'value':str(sys.exc_info()[1])}]

    def conditions(self):
       popup = ConditionPopup(main=self, db=self.db, select_tab=None)
       popup.open()
		
    def clear(self):
       self.rv.data = []

    def delete(self):
       popup = DeletePopup(main=self)
       popup.open()

    def insert(self):
       popup = InsertPopup(main=self)
       popup.open()

    def update(self):
       popup = UpdatePopup(main=self)
       popup.open()

    def exist(self):
       popup = ExistPopup(main=self, db=self.db, select_tab=None)
       popup.open()

class MiniPopup(Popup):
    def __init__(self, db, tab, attr, value, caller, **kwargs):

        self.mini = UV()
        self.db = db
        self.tab = tab
        self.attr = attr
        self.value = value
        self.caller = caller
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.mini)
        btn = Button(text='Confirm', size_hint=(1,0.2))
        box.add_widget(btn)
        
        #print(attr, value)
        result = [{'attr':a, 'value':v} for a,v in zip(attr, value)]
        self.mini.data = result

        super(MiniPopup, self).__init__(content=box,title='Tuple Update',
                                    size_hint=(None, None), size=(1000, 800),
                                    **kwargs)

        btn.bind(on_press=self.confirm)

    def confirm(self, x):
        #print(self.mini.children[0].children)
        new = []
        comm = 'UPDATE {} SET {} WHERE {};'
        for tup in self.mini.children[0].children:
             new.insert(0,tup.children[0].text)
        
        # print(self.tab, self.attr, self.value, new)
        set_str = ''
        for a,n in zip(self.attr, new):
             if n != '':
                set_str += ' {}=\"{}\",'.format(a,n)
        set_str = set_str[:-1]

        where_str = ''
        for a,v in zip(self.attr, self.value):
             where_str += ' {}=\"{}\" and'.format(a,v)
        where_str = where_str[:-4]
        
        comm = comm.format(self.tab,set_str,where_str)
        print(comm)
        try:
           self.db.query(comm)
        except:
           print(str(sys.exc_info()[1]))

        self.caller.execute('SELECT * FROM {};'.format(self.tab))
        self.caller.sqlinput.text = comm
        
        self.dismiss()


class DBPopup(Popup):
    def __init__(self, main, middle, size=(1200, 1000), **kwargs):
        self.caller = main
        self.db = main.db
        _,r = self.db.query(
             'SELECT table_name FROM information_schema.tables where table_schema=\'MFCom\';')

        dropdown = DropDown()
        for a in r:
             btn = Button(text='{}'.format(str(a[0]))  , size_hint_y=None)
             btn.bind(on_release=lambda btn: dropdown.select(btn.text))
             dropdown.add_widget(btn)
        self.dbtn = Button(text='Relations', size_hint=(1, 0.2))
        self.dbtn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=self.show_table)

        box = BoxLayout(orientation='vertical')
        box.add_widget(self.dbtn)
        box.add_widget(middle)
        btn = Button(text='Confirm', size_hint=(1,0.2))
        box.add_widget(btn)

        super(DBPopup, self).__init__(content=box,
                                    size_hint=(None, None), size=size,
                                    **kwargs)

        btn.bind(on_press=self.confirm)

    def show_table(self, instance, x):
        setattr(self.dbtn, 'text', x)
        self.select_tab = x

    def confirm(self):
        if hasattr(self, 'select_tab'):
            self.caller.execute('SELECT * FROM {};'.format(self.select_tab))
        self.dismiss()

class UpdatePopup(DBPopup):
    def __init__(self, **kwargs):
        self.up = RV()
        super(UpdatePopup, self).__init__(title='Update', middle=self.up, **kwargs)

    def show_table(self, instance, x):
        super(UpdatePopup, self).show_table(instance, x)
        a,r = self.db.query('Select * from '+self.select_tab+';')
        temp = []
        for v in r:
            tup = (str(x) for x in v)
            temp.append(tup)
        self.attr = a
        self.up.data = [{'text':','.join(v)} for v in temp]


    def confirm(self, x):
        #print(self.fill.children[0].children)
        if hasattr(self, 'select_tab'):
               for lab in self.up.children[0].children:
                    if lab.selected:
                         v = self.up.data[lab.index]['text'].split(',')
                         popup = MiniPopup(db=self.db, 
                                           tab=self.select_tab, 
                                           attr=self.attr,
                                           value=v,
                                           caller=self.caller)
                         popup.open()
       
        super(UpdatePopup, self).confirm()
        
class InsertPopup(DBPopup):
    def __init__(self, **kwargs):
        self.fill = IV()
        super(InsertPopup, self).__init__(title='Insertion', middle=self.fill, **kwargs)

    def show_table(self, instance, x):
        super(InsertPopup, self).show_table(instance, x)
        a,_ = self.db.query('Select * from '+self.select_tab+';')
        self.attr = a
        #print(a)
        self.fill.data = [{'value':v} for v in a]

    def confirm(self, x):
        #print(self.fill.children[0].children)
        comm = 'INSERT INTO {} VALUES ({});'
        result = []
        for lab in self.fill.children[0].children:
            result.insert(0,'\"'+lab.children[0].text+'\"')
                
        if hasattr(self, 'select_tab') and result != []:
            comm = comm.format(self.select_tab, ','.join(result)) 

            print(comm)
            try:
               self.caller.sqlinput.text = comm
               self.db.query(comm)
            except:
               print(str(sys.exc_info()[1]))

        super(InsertPopup, self).confirm()

class DeletePopup(DBPopup):
    def __init__(self, **kwargs):
        self.rv = RV()
        super(DeletePopup, self).__init__(title='Deletion', middle=self.rv, **kwargs)

    def show_table(self, instance, x):
        super(DeletePopup, self).show_table(instance, x)
        a,r = self.db.query('Select * from '+self.select_tab+';')
        temp = []
        for v in r:
            tup = (str(x) for x in v)
            temp.append(tup)
        self.attr = a
        self.rv.data = [{'text':','.join(v)} for v in temp]

    def confirm(self, x):
        #print(self.rv.children[0].children)
        if hasattr(self, 'select_tab'):
             for lab in self.rv.children[0].children:
                  if lab.selected:
                      comm = 'Delete From '+self.select_tab+' Where '
                      value = self.rv.data[lab.index]['text'].split(',')
                      #print(self.attr,value)
                      for a,v in zip(self.attr,value):
                           comm += str(a)+'=\"'+str(v)+'\" and '
                      comm = comm[:-4]+';'
                      print(comm)
                      try:
                         self.caller.sqlinput.text = comm
                         self.db.query(comm)
                      except:
                         print(str(sys.exc_info()[1]))
                 
        super(DeletePopup, self).confirm()

class ConditionPopup(DBPopup):
    def __init__(self, db, select_tab, **kwargs):
        self.con = CV(db=db)
        self.select_tab = select_tab
        super(ConditionPopup, self).__init__(title='Condtional Query',
                                             middle=self.con,
                                             **kwargs)
        if select_tab != None:
              self._show()

    def show_table(self, instance, x):
        super(ConditionPopup, self).show_table(instance, x)
        popup = ConditionPopup(main=self.caller,
                               db=self.db,  
                               select_tab=str(self.select_tab))
        popup.open()
        self.dismiss()
        
    def _show(self):
        a,_ = self.db.query('Select * from '+self.select_tab+';')
        self.attr = a
        #print(a)
        self.con.data = [{'value':''}]
        self.con.change(a)
        self.dbtn.text = self.select_tab


    def confirm(self, x):
        # print(self.con.children[0].children)
        value = [[],[],[]]
        ids = ['attrbtn','abtn','con_value']
        comm = "SELECT {} FROM " + self.select_tab
        if hasattr(self, 'select_tab'):
             for lab in self.con.children[0].children:
                 for l,i in zip(value, ids):
                     l.append(lab.ids[i].text)
                 
        cstr = ''
        hstr = ' HAVING '
        has_h = False
        for attr, agg, v in zip(*value):
             if attr == 'Attribute':
                  continue
             elif agg == 'Aggregate Function':
                  cstr += '{},'.format(attr)
             elif agg != 'HAVING':
                  cstr += '{}({}),'.format(agg,attr) 
             else: 
                  has_h = True
                  hstr += '{}{},'.format(attr,v)
             
        if cstr=='': cstr = '* '
        if has_h:
             comm = comm.format(cstr[:-1]) + hstr[:-1]
        else:
             comm = comm.format(cstr[:-1])
 
        comm += ';'
        print(comm)
        try:
            self.caller.sqlinput.text = comm
            self.caller.execute(comm)
        except:
            print(str(sys.exc_info()[1]))
       
        self.dismiss()


class ExistPopup(DBPopup):
    def __init__(self, db, select_tab, **kwargs):
        self.ev = EV(db=db)
        self.select_tab = select_tab
        super(ExistPopup, self).__init__(title='Existentcy',
                                         middle=self.ev,
                                         size=(1200,400),
                                         **kwargs)

        if select_tab != None:
              self._show()

    def show_table(self, instance, x):
        super(ExistPopup, self).show_table(instance, x)
        popup = ExistPopup(main=self.caller,
                           db=self.db,  
                           select_tab=str(self.select_tab))
        popup.open()
        self.dismiss()
        
    def _show(self):
        a,_ = self.db.query('Select * from '+self.select_tab+';')
        self.attr = a
        #print(a)
        self.ev.data = [{'value':''}]
        self.ev.change(a)
        self.dbtn.text = self.select_tab

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class IV(RecycleView):
    def __init__(self, **kwargs):
        super(IV, self).__init__(**kwargs)

class UV(RecycleView):
    def __init__(self, **kwargs):
        super(UV, self).__init__(**kwargs)

class CV(RecycleView):
    def __init__(self, db, **kwargs):
        self.db = db
        self.attr = ''
        super(CV, self).__init__(**kwargs)
        
    def connect(self, btn):
        add = AggregateDropDown()
        btn.bind(on_release=add.open)
        add.bind(on_select=lambda instance, x: setattr(btn, 'text', x))

    def build_attr(self, dbtn):
        dd = DropDown()
        for a in self.attr:
             btn = Button(text='{}'.format(str(a))  , size_hint_y=None)
             btn.bind(on_release=lambda btn: dd.select(btn.text))
             dd.add_widget(btn)
        dbtn.bind(on_release=dd.open)
        dd.bind(on_select=lambda instance, x: setattr(dbtn, 'text', x))

    def change(self, attr):
        self.attr = attr

    def add(self):
        self.data.append({'value':''})
    
class EV(RecycleView):
    def __init__(self, db, **kwargs):
        self.db = db
        self.edd = None
        self.odd = None
        self.attr = ''
        super(EV, self).__init__(**kwargs)

    def connect(self, btn):
        edd = ExistDropDown()
        btn.bind(on_release=edd.open)
        edd.bind(on_select=lambda instance, x: setattr(btn, 'text', x))

    def build_attr(self, dbtn):
        dd = DropDown()
        for a in self.attr:
             btn = Button(text='{}'.format(str(a))  , size_hint_y=None)
             btn.bind(on_release=lambda btn: dd.select(btn.text))
             dd.add_widget(btn)
        dbtn.bind(on_release=dd.open)
        dd.bind(on_select=lambda instance, x: setattr(dbtn, 'text', x))

    def build_relation(self, dbtn):
         if self.edd == None:
             _,r = self.db.query('SELECT table_name FROM information_schema.tables \
                                 where table_schema=\'MFCom\';')

             self.edd = DropDown()
             for a in r:
                 btn = Button(text='{}'.format(str(a[0]))  , size_hint_y=None)
                 btn.bind(on_release=lambda btn: self.edd.select(btn.text))
                 self.edd.add_widget(btn)
             dbtn.bind(on_release=self.edd.open)
             self.edd.bind(on_select=lambda instance, x: self.build_oattr(instance, x ,dbtn))
             self.edd.bind(on_select=lambda instance, x: setattr(dbtn, 'text',x))

    def build_oattr(self, instance, x, dbtn):
        # print(instance, x)
        a,_ = self.db.query('SELECT * FROM {}'.format(x))
        tbtn = dbtn.parent.ids['o_attrbtn']
        if self.odd == None:
             self.odd = DropDown()
             self._build(self.odd, a)
             tbtn.bind(on_release=self.odd.open)
             self.odd.bind(on_select=lambda instance, x: setattr(tbtn, 'text',x))
        else:
             self.odd.unbind()
             self._build(self.odd, a)     
             self.odd.bind(on_select=lambda instance, x: setattr(tbtn, 'text',x))
             tbtn.text = 'Other Attribute'

    def _build(self, dd, r):
        dd.clear_widgets()
        for a in r:
             btn = Button(text='{}'.format(str(a))  , size_hint_y=None)
             btn.bind(on_release=lambda btn: dd.select(btn.text))
             dd.add_widget(btn)

    def change(self, attr):
        self.attr = attr


class ExistDropDown(DropDown):
	pass

class AggregateDropDown(DropDown):
	pass

class MyApp(App):

    title = 'My Database'
    def __init__(self):
        self.db = Db()
        super(MyApp, self).__init__()

    def build(self):
        Window.size = 1200,800
        return Table(self.db)

    def on_stop(self):
        self.db.close()


if __name__ == '__main__':
    MyApp().run()
