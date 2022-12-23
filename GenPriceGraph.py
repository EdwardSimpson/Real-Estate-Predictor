# Capstone Data Extract

from pickle import TRUE
import math
from re import A
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# from sklearn.preprocessing import MinMaxScaler
 # https://builtin.com/data-science/time-series-forecasting-python
 # https://ucr.fbi.gov/crime-in-the-u.s/2010/crime-in-the-u.s.-2010/tables/10tbl08.xls/view
 # https://simplemaps.com/data/us-cities need to cite
 # https://jcutrer.com/python/learn-geopandas-plotting-usmaps
 # https://towardsdatascience.com/the-easiest-way-to-plot-data-from-pandas-on-a-world-map-1a62962a27f3

def main():
    return 0

def getRegionData(RegionNum):
    """
     Gets a numpy array, of a specific city, based on Region Number
    """
    hp = pd.read_csv('data/House_Prices.csv')
    hp.drop(hp.iloc[:,1:5], inplace=True, axis=1)
    hp = hp.loc[hp['RegionID'] == RegionNum]
    hp = hp.iloc[:,1:]
    hp=hp.transpose(copy=False)
    hp=hp.to_numpy()

    return hp
    
def plotRegionData(RegionNum):
    """
     Plots House Price Data based on the Region Number
    """
    data = hp.loc[hp['RegionID'] == int(RegionNum)].iloc[0]
    reg = data[1]
    data=data[2:]
    data = data.to_numpy()
    y = pd.Series(range(0,data.shape[0]))
    plt.tick_params(left = True, right = False , labelleft = True ,labelbottom = False, bottom = False)
    plt.scatter(y,data,s=1)
    plt.xlabel('Time')
    plt.ylabel('Cost')
    plt.title('Avg House Price in '+str(reg))
    plt.show()

    return 0

def plotRegionRent(RegionNum):
    """
     Plots House Price Data based on the Region Number
    """
    datar = hr.loc[hr['RegionID'] == int(RegionNum)].iloc[0]
    reg = datar[1]
    datar=datar[2:]
    datar = datar.to_numpy()
    y = pd.Series(range(0,datar.shape[0]))
    plt.tick_params(left = True, right = False , labelleft = True ,labelbottom = False, bottom = False)
    plt.scatter(y,datar,s=1)
    plt.xlabel('Time')
    plt.ylabel('Cost')
    plt.title('Avg House Rent in '+str(reg))
    plt.show()
    return 0

def getRegionNum(City, State):
    """
     Gets Region Number based on entered City and Date
    """
    hp = pd.read_csv('data/House_Prices.csv')
    hp.drop(hp.iloc[:,5:], inplace=True, axis=1)
    hp = hp.loc[hp['RegionName'] == City+", "+State]

    #add error checker 10.3.22

    return hp.at[1,"RegionID"]  

def plotMap():
    """
     Plots a normalized val on to a US map
    """
    coords = pd.read_csv('data/Coords.csv', encoding='ISO-8859-1')

    regions = hp['RegionID']

    mapi = pd.DataFrame(columns=['lat','lng','val'])

    for i in range(len(regions)):
        tmp = coords.loc[coords['RegionID'] == regions[i]]
        if not tmp.empty:
            tmp.iloc[0]
            lat = float(tmp['lat'])
            lng = float(tmp['long'])

            mapi = mapi.append({'lat': lat, 'lng': lng, 'val': int(getScore(regions[i]))}, ignore_index=True)


    fig, ax = plt.subplots(figsize=(20,20))

    countries = gpd.read_file('data/usa-states-census-2014.shp')

    # val = MinMaxScaler().fit_transform(np.array(mapi['val']).reshape(-1,1))
    # siz = ((val+1)*5)**2
    
    countries.plot(color="lightgray",ax=ax)
    mapi.plot(x="lng",y="lat",kind="scatter",c="val",colormap="YlOrRd",ax=ax,alpha=0.5)
    ax.grid(b=True, alpha=0.5)
  
    plt.show()

    return 0

def getScore(RID):
    """
    Generate score for a region, out of 1000
    """
    # adjustable parameters
    pDif = 0.2 
    pCost = 0.1
    pRent = 0.1
    pYTP = 0.6

    Score = pDif*genDif(RID)+pCost*genCost(RID)+pRent*genPredRent(RID)+pYTP*genYTP(RID)

    return Score

