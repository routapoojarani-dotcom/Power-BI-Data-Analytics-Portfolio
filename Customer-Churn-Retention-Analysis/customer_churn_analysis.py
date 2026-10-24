import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# CONFIGURATION
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('Blues_r')
os.makedirs('images', exist_ok=True)

COLORS = {
    'churn':    '#E63946',
    'retain':   '#2E86AB',
    'neutral':  '#457B9D',
    'accent':   '#F4A261',
    'light':    '#A8DADC',
}

# 1. LOAD DATA
df = pd.read_csv('data/synthetic_customer_churn_100k.csv')

# 2. DATA QUALITY REPORT
print('-' * 50)
print('DATA QUALITY REPORT')
print('-' * 50)
print(f'Records loaded      : {len(df):,}')
print(f'Columns             : {df.shape[1]}')
print(f'Duplicate rows      : {df.duplicated().sum()}')
print(f'Duplicate CustomerID: {df["CustomerID"].duplicated().sum()}')

print('\nMissing values:')
missing = df.isnull().sum()
if missing.sum() == 0:
    print('  None — dataset is complete')
else:
    for col, n in missing[missing > 0].items():
        print(f'  {col:<20} {n:>5} ({n/len(df):.1%})')

print('\nNegative TotalCharges:',
      (df['TotalCharges'] < 0).sum(), 'records')
print('Data types:')
print(df.dtypes.to_string())
print('-' * 50)

# 3. DATA CLEANING
df_clean = df.copy()

# Fix negative TotalCharges — set to absolute value
# (likely data entry sign error; small values, short-tenure customers)
neg_mask = df_clean['TotalCharges'] < 0
print(f'\nCleaning: {neg_mask.sum()} negative TotalCharges set to absolute value')
df_clean.loc[neg_mask, 'TotalCharges'] = df_clean.loc[neg_mask, 'TotalCharges'].abs()

# Standardise Contract values (already clean — confirm)
print('Contract values:', df_clean['Contract'].unique())

# Encode binary target
df_clean['Churn_Binary'] = (df_clean['Churn'] == 'Yes').astype(int)

# Encode Gender
df_clean['Gender_Enc'] = df_clean['Gender'].map({'Female': 0, 'Male': 1, 'Other': 2})

