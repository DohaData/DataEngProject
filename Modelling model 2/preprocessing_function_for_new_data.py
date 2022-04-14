import numpy as np

def process_df(original_df):
    df = original_df.copy()
    df['delay_signup_purchase'] = (df['signup_time'] - df['purchase_time']).dt.seconds
    for cat_col in ['device_id','source','browser','sex']:
        cat_mapper = dict(zip(df[cat_col].unique(), range(1, len(df[cat_col].unique())+1)))
        df[cat_col] = df[cat_col].replace(cat_mapper)
    for col_prefix in ['signup', 'purchase']:
        df[f'{col_prefix}_year'] = df[f'{col_prefix}_time'].dt.year
        df[f'{col_prefix}_month'] = df[f'{col_prefix}_time'].dt.month
        df[f'cos_{col_prefix}_month'] = np.cos(2.*np.pi*df[f'{col_prefix}_month']/12.)
        df[f'sin_{col_prefix}_month'] = np.sin(2.*np.pi*df[f'{col_prefix}_month']/12.)
        df[f'{col_prefix}_hour'] = df[f'{col_prefix}_time'].dt.hour
        df[f'cos_{col_prefix}_hour'] = np.cos(2.*np.pi*df[f'{col_prefix}_hour']/24.)
        df[f'sin_{col_prefix}_hour'] = np.sin(2.*np.pi*df[f'{col_prefix}_hour']/24.)
        df[f'{col_prefix}_minute'] = df[f'{col_prefix}_time'].dt.minute
        df[f'cos_{col_prefix}_minute'] = np.cos(2.*np.pi*df[f'{col_prefix}_minute']/60.)
        df[f'sin_{col_prefix}_minute'] = np.sin(2.*np.pi*df[f'{col_prefix}_minute']/60.)
        df[f'{col_prefix}_weekDay'] = df[f'{col_prefix}_time'].dt.dayofweek
        df[f'cos_{col_prefix}_weekDay'] = np.cos(2.*np.pi*df[f'{col_prefix}_weekDay']/7.)
        df[f'sin_{col_prefix}_weekDay'] = np.sin(2.*np.pi*df[f'{col_prefix}_weekDay']/7.)
        df = df.drop(columns=[f'{col_prefix}_time'])
    return df