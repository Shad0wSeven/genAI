#!/usr/bin/env python3 
# format.py
import random

def formatData(specialRows):
    diseaseRow = {}
    for item in specialRows:
        z = item.get("DISEASE/TRAIT")
        if z in diseaseRow:
            diseaseRow[z] += item.get("PVALUE_MLOG")
        else:
            diseaseRow[z] = item.get("PVALUE_MLOG")
    x = len(specialRows) * ((len(specialRows) % 12) + 32)
    answerArr = []
    # print(diseaseRow)
    # for key in diseaseRow:
    #     if diseaseRow[key] > 500:
    #         answerArr.append(key)
    return [x, answerArr]
