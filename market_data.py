
import datetime
import requests
import streamlit as st
import csv
import pandas as pd
api_key="zVf2sqpA4yrxKe_wrudpheSPUNCnSIV2"

#limit="50000"


def Aggregates(ticker,start_date,end_date):


    link= "https://api.polygon.io/v2/aggs/ticker/"
    url = link + ticker+"/range/1/minute/" +str(start_date)+"/"+str(end_date)+"?adjusted=true&sort=asc&limit=50000&"+"apikey="+api_key

    r=requests.get(url)
    data =r.json()

    #st.json(data)  UNCOMMENT TO DISPLAY DATA FOR DEBUG PURPOSE.

    if 'results' in data:
        df=pd.DataFrame(data['results'])
        
        return df
    else:

        st.write("results are not in dictionary. Please check URL and data")
        st.write("URL to fetch Data:",url)
        st.json(data)
        df=pd.DataFrame([0]) # POPULATING DF WITH 0 SO THAT ON RETURN WE CAN CHECK
        return df


def DailyOpenclose(ticker,date):

    link="https://api.polygon.io/v1/open-close/"
    url=link+ticker+"/"+str(date)+"?adjusted=true&"+"apikey="+api_key
    r=requests.get(url)
    data =r.json()
    print(data)
    #st.json(data)
    print(data['status'])
    if data['status'] == 'NOT_FOUND':
        st.error("No Data found")
        st.json(data)
        df=pd.DataFrame([data])
        print(df)
        print(df.status)
        return df

    elif data['status'] == 'OK':
        df=pd.DataFrame([data])
        print(df)
        print(df.status)
        return df
    else:
        df=pd.DataFrame({"status":"Not OK"})
        return df

def PreviousClose(ticker):
    link="https://api.polygon.io/v2/aggs/ticker/"
    url=link+ticker+"/prev?adjusted=true&"+"apikey="+api_key

    r=requests.get(url)
    data =r.json()
    #st.json(data)
    if 'results' in data:
        df=pd.DataFrame(data['results'])
        #st.dataframe(df)
        return df
    else:

        st.write("results are not in dictionary. Please check URL and data")
        st.write("URL to fetch Data:",url)
        st.json(data)
        df=pd.DataFrame([0])
        return df #check for columns

def Quotes(ticker):
    link="https://api.polygon.io/v3/quotes/"
    url=link+ticker+"?limit=50000&"+"apikey="+api_key

    r=requests.get(url)
    data =r.json()
    
    if 'results' in data:
        df=pd.DataFrame(data['results'])
        st.dataframe(df)
        return df
    else:

        st.write("results are not in dictionary. Please check URL and data")
        st.write("URL to fetch Data:",url)
        st.json(data)
        df=pd.DataFrame([0])
        return df


def SnapshotOption(underlying,ticker):
    link="https://api.polygon.io/v3/snapshot/options/"
    url=link+underlying+"/"+"O:"+ticker+"?apikey="+api_key
    r=requests.get(url)
    data =r.json()

    #print(data['results']['last_quote'])
    if 'results' in data:
        #st.info("We will add the values now")
        df=pd.DataFrame([data['results']])
        #st.dataframe(df)
        return df
    else:
        st.write("results are not in dictionary. Please check URL and data")
        st.write("URL to fetch Data:",url)
        st.json(data)
        df=pd.DataFrame([0])
        return df

def SnapshotStock(ticker):

    link="https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/"
    url=link+ticker+"?"+"apikey="+api_key

    r= requests.get(url)
    data = r.json()
    st.json(data)
    
    if 'ticker' in data:
        df=pd.DataFrame([data['ticker']])
        return df
    else:

        st.write("results are not in dictionary. Please check URL and data")
        st.write("URL to fetch Data:",url)
        st.json(data)
        df=pd.DataFrame([0])
        return df

def TrueSessionState():
    st.session_state['bt'] = True

def FalseSessionState():
    st.session_state['bt'] = False

# Stremlit part

