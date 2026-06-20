from mteam_cli.api.digest import _parse_float, _age_hours


def test_parse_float_valid():
    assert _parse_float("8.5") == 8.5
    assert _parse_float(9) == 9.0


def test_parse_float_empty_or_bad():
    assert _parse_float("") is None
    assert _parse_float(None) is None
    assert _parse_float("N/A") is None


def test_age_hours_recent():
    # 距离 reference 2 小时
    age = _age_hours("2026-06-05 10:00:00", now="2026-06-05 12:00:00")
    assert age == 2.0


def test_age_hours_unparseable_returns_none():
    # 解析失败返回 None（调用方据此保留条目，宁多勿漏）
    assert _age_hours("not-a-date", now="2026-06-05 12:00:00") is None


from mteam_cli.api.digest import _shape


def test_shape_extracts_fields():
    t = {
        "id": "123",
        "smallDescr": "某电影名",
        "name": "Movie.Name.2026",
        "imdbRating": "9.1",
        "doubanRating": "8.8",
        "size": "1073741824",
        "createdDate": "2026-06-05 10:00:00",
    }
    row = _shape(t, mode="movie", imdb=9.1)
    assert row["id"] == "123"
    assert row["title"] == "某电影名"          # smallDescr 优先
    assert row["type"] == "电影"
    assert row["imdb"] == 9.1
    assert row["douban"] == "8.8"
    assert row["size"] == "1.0 GiB"           # humanize binary
    assert row["createdDate"] == "2026-06-05 10:00:00"


def test_shape_falls_back_to_name():
    t = {"id": "1", "name": "Fallback", "imdbRating": "8.0"}
    row = _shape(t, mode="tvshow", imdb=8.0)
    assert row["title"] == "Fallback"
    assert row["type"] == "电视剧"
