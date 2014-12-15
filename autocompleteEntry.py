from tkinter import *
import re


class AutocompleteEntry(Entry):
    def __init__(self, commandes, *args, **kwargs):
        self.parent = args[0]
        self.commandes = commandes
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
            words = self.comparisonBD()
            print(words)
            if words:
                print(words)
                if not self.lb_up:
                    self.lb = Listbox(self.parent)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    print(w)
                    self.lb.insert(END,w.texte)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

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
        return self.commandes.searchText(self.var.get())

if __name__ == '__main__':
    root = Tk()

    entry = AutocompleteEntry(lista, root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()
