# Finance Daily Brief

一个可落地的“每日财经新闻简报”程序：
- 拉取多个财经 RSS 源
- 去重与打分排序
- 生成简短 Markdown 日报

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main --date today --max-items 8
```

输出示例：
- `output/daily_YYYYMMDD.md`

## 配置新闻源
编辑 `sources.yaml`：

```yaml
sources:
  - name: Reuters Business
    url: https://feeds.reuters.com/reuters/businessNews
    weight: 1.0
  - name: CNBC World
    url: https://www.cnbc.com/id/100727362/device/rss/rss.html
    weight: 0.8
```

## 定时执行（cron）

每天 8:00 生成日报：

```cron
0 8 * * * cd /workspace/test && /usr/bin/python3 -m app.main --date today --max-items 10
```

## 说明
- 默认仅用 RSS 元数据（标题+简介）进行摘要，便于快速稳定运行。
- 若你后续要加大模型摘要，可在 `app/summarizer.py` 里接入任意 LLM API。
