import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import click as ck
import numpy as np
import pandas as pd
import logging
import math
import os
from collections import deque
import pickle as pkl
import torch
import torch.nn as nn
import torch.nn.functional as F

from sklearn.manifold import TSNE
from sklearn.metrics import roc_curve, auc, matthews_corrcoef
import matplotlib.pyplot as plt
from scipy.stats import rankdata

logging.basicConfig(level=logging.INFO)
import operator
from collections import Counter

class ELModel(nn.Module):
    
    def __init__(self, nb_classes, nb_relations, embedding_size, batch_size, margin, reg_norm):
        super(ELModel, self).__init__()
        self.nb_classes = nb_classes
        self.nb_relations = nb_relations
        self.embedding_size = embedding_size
        self.batch_size = batch_size
        self.margin = margin
        self.reg_norm = reg_norm
        width = 3
        
        self.inf = 5.0 # For top radius
        self.cls_embeddings = nn.Embedding( nb_classes, embedding_size + 1)
        self.rel_embeddings = nn.Embedding( nb_relations, embedding_size + 1)

def load_eval_data(data_file):
    data = []
    rel = f'SubClassOf'
    with open(data_file, 'r') as f:
        for line in f:
            it = line.strip().split()
            id1 = it[0]
            id2 = it[1]
            data.append((id1, id2))
    return data

def evaluate_hits(data,cls_embeds_file, embedding_size, batch_size, margin, reg_norm):
    with open(cls_embeds_file, 'rb') as f:
        cls_df = pkl.load(f)
    nb_classes = len(cls_df['cls'])
    nb_relations = len(cls_df['rel'])
    model = ELModel(nb_classes, nb_relations, embedding_size, batch_size, margin, reg_norm).cuda()
    model.load_state_dict(cls_df['embeddings'])   
    model.eval()

    embeds_list = model.cls_embeddings(torch.tensor(list(range(nb_classes))).cuda())
#     print(list(range(nb_classes)))
#     embeds_list = cls_df['embeddings'].values

#     classes = {v: k for k, v in enumerate(cls_df['classes'])}
    classes = cls_df['classes']
    rel = model.rel_embeddings(torch.tensor(0).cuda()).detach().cpu().numpy()
    rel = rel[:-1]
    
    embeds_list = embeds_list.detach().cpu().numpy()

    size = len(embeds_list[0])
#     embeds = np.zeros((nb_classes, size), dtype=np.float32)
#     for i, emb in enumerate(embeds_list):
#         embeds[i, :] = emb
    embeds =  embeds_list   
    embeds = embeds[:, :-1]
#     print(classes)
    
    top1 = 0
    top10 = 0
    top100 = 0
    mean_rank = 0
    rank_vals =[]
    for test_pts in data:
        c = test_pts[0]
        d = test_pts[1]
        index_c = classes[c]
        index_d = classes[d]
        dist =  np.linalg.norm(embeds - embeds[index_d], axis=1) 
        dist_dict = {i: dist[i] for i in range(0, len(dist))} 
        s_dst = dict(sorted(dist_dict.items(), key=operator.itemgetter(1)))
        s_dst_keys = list(s_dst.keys())
        ranks_dict = { s_dst_keys[i]: i for i in range(0, len(s_dst_keys))}
        rank_c = ranks_dict[index_c]
        mean_rank += rank_c
        rank_vals.append(rank_c)
        if rank_c == 1:
            top1 += 1
        if rank_c <= 10:
            top10 += 1
        if rank_c <= 100:
            top100 += 1
    
    n = len(data)
    top1 /= n
    top10 /= n
    top100 /= n
    mean_rank /= n
    total_classes = len(embeds)
    return top1,top10,top100,mean_rank,rank_vals,total_classes  

def compute_rank_percentile(scores,x):
    scores.sort()
    per = np.percentile(scores,x)
    return per

import statistics
def compute_median_rank(rank_list):
    med = np.median(rank_list)
    return med    

