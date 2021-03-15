import pandas as pd 
from collections import Counter

def clean_insults_data(csv_file):
    df = pd.read_csv(csv_file, index_col=0, parse_dates=['date'])
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    return df 

def clean_all_tweets_data(csv_file):
    df = pd.read_csv(csv_file, parse_dates=['date'])
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    return df

def get_mentions(x):
    return Counter(x['mentions'])

def filter_mentions(x):
    for k, v in x.items():
        if v > 1 and str(k)!='nan':
            return {k:v}
        
# topic analysis 

def get_ents(doc):
    doc_ents = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON' or ent.label_=='ORG':    
            ent_info = {'label':ent.label_, 'text':ent.text}
            doc_ents.append(ent_info)
    return doc_ents

def get_orgs_mentions(subset):
    pers = []
    orgs = []
    for s in subset['entities']:
        for ent in s:
            if ent['label'] == 'ORG':
                orgs.append(ent['text'].lower())
    return orgs

def count_org_mentions(org_ents):
    org_ent_dict = {}
    org_ent_dict['fake_news'] = sum('fake news' in s for s in org_ents)
    org_ent_dict['fake_news'] += sum('lamestream' in s for s in org_ents)
    org_ent_dict['fake_news'] += sum('fake' in s for s in org_ents)
    org_ent_dict['fake_news'] += sum('corrupt' in s for s in org_ents)
    org_ent_dict['border security'] = sum('border security' in s for s in org_ents)
    org_ent_dict['border security'] += sum('defense' in s for s in org_ents)
    org_ent_dict['impeachment'] = sum('impeachment' in s for s in org_ents)
    org_ent_dict['impeachment'] += sum('witch hunt' in s for s in org_ents)
    org_ent_dict['impeachment'] += sum('senate' in s for s in org_ents)
    org_ent_dict['nato'] = sum('nato' in s for s in org_ents)
    org_ent_dict['fbi'] = sum('fbi' in s for s in org_ents)
    org_ent_dict['trade'] = sum('eu' in s for s in org_ents)
    org_ent_dict['trade'] += sum('china' in s for s in org_ents)
    org_ent_dict['trade'] += sum('tariff' in s for s in org_ents)
    org_ent_dict['jobs'] = sum('jobs' in s for s in org_ents)
    return org_ent_dict

def get_pers_mentions(subset):
    pers = []
    orgs = []
    for s in subset['entities']:
        for ent in s:
            if ent['label'] == 'PERSON':
                pers.append(ent['text'].lower())
    return pers

def make_df(ym_org_ents):
    dfs = []
    for i in range(len(ym_org_ents)):
        topics_from_ents_df = pd.DataFrame.from_dict(ym_org_ents['topics'].iloc[i], orient='index').reset_index().rename(columns={'index':'topic', 0:'mentions'})
        date = pd.Series(ym_org_ents['year_month'].iloc[i])
        date.name = 'date'
        topics_per_ym = pd.concat([topics_from_ents_df,date], axis=1).fillna(method='ffill')
        dfs.append(topics_per_ym)
    topics = pd.concat(dfs)
    return topics