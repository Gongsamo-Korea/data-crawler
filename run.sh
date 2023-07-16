#!/bin/bash

# 메모장에서 읽기 
page_num_file="/home/ubuntu/gongsamo/crawler/page_number.txt"
PAGE_NUM=$(<"$page_num_file") --> 메모장에서 추출한 page_number 값 (ex. 155)

# API endpoint URL
API_URL="http://127.0.0.1:5000/$PAGE_NUM"

# Make API request
RESPONSE=$(curl -s -X POST "$API_URL") --> API 호출

# Print the API response
echo "API Response:"
echo "$RESPONSE" --> API 호출 리턴 메시지

# 메모장에 페이지 넘버 수정
((PAGE_NUM++)) --> 다음 뉴스레터를 위해 page_number 값에 +1 
echo "$PAGE_NUM" > "$page_num_file" --> +1한 page_number 값을 메모장에 작성