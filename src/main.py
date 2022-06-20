from tkinter import *
import layout

def main():
    root = Tk() 
    
    m = layout.appMenu(root,None,'Statistics data analysis tool')
    
    root.mainloop()

if __name__ == "__main__":
    main()