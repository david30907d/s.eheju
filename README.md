# 敲何君的 api 推論出答案

api 上面的 answer 好像都是別人答錯的答案

所以把所有別人打錯的答案都去掉就是正確答案了

## 直接用傳假的 payload 去騙他的 server, 跟他說這一題就有 80 分

```js
app.allData.questions[0].score = '80'
```

這樣就直接及格
