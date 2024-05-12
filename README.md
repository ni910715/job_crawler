# 104人力銀行職缺爬蟲
## 流程
1. 透過selenium套件實現自動化爬蟲
2. 抓取職缺資訊
3. 使用pandas套件進行分析
4. 分析公司熱門需求技能
5. 將資料儲存至excel

## 遇到問題
```
list index out of range
```
經過仔細比對抓取到的元素數量與實際刊登的職缺數後，發現元素數量大於刊登數，導致錯誤。  
**解決方法：**  
原本使用`TAG_NAME`定位元素，後修改為較為精準的`CSS_SELECTOR`。  
```python
jobs = driver.find_elements(By.CSS_SELECTOR, "div#js-job-content article")
```