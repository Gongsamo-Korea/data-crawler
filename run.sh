#!/bin/bash

# 메모장에서 읽기 
page_num_file="/home/ubuntu/gongsamo/crawler/page_number.txt"
PAGE_NUM=$(<"$page_num_file") 

# API endpoint URL
API_URL="http://127.0.0.1:5000/$PAGE_NUM"

# Make API request
RESPONSE=$(curl -s -X POST "$API_URL") 

# Print the API response
echo "API Response:"
echo "$RESPONSE" 

# 메모장에 페이지 넘버 수정
((PAGE_NUM++)) 
echo "$PAGE_NUM" > "$page_num_file" 
