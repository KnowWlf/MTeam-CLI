"""命令层测试：digest 空结果文案（堵回归——曾对 seeders 类型谎报 IMDB）。"""

import asyncio
import importlib
from types import SimpleNamespace

import mteam_cli.core.config as config_mod
import mteam_cli.cli.commands.digest as digest_cmd


def _settings(monkeypatch, env):
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    importlib.reload(config_mod)
    # digest 命令引用的是 config_mod 里的 Settings；reload 后取最新
    return config_mod.Settings.from_env()


def _args(**over):
    base = dict(
        account=None, min_imdb=None, types=None, hours=None,
        limit=None, min_seeders=None, raw=False, output_format="table",
    )
    base.update(over)
    return SimpleNamespace(**base)


def test_empty_message_mentions_seeders_for_music(monkeypatch):
    """music-only 查询无结果时，文案必须提做种门槛，不能只谎报 IMDB。"""
    settings = _settings(monkeypatch, {
        "MTEAM_USERNAME_1": "u1", "MTEAM_API_KEY_1": "k1",
        "MTEAM_DIGEST_TYPES": "music",
        "MTEAM_DIGEST_MIN_SEEDERS": "30",
    })

    async def fake_fetch(*a, **k):
        return []
    monkeypatch.setattr(digest_cmd, "fetch_high_score_digest", fake_fetch)

    captured = {}
    monkeypatch.setattr(digest_cmd, "notice", lambda msg: captured.setdefault("msg", msg))

    rc = asyncio.run(digest_cmd._run(_args(), settings))
    assert rc == 0
    assert "做种" in captured["msg"]      # 提到 seeders 信号
    assert "30" in captured["msg"]        # 实际生效的门槛
