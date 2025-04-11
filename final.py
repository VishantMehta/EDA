import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#reading dataset
df = pd.read_csv("python datasetca.csv")
print(df)

#Exploring the dataset
print("Shape of dataset:", df.shape)
missing = df.isnull().sum()
print("Missing values in each column:\n", missing)
print("Info:\n",df.info())
print("Description:\n",df.describe())


#-----Cleaning the dataset------------------------------------------------------------------------------------

#filling missing values in 'Gender' column with 'N/A'
print("number of missing values in the 'Gender':", df['Gender'].isnull().sum())
df['Gender'] = df['Gender'].fillna('N/A')
print("Gender Gaps After:", df['Gender'].isnull().sum())

#Age:replacing missing values with 0 and ensuring the column is numeric
print("number of missing values in 'Age':", df['Age'].isnull().sum())  
df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(0)
print("Age Gaps After:", df['Age'].isnull().sum())  

#assigning 'N/A' to missing category
print("number of missing values in 'Category':", df['Category'].isnull().sum())  
df['Category'] = df['Category'].fillna('N/A')
print("Category Gaps After:", df['Category'].isnull().sum())  

#handling missing candidate names
print("number of missing values in the 'Candidate Name':", df['Candidate Name'].isnull().sum())  
df['Candidate Name'] = df['Candidate Name'].fillna('Unknown')
print("Candidate Name Gaps After:", df['Candidate Name'].isnull().sum())  

#Party Name: 'Unknown' for missing values
print("number of missing values in the 'Party Name':", df['Party Name'].isnull().sum())  
df['Party Name'] = df['Party Name'].fillna('Unknown')
print("Party Name Gaps After:", df['Party Name'].isnull().sum())

#Dropping NOTA (not a real contender)
print("Rows Before:", len(df))  
df = df[df['Candidate Name'] != 'NOTA'] 
print("Rows After Dropping NOTA:", len(df)) 


#Making columns numeric, 0 for blanks
numeric_cols = ['Total Votes Polled In The Constituency', 'Valid Votes', 
                'Votes Secured - General', 'Votes Secured - Postal', 
                'Votes Secured - Total', 'Total Electors']  
for col in numeric_cols:
    print("Before -", col, "Gaps:", df[col].isnull().sum())  
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) 
    print("After -", col, "Gaps:", df[col].isnull().sum())  

#recheck after cleaning
print("Final Size:", df.shape)  
print("Any Gaps Left?:\n", df.isnull().sum())  
print("Final Types:\n", df.dtypes)  

#---------------------OBJ 1:-------------------------------------------------------------------------------------------------------
#Objective 1: Analyze the Demographic Composition of Candidates
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1']
title_color = '#2C3E50' 

#1.1 Visualize the distribution of candidates by gender using a bar chart
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Gender', hue='Gender', palette=colors[:3], edgecolor='black', linewidth=1, legend=False)
plt.title('1.1 Gender Split of Candidates', fontsize=14, color=title_color)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Candidate Count', fontsize=12)
plt.show()

#1.2  Ages(Histogram with a Curve)
plt.figure(figsize=(10, 5))
sns.histplot(data=df[df['Age'] > 0], x='Age', bins=20, kde=True, color=colors[1], edgecolor='black', linewidth=1)
plt.title('1.2 Age Range of Candidates', fontsize=14, color=title_color)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Candidate Count', fontsize=12)
plt.show()

#1.3 Proportional breakdown of candidates by social category using a pie chart
plt.figure(figsize=(8, 8))
category_counts = df['Category'].value_counts()
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', colors=colors)
plt.title('1.3 Social Category Breakdown', fontsize=14, color=title_color)
plt.show()



#---------------------OBJ 2:-------------------------------------------------------------------------------------------------------

#Objective 2: Evaluate Party Performance Across Constituencies
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1', 
          '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71']  
title_color = '#2C3E50'

#2.1 Candidates Spread Out Per Party (Box Chart)
plt.figure(figsize=(12, 6))
candidates_per_constituency = df.groupby(['Party Name', 'PC Name']).size().reset_index(name='Candidate Count')
top_10_parties = df['Party Name'].value_counts().head(10).index  
df_top_10 = candidates_per_constituency[candidates_per_constituency['Party Name'].isin(top_10_parties)]
sns.boxplot(data=df_top_10, x='Party Name', y='Candidate Count', hue='Party Name', palette=colors[:10], legend=False)
plt.title('2.1 Candidate Spread by Top 10 Parties', fontsize=14, color=title_color)
plt.xlabel('Party Name', fontsize=12)
plt.ylabel('Candidates per Constituency', fontsize=12)
plt.xticks(rotation=45) 
plt.show()

