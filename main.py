
import GenPriceGraph as g
import tkinter as tk
import pandas as pd

def main():

    g.init()

    root = tk.Tk()

    root.geometry("800x500")
    root.title("Real Estate Predictor")

    label = tk.Label(root, text="Welcome to REP", font=('Terminal', 18))
    label.pack(padx=20,pady=20)

    btn1 = tk.Button(root, text="Overall", font=('Terminal',16), command=overall)
    btn1.place(x=10,y=50)

    btn2 = tk.Button(root, text="Specific", font=('Terminal',16), command=specific)
    btn2.place(x=10,y=100)

    btn3 = tk.Button(root, text="Analyze", font=('Terminal',16), command=analyze)
    btn3.place(x=10,y=150)

    root.mainloop()

    return 0

def overall():
    def applytolabel(x):
        r = len(x)
        c = len(x[0])

        e = ''
        for i in range(r):
            for j in range(c):
                e += x[i][j]+'\t'
                if j==1:
                    for k in range(35-len(x[i][j])):
                        e += ' '
            e += '\n'
        return e

    page1 = tk.Tk()
    page1.geometry("900x500")
    page1.title("REP - Overall")

    btn1 = tk.Button(page1, text="Plot Map", font=('Terminal',16), command=g.plotMap)
    btn1.pack(padx=10,pady=10,side='top')

    scores = []
    regions = g.hp['RegionID']
    regNames = g.hp['RegionName']
    for i in range(len(regions)):
        scores.append([str(regions[i]),str(regNames[i]),str(int(g.getScore(regions[i])))])

    scores = pd.DataFrame(scores)
    scores = scores.sort_values(2, ascending=False)
    scores = scores.values.tolist()
    scores.insert(0, ['Reg','City Name','Score'])

    s = tk.Scrollbar(page1, orient='vertical')
    s.pack(side='right', fill='y')

    label = tk.Text(page1, width=60, height=420, font=('Terminal',16), yscrollcommand= s.set)
    label.insert('end',applytolabel(scores))
    label.configure(state='disabled')
    label.pack(padx=20,pady=20)



    s.config(command=label.yview)

    page1.mainloop()
    return 0

def specific():
    def applytolabel(x):
        r = len(x)
        c = len(x[0])

        e = ''
        for i in range(r):
            for j in range(c):
                e += x[i][j]+'\t'
            e += '\n'
        return e

    rlist = []
    regions = g.hp['RegionID']
    regNames = g.hp['RegionName']
    for i in range(len(regions)):
        rlist.append([str(regions[i]),str(regNames[i])])

    page2 = tk.Tk()
    page2.geometry("800x500")
    page2.title("REP - Specific")

    s = tk.Scrollbar(page2, orient='vertical')
    s.pack(side='right', fill='y')

    label = tk.Text(page2, width=40, height=420, font=('Terminal',16), yscrollcommand= s.set)
    label.insert('end',applytolabel(rlist))
    label.configure(state='disabled')
    label.pack(padx=20,pady=40,side='left')

    label2 = tk.Label(page2, text="Enter Region ID", font=('Terminal', 16))
    label2.pack(padx=40,pady=20, side='top')

    entry = tk.Entry(page2,font=('Terminal',16),width=6)
    entry.insert('end','102001')
    entry.pack(padx=40,pady=10,side='top')  

    btn1 = tk.Button(page2, text="Plot Price", font=('Terminal',16), command=lambda : g.plotRegionData(int(entry.get())))
    btn1.pack(padx=10,pady=10,side='top')

    btn2 = tk.Button(page2, text="Plot Rent", font=('Terminal',16), command=lambda : g.plotRegionRent(entry.get()))
    btn2.pack(padx=10,pady=10,side='top')


    page2.mainloop()

    return 0

