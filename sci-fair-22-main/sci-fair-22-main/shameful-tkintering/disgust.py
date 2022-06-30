
import tkinter as tk
import asyncio



    
def startgui():
    root = tk.Tk()
    root.title('CalligraphyCoin')
    root.geometry('300x200+50+50')
    root.resizable(False, False)
    root.iconbitmap(r'C:\Users\trist\OneDrive\Documents\Code\sci-fair-22\shameful-tkintering\logo.ico')
    print("New window created")
    root.mainloop()



async def main():
    while True:
        for i in range(10000):
            print(i)
            await asyncio.sleep(1)

async def booter():
    await asyncio.gather(main(), asyncio.get_event_loop().run_in_executor(None, startgui))

asyncio.run(booter())