def main():

    st.title("Data Extraction Tool")

    st.markdown('Welcome to this Data gathering tool! First Select your desired financial instrument using the sidebar on the left. Then Select the Tabs below as per your data requirements.')
    category=["Polygon Stocks","Polygon Options", "Indian Market"]
    
    choice=st.sidebar.radio("Select your desired data category",category)
    if choice == "Polygon Stocks":
        tabnames=["Aggregate (Bars)","Daily Open/Close","PreviousClose","Quotes","Snapshots"]
        tab1,tab2,tab3,tab4,tab5,=st.tabs(tabnames)

        with tab1:
            st.markdown("Get aggregate bars for a stock over a given date range.  Currently available data is of 'Minute' timespan.")
            # DATA ENTRY BY USER
            col1,col2,col3=st.columns(3)
            with col1:
                ticker=st.text_input("Enter stock Ticker",key='1',help="Stock Tickers are case sensitive. For e.g. 'MSFT' will be able to fetch the data. 'msft' will return empty data.")
                if ticker:
                    st.success("Ticker Entered")
            with col2:
                start_date=st.date_input("Enter Start Date")
                #st.success("Entered start Date:",start_date)

            with col3:
                end_date=st.date_input("Enter End Date")
                #st.success("Entered end Date:",end_date)

            
            #===============================================================================================

            # DATA GATHERING FROM POLYGON
            col1,col2=st.columns([2,1])
            # Info about data.  Generate Data Button Download Data
            #with col1:
            f1=st.button("Fetch Data From Polygon")
            if f1:
                if ticker == "" :
                    st.error("NO Ticker Provided. Please enter the ticker")
                else:
                    df=Aggregates(ticker,start_date,end_date)
                    if df.size > 1:

                        st.dataframe(df.head())
                        file_n="Aggregates_"+str(start_date)+"_"+str(end_date)+"_"+ticker+".csv"
                        download=st.download_button("Download Data in CSV format",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

# -----------------------------------------------------------------------------------------------------------------------------------------------------
        with tab2:

            st.markdown("Get the open, close and afterhours prices of an options contract on a certain date.")

            # DATA ENTRY BY USER
            col1,col2=st.columns(2)
            with col1:
                ticker=st.text_input("Enter a stock Ticker",key="2",help="Stock Tickers are case sensitive. For e.g. 'MSFT' will be able to fetch the data. 'msft' will return empty data.")
                if ticker:
                    st.info("Ticker Entered")

            with col2:
                date=st.date_input("Enter The Date")

            #===============================================================================================
            # DATA GATHERING FROM POLYGON
            col1,col2=st.columns([2,1])
            with col1:

                f2=st.button("Fetch Data From Polygon",key='12')
                if f2:
                    if ticker == "" :
                        st.error("NO Ticker Provided. Please enter the ticker")
                    else:
                        df=DailyOpenclose(ticker,date)
                        if df['status'].iloc[0] == 'OK':
                            st.dataframe(df.head())
                            file_n="DailyOpenClose_"+str(date)+"_"+ticker+".csv"
                            #df=DailyOpenclose(ticker,date)
                            #if df is not None:
                            download=st.download_button("Download Data in CSV format",key="2",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

# -----------------------------------------------------------------------------------------------------------------------------------------------------
        with tab3:

            st.markdown("Get the previous day's open, high, low, and close (OHLC) for the specified stock ticker.")
            ticker=st.text_input("Enter a stock Ticker",key="3",help="Stock Tickers are case sensitive. For e.g. 'MSFT' will be able to fetch the data. 'msft' will return empty data.")
            if ticker:
                st.info("Ticker Entered")

            f3=st.button("Fetch Data From Polygon",key="31")
            if f3:
                if ticker == "" :
                    st.error("NO Ticker Provided. Please enter the ticker")
                else:
                    df=PreviousClose(ticker)    
                    if df.size > 1:
                        st.success("Snapshot of Data")
                        st.dataframe(df)
                        file_n="PreviousClose_"+ticker+".csv"
                    #df=PreviousClose(ticker)
                    #if df is not None:
                        download=st.download_button("Download Data in CSV format",key="3",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')
# -----------------------------------------------------------------------------------------------------------------------------------------------------
        with tab4:
            st.markdown("Get quotes for a stock ticker symbol in a given time range.")
            ticker=st.text_input("Enter a stock Ticker",key="4",help="Stock Tickers are case sensitive. For e.g. 'MSFT' will be able to fetch the data. 'msft' will return empty data.")
            if ticker:
                st.info("Ticker Entered")
            f4=st.button("Fetch Data From Polygon",key="41")
            if f4:
                if ticker == "" :
                    st.error("NO Ticker Provided. Please enter the ticker")
                else:
                    df=Quotes(ticker)

                    if df.size > 1: # checking if df has more than 1 cols. ==> Doesnt contain 0. have legit data.
                        st.success("Snapshot of Data")
                        st.dataframe(df)
                        file_n="Quotes_"+ticker+".csv"
                    #df=PreviousClose(ticker)
                    #if df is not None:
                        download=st.download_button("Download Data in CSV format",key="4",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

        with tab5:
            st.markdown("Get the most up-to-date market data for a single traded stock ticker.")
            
            ticker=st.text_input("Enter underlying Asset",key="5",help="Stock Tickers are case sensitive. For e.g. 'MSFT' will be able to fetch the data. 'msft' will return empty data.")
            if ticker:
                st.info("Value is Entered")

            f5=st.button("Fetch Data From Polygon",key="f5")
            if f5:
                if ticker == "" :
                    st.error("Please provide ticker.")
                else:
                    df=SnapshotStock(ticker)

                    if df.size > 1: # checking if df has more than 1 cols. ==> Doesnt contain 0. have legit data.
                        st.success("Snapshot of Data")
                        st.dataframe(df)
                        file_n="snapshot_"+ticker+".csv"
                        download=st.download_button("Download Data in CSV format",key="5",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')




# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=--=-==-=-=-=-=-=--=-=-=-=-=-=-=

    elif choice =="Polygon Options":
        #st.write("We have selected Options")
        tabnames=["Aggregate (Bars)","Daily Open/Close","PreviousClose","Quotes","Snapshots"]
        tab1,tab2,tab3,tab4,tab5,=st.tabs(tabnames)

        with tab1:

            #st.header("Aggregates (Bars):")
            st.markdown("Get aggregate bars for an option contract over a given date range.  Currently available data is of 'Minute' timespan.")
            # DATA ENTRY BY USER
            col1,col2,col3=st.columns(3)
            with col1:
                ticker="O:"+st.text_input("Enter Options Ticker",key="op1",help="sample MSFT220805C00275000")
                if ticker:
                    st.info("Ticker Entered")
            with col2:
                start_date=st.date_input("Enter Start Date",key="ot1")
                #st.success("Entered start Date:",start_date)
            with col3:
                end_date=st.date_input("Enter End Date",key="op2")
                #st.success("Entered end Date:",end_date)
            
            #===============================================================================================
            # DATA GATHERING FROM POLYGON
            col1,col2=st.columns([2,1])
            # Info about data.  Generate Data Button Download Data
            
            f1=st.button("Fetch Data From Polygon",key="1")
            if f1:
                if ticker == "" :
                    st.error("NO Ticker Provided. Please enter the ticker")
                else:
                    df=Aggregates(ticker,start_date,end_date)
                    if df.size > 1:

                        st.dataframe(df.head())
                        file_n="Aggregates_"+str(start_date)+"_"+str(end_date)+".csv"
                        download=st.download_button("Download Data in CSV format",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

#---------------------------------------------------------------------------------------------------------------------------------------------

        with tab2:

            st.markdown("Get the open, close and afterhours prices of an options contract on a certain date.")
            # DATA ENTRY BY USER
            col1,col2=st.columns(2)
            with col1:
                ticker="O:"+st.text_input("Enter Options Ticker",key="2",help="sample MSFT220805C00275000")
                if ticker:
                    st.info("Ticker Entered")

            with col2:
                date=st.date_input("Enter The Date")

            #===============================================================================================
            # DATA GATHERING FROM POLYGON
            col1,col2=st.columns([2,1])
            with col1:

                f2=st.button("Fetch Data From Polygon",key="col2")
                if f2:
                    if ticker == "" :
                        st.error("NO Ticker Provided. Please enter the ticker")
                    else:
                        df=DailyOpenclose(ticker,date)
                        if df["status"].iloc[0] == 'OK':
                            st.dataframe(df.head())
                            file_n="DailyOpenClose_"+str(date)+"_"+ticker+".csv"  
                            download=st.download_button("Download Data in CSV format",key="2",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')
#----------------------------------------------------------
        with tab3:

            #st.header("Previous Close")
            st.markdown("Get previous close for an option contract.")
            ticker="O:"+st.text_input("Enter an Options Ticker",key="3",help="sample MSFT220805C00275000")
            if ticker:
                st.info("Ticker Entered")
            f3=st.button("Fetch Data From Polygon",key="tab3")
            if f3:
                if ticker == "" :
                    st.error("NO Ticker Provided. Please enter the ticker")
                else:
                    df=PreviousClose(ticker)
                    if df.size > 1: 
                        st.success("Snapshot of Data")
                        st.dataframe(df)
                        file_n="PreviousClose_"+ticker+".csv"
                    
                        download=st.download_button("Download Data in CSV format",key="3",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

#-----------------------------------------------------------------------------

        with tab4:
            st.markdown("Get quotes for an options ticker symbol in a given time range.")
            ticker="O:"+st.text_input("Enter Options Ticker",key="4",help="sample MSFT220805C00275000")
            if ticker:
                st.info("Ticker Entered")
            f4=st.button("Fetch Data From Polygon",key="tab4")
            if f4:
                if ticker == "" :
                    st.error("NO Ticker Provided. Please enter the ticker")
                else:
                    df=Quotes(ticker)

                    if df.size > 1: 
                        st.success("Snapshot of Data")
                        st.dataframe(df)
                        file_n="Quotes_"+ticker+".csv"
                    
                        download=st.download_button("Download Data in CSV format",key="4",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

    #-----------------------------------------------------------------------------
        with tab5:
            st.markdown("Get a snapshot for an options ticker symbol in a given time range.")
            col1,col2=st.columns(2)
            with col1:
                underlying=st.text_input("Enter underlying Asset")
            with col2:
                ticker=st.text_input("Enter Options Contract",key="tab55",help="sample MSFT220805C00275000")
            if ticker and underlying:
                st.info("Values are Entered")

            f5=st.button("Fetch Data From Polygon",key="t5")
            if f5:
                if ticker == "" or underlying == "" :
                    st.error("Please provide both Values.")
                else:
                    df=SnapshotOption(underlying,ticker)

                    if df.size > 1: # checking if df has more than 1 cols. ==> Doesnt contain 0. have legit data.
                        st.success("Snapshot of Data")
                        st.dataframe(df)
                        file_n="snapshot_"+ticker+".csv"
                    #df=PreviousClose(ticker)
                    #if df is not None:
                        download=st.download_button("Download Data in CSV format",key="55",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')

    elif choice =="Indian Market":
        st.markdown("We have two types of data for stock tickers. Options and Futures.")
        st.markdown("First,select a date to view avaialble companies. Then select which financial instrument's data you want to download.")
        if 'bt'not in st.session_state:
            st.session_state['bt'] = False
        dat=st.date_input("Enter a date",key="31",on_change=FalseSessionState)
        
        x = datetime.date(2019,5,31)
        #print(type(dat))
        d1=st.button("Fetch Data",key="in3",on_click=TrueSessionState)         
        if st.session_state['bt']:      
            if dat < x:
                filename="GFDLNFO_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)
                print(filename)
            else:
                filename="GFDLNFO_BACKADJUSTED_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)
            try:
                raw_data=pd.read_csv("data/{0}.csv".format(filename))
                sep_ticker=[]
                tickers=list(raw_data["Ticker"].unique())
                for tic in tickers:
                    ticr=""
                    if "-" not in tic:
                        for t in tic:
                            if t.isdigit():
                                break
                            else:
                                ticr+=t 
                    sep_ticker.append(ticr)    

                unique_companies=list(set(sep_ticker))
                #   2. Seperate options from futures
                #unique_companies=[s for s in sep_ticker if ".NFO" not in s] 
                unique_ticker=st.selectbox("Select the company whose data you want to download",sorted(unique_companies))
                if unique_ticker:
                    #st.text("You have selected {0}".format(unique_ticker))
                    available_options=[]
                    available_futures=[]
                # Split unique ticker for futures and options contracts
                    for ele in tickers:
                        if unique_ticker in ele:# if BANKNIFTY in BANKNIFTY-I.NFO. ISSUE WAS WHEN WE CHECK IF NIFTY IN BANKNIFTY
                            if "-" in ele:
                                # CHECK IF ELE AND UNIQUE TICKER ARE EXACT MATCH. 
                                tic_extract= ele.split("-")[0] # INPUT -> BANKNIFTY-I.NFO , O/p -> BANKNIFTY 
                                if tic_extract == unique_ticker:
                                    available_futures.append(ele.split(".")[0])
                              
                            else:# check if option tickers are matching 
                                t_extract=""
                                for e in ele.split(".")[0]:
                                    if e.isdigit():# BREAK AS SOON AS YOU HIT A DIGIT. THIS WILL SEPERATE TICKER AND ITS OPTIONS CONTRACT
                                        break
                                    else:
                                        t_extract+=e
                                if t_extract == unique_ticker: # MATCHING EXTRACTED TICKER WITH UNIQUE TICKER
                                    available_options.append(ele.split(".")[0])   
                               

                    col1,col2,col3 = st.columns(3)
                    with col1:

                        st.markdown("Select Option contracts for {0}".format(unique_ticker))
                        selected_options = st.selectbox("Select Option contracts",available_options)
                        if selected_options:
                            #download=st.download_button("Download Data in CSV format",key="5",data=df.to_csv(index=False),file_name=file_n,mime='text/csv')
                            #st.text("You have selected {0}".format(selected_options))
                            file="{0}.csv".format(selected_options)
                            #df=raw_data[raw_data["Ticker"].str.contains(selected_options)]
                            df=raw_data[raw_data["Ticker"]==selected_options]
                            download_selection=st.download_button("Download Data in CSV format",key="1",data=df.to_csv(index=False),file_name=file,mime='text/csv')

                    with col2:

                        st.markdown("Select Futures contracts for {0}".format(unique_ticker))
                        selected_futures = st.selectbox("Select Futures contracts", available_futures)
                        if selected_futures:
                            file="{0}.csv".format(selected_futures)
                            con=selected_futures+".NFO"
                            df=raw_data[raw_data["Ticker"]==con]
                            #df=raw_data[raw_data["Ticker"].str.contains(selected_futures)] CHANGED. REASON: BANKNIFTY-II WAS ALSO HAVING DATA OF BANKNIFTY-III. AS STR.CONTAINS() MATCHED 
                            download_selection=st.download_button("Download Data in CSV format",key="2",data=df.to_csv(index=False),file_name=file,mime='text/csv') 
                #session_state = SessionState.get(col1=False,col2=False)
 
                    with col3:
                        #data_range=st.radio("Do you want multiperiod data for {0}?".format(unique_ticker),["Yes","No"])

                        st.markdown("Here you can download combined data of options and futures for {0} over a period of time".format(unique_ticker))
                        # entry date is "dat"
                        end_date=st.date_input("Enter end date",key="7")
                        day_delta=datetime.timedelta(days=1)
                        fd=st.button("Fetch Data",key="7")
                        if fd:
                            st.info("You will get your data here soon.")
                            # Loop through files processing the data and adding it to the DF 
                            df_merged=pd.DataFrame()
                            while dat <= end_date:
                                if dat < x:
                                    filename="GFDLNFO_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)
                                    
                                else:
                                    filename="GFDLNFO_BACKADJUSTED_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)
                                # import csv file for the date.
                                try:
                                    r_data=pd.read_csv("data/{0}.csv".format(filename))
                                    #print(raw_data.head())
                                #st.dataframe(raw_data.head(30))
                                except FileNotFoundError:
                                    dat = dat + day_delta
                                    #st.error("Data is not available for selected date. Please try again with different date.")
                                    continue
                               
                                finally:
                                    print("Unique ticker",unique_ticker)
                                    print(r_data.head(2))
                                    print(available_futures[0])

                                    tickers=list(r_data["Ticker"].unique())
                                    for ele in tickers: # e.g. first ticker in df = BANKNIFTY-I.NFO
                                        if unique_ticker in ele: # if BANKNIFTY in BANKNIFTY-I.NFO. ISSUE IS WHEN WE CHECK IF NIFTY IN BANKNIFTY
                                            if "-" in ele:
                                                # CHECK IF ELE AND UNIQUE TICKER ARE EXACT MATCH. 
                                                #tic_extract= ele.split("-")[0] # INPUT -> BANKNIFTY-I.NFO , O/p -> BANKNIFTY 
                                                #if tic_extract == unique_ticker:
                                                 #   available_futures.append(ele.split(".")[0])
                                                print(".")  
                                            else:
                                                t_extract=""
                                                for e in ele.split(".")[0]:
                                                    if e.isdigit():
                                                        break
                                                    else:
                                                        t_extract+=e
                                                if t_extract == unique_ticker:
                                                    available_options.append(ele.split(".")[0])     
                                    
                                    if not available_options: # List will be empty if contract is not present for that day. IF it is empty, move to next date.
                                        dat = dat + day_delta
                                        continue 
                                    print("Available option snapshot",available_options)     
                                 # create availavle_options list. everyday might have different sets of contracts.   
                                 # create df and add futures - I data to it.
                                    con=selected_futures+".NFO" # hardcode here.
                                    print("here lies con---------------------",con)
                                    

                                    df_fut=r_data[r_data["Ticker"]==con]
                                    print("-----------------------------Future Head------------------------")
                                    print(df_fut)
                                    if df_merged.empty: 
                                        df_merged=df_fut
                                        print("---------------------------------------------------------")
                                        print(df_merged)
                                        print("---------------------------------------------------------")
                                    
                                    st.dataframe(df_merged)
                                # iterate through available options, change col names and merge into df_merged

                                    for con in available_options:
                                        
                                        df_op=r_data[r_data["Ticker"]==con]
                                        name=con.split(".")[0]
                                        df_op.drop(columns=["Ticker","Date"],inplace=True)
                                        
                                        df_op.columns=["Time",name+"_O",name+"_H",name+"_L",name+"_C",name+"_Vol",name+"_O.Interest"]
                                        
                                        #df_merged=df_merged.merge(df_op,how="outer",on="Time")
                                        df_merged=pd.concat([df_merged,df_op],axis=1)
                                        print(df_merged)
                                        
                                       
                                    print("Before Update",dat)
                                    dat = dat + day_delta
                                    print("After Update",dat)
                                    st.dataframe(df_merged)

                                    
                            file_n="Combined_Data_"+str(unique_ticker)+"_" + str(dat)+"_"+str(end_date)+".csv"
                            download=st.download_button("Download range data",data=df_merged.to_csv(index=False),file_name=file_n,mime='text/csv')
                            
                #print(raw_data.head())
            #st.dataframe(raw_data.head(30))
            except FileNotFoundError:
                st.error("Data is not available for selected date. Please try again with different date.")
            # Display Unique comanpanies whose data is available.
            # Upon selection of company, show unique contracts that are available.
            #   1. Seperate Ticker from numbers

                
#---------------------------------------------------------------------------------------------------------------------------------------------


        st.markdown("Here you can download combined data of options and futures")#for {0} over a period of time".format(unique_ticker))
        # entry date is "dat"
        end_date=st.date_input("Enter end date",key="7")
        day_delta=datetime.timedelta(days=1)             
        st.info("You will get your data here soon.")
        # Loop through files processing the data and adding it to the DF 
        df_options=pd.DataFrame()
        df_futures=pd.DataFrame()
        
           
        choices=["Options","Futures"]
        ch=st.radio("Which instrument's combined data do you want?",choices)
        if ch =="Options":
            while dat <= end_date:
                if dat < x:
                    filename="GFDLNFO_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)      
                else:
                    filename="GFDLNFO_BACKADJUSTED_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)
                # import csv file for the date.
                try:
                    r_data=pd.read_csv("/home/rahul/data/{0}.csv".format(filename))
                    av_options=[]
                    #av_futures=[]
                    tickers=list(r_data["Ticker"].unique())
                    for ele in tickers: # e.g. first ticker in df = BANKNIFTY-I.NFO
                        if unique_ticker in ele: # if BANKNIFTY in BANKNIFTY-I.NFO. ISSUE IS WHEN WE CHECK IF NIFTY IN BANKNIFTY
                            if "-" in ele:
                                continue      
                            else:
                                t_extract=""
                                for e in ele.split(".")[0]:
                                    if e.isdigit():
                                        break
                                    else:
                                        t_extract+=e
                                if t_extract == unique_ticker:
                                    av_options.append(ele)   

                    for options in av_options:
                        df_op = r_data[r_data["Ticker"]==options]
                        df_op.dropna(inplace=True)
                        
                        if df_options.empty:
                            df_options=df_op
                        else:
                            df_options=df_options.merge(df_op,how="outer",on=["Date","Time"])                
                    start_date += datetime.timedelta(days=1)
                except FileNotFoundError:
                    dat = dat + day_delta
                    continue               
            
            if not df_options.empty:
                file_n="Options_Data_"+str(unique_ticker)+"_" + str(dat)+"_"+str(end_date)+".csv"
                df_options.sort_values(["Date","Time"],inplace=True)
                df_options.dropna(subset=["Date"],inplace=True)
                download=st.download_button("Download Options Data",data=df_options.to_csv(index=False),file_name=file_n,mime='text/csv')

        elif ch=="Futures":
            while dat <= end_date:
                if dat < x:
                    filename="GFDLNFO_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)  
                else:
                    filename="GFDLNFO_BACKADJUSTED_"+str(dat.day).zfill(2)+str(dat.month).zfill(2)+str(dat.year)
                # import csv file for the date.
                try:
                    r_data=pd.read_csv("/home/rahul/data/{0}.csv".format(filename))
                    #av_options=[]
                    av_futures=[]
                    tickers=list(r_data["Ticker"].unique())
                   
                    for ele in tickers: # e.g. first ticker in df = BANKNIFTY-I.NFO
                        if unique_ticker in ele: # if BANKNIFTY in BANKNIFTY-I.NFO. ISSUE IS WHEN WE CHECK IF NIFTY IN BANKNIFTY
                            if "-" in ele:
                                tic_extract= ele.split("-")[0] # INPUT -> BANKNIFTY-I.NFO , O/p -> BANKNIFTY 
                                if tic_extract == unique_ticker:
                                    av_futures.append(ele)
                    
                            else:
                                continue
                    
                    if not av_futures:
                        dat + dat + day_delta
                        continue           

                    for fut in av_futures:
                        #print("current Futures:",fut)
                        df_fut=r_data[r_data["Ticker"]==fut]
                        
                        df_fut.dropna(inplace=True)
                        if df_futures.empty:
                            df_futures=df_fut
                        else:
                            df_futures=pd.concat([df_futures,df_fut])
                    
                    start_date += datetime.timedelta(days=1)
                
                except FileNotFoundError:

                    dat = dat + day_delta
                    continue               
            
            if not df_futures.epmty:
                file_n="Futures_Data_"+str(unique_ticker)+"_" + str(dat)+"_"+str(end_date)+".csv"
                df_futures.sort_values(["Date","Time"],inplace=True)
                df_futures.dropna(subset=["Date"],inplace=True)
                download=st.download_button("Download Futures Data",data=df_futures.to_csv(index=False),file_name=file_n,mime='text/csv')
             


if __name__ == '__main__':
    main()