def calculate_percentile_1000(scores):
    ranks_1000=[]
    for item in scores:
        if item < 1000:
            ranks_1000.append(item)
    n_1000 = len(ranks_1000)
    nt = len(scores)
    percentile = (n_1000/nt)*100
    return percentile

def compute_rank_roc(ranks, n):
    auc_lst = list(ranks.keys())
    auc_x = auc_lst[1:]
    auc_x.sort()
    auc_y = []
    tpr = 0
    sum_rank = sum(ranks.values())
    for x in auc_x:
        tpr += ranks[x]
        auc_y.append(tpr / sum_rank)
    auc_x.append(n)
    auc_y.append(1)
    auc = np.trapz(auc_y, auc_x)/n
    return auc

def out_results(rks_vals):
    med_rank = compute_median_rank(rks_vals)
    print("Median Rank:",med_rank)
    per_rank_90 = compute_rank_percentile(rks_vals,90)
    print("90th percentile rank:",per_rank_90)
    percentile_below1000 = calculate_percentile_1000(rks_vals)
    print("Percentile for below 1000:",percentile_below1000)
    print("% Cases with rank greater than 1000:",(100 - percentile_below1000))

def print_results(rks_vals,n):
    print("top1:",top1)
    print("top10:",top10)
    print("top100:",top100)
    print("Mean Rank:",mean_rank)
    rank_dicts = dict(Counter(rks_vals))
    print("AUC:",compute_rank_roc(rank_dicts,n))
    out_results(rks_vals) 


tag='OWL2EL_2'
AEL_dir = 'experiments/results/'
test_file = 'experiments/data/'+tag+'/test.txt'
test_data = load_eval_data(test_file)

margin = 0.1
embedding_size = 100
batch_size =  1000
reg_norm=1
learning_rate=3e-4
cls_embeds_file = 'OWL2EL_2.pkl'


print('start evaluation of OWL2EL_2........')
top1,top10,top100,mean_rank,rank_vals,n_cls = evaluate_hits(test_data,cls_embeds_file,embedding_size,batch_size,margin,reg_norm)


print("EmEL Results on test data")
print_results(rank_vals,n_cls)

tag='OWL2EL_3'
AEL_dir = 'experiments/results/'
test_file = 'experiments/data/'+tag+'/test.txt'
test_data = load_eval_data(test_file)

margin = 0
embedding_size = 200
batch_size =  1000
reg_norm=1
learning_rate=3e-4
cls_embeds_file = 'OWL2EL_3.pkl'


print('start evaluation of OWL2EL_3........')
top1,top10,top100,mean_rank,rank_vals,n_cls = evaluate_hits(test_data,cls_embeds_file,embedding_size,batch_size,margin,reg_norm)


print("EmEL Results on test data")
print_results(rank_vals,n_cls)


tag='OWL2EL_4'
AEL_dir = 'experiments/results/'
test_file = 'experiments/data/'+tag+'/test.txt'
test_data = load_eval_data(test_file)

margin = 0.1
embedding_size = 100
batch_size =  1000
reg_norm=1
learning_rate=3e-4
cls_embeds_file = 'OWL2EL_4.pkl'


print('start evaluation of OWL2EL_4........')
top1,top10,top100,mean_rank,rank_vals,n_cls = evaluate_hits(test_data,cls_embeds_file,embedding_size,batch_size,margin,reg_norm)


print("EmEL Results on test data")
print_results(rank_vals,n_cls)


tag='OWL2EL_5'
AEL_dir = 'experiments/results/'
test_file = 'experiments/data/'+tag+'/test.txt'
test_data = load_eval_data(test_file)

margin = -0.1
embedding_size = 100
batch_size =  1000
reg_norm=1
learning_rate=3e-4
cls_embeds_file = 'OWL2EL_5.pkl'


print('start evaluation of OWL2EL_5........')
top1,top10,top100,mean_rank,rank_vals,n_cls = evaluate_hits(test_data,cls_embeds_file,embedding_size,batch_size,margin,reg_norm)


print("EmEL Results on test data")
print_results(rank_vals,n_cls)


