# 工作流说明

本仓库当前有一个统一的 GitHub Actions 主工作流，外加两个手动备用工作流：

- `build-release.yml`
  负责 iOS `.tipa` 和 Android APK 的统一构建，顺序是 iOS -> Android -> 发布到同一个 Release。
- `build-tipa.yml`
  手动备用，只打 iOS `.tipa`。
- `build-apk.yml`
  手动备用，只打 Android APK。

## 触发方式

- 主工作流和两个备用工作流都支持手动 `workflow_dispatch`。
- `build-release.yml` 会在 `main` 分支推送时触发，只要本次提交涉及 `index.html`、`data/`、`games/`、`styles/`。
- `build-tipa.yml` 和 `build-apk.yml` 现在只作为手动备用，不会在推送时自动触发。

## 发布结果

- iOS 产物会发布为 `MyGames.tipa`。
- Android 产物会发布为 `MyGames-android-debug.apk`。

## 注意

- 现在已经合并成一个主 workflow，推送后会按顺序构建两端并统一发布。