#2.2 vote share percentages of the top 10 parties(horizontal bar chart)
party_votes = df.groupby('Party Name')['Votes Secured - Total'].sum().sort_values(ascending=False).head(10)
vote_share = (party_votes / df['Votes Secured - Total'].sum()) * 100  
plt.figure(figsize=(12, 6))
sns.barplot(x=vote_share.values, y=vote_share.index, hue=vote_share.index, palette=colors[:10], edgecolor='black', linewidth=1, legend=False)
plt.title('2.2 Top 10 Parties by Vote Share (%)', fontsize=14, color=title_color)
plt.xlabel('Vote Share (%)', fontsize=12)
plt.ylabel('Party Name', fontsize=12)
plt.show()

#Summary for Objective 2
top_10_parties_candidates = df['Party Name'].value_counts().head(10)
print("Top 10 Parties by Candidate Count:\n", top_10_parties_candidates)
print("\nTop 10 Parties by Vote Share (%):\n", vote_share)
print("\nHow Candidates Spread Out (Top 10):\n", df_top_10.groupby('Party Name')['Candidate Count'].describe())

#---------------------OBJ 3:-------------------------------------------------------------------------------------------------------

#Objective 3: Examine the Influence of Social Categories on Voting Outcomes
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1', 
          '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71']
title_color = '#2C3E50'

#3.1 Vote Share by Category (Bar Chart)
plt.figure(figsize=(10, 6))
category_votes = df.groupby('Category')['Votes Secured - Total'].sum()
vote_share_by_category = (category_votes / df['Votes Secured - Total'].sum()) * 100
sns.barplot(x=vote_share_by_category.index, y=vote_share_by_category.values, hue=vote_share_by_category.index, palette=colors[:len(category_votes)], edgecolor='black', linewidth=1, legend=False)
plt.title('3.1 Vote Share by Category (%)', fontsize=14, color=title_color)
plt.xlabel('Social Category', fontsize=12)
plt.ylabel('Vote Share (%)', fontsize=12)
plt.show()

#3.2 Vote Spread by Category (Box Chart)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Category', y='Votes Secured - Total', hue='Category', palette=colors[:len(category_votes)], legend=False)
plt.title('3.2 Vote Spread by Category', fontsize=14, color=title_color)
plt.xlabel('Social Category', fontsize=12)
plt.ylabel('Votes Secured', fontsize=12)
plt.show()

#numerical summary for Objective 3 
print("Vote Share by Category (%):\n", vote_share_by_category)
print("Average Votes by Category:\n", df.groupby('Category')['Votes Secured - Total'].mean())

#---------------------OBJ 4:-------------------------------------------------------------------------------------------------------
#Objective 4:Voter Turnout Variations by State

colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1', 
          '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71']
title_color = '#2C3E50'
# Turnout percentage
df['Voter Turnout (%)'] = (df['Total Votes Polled In The Constituency'] / df['Total Electors']) * 100
# Splitting out states from constituency names
df['State'] = df['PC Name'].str.split(' - ').str[0].str.strip()
# average voter turnout for top 10 states (Bar Chart)
plt.figure(figsize=(12, 6))
state_turnout = df.groupby('State')['Voter Turnout (%)'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=state_turnout.index, y=state_turnout.values, hue=state_turnout.index, palette=colors[:10], edgecolor='black', linewidth=1, legend=False)
plt.title('4.1 Top 10 States by Average Turnout (%)', fontsize=14, color=title_color)
plt.xlabel('State', fontsize=12)
plt.ylabel('Average Turnout (%)', fontsize=12)
plt.xticks(rotation=45)
plt.show()

#Numerical summary for Objective 4 
print("Average Turnout by State (Top 10):\n", state_turnout)

#---------------------OBJ 5:-------------------------------------------------------------------------------------------------------

#Objective 5: Impact of Postal Votes on Candidate Performance
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1', 
          '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71']
title_color = '#2C3E50'
#5.1 Compare general, postal, and total votes for the top 10 candidates(Line Chart)
plt.figure(figsize=(12, 6))
top_10_candidates = df.nlargest(10, 'Votes Secured - Total')
x = range(len(top_10_candidates))
plt.plot(x, top_10_candidates['Votes Secured - General'], label='General Votes', color=colors[0], marker='o', linewidth=2)
plt.plot(x, top_10_candidates['Votes Secured - Postal'], label='Postal Votes', color=colors[1], marker='s', linewidth=2)
plt.plot(x, top_10_candidates['Votes Secured - Total'], label='Total Votes', color=colors[2], marker='^', linewidth=2)
plt.title('5.1 Votes Breakdown for Top 10 Candidates', fontsize=14, color=title_color)
plt.xlabel('Candidate Index', fontsize=12)
plt.ylabel('Vote Count', fontsize=12)
plt.xticks(x, top_10_candidates['Candidate Name'], rotation=45)
plt.legend(title='Vote Type')
plt.show()