def genCost(RID, grabFlag=0):
    # cost of house
    # normalize then * by 1000
    cost = hp.loc[hp['RegionID'] == RID, '7/31/2022'].iloc[0]
    costTrue=cost
    cost = -1000 * ((cost - hpMin)/(hpMax - hpMin)) + 1000
    cost = math.trunc(cost)

    if grabFlag==1:
        return int(costTrue)

    return int(cost)

def genDif(RID, grabFlag=0):
    # predicited cost of house - current
    # using forecasting - simple exponential smoothing

    data = hp.loc[hp['RegionID'] == RID].iloc[0]
    data = data[2:]

    test_as = np.arange(0.2,0.9,0.05)
    minA=0.1
    minSSE=ses(data.to_numpy(),1,0.1)

    for i in range(len(test_as)):
        a = test_as[i]
        tmp = ses(data.to_numpy(),1,a)
        if tmp<minSSE:
            minA=a
            minSSE=tmp

    pred = ses(data.to_numpy(),3,minA,grabFlag=1, printFlag=0)


    dif = data['7/31/2022'] - pred

    # get min and max for avg house prices
    mind = -1*13000
    maxd = 13000

    if dif>maxd:
        score=1000
    elif dif<mind:
        score=0
    else:
        score = (dif-mind)/(maxd-mind)
        score *= 1000
        
    if grabFlag==1:
        return dif

    return score

def genYTP(RID, grabFlag=0):
    # years to pay back based on current price and rent
    price = hp.loc[hp['RegionID'] == RID, '7/31/2022'].iloc[0]
    rent = hr.loc[hr['RegionID'] == RID, '2022-07'].iloc[0]

    i=0
    while price > 0 :
        i+=1
        price -= rent

    # change into years
    i /= 12
    yr = round(i,1)

    # normalization based off of manual input, based on avg
    i = (yr-2)/(40-2)
    i = -1000 * i + 1000
    if i<=0:
        i=0
    elif i>=1000:
        i=1000

    if grabFlag==1:
        return yr

    return int(i)

def genPredRent(RID, grabFlag=0):
    # predicted rent
    rent = hr.loc[hr['RegionID'] == RID].iloc[0]
    rent = rent[2:]

    test_as = np.arange(0.2,0.9,0.05)
    minA=0.1
    minSSE=ses(rent.to_numpy(),1,0.1)

    for i in range(len(test_as)):
        a = test_as[i]
        tmp = ses(rent.to_numpy(),1,a)
        if tmp<minSSE:
            minA=a
            minSSE=tmp

    pred = ses(rent.to_numpy(),3,minA,grabFlag=1, printFlag=0)

    if pred>hrMax:
        score=1000
    elif pred<hrMin:
        score=0
    else:
        score = (pred-hrMin)/(hrMax-hrMin)
        score *= 1000

    if grabFlag==1:
        return pred

    return int(score)

def ses(x, n, a, grabFlag=0, printFlag=0):
    cols = len(x)
    x = np.append(x,[np.nan]*n)

    f = np.full(cols+n,np.nan)
    f[1]=x[0]

    for i in range(2,cols+1):
        f[i] = a*x[i-1]+(1-a)*f[i-1]

    f[cols+1:]=f[i]
    df = pd.DataFrame.from_dict({"Demand":x,"Forecast":f,"Error":x-f})

    RMSE = (df["Error"]**2).sum()/len(df)
    # print("SSE:",round(RMSE,2))
    if printFlag==1:
        df.index.name = "Periods"
        df[["Demand","Forecast"]].plot(title="Simple Smoothing",style=["-","--"])
        plt.show()

    if grabFlag == 0:
        return RMSE
    else:
        return f[cols+1]

def init():
    global hp, hpMax, hpMin
    global hr, hrMax, hrMin

    hp = pd.read_csv('data/House_Prices_Fixed.csv')
    hr = pd.read_csv('data/House_Rental.csv')

    #get min and maxes
    hpMax = hp.iloc[:,2:].max(axis=0).max()
    hpMin = hp.iloc[:,2:].min(axis=0).min()

    hrMax = hr.iloc[:,2:].max(axis=0).max()
    hrMin = hr.iloc[:,2:].min(axis=0).min()


    
    # calculating stardard deviation across price data
    med = hp.iloc[:,2:].median(axis=1)[0]

    hpStd = hp.copy(deep=True)
    hpStd = hpStd.iloc[:,2:]
    hpStd = hpStd.to_numpy()
    hpStd = np.nan_to_num(hpStd,nan=med)
    hpStd = np.std(hpStd)
    

    return 0

if __name__ == "__main__":
    main()