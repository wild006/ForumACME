from tkinter import *
import re


class AutocompleteEntry(Entry):
    def __init__(self, commandes, vue, *args, **kwargs):
        self.parent = args[0]
        self.commandes = commandes
        self.vue = vue #message ou sujet
        Entry.__init__(self, *args, **kwargs)
        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            #words = self.comparison()
            self.words = self.comparisonBD()
            print(self.words)
            if self.words:
                if not self.lb_up:
                    self.lb = Listbox(self.parent, width = self.winfo_width())
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in self.words:
                    print(w)
                    try:
                        self.lb.insert(END,w.texte) #message
                    except:
                        self.lb.insert(END,w.nom) #sujet
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):
        #print(event, self.words[self.lb.curselection()[0]].texte)
        messageChoisi = self.words[self.lb.curselection()[0]]
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    #def comparison(self):
    #    pattern = re.compile('.*' + self.var.get() + '.*')
    #    return [w for w in self.lista if re.match(pattern, w)]

    def comparisonBD(self):
        return self.vue.onSearchComparaison(self.var.get())

if __name__ == '__main__':
    root = Tk()

    entry = AutocompleteEntry(lista, root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()