#5.2 General vs Postal Votes(Scatter Chart)
plt.figure(figsize=(10, 6))
plt.scatter(df['Votes Secured - General'], df['Votes Secured - Postal'], 
            s=df['Votes Secured - Total'] / 1000, color=colors[3], alpha=0.6, edgecolor='black', linewidth=0.5)
plt.title('5.2 General vs. Postal Votes (Size = Total)', fontsize=14, color=title_color)
plt.xlabel('General Votes', fontsize=12)
plt.ylabel('Postal Votes', fontsize=12)
plt.xscale('log')
plt.yscale('log')
plt.show()

#numerical summary for Objective 5 
print("Average Votes by Type:\n", df[['Votes Secured - General', 'Votes Secured - Postal', 'Votes Secured - Total']].mean())
print("\nHow Votes Relate:\n", df[['Votes Secured - General', 'Votes Secured - Postal', 'Votes Secured - Total']].corr())
print("\nTop 10 Candidates by Votes:\n", top_10_candidates[['Candidate Name', 'PC Name', 'Votes Secured - General', 'Votes Secured - Postal', 'Votes Secured - Total']])


#---------------------OBJ 6:-------------------------------------------------------------------------------------------------------

#Objective 6: Correlations Between Electors and Vote Metrics
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1', 
          '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71']
title_color = '#2C3E50'

#Select relevant columns
metrics = ['Total Electors', 'Total Votes Polled In The Constituency', 'Valid Votes']
df_metrics = df[metrics]

#6.1 correlation between electors, votes polled, and valid votes(Heatmap)
plt.figure(figsize=(8, 6))
corr_matrix = df_metrics.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('6.1 How Electors, Votes Polled, and Valid Votes Connect', fontsize=14, color=title_color)
plt.show()

#6.2 pairwise relationships among electors, votes polled, and valid votes(pairwise plot)
pair_plot = sns.pairplot(df_metrics)
pair_plot.fig.suptitle('6.2 Pairing Up Electors, Votes Polled, and Valid Votes', fontsize=14, color=title_color, y=1.02)
plt.show()

# Numerical summary for Objective 6 
print("Correlation Breakdown:\n", corr_matrix)
print("\nBasic Stats:\n", df_metrics.describe())

#---------------------OBJ 7:-------------------------------------------------------------------------------------------------------

#Objective 7: Analyze the Prevalence and Distribution of NOTA Votes

#Loading my original data
df_original = pd.read_csv('python datasetca.csv')
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F9A825', '#45B7D1', 
          '#D4A5A5', '#9B59B6', '#3498DB', '#E67E22', '#2ECC71']
title_color = '#2C3E50'

# Pulling states
df_original['State'] = df_original['PC Name'].str.split(' - ').str[0].str.strip()
nota_df = df_original[df_original['Candidate Name'] == 'NOTA'].copy()
# Numeric consistency
nota_df.loc[:, 'Votes Secured - Total'] = pd.to_numeric(nota_df['Votes Secured - Total'], errors='coerce').fillna(0)
# Group by state and get top 10 based on NOTA votes
nota_by_state = nota_df.groupby('State')['Votes Secured - Total'].sum().sort_values(ascending=False).head(10)

# 7.1 Visualize the total NOTA votes for the top 10 states (Bar Chart)
plt.figure(figsize=(12, 6))
sns.barplot(x=nota_by_state.index, 
            y=nota_by_state.values, 
            hue=nota_by_state.index, 
            palette=colors[:10], 
            edgecolor='black', 
            linewidth=1, 
            legend=False)

plt.title('7.1 Top 10 States for NOTA Votes', fontsize=14, color=title_color)
plt.xlabel('State', fontsize=12)
plt.ylabel('Total NOTA Votes', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# 7.2 Proportional distribution of NOTA votes among the top 10 states (Pie Chart)
plt.figure(figsize=(8, 8))
nota_share = (nota_by_state / nota_by_state.sum()) * 100
plt.pie(nota_share, labels=nota_share.index, autopct='%1.1f%%', colors=colors[:10])
plt.title('7.2 NOTA Share in Top 10 States', fontsize=14, color=title_color)
plt.show()