def analyze():
    def applytolabel(x):
        r = len(x)
        c = len(x[0])

        e = ''
        for i in range(r):
            for j in range(c):
                e += x[i][j][:20]+'\t'
                if j==1:
                    for k in range(max(25-len(x[i][j]),5)):
                        e += ' '
                elif j==2:
                    for k in range(10-len(x[i][j])):
                        e += ' '
            e += '\n'
        return e
    def b1():
        label.delete('1.0','end')

        glist = []
        regions = g.hp['RegionID']
        regNames = g.hp['RegionName']

        for i in range(len(regions)):
            glist.append([str(regions[i]),str(regNames[i]),str(int(g.genDif(regions[i],grabFlag=1))),str(int(g.genDif(regions[i])))])

        glist = pd.DataFrame(glist)
        glist[2] = pd.to_numeric(glist[2])
        glist = glist.sort_values(2, ascending=False)
        glist[2] = glist[2].astype(str)
        glist = glist.values.tolist()
        glist.insert(0, ['Reg','City Name','Growth','Score'])

        label.insert('end',applytolabel(glist))
        return 0
    def b2():
        label.delete('1.0','end')

        glist = []
        regions = g.hp['RegionID']
        regNames = g.hp['RegionName']
         
        for i in range(len(regions)):
            glist.append([str(regions[i]),str(regNames[i]),str(int(g.genCost(regions[i],grabFlag=1))),str(int(g.genCost(regions[i])))])

        glist = pd.DataFrame(glist)
        glist[2] = pd.to_numeric(glist[2])
        glist = glist.sort_values(2, ascending=False)
        glist[2] = glist[2].astype(str)
        glist = glist.values.tolist()
        glist.insert(0, ['Reg','City Name','Cost','Score'])

        label.insert('end',applytolabel(glist))
        return 0
    def b3():
        label.delete('1.0','end')

        glist = []
        regions = g.hp['RegionID']
        regNames = g.hp['RegionName']

        for i in range(len(regions)):
            glist.append([str(regions[i]),str(regNames[i]),str(int(g.genPredRent(regions[i],grabFlag=1))),str(int(g.genPredRent(regions[i])))])

        glist = pd.DataFrame(glist)
        glist[2] = pd.to_numeric(glist[2])
        glist = glist.sort_values(2, ascending=False)
        glist[2] = glist[2].astype(str)
        glist = glist.values.tolist()
        glist.insert(0, ['Reg','City Name','Pred Rent','Score'])

        label.insert('end',applytolabel(glist))
        return 0
    def b4():
        label.delete('1.0','end')

        glist = []
        regions = g.hp['RegionID']
        regNames = g.hp['RegionName']

        for i in range(len(regions)):
            glist.append([str(regions[i]),str(regNames[i]),str(int(g.genYTP(regions[i],grabFlag=1))),str(int(g.genYTP(regions[i])))])

        glist = pd.DataFrame(glist)
        glist[2] = pd.to_numeric(glist[2])
        glist = glist.sort_values(2, ascending=False)
        glist[2] = glist[2].astype(str)
        glist = glist.values.tolist()
        glist.insert(0, ['Reg','City Name','YTP','Score'])

        label.insert('end',applytolabel(glist))
        return 0

    page3 = tk.Tk()
    page3.geometry("900x500")
    page3.title("REP - Analyze")

    s = tk.Scrollbar(page3, orient='vertical')
    s.pack(side='right', fill='y')

    label = tk.Text(page3, width=60, height=420, font=('Terminal',16), yscrollcommand= s.set)
    label.pack(padx=20,pady=40,side='left')

    label2 = tk.Label(page3, text="Select Field", font=('Terminal', 16))
    label2.pack(padx=40,pady=20, side='top')

    btn1 = tk.Button(page3, text="Growth", font=('Terminal',16), command=b1)
    btn1.pack(padx=10,pady=10,side='top')

    btn2 = tk.Button(page3, text="Cost", font=('Terminal',16), command=b2)
    btn2.pack(padx=10,pady=10,side='top')

    btn3 = tk.Button(page3, text="Rent", font=('Terminal',16), command=b3)
    btn3.pack(padx=10,pady=10,side='top')

    btn4 = tk.Button(page3, text="YTP", font=('Terminal',16), command=b4)
    btn4.pack(padx=10,pady=10,side='top')


    page3.mainloop()

    return 0

if __name__ == "__main__":
    main()