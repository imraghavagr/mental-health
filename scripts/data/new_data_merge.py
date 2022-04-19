import pandas as pd

##reading both datasets
df1 = pd.read_csv('../../data/raw/Mental Health Checker.csv')
df2 = pd.read_csv('../../data/raw/survey.csv')

#droping unnecessary features from df1 and df2

df1.drop('Timestamp',axis=1,inplace=True)
df2.drop(columns=['Timestamp','Username','Please enter your name','How comfortable were you with the Survey Questions?','Please feel free to provide any kind of feedback!'],axis = 1,inplace=True)

#changin column names of df2 to that of df1
cols = df1.columns
df2.columns = cols

#vertially concatenating df1 and df2
df3 = pd.concat([df1,df2],axis=0)

#correcting values

#no_yes_maybe/ no_yes
no_yes_maybe_cols = ["loan","friend_help","share_feel","have_someone","bullied","family_support","compare_life","religious","goal","suicidal","sleep_disorder","love_someone","die_someone","thoughts_command","self_harm","thoughts_acted","thoughts_acted2","voices","harming_others","suicide","suicidal_thoughts","therapy"]
for x in no_yes_maybe_cols:
    df3[x].replace(to_replace="Yes",value="yes",inplace=True)
    df3[x].replace(to_replace="No",value="no",inplace=True)
    df3[x].replace(to_replace="Maybe",value="maybe",inplace=True)

df3["friend_help"].replace(to_replace="idk",value="maybe",inplace=True)


df3['marital'].replace(to_replace ="Single",value ="single",inplace=True)
df3['marital'].replace(to_replace ="Married",value ="married",inplace=True)

df3['income'].replace(to_replace ="<10000",value ="<10",inplace=True)
df3['income'].replace(to_replace ="<20000",value ="<20",inplace=True)
df3['income'].replace(to_replace ="<30000",value ="<30",inplace=True)
df3['income'].replace(to_replace ="30000+",value ="30+",inplace=True)
df3['income'].replace(to_replace ="50000+",value ="50+",inplace=True)

df3['friend_no'].replace(to_replace="None",value="none",inplace=True)
df3['friend_no'].replace(to_replace="3 +",value="3+",inplace=True)

df3['friend_interact'].replace(to_replace="3 +",value="3+",inplace=True)
df3['friend_interact'].replace(to_replace="none",value="0",inplace=True)

df3['lonely'].replace(to_replace="Yes",value="yes",inplace=True)
df3['lonely'].replace(to_replace="No",value="no",inplace=True)
df3['lonely'].replace(to_replace="Maybe",value="maybe",inplace=True)
df3['lonely'].replace(to_replace="Sometimes",value="sometimes",inplace=True)
df3['lonely'].replace(to_replace="Never felt lonely",value="never",inplace=True)

df3['hangout'].replace(to_replace="None",value="none",inplace=True)

df3['mental_disorder'].replace(to_replace="Depression",value="depression",inplace=True)
df3['mental_disorder'].replace(to_replace="Stress",value="stress",inplace=True)
df3['mental_disorder'].replace(to_replace="Anxiety",value="anxiety",inplace=True)

df3['thoughts_time'].replace(to_replace="Night",value="night",inplace=True)
df3['thoughts_time'].replace(to_replace="Evening",value="evening",inplace=True)
df3['thoughts_time'].replace(to_replace="Morning",value="morning",inplace=True)

# handling missing values
for x in df3.columns:
    if df3[x].isnull().sum()>0:
        df3[x].fillna(df3[x].mode()[0],inplace=True)

#saving new csv file inside 'processed' directory
df3.to_csv('../../data/processed/completeData.csv',index=False)