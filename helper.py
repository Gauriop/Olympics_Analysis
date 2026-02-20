import numpy as np

def fetch_medal_tally(df,year,country):
  medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  flag=0
  if year == 'Overall'and country=='Overall':
    temp_df=medal_df
  if year=='Overall'and country!='Overall':
    flag=1
    temp_df=medal_df[medal_df['region']==country]
  if year!='Overall'and country=='Overall':
    temp_df=medal_df[medal_df['Year']==int(year)]
  if year!='Overall'and country!='Overall':
    temp_df = medal_df[
    (medal_df['Year'] == int(year)) &
    (medal_df['region'] == country)
]

  if flag==1:
    x=temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values('Year', ascending=True).reset_index()
  else:
      x=temp_df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
  x['total']=x['Gold']+x['Silver']+x['Bronze']

  return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    #to cast an object (like a DataFrame, Series, or array) to a specified data type.
    medal_tally['Gold']=medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['total'] = medal_tally['total'].astype(int)

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    return nations_over_time

def events_over_timed(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
    events_over_time.rename(columns={'Year': 'Year', 'count': 'Event'}, inplace=True)
    return events_over_time

def athelete_over_timed(df):
    athlete_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year')
    return athlete_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']   # Fix column names properly

    x = x.head(15)

    # Merge to get Sport and region
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left') \
         .drop_duplicates('Name')

    return x
def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                            inplace=True)
    new_df = temp_df[temp_df['region'] ==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_country_wise(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['region'] == sport]

    # Count medals per athlete
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']   # Fix column names properly

    x = x.head(15)

    # Merge to get Sport and region
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left') \
         .drop_duplicates('Name')

    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
