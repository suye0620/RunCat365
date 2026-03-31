# 番茄工作模式功能实现计划

## 功能概述

* **Normal模式**：现有功能，保持不变

* **Work模式**（新增）：番茄钟工作模式，根据工作/休息状态自动切换runner

  * 工作阶段：显示"工作"类型runner，倒计时30分钟

  * 休息阶段：显示"休息"类型runner，等待用户开始新的番茄钟

## 数据结构设计

### 1. 新增配置文件 `work_mode_config.json`

存储位置：项目根目录（与 `settings.json` 同级）

JSON结构设计：

```json
{
  "current_mode": "Normal",
  "pomodoro": {
    "work_duration": 1800,
    "groups": [
      {
        "group_id": "group_1",
        "group_name": "小狗",
        "runners": [
          {
            "runner_name": "小狗工作",
            "action_type": "work",
            "is_custom": true
          },
          {
            "runner_name": "小狗休息",
            "action_type": "rest",
            "is_custom": true
          }
        ]
      }
    ]
  }
}
```

### 2. Runner元数据扩展字段

每个runner需要新增：

* `enabled_modes: string[]` - 适用模式，\["Normal"] 或 \["Normal", "Work"]，默认为 \["Normal"]

* `group_id: string|null` - 所属组ID，null表示不属于任何组

* `action_type: string|null` - 组内动作类型，"work" 或 "rest"，null表示不指定

## 实现步骤与顺序

### 阶段一：数据层和配置管理（先做）

**步骤1：创建 WorkModeManager 类**

* 位置：`app/work_mode/work_mode_manager.py`

* 功能：

  * 加载/保存 `work_mode_config.json`

  * 获取当前模式（Normal/Work）

  * 获取所有分组信息

  * 添加/删除/修改分组

  * 根据动作类型随机选择runner（同类型多个按等概率随机）

  * 获取当前番茄钟状态（工作中/休息中）

  * 倒计时管理

**步骤2：扩展 SettingsManager 新增模式相关设置**

* 在 `settings.json` 默认配置中添加 `current_mode`

* 添加 `get_current_mode()` 和 `set_current_mode()` 方法

* 保持向后兼容，默认 "Normal"

### 阶段二：UI层 - 托盘菜单改造（第二步）

**步骤3：在主菜单添加 Mode 一级菜单项**

* 文件：`app/main.py` 的 `_setup_menu()` 方法

* 添加 Mode 子菜单，包含：

  * Normal 单选

  * Work 单选

  * 当前模式选中打勾

* 切换模式时：

  * 保存设置

  * 切换对应的runner

  * Work模式下弹出系统确认对话框

**步骤4：Work模式下番茄钟状态菜单项**

* 当进入Work模式，托盘菜单额外添加：

  * 分隔线

  * "Pomodoro: 休息" / "Pomodoro: 工作中 (XX:XX)" （显示剩余时间）

  * "取消工作" 选项（工作中可见，点击取消，回到休息）

* 更新计时器，每秒刷新菜单文字显示剩余时间

### 阶段三：管理界面优化（第三步）

**步骤5：重构 SettingsForm（Manage Runners窗口）**

* 文件：`app/settings/settings_form.py`

* 新增分组管理区域：

  * 显示现有分组列表

  * 创建新分组按钮

  * 删除分组按钮

  * 为选中runner添加到分组功能

  * 设置runner动作类型（work/rest）下拉选择

* 现有runner列表新增列显示：所属分组、动作类型

* 需要将现有垂直布局改为分段，上部分是runner列表，下部分是分组管理

**步骤6：添加分组管理UI功能**

* 创建分组：弹窗输入分组名称，生成唯一group\_id

* 删除分组：确认对话框，删除后runner的group\_id设为null

* 编辑分组：可以将runner添加到分组，移出分组，修改动作类型

### 阶段四：番茄钟核心逻辑（第四步）

**步骤7：实现番茄钟倒计时逻辑**

* WorkModeManager 维护：

  * `is_working: bool` - 是否正在工作

  * `remaining_seconds: int` - 剩余秒数

  * `timer: QTimer` - 倒计时定时器（每秒触发一次）

* 开始工作：

  * 设置 is\_working = True

  * 剩余时间 = 30分钟（可配置）

  * 启动定时器

  * 随机选择一个work类型runner并切换显示

* 倒计时每秒：

  * 剩余秒数 -1

  * 更新托盘菜单显示剩余时间

* 工作结束：

  * 停止定时器

  * is\_working = False

  * 随机选择一个rest类型runner并切换显示

  * 弹出系统通知"番茄钟结束，请休息"（调用系统原生通知）

  * 等待用户再次开始

**步骤8：系统通知调用**

* Windows：使用 `ctypes` 调用 Windows Notification API

* macOS：预留接口，通过 `pyobjc` 调用（可选实现，先保证Windows可用）

* 点击通知可以直接开始新的番茄钟

### 阶段五：集成和切换逻辑（最后一步）

**步骤9：集成到主程序切换逻辑**

* 文件：`app/main.py`

* 模式切换时：

  * Normal模式：恢复原来选中的runner

  * Work模式：

    * 如果没有分组配置，提示用户先去Manage Runners配置

    * 如果有分组，弹出确认对话框"开始番茄工作吗？"

    * 确定 → 开始工作倒计时，选择work runner

    * 取消 → 进入休息状态，选择rest runner

**步骤10：悬浮球和托盘图标同步切换**

* Work模式下，托盘和悬浮球都显示对应状态的runner

* 切换runner时同时更新托盘和悬浮球

**步骤11：状态持久化**

* 保存当前模式、当前番茄钟状态、剩余时间到配置文件

* 程序重启后恢复状态

## 调用次序关系

```
1. 程序启动
   ↓
2. SettingsManager 加载当前模式
   ↓
3. WorkModeManager 加载分组配置和番茄钟状态
   ↓
4. 根据模式加载对应runner
   ↓
   - Normal: 加载settings中保存的runner
   - Work: 根据当前番茄钟状态加载对应类型runner
```

用户操作流程：

```
用户点击托盘 → 选择 Mode → 选择 Work
   ↓
弹出确认框 "需要进入番茄工作时间吗？"
   ↓
[确定] → 开始30分钟倒计时 → 显示work runner
   ↓
倒计时结束 → 自动切换到rest runner → 弹出系统通知提示休息
   ↓
用户可以再次点击开始新的番茄钟
```

## 文件修改清单

| 文件                                   | 修改类型 | 说明                  |
| ------------------------------------ | ---- | ------------------- |
| `app/work_mode/work_mode_manager.py` | 新建   | Work模式配置和番茄钟逻辑管理    |
| `app/settings/settings_manager.py`   | 修改   | 添加current\_mode读写方法 |
| `app/main.py`                        | 修改   | 添加Mode菜单项，模式切换逻辑    |
| `app/settings/settings_form.py`      | 修改   | 扩展管理界面，添加分组管理功能     |
| `work_mode_config.json`              | 新建   | 配置文件（运行时自动生成）       |

## 依赖关系

* 不需要新增pip依赖

* Windows通知使用ctypes内置，不需要额外安装

* macOS预留接口，后续可扩展

## 关键注意事项

1. **向后兼容**：现有Normal模式功能完全不变
2. **默认状态**：所有现有runner默认只适用Normal模式，需要用户手动在管理界面添加到Work分组
3. **随机选择**：同组同动作类型多个runner时，按等概率随机选择
4. **实时更新**：番茄钟倒计时每秒更新托盘菜单显示剩余时间
5. **状态持久化**：程序重启恢复番茄钟状态