# Encode Contract
df_clean['Contract_Enc'] = df_clean['Contract'].map(
    {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
)

# 4. FEATURE ENGINEERING
# Tenure groups
df_clean['TenureGroup'] = pd.cut(
    df_clean['Tenure'],
    bins=[0, 12, 24, 48, 72],
    labels=['0-12 months', '13-24 months', '25-48 months', '49-72 months']
)

# Average monthly spend proxy (TotalCharges / Tenure)
df_clean['AvgMonthlySpend'] = (
    df_clean['TotalCharges'] / df_clean['Tenure']
).round(2)

# Customer risk score:
# High risk = month-to-month + tenure <= 12 + above-median monthly charges
median_charge = df_clean['MonthlyCharges'].median()
df_clean['HighRisk'] = (
    (df_clean['Contract'] == 'Month-to-month') &
    (df_clean['Tenure'] <= 12) &
    (df_clean['MonthlyCharges'] > median_charge)
).astype(int)

# Age group
df_clean['AgeGroup'] = pd.cut(
    df_clean['Age'],
    bins=[17, 30, 45, 60, 80],
    labels=['18-30', '31-45', '46-60', '61-80']
)

print('\nFeature engineering complete:')
print(f'  TenureGroup distribution:\n{df_clean["TenureGroup"].value_counts().sort_index()}')
print(f'\n  High-risk customers: {df_clean["HighRisk"].sum():,}')
hr_churn = df_clean[df_clean['HighRisk'] == 1]['Churn_Binary'].mean()
print(f'  Churn rate in high-risk segment: {hr_churn:.1%}')

# 5. OUTLIER DETECTION
print('\n' + '-' * 50)
print('OUTLIER DETECTION (IQR METHOD)')
print('-' * 50)
for col in ['Age', 'Tenure', 'MonthlyCharges', 'TotalCharges']:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    n_out = ((df_clean[col] < Q1 - 1.5 * IQR) |
             (df_clean[col] > Q3 + 1.5 * IQR)).sum()
    print(f'  {col:<20} {n_out:>4} outliers | '
          f'Q1={Q1:.1f}  Q3={Q3:.1f}  IQR={IQR:.1f}')

# 6. STATISTICAL VALIDATION
print('\n' + '-' * 50)
print('CORRELATION WITH CHURN')
print('-' * 50)
corr_cols = ['Age', 'Tenure', 'MonthlyCharges', 'TotalCharges',
             'Contract_Enc', 'Churn_Binary']
corr = df_clean[corr_cols].corr()['Churn_Binary'].drop('Churn_Binary').sort_values()
for feat, val in corr.items():
    direction = '(negative — less churn)' if val < 0 else '(positive — more churn)'
    print(f'  {feat:<20} {val:>7.4f}  {direction}')

# 7. KEY METRICS
total_customers   = len(df_clean)
churned           = df_clean['Churn_Binary'].sum()
churn_rate        = churned / total_customers
retained          = total_customers - churned
total_revenue     = df_clean['TotalCharges'].sum()
churned_revenue   = df_clean[df_clean['Churn_Binary'] == 1]['TotalCharges'].sum()
monthly_at_risk   = df_clean[df_clean['Churn_Binary'] == 1]['MonthlyCharges'].sum()

print('\n' + '-' * 50)
print('KEY BUSINESS METRICS')
print('-' * 50)
print(f'Total customers       : {total_customers:,}')
print(f'Churned               : {churned:,}  ({churn_rate:.1%})')
print(f'Retained              : {retained:,}')
print(f'Total revenue         : ${total_revenue:,.0f}')
print(f'Revenue from churned  : ${churned_revenue:,.0f}  ({churned_revenue/total_revenue:.1%})')
print(f'Monthly revenue at risk: ${monthly_at_risk:,.0f}')
print('-' * 50)

# 8. EDA COMPUTATIONS
# Churn by contract
contract_churn = (
    df_clean.groupby('Contract')
    .agg(total=('CustomerID', 'count'), churned=('Churn_Binary', 'sum'))
    .assign(churn_rate=lambda x: x['churned'] / x['total'] * 100)
    .sort_values('churn_rate', ascending=False)
)

# Churn by tenure group
tenure_churn = (
    df_clean.groupby('TenureGroup', observed=True)
    .agg(total=('CustomerID', 'count'), churned=('Churn_Binary', 'sum'))
    .assign(churn_rate=lambda x: x['churned'] / x['total'] * 100)
)

# Churn by payment method
payment_churn = (
    df_clean.groupby('PaymentMethod')
    .agg(total=('CustomerID', 'count'), churned=('Churn_Binary', 'sum'))
    .assign(churn_rate=lambda x: x['churned'] / x['total'] * 100)
    .sort_values('churn_rate', ascending=False)
)

print('\nChurn by contract:')
print(contract_churn.round(2))
print('\nChurn by tenure group:')
print(tenure_churn.round(2))
print('\nChurn by payment method:')
print(payment_churn.round(2))

# 9. VISUALISATIONS
def save(name):
    plt.savefig(f'images/{name}', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: images/{name}')

# Churn distribution 
fig, ax = plt.subplots(figsize=(7, 5))
labels = ['Retained\n66,856', 'Churned\n33,144']
sizes  = [66856, 33144]
colors = [COLORS['retain'], COLORS['churn']]
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 12}
)
for at in autotexts:
    at.set_fontweight('bold')
    at.set_fontsize(13)
ax.set_title('Customer Churn Distribution', fontsize=14, fontweight='bold', pad=20)
save('01_churn_distribution.png')

# Churn rate by contract 
fig, ax = plt.subplots(figsize=(8, 5))
contracts = contract_churn.index.tolist()
rates     = contract_churn['churn_rate'].values
bar_colors = [COLORS['churn'] if r > 30 else COLORS['retain'] for r in rates]
bars = ax.bar(contracts, rates, color=bar_colors, edgecolor='white', linewidth=0.8)
for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Churn Rate by Contract Type', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Contract Type', fontsize=12)
ax.set_ylabel('Churn Rate (%)', fontsize=12)
ax.set_ylim(0, 58)
ax.axhline(y=33.1, color='gray', linestyle='--', linewidth=1, alpha=0.7,
           label=f'Overall rate: 33.1%')
