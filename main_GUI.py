from tkinter import *

class PlayBlackJackGUI:
    """ Blackjack game GUI """
    
    ICON_MASTER_PATH = "C:/Users/mathi/Documents/amusement/python/blackjack/icon_master.ico"
    
    def __init__(self):
        self.master = Tk()
        
        # master's customization
        self.master.title("Blackjack")
        self.master.geometry("800x550")
        self.master.minsize(800,550)
        self.master.maxsize(800,550)
        self.master.iconbitmap(self.ICON_MASTER_PATH)
        
        
        
        self.master.mainloop()
        
        

if __name__ == "__main__":
    PlayBlackJackGUI()
        