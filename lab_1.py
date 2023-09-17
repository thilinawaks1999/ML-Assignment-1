# -*- coding: utf-8 -*-
"""Lab 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bweYzugUafrqQZChs1mlyV0Yu93p0BTN
"""

import pandas as pd

train_data = pd.read_csv('/content/drive/MyDrive/ML/train.csv')
valid_data = pd.read_csv('/content/drive/MyDrive/ML/valid.csv')

print(len(train_data))
print(len(valid_data))

train_data.head()

valid_data.head()

labels = ['label_1','label_2','label_3','label_4']
train_data['label_1'].value_counts()

train_data['label_2'].value_counts()

train_data['label_3'].value_counts()

train_data['label_4'].value_counts()

train_data.info()

train_data.describe()

from sklearn.preprocessing import RobustScaler

features = train_data.columns.values.tolist()[:-4]

scaler = RobustScaler()

X_train = {}
y_train = {}
X_valid = {}
y_valid = {}

for label in labels:

  if label == 'label_2':
    train_df = train_data[train_data['label_2'].notna()]
    valid_df = valid_data[valid_data['label_2'].notna()]
  else:
    train_df = train_data
    valid_df = valid_data

  X_train[label] = pd.DataFrame(scaler.fit_transform(train_df.drop(labels, axis=1)), columns = features)
  X_valid[label] = pd.DataFrame(scaler.transform(valid_df.drop(labels, axis=1)), columns = features)
  y_train[label] = train_df[label]
  y_valid[label] = valid_df[label]

y_train['label_3']
#change label number get values for 4 labels after here.

from sklearn import svm

clf = svm.SVC()
clf.fit(X_train['label_3'], y_train['label_3'])

from sklearn import metrics

pred_1 = clf.predict(X_valid['label_3'])

print(metrics.confusion_matrix(y_valid['label_3'], pred_1))
print(metrics.accuracy_score(y_valid['label_3'], pred_1))
print(metrics.precision_score(y_valid['label_3'], pred_1, average="weighted"))
print(metrics.recall_score(y_valid['label_3'], pred_1, average="weighted"))

from sklearn.feature_selection import SelectKBest, f_classif

selector_1 = SelectKBest(f_classif, k = 100)
X_1 = selector_1.fit_transform(X_train['label_3'], y_train['label_3'])

clf = svm.SVC()
clf.fit(X_1, y_train['label_3'])
pred_1 = clf.predict(selector_1.transform(X_valid['label_3']))

print(metrics.confusion_matrix(y_valid['label_3'], pred_1))
print(metrics.accuracy_score(y_valid['label_3'], pred_1))
print(metrics.precision_score(y_valid['label_3'], pred_1, average="weighted"))
print(metrics.recall_score(y_valid['label_3'], pred_1, average="weighted"))

from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel

lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X_train['label_3'], y_train['label_3'])
model = SelectFromModel(lsvc, prefit=True)
X_2 = model.transform(X_train['label_3'])

clf = svm.SVC()
clf.fit(X_2, y_train['label_3'])
pred_2 = clf.predict(model.transform(X_valid['label_3']))

print(metrics.confusion_matrix(y_valid['label_3'], pred_2))
print(metrics.accuracy_score(y_valid['label_3'], pred_2))
print(metrics.precision_score(y_valid['label_3'], pred_2, average="weighted"))
print(metrics.recall_score(y_valid['label_3'], pred_2, average="weighted"))

from sklearn.decomposition import PCA

pca = PCA(n_components=0.99,svd_solver='full')
pca.fit(X_train['label_3'])

X_t_trans = pd.DataFrame(pca.transform(X_train['label_3']))
X_v_trans = pd.DataFrame(pca.transform(X_valid['label_3']))

clf = svm.SVC()
clf.fit(X_t_trans, y_train['label_3'])

pred_3 = clf.predict(X_v_trans)

print(metrics.confusion_matrix(y_valid['label_3'], pred_3))
print(metrics.accuracy_score(y_valid['label_3'], pred_3))
print(metrics.precision_score(y_valid['label_3'], pred_3, average="weighted"))
print(metrics.recall_score(y_valid['label_3'], pred_3, average="weighted"))

print(X_1.shape, X_2.shape, X_t_trans.shape)

print(X_t_trans.shape[1])

test_data = pd.read_csv('/content/drive/MyDrive/ML/test.csv')

test_data

X_test = {}

test_df = test_data

for label in labels:
  X_test[label] = pd.DataFrame(scaler.fit_transform(test_df.drop(labels, axis=1)), columns = features)

from sklearn import svm

clf = svm.SVC()
clf.fit(X_train['label_3'], y_train['label_3'])

pred_1 = clf.predict(X_test['label_3'])

from sklearn.decomposition import PCA

pca = PCA(n_components=0.99,svd_solver='full')
pca.fit(X_train['label_3'])

X_t_trans = pd.DataFrame(pca.transform(X_train['label_3']))
X_v_trans = pd.DataFrame(pca.transform(X_test['label_3']))

clf = svm.SVC()
clf.fit(X_t_trans, y_train['label_3'])

pred_3 = clf.predict(X_v_trans)

df = pd.DataFrame({'Predicted labels before feature engineering':pred_1, 'Predicted labels after feature engineering':pred_3, 'No of new features':X_t_trans.shape[1]})

df

for i in range (X_t_trans.shape[1]):
  df['new_feature_'+str(i+1)] = X_t_trans[i]

df

df.to_csv('/content/drive/MyDrive/ML/label3.csv', index=False)