ax.legend(fontsize=10)
save('02_churn_by_contract.png')

# Churn rate by tenure group 
fig, ax = plt.subplots(figsize=(8, 5))
tg_labels = tenure_churn.index.tolist()
tg_rates  = tenure_churn['churn_rate'].values
bar_colors = [COLORS['churn'] if r > 40 else COLORS['neutral'] for r in tg_rates]
bars = ax.bar(tg_labels, tg_rates, color=bar_colors, edgecolor='white', linewidth=0.8)
for bar, rate in zip(bars, tg_rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Churn Rate by Tenure Group', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Customer Tenure', fontsize=12)
ax.set_ylabel('Churn Rate (%)', fontsize=12)
ax.set_ylim(0, 76)
ax.axhline(y=33.1, color='gray', linestyle='--', linewidth=1, alpha=0.7,
           label='Overall rate: 33.1%')
ax.legend(fontsize=10)
save('03_churn_by_tenure.png')

# Monthly charges distribution by churn 
fig, ax = plt.subplots(figsize=(9, 5))
churned_mc  = df_clean[df_clean['Churn_Binary'] == 1]['MonthlyCharges']
retained_mc = df_clean[df_clean['Churn_Binary'] == 0]['MonthlyCharges']
ax.hist(retained_mc, bins=40, alpha=0.6, color=COLORS['retain'],
        label=f'Retained (avg ${retained_mc.mean():.0f})', density=True)
ax.hist(churned_mc, bins=40, alpha=0.6, color=COLORS['churn'],
        label=f'Churned (avg ${churned_mc.mean():.0f})', density=True)
ax.axvline(retained_mc.mean(), color=COLORS['retain'], linestyle='--', linewidth=1.5)
ax.axvline(churned_mc.mean(), color=COLORS['churn'], linestyle='--', linewidth=1.5)
ax.set_title('Monthly Charges Distribution — Churned vs Retained',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Monthly Charges ($)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(fontsize=11)
save('04_monthly_charges_distribution.png')

# Churn rate by payment method 
fig, ax = plt.subplots(figsize=(9, 5))
pm_labels = payment_churn.index.tolist()
pm_rates  = payment_churn['churn_rate'].values
bars = ax.barh(pm_labels, pm_rates, color=COLORS['neutral'],
               edgecolor='white', linewidth=0.8)
for bar, rate in zip(bars, pm_rates):
    ax.text(rate + 0.2, bar.get_y() + bar.get_height() / 2,
            f'{rate:.1f}%', va='center', fontweight='bold', fontsize=11)
ax.set_title('Churn Rate by Payment Method', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Churn Rate (%)', fontsize=12)
ax.set_xlim(0, 40)
ax.axvline(x=33.1, color='gray', linestyle='--', linewidth=1, alpha=0.7)
save('05_churn_by_payment.png')

# Correlation heatmap 
fig, ax = plt.subplots(figsize=(8, 6))
corr_matrix = df_clean[['Age', 'Tenure', 'MonthlyCharges',
                          'TotalCharges', 'Contract_Enc',
                          'Churn_Binary']].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, ax=ax,
            linewidths=0.5, cbar_kws={'shrink': 0.8})
ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold', pad=15)
plt.xticks(rotation=30, ha='right')
save('06_correlation_heatmap.png')

# Revenue impact 
fig, ax = plt.subplots(figsize=(7, 5))
rev_labels = ['Retained\nCustomers', 'Churned\nCustomers']
rev_values = [total_revenue - churned_revenue, churned_revenue]
rev_colors = [COLORS['retain'], COLORS['churn']]
bars = ax.bar(rev_labels, rev_values, color=rev_colors,
              edgecolor='white', linewidth=0.8, width=0.5)
for bar, val in zip(bars, rev_values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1_000_000,
            f'${val/1e6:.1f}M', ha='center', va='bottom',
            fontweight='bold', fontsize=13)
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x/1e6:.0f}M'))
ax.set_title('Total Revenue by Churn Status', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Total Revenue (USD)', fontsize=12)
ax.set_ylim(0, max(rev_values) * 1.2)
save('07_revenue_impact.png')

# EXPORT CLEAN DATASET
os.makedirs('data', exist_ok=True)
df_clean.to_csv('data/cleaned_churn_data.csv', index=False)