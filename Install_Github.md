

### Github



![image-20220830235747669](https://github.com/RyoIto-jp/CompanyDataOrganization/blob/masterInstall_Github.assets\image-20220830235747669.png)



Download and Run

**[64-bit Git for Windows Setup](https://github.com/git-for-windows/git/releases/download/v2.37.2.windows.2/Git-2.37.2.2-64-bit.exe).**

![image-20220830235833379](Install_Github.assets\image-20220830235833379.png)



![image-20220831000138076](Install_Github.assets\image-20220831000138076.png)



![image-20220831000205401](Install_Github.assets\image-20220831000205401.png)



![image-20220831000219813](Install_Github.assets\image-20220831000219813.png)



![image-20220831000237648](Install_Github.assets\image-20220831000237648.png)



![image-20220831000252139](Install_Github.assets\image-20220831000252139.png)



![image-20220831000259890](Install_Github.assets\image-20220831000259890.png)



![image-20220831000315177](Install_Github.assets\image-20220831000315177.png)



![image-20220831000324967](Install_Github.assets\image-20220831000324967.png)



![image-20220831000331796](Install_Github.assets\image-20220831000331796.png)



![image-20220831000341973](Install_Github.assets\image-20220831000341973.png)



![image-20220831000347159](Install_Github.assets\image-20220831000347159.png)



![image-20220831000359282](Install_Github.assets\image-20220831000359282.png)





## VSCODE

![image-20220831000516575](Install_Github.assets\image-20220831000516575.png)

![image-20220831000525922](Install_Github.assets\image-20220831000525922.png)

![image-20220831000551641](Install_Github.assets\image-20220831000551641.png)

![image-20220831000607503](Install_Github.assets\image-20220831000607503.png)

![image-20220831000619381](Install_Github.assets\image-20220831000619381.png)





### Github

```bash
git init

git remote add origin <https://github.com/RyoIto-jp/CompanyDataOrganization.git>

git add .gitignore

git commit -m "first commit"

git branch -M main

git push -u origin master

# -- ファイルサイズ100MBオーバーエラーの時
#ファイル全体キャッシュ削除
git rm -r --cached .

# 直前に戻る
git reset --hard HEAD

# 戻る場所を指定
git log

git reset --soft f85f72e3b0fde923ace815e253f2268a20d5649a
```

以下をインストールでいろいろ管理楽に。100MBオーバーの件はこれで解決。

GitLens — Git supercharged



### 参考

https://qiita.com/shungo_m/items/b73ff5b1ec6d69bb5c50

