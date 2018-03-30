
# 对外提供的接口

> 整理时间 2018-03-30

抓取销售的房产
```html
GET /scrap/sell-room
```

更新租房信息
```html
GET /scrap/rent-room
 ```

## 1.获取房产信息


```html

/GET
/house/<int:page>
page 分页
```
## 2.获取用户头像

```html
/GET
/avatar/<imageid>

```

## 3.获取房产图片

```html
/GET
/image/<imageid>
```

## 4.查询销售房产

```html
GET /sell-search-house/<key_word>/<int:page>
```

## 5.销售房产各种排序

```html
GET /sell-cond-house/<orderby>/<int:page>
```