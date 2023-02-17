#importing the necessary libraries
import pandas as pd
from geopy.distance import great_circle

#Reading the csv dataset as python dataframe
df=pd.read_csv("assignment_data.csv")

#Creating new column "geo_points" to make a list of latitude and longitude.
#So that we can calculate the distance between the two locations easily using geopy library.

df['geo_points']=list(zip(df["latitude"],df["longitude"]))

#calculating the distance between the successive locations using geopy library, geocircle distance function.
#Calculating the maximum number of single-character edits using the Levenshtein distance.

#function for calculating the Levenshtein distance
def levenshteinDistance(A, B):
    N, M = len(A), len(B)
    # Create an array of size NxM
    dp = [[0 for i in range(M + 1)] for j in range(N + 1)]

    # Base Case: When N = 0
    for j in range(M + 1):
        dp[0][j] = j
    # Base Case: When M = 0
    for i in range(N + 1):
        dp[i][0] = i
    # Transitions
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j], # Insertion
                    dp[i][j-1], # Deletion
                    dp[i-1][j-1] # Replacement
                )

    return dp[N][M]

#creating a column for checking the similarity between the two locations and assigned default value as 0
df["is_similar"]=0

#Looping through all the rows to find the nearby locations and similar names 

for i in range(len(df)-1):
    dis=(great_circle(df.iloc[i, 3], df.iloc[i+1, 3]).miles)*1610  #for calculating the distances between two succesive locations
    lev_dis=levenshteinDistance(df.iloc[i, 3], df.iloc[i+1, 3])    #for findig the Levenshtein distance
    if dis<200 and lev_dis<5:  #Checking the similarity
        df.iloc[i,4]=1
        df.iloc[i+1,4]=1  #assigning the True values as 1
     

    
    
#dropping unnessary columns
df.drop("geo_points",axis=1,inplace=True)

#renaming the columns according to the requirement
df.rename(columns = {'latitude':'lat', 'longitude':'lon'}, inplace = True)

#generating final required csv file
df.to_csv("submission.csv",index=False)

