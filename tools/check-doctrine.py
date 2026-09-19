#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-doctrine.py — Assayance 对自身的应用（T3：验收标准本身也是被检对象）。

这个脚本不检查"文档写得好不好"，只检查四件可判定的事：

  C1 判据在场     T0..T5 在 README 与 llms.txt 中都出现，且编号集合一致
  C2 两处一致     README 与 llms.txt 的判据标题不得漂移（防 T4 违反）
  C3 品牌隔离     理论线不得出现域品牌串（医械线在此不可见）
  C4 无占位残留   TODO/TBD/FIXME/XXX/【】 等未完成标记不得进主干

每一条都能被判 False —— 这正是本文件存在的意义。
用 --selftest 运行阳性/阴性对照，证明这些检查真的会失败（T1 反照）。
"""
import os
import re
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")  # noqa: T2-except-then-pass
    except Exception:
        # Declared, not hidden: this only affects console encoding on legacy
        # terminals. It cannot turn a failing check into a passing one, so
        # swallowing it here does not create a silent pass.
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
LLMS = os.path.join(ROOT, "llms.txt")

CANON = ["T0", "T1", "T2", "T3", "T4", "T5"]

BANNED_BRAND = ["medxpert", "medxpert.cn", "medxpertglobal"]

PLACEHOLDER = [
    r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bXXX\b",
    r"【[^】]{0,20}】", r"\{\{[^}]{0,20}\}\}", r"<PLACEHOLDER>",
]

CHECKED_FILES = ["README.md", "llms.txt", "LICENSE", "CITATION.cff"]


def read(p):
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def check_doctrine(root):
    """返回 (problems:list[str], notes:list[str])。可注入 root 以便对照。"""
    problems, notes = [], []

    rp = os.path.join(root, "README.md")
    lp = os.path.join(root, "llms.txt")
    rm, lm = read(rp), read(lp)

    if rm is None:
        problems.append("C1 缺 README.md（教义载体不存在）")
    if lm is None:
        problems.append("C1 缺 llms.txt（AI 可读骨架不存在）")
    if rm is None or lm is None:
        return problems, notes

    def present(txt, tag):
        return re.search(r"(?<![A-Za-z0-9])%s(?![0-9])" % tag, txt) is not None

    miss_r = [t for t in CANON if not present(rm, t)]
    miss_l = [t for t in CANON if not present(lm, t)]
    if miss_r:
        problems.append("C1 README 缺判据：%s" % ", ".join(miss_r))
    else:
        notes.append("C1 README 六条编号齐备")
    if miss_l:
        problems.append("C1 llms.txt 缺判据：%s" % ", ".join(miss_l))
    else:
        notes.append("C1 llms.txt 六条编号齐备")

    # 只认"标题行"上的编号，不认正文里偶然出现的 (T5)。
    # 早先版本用 re.search 抓全文首个匹配，结果把 README 正文行 56 的 "(T5)"
    # 拿去和 llms.txt 的标题行相比 —— 错位比较，误报漂移。
    def titles(txt):
        out = {}
        for line in txt.splitlines():
            s = line.strip()
            if not (s.startswith("#") or s.startswith("- ") or s.startswith("* ")):
                continue
            m = re.match(r"^[#\-\*\s]*\**\s*(T\d)\b\s*\**\s*[·:：\-—]?\s*(.{0,90})", s)
            if m:
                tag = m.group(1)
                if tag not in out:
                    body = m.group(2).replace("*", "").strip()
                    body = re.split(r"\s+—\s+|（|\(", body)[0].strip()
                    out[tag] = body
        return out

    def norm(s):
        s = s.lower()
        s = re.sub(r"\b(the|a|an)\b", "", s)
        s = re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", s)
        return s

    tr, tl = titles(rm), titles(lm)
    for tag in CANON:
        if tag in tr and tag in tl:
            a, b = norm(tr[tag]), norm(tl[tag])
            if not a or not b:
                continue
            # 一致判定：短的一方整体出现在长的一方里（去掉冠词后应逐字相同）
            ok = a in b or b in a
            if not ok:
                problems.append("C2 %s 标题漂移：README「%s」 vs llms「%s」" % (tag, tr[tag][:20], tl[tag][:20]))
    if not any(p.startswith("C2") for p in problems):
        notes.append("C2 README 与 llms.txt 判据标题一致")

    for fn in CHECKED_FILES:
        txt = read(os.path.join(root, fn))
        if txt is None:
            problems.append("C3 缺文件 %s" % fn)
            continue
        low = txt.lower()
        hit = [b for b in BANNED_BRAND if b in low]
        if hit:
            problems.append("C3 %s 出现域品牌串：%s（理论线必须隔离）" % (fn, ", ".join(sorted(set(hit)))))
    if not any(p.startswith("C3") for p in problems):
        notes.append("C3 四文件零品牌串")

    for fn in ("README.md", "llms.txt"):
        txt = read(os.path.join(root, fn))
        if txt is None:
            continue
        for pat in PLACEHOLDER:
            for m in re.finditer(pat, txt):
                problems.append("C4 %s 残留占位标记：%s" % (fn, m.group(0)))
    if not any(p.startswith("C4") for p in problems):
        notes.append("C4 无占位残留")

    return problems, notes


def cmd_check():
    problems, notes = check_doctrine(ROOT)
    for n in notes:
        print("  ok   %s" % n)
    for p in problems:
        print("  FAIL %s" % p)
    if problems:
        print("\ncheck-doctrine: %d problem(s)" % len(problems))
        return 1
    print("\ncheck-doctrine: clean")
    return 0


def _mk(tmp, readme=None, llms=None, lic=None, cit=None):
    os.makedirs(tmp, exist_ok=True)
    base_r = "\n\n".join(
        "### T%d · Criterion %d（判据%d）\n\nBody line for T%d." % (i, i, i, i) for i in range(6))
    base_l = "\n".join(
        "- **T%d · Criterion %d** — summary for T%d" % (i, i, i) for i in range(6))
    open(os.path.join(tmp, "README.md"), "w", encoding="utf-8").write(
        readme if readme is not None else base_r)
    open(os.path.join(tmp, "llms.txt"), "w", encoding="utf-8").write(
        llms if llms is not None else base_l)
    open(os.path.join(tmp, "LICENSE"), "w", encoding="utf-8").write(
        lic if lic is not None else "clean text")
    open(os.path.join(tmp, "CITATION.cff"), "w", encoding="utf-8").write(
        cit if cit is not None else "clean text")


def cmd_selftest():
    import shutil
    cases = []

    def run(name, expect_problem_substr, **kw):
        tmp = tempfile.mkdtemp(prefix="doctrine-")
        try:
            _mk(tmp, **kw)
            probs, _ = check_doctrine(tmp)
            hit = any(expect_problem_substr in p for p in probs)
            cases.append((name, hit, bool(probs), expect_problem_substr))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    only5 = "\n\n".join("### T%d · Criterion %d（判据%d）" % (i, i, i) for i in range(5))
    noT2 = "\n".join("- **T%d · Criterion %d** — summary" % (i, i) for i in [0, 1, 3, 4, 5])
    drift_r = "\n\n".join(
        "### T%d · %s criterion（判据%d）" % (i, "Alpha" if i == 0 else "Criterion", i)
        for i in range(6))
    drift_l = "\n".join(
        "- **T%d · %s criterion** — summary" % (i, "Beta" if i == 0 else "Criterion")
        for i in range(6))
    full_r = "\n\n".join("### T%d · Criterion %d（判据%d）" % (i, i, i) for i in range(6))

    run("干净样本（应无问题）", "__never__")
    run("README 缺 T5", "C1 README 缺判据", readme=only5)
    run("llms 缺 T2", "C1 llms.txt 缺判据", llms=noT2)
    run("标题漂移", "C2", readme=drift_r, llms=drift_l)
    run("品牌串混入 LICENSE", "C3 LICENSE", lic="powered by MedXpert")
    run("占位残留", "C4 README", readme=full_r + "\n\nTODO finish")
    run("正文里的编号不算标题（防错位误报）", "__never__",
        readme=full_r.replace("### T5", "### T5") + "\n\nSee (T5) in prose for details.")

    fails = 0
    for name, hit, any_problem, expect in cases:
        ok = (not any_problem) if expect == "__never__" else hit
        if not ok:
            fails += 1
        print("  %s  %-30s problems=%s" % ("ok " if ok else "FAIL", name, any_problem))

    print("\nselftest: %d case(s), %d failure(s)" % (len(cases), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(cmd_selftest())
    sys.exit(cmd_check())
