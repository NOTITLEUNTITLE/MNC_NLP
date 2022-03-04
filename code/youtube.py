#!/usr/bin/env python
# coding: utf-8

# In[11]:


# import os
# os.getcwd()


# In[ ]:


# from transformers import ElectraTokenizerFast, ElectraModel, TFElectraModel
# tokenizer_electra = ElectraTokenizerFast.from_pretrained("kykim/electra-kor-base")
# model_electra_pt = ElectraModel.from_pretrained("kykim/electra-kor-base")    # pytorch


# In[3]:



# !git clone https://github.com/kiyoungkim1/ReadyToUseAI

from ReadyToUseAI.src.nlp import make_sample_dataset, bert_sequence_classification
make_sample_dataset.nsmc(mode='test', text_only=False)  # mode: which datasets? 'train' or 'test'


# In[4]:


CLS = bert_sequence_classification.Classification(model_name='kykim/bert-kor-base', min_sentence_length=5, MAX_LEN=128, batch_size=32, use_bert_tokenizer=True)
CLS.dataset(data_path='./data.xlsx')
CLS.load_model(mode='train')
CLS.train(epochs=200, dataset_split=0.1)


# In[ ]:


import pandas as pd
test = pd.read_csv("/USER/3_WEEK/MNC_NLP/test/test.csv")
test_list = test["comment"].values.tolist()
type(test_list)
# test_list


# In[ ]:


# sentences = ['영화 재밌어요', '영화 재미없어요', '그냥 시간떼우기용', '완전 추천작']
sentences = test_list
saved_model_path='model/saved/3'

CLS = bert_sequence_classification.Classification(model_name='kykim/bert-kor-base', min_sentence_length=5, MAX_LEN=128, batch_size=64, use_bert_tokenizer=True)
CLS.load_model(mode='inference', saved_model_path=saved_model_path)
logit = CLS.inference(sentences=sentences)
print(logit)


# In[ ]:


from collections import Counter
# a = Counter(logit)    # model.csv   5epochs
# b = Counter(logit_1)  # model_1.csv 15epochs
c = Counter(logit)


# In[ ]:


# print(a)
# print(b)
print(c)


# In[40]:


submit = pd.read_csv("/USER/3_WEEK/MNC_NLP/test/sample_submission.csv")


# In[41]:


# 0 ['none' 'none']
# 1 ['none' 'hate']
# 2 ['others' 'none']
# 3 ['others' 'hate']
# 4 ['gender' 'none']
# 5 ['gender' 'hate']
for i in range(len(logit)):
    if logit[i] == 0:
        submit.iloc[i] = [i, 'none', 'none']
    elif logit[i] == 1:
        submit.iloc[i] = [i, 'none', 'hate']
    elif logit[i] == 2:
        submit.iloc[i] = [i, 'others', 'none']
    elif logit[i] == 3:
        submit.iloc[i] = [i, 'others', 'hate']
    elif logit[i] == 4:
        submit.iloc[i] = [i, 'gender', 'none']
    elif logit[i] == 5:
        submit.iloc[i] = [i, 'gender', 'hate']


# In[42]:


# submit


# In[43]:


submit.to_csv("/USER/3_WEEK/MNC_NLP/submit/model_2_200epochs.csv")


# In[ ]:




