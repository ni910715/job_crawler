# 104人力銀行職缺爬蟲
## 流程
1. 透過selenium套件實現自動化爬蟲
2. 抓取職缺資訊
3. 使用pandas套件進行分析
4. 分析公司熱門需求技能
5. 將資料儲存至excel

## Pandas分析
- [x] 篩選學歷與經驗
- [ ] 統計各項技能佔比
- [ ] 職缺與地區關係
## 遇到問題
### 元素定位數量錯誤
```
list index out of range
```
---
經過仔細比對抓取到的元素數量與實際刊登的職缺數後，發現元素數量大於刊登數，導致錯誤。  
**解決方法：**  
原本使用`TAG_NAME`定位元素，後修改為較為精準的`CSS_SELECTOR`。  
```python
jobs = driver.find_elements(By.CSS_SELECTOR, "div#js-job-content article")
```
參考網址：https://jzchangmark.wordpress.com/2015/03/16/selenium-%E4%BD%BF%E7%94%A8-css-locator-%E5%AE%9A%E4%BD%8D%E5%85%83%E4%BB%B6/
### 技能欄位統計問題
#### 統計技能數量時出現數量錯誤
使用Pandas讀取CSV檔案時，資料將視為字串（包括列表），所以一開始將職缺所需技能儲存為列表型態會導致後續轉回列表時，出現多餘的引號和中括號。  
**解決方法：**  
將職缺所需的全部技能加入列表後，透過`,`連接，形成一個完整的字串。  
```python
skill_str = ', '.join(skill_list)
```
將原有的完整字串透過`,`分割後轉換回列表。  
```python
data['技能'] = data['技能'].str.split(', ') # 將原本以 , 分隔的技能字串轉換回list
```
透過`.apply()`的方式加入函式進行篩選。  
```python
condition2 = data['技能'].apply(lambda skills: input_skill in skills) # 將list的每一項確認是否包含指定技能
```
最後透過`.shape()`顯示數量。
```python
print(f'{input_skill}相關的職缺有{best_skill.shape[0]}個')
```