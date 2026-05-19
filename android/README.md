# Android 接入说明

这是 `myGames` 的 Android 壳层工程，作用是把仓库根目录中的静态小游戏内容打包成 APK。

## 结构

- `android/app/src/main/java/com/zim/mygames/MainActivity.kt`
  WebView 入口，负责加载本地首页和处理返回键、外链。
- `android/app/build.gradle`
  构建时自动把仓库根目录的 `index.html`、`data/`、`games/`、`styles/` 同步到 APK 资源里。
- `android/Scripts/build-apk.bat`
  Windows 本机一键打包入口。

## 推荐方式：GitHub 自动打包

适合不想配置本机 Android 环境的情况。

1. 把代码推送到 GitHub。
2. 打开仓库的 `Actions`。
3. 选择 `Build MyGames iOS + Android`。
4. 点击 `Run workflow`。
5. 等待完成后，到 `Releases` 下载同一个版本里的 `.tipa` 和 `.apk`。

这个 APK 是 debug 包，已经自动签名，适合直接安装测试和小范围分发。

## 本机方式：一键脚本

如果本机已经补齐 Android 构建环境，可以双击：

```bat
android\Scripts\build-apk.bat
```

成功后产物在：

```text
dist\MyGames-android-debug.apk
```

如果提示找不到 Gradle，优先使用 GitHub Actions 云端打包。

## 本机环境要求

只安装 Android SDK 还不够，本机要能“一键打包”，至少需要下面这些：

- Android Studio Hedgehog 或更高版本，或单独可用的 Gradle 环境
- JDK 17
- Android SDK 34
- `platforms;android-34`
- `build-tools;34.0.0`
- 可用的 `gradle`，或者后续补上 `android/gradlew` 包装器

如果你不想自己配环境，直接用 GitHub Actions 更省事。

## 关于 HBuilderX

当前项目已经采用“静态内容 + 原生壳”的结构，HBuilderX 不是最合适的打包入口。
继续使用 Android WebView 壳层，能和现有 iOS `WKWebView` 壳层保持一致，维护成本更低。

## 说明

- iOS 和 Android 共用同一套内容目录。
- 后续新增游戏，只要继续放进根目录对应目录即可，两端都会一起打包。
- push 到 `main` 后，只要本次提交改了游戏内容目录，就会先构建 iOS，再构建 Android，最后统一发布到同一个 Release